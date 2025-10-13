import subprocess
import tempfile
from io import BytesIO
import os
import sys
import shutil


def docx_to_pdf(docx_bytes: bytes) -> BytesIO:
    """
    Convert a DOCX file (provided as bytes) to PDF using LibreOffice.

    Args:
        docx_bytes (bytes): The DOCX file content as bytes.

    Returns:
        BytesIO: PDF file content as a BytesIO buffer.

    Raises:
        FileNotFoundError: If LibreOffice is not installed or not found.
        subprocess.CalledProcessError: If LibreOffice fails to convert the file.
    """

    # Write DOCX bytes to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx:
        temp_docx.write(docx_bytes)
        temp_docx.flush()
        docx_path = temp_docx.name

    # Set output PDF path
    pdf_path = docx_path.replace(".docx", ".pdf")

    # Find LibreOffice executable based on platform
    soffice_cmd = None

    if sys.platform == "win32":
        # Common LibreOffice installation paths on Windows
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                soffice_cmd = path
                break

        # If not found in common paths, try to find it in PATH
        if not soffice_cmd:
            soffice_cmd = shutil.which("soffice")
    else:
        # Linux/Mac: assume 'soffice' is in PATH
        soffice_cmd = "soffice"

    if not soffice_cmd:
        raise FileNotFoundError(
            "LibreOffice is not installed or not found. "
            "Please install LibreOffice from https://www.libreoffice.org/download/download/"
        )

    # Convert DOCX to PDF using LibreOffice in headless mode
    subprocess.run(
        [
            soffice_cmd,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            os.path.dirname(docx_path),
            docx_path,
        ],
        check=True,
    )

    # Read the generated PDF into a BytesIO buffer
    pdf_buffer = BytesIO(open(pdf_path, "rb").read())

    # Cleanup temporary files
    os.remove(docx_path)
    os.remove(pdf_path)

    return pdf_buffer
