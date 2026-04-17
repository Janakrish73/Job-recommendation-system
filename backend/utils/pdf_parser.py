import pdfplumber
import re


def extract_text_from_pdf(filepath: str) -> str:
    """
    Extract all text from a PDF file using pdfplumber.
    Returns clean text as a single string.
    """
    text_parts = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        print(f"[PDF Parser] Error reading {filepath}: {e}")
        return ""

    full_text = " ".join(text_parts)
    # Normalize whitespace
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    return full_text


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes (in-memory, no file save needed).
    """
    import io
    text_parts = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
    except Exception as e:
        print(f"[PDF Parser] Error reading PDF bytes: {e}")
        return ""

    full_text = " ".join(text_parts)
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    return full_text
