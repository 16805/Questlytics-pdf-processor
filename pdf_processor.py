import fitz # PyMuPDF
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF. Handles both digital and scanned PDFs.

    Args:
        pdf_path (str): The path to the PDF file

    Returns:
        str: Extracted and cleaned text
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        if len(text.strip()) > 100:
            return clean_text(text)
    except Exception as e:
        print(f"[Digital Extraction Failed] {e}")

    try:
        images = convert_from_path(pdf_path)
        for image in images:
            text += pytesseract.image_to_string(image)
        return clean_text(text)
    except Exception as e:
        print(f"[OCR Failed] {e}")
        return ""


def clean_text(raw_text: str) -> str:
    """
    Clean extracted text by removing empty lines and extra spaces.

    Args:
        raw_text (str): Raw extracted text

    Returns:
        str: Cleaned text
    """
    lines = raw_text.splitlines()
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)


"""if __name__=="__main__":
    pdf_file_path="sample.pdf"
    result=extract_text_from_pdf(pdf_file_path)
    print(result)"""
