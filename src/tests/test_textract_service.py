import os
import boto3
from io import BytesIO
import fitz
import docx
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

textract = boto3.client(
    "textract",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def extract_resume_text_from_s3(bucket_name: str, file_key: str) -> str:
    """
    Extracts text from PDF or DOCX stored in S3.
    - PDFs: uses PyMuPDF (digital text) or Textract (scanned PDF)
    - DOCX: uses python-docx
    """
    file_ext = file_key.lower().split(".")[-1]

    if file_ext not in ["pdf", "docx"]:
        raise ValueError("Only PDF and DOCX files are supported.")

    # Get file bytes from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_bytes = obj["Body"].read()

    # --- DOCX ---
    if file_ext == "docx":
        doc_stream = BytesIO(file_bytes)
        doc = docx.Document(doc_stream)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    # --- PDF ---
    elif file_ext == "pdf":
        # Try extracting digital text first using PyMuPDF
        try:
            pdf_stream = BytesIO(file_bytes)
            pdf = fitz.open(stream=pdf_stream, filetype="pdf")
            print("PDF pages:", pdf.page_count, "is_encrypted:", pdf.is_encrypted)
            texts = []
            for page in pdf:
                page_text = page.get_text()
                if page_text and page_text.strip():
                    texts.append(page_text.strip())
            text = "\n".join(texts)
            if text.strip():  # if text found, return it
                return text
        except Exception as e:
            print("PyMuPDF read error:", repr(e))

        # Fallback to Textract S3 request
        try:
            response = textract.detect_document_text(
                Document={"S3Object": {"Bucket": bucket_name, "Name": file_key}}
            )
            lines = [b["Text"] for b in response["Blocks"] if b["BlockType"] == "LINE"]
            return "\n".join(lines)
        except textract.exceptions.UnsupportedDocumentException:
            print(
                "Textract S3 call: UnsupportedDocumentException - falling back to page images."
            )

        # Final fallback: render PDF pages to PNG and call Textract with image bytes
        try:
            pdf_stream = BytesIO(file_bytes)
            pdf = fitz.open(stream=pdf_stream, filetype="pdf")
            all_lines = []
            for page in pdf:
                pix = page.get_pixmap(dpi=300)  # increase dpi for OCR quality
                img_bytes = pix.tobytes("png")
                resp = textract.detect_document_text(Document={"Bytes": img_bytes})
                lines = [b["Text"] for b in resp["Blocks"] if b["BlockType"] == "LINE"]
                all_lines.extend(lines)
            return "\n".join(all_lines)
        except Exception as e:
            print("Final fallback failed:", repr(e))
            raise


file_key = "resumes/resume_20251013144653.docx"
bucket_name = "chatbot-attachments-abhi"

response = extract_resume_text_from_s3(bucket_name=bucket_name, file_key=file_key)
print(response)
