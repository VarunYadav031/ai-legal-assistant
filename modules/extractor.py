from pypdf import PdfReader
from docx import Document
import io


# ---------------- SAFE PDF EXTRACTION ----------------
def _extract_pdf(file_stream):

    text = ""

    try:
        reader = PdfReader(file_stream)

        # handle encrypted PDFs safely
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                return "⚠️ Encrypted PDF cannot be read"

        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                print("Page extraction error:", str(e))
                continue

    except Exception as e:
        print("PDF Read Error:", str(e))
        return "⚠️ PDF file is corrupted or unreadable"

    return text.strip()


# ---------------- DOCX ----------------
def _extract_docx(file_stream):

    try:
        doc = Document(file_stream)
        return "\n".join([p.text for p in doc.paragraphs])

    except Exception as e:
        print("DOCX Error:", str(e))
        return "⚠️ DOCX file could not be read"


# ---------------- TXT ----------------
def _extract_txt(file_stream):

    try:
        return file_stream.read().decode("utf-8")

    except Exception as e:
        print("TXT Error:", str(e))
        return "⚠️ TXT file could not be read"


# ---------------- MAIN FUNCTION (FILE PATH) ----------------
def extract_text(file_path):

    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            return _extract_pdf(f)

    elif file_path.endswith(".docx"):
        return _extract_docx(file_path)

    elif file_path.endswith(".txt"):
        return _extract_txt(file_path)

    else:
        raise ValueError("Unsupported file format")


# ---------------- STREAMLIT SAFE WRAPPER ----------------
def extract_text_from_pdf(file):

    """
    Streamlit uploader safe version
    """

    if file is None:
        return ""

    try:
        # reset pointer (IMPORTANT FIX for Streamlit)
        file.seek(0)

        return _extract_pdf(file)

    except Exception as e:
        print("Streamlit PDF Error:", str(e))
        return "⚠️ PDF could not be processed (file may be corrupted)"