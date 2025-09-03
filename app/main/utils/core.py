import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using PyMuPDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()


def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """
    Splits text into chunks for better embeddings.
    
    Args:
        text (str): The full text extracted from the PDF.
        chunk_size (int): Max characters per chunk.
        chunk_overlap (int): Overlap between chunks for context preservation.
    
    Returns:
        List[str]: A list of chunked text strings.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    return splitter.split_text(text)
