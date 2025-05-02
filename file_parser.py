import os
import PyPDF2
import docx
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import io
import base64

def extract_text_from_pdf(pdf_content):
    try:
        # Create a PDF file object from the binary content
        pdf_file = io.BytesIO(base64.b64decode(pdf_content))
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_text_from_docx(docx_content):
    try:
        # Create a Word document object from the binary content
        doc_file = io.BytesIO(base64.b64decode(docx_content))
        doc = docx.Document(doc_file)
        
        # Extract text from all paragraphs
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {str(e)}")
        return ""

def extract_text_from_image(image_content):
    try:
        # Create an image object from the binary content
        image_file = io.BytesIO(base64.b64decode(image_content))
        image = Image.open(image_file)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {str(e)}")
        return ""

def extract_text_from_file(file_info):
    try:
        filename = file_info.get("name", "").lower()
        content = file_info.get("content", "")
        
        if not content:
            return "Le fichier est vide."
            
        # Determine file type and extract text accordingly
        if filename.endswith('.pdf'):
            return extract_text_from_pdf(content)
        elif filename.endswith(('.doc', '.docx')):
            return extract_text_from_docx(content)
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            return extract_text_from_image(content)
        else:
            # For plain text files or unknown types, try to decode as text
            try:
                return base64.b64decode(content).decode('utf-8')
            except:
                return "Format de fichier non pris en charge."
    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")
        return f"Erreur lors du traitement du fichier: {str(e)}"