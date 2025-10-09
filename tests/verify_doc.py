from docx import Document

try:
    doc = Document("generated_doc.docx")
    print("✅ File opened successfully! Total paragraphs:", len(doc.paragraphs))
except Exception as e:
    print("❌ File corrupted:", e)
