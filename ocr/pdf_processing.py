from docx import Document
from reportlab.pdfgen import canvas
from ocr.image_processing import pdf_to_images, image_to_text

def convert_to_text(pdf_path):
    images = pdf_to_images(pdf_path)
    text = '\n'.join([image_to_text(image) for image in images])
    return text

def convert_to_word(pdf_path, result_path):
    text = convert_to_text(pdf_path)
    doc = Document()
    doc.add_paragraph(text)
    doc.save(result_path)

def convert_to_pdf(pdf_path, result_path):
    text = convert_to_text(pdf_path)
    c = canvas.Canvas(result_path)
    c.drawString(100, 750, text)
    c.save()
