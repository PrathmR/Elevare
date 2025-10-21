import fitz  # PyMuPDF
import docx

def extract_text_from_resume(filepath):
    """
    Extract text from resume files (PDF or DOCX)
    
    Args:
        filepath (str): Path to the resume file
        
    Returns:
        str: Extracted text from the resume
    """
    try:
        # Check file type and extract text accordingly
        if filepath.endswith(".pdf"):
            doc = fitz.open(filepath)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            return text
        elif filepath.endswith(".docx") or filepath.endswith(".doc"):
            doc = docx.Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            return "Unsupported file format."
    except Exception as e:
        print(f"Error extracting text from {filepath}: {str(e)}")
        return f"Error extracting text: {str(e)}"
