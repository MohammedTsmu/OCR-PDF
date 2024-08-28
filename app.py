from flask import Flask, render_template, flash, redirect, url_for, send_file, request
from config import Config
from forms import UploadPDFForm
from utils import save_file, create_folders
from ocr.pdf_processing import convert_to_text, convert_to_word, convert_to_pdf, convert_to_txt
import os

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    create_folders()

def paginate_text(text, lines_per_page=20):
    """Splits text into pages with a specified number of lines per page."""
    lines = text.split('\n')
    pages = ['\n'.join(lines[i:i + lines_per_page]) for i in range(0, len(lines), lines_per_page)]
    return pages

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadPDFForm()
    if form.validate_on_submit():
        file_path = save_file(form.pdf.data, 'UPLOAD_FOLDER')
        filename_base = os.path.splitext(os.path.basename(file_path))[0]
        result_text = os.path.join(app.config['RESULT_FOLDER'], f'{filename_base}.txt')
        result_word = os.path.join(app.config['RESULT_FOLDER'], f'{filename_base}.docx')
        result_pdf = os.path.join(app.config['RESULT_FOLDER'], f'{filename_base}_converted.pdf')
        
        # Convert and save files
        convert_to_txt(file_path, result_text)
        convert_to_word(file_path, result_word)
        convert_to_pdf(file_path, result_pdf)
        
        # Read the text content to pass to the template
        with open(result_text, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Paginate the text
        pages = paginate_text(text)
        
        flash('File successfully converted!', 'success')
        return render_template(
            'result.html', 
            pages=pages, 
            word=os.path.basename(result_word), 
            pdf=os.path.basename(result_pdf), 
            text=os.path.basename(result_text)
        )
    return render_template('home.html', form=form)

@app.route('/download/<filename>')
def download_file(filename):
    """Handles file download."""
    file_path = os.path.join(app.config['RESULT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found.', 'error')
        return redirect(url_for('home'))

@app.route('/page/<int:page_number>')
def show_page(page_number):
    """Displays a specific page of the text."""
    text_filename = request.args.get('text')
    word_filename = request.args.get('word')
    pdf_filename = request.args.get('pdf')

    if not text_filename or not word_filename or not pdf_filename:
        flash('Invalid request parameters.', 'error')
        return redirect(url_for('home'))

    text_file_path = os.path.join(app.config['RESULT_FOLDER'], text_filename)
    if not os.path.exists(text_file_path):
        flash('Text file not found.', 'error')
        return redirect(url_for('home'))

    # Read and paginate the text content
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    pages = paginate_text(text)
    
    if page_number < 1 or page_number > len(pages):
        flash('Page not found.', 'error')
        return redirect(url_for('home'))

    return render_template(
        'result.html',
        pages=pages,
        page_number=page_number,
        total_pages=len(pages),
        word=word_filename,
        pdf=pdf_filename,
        text=text_filename
    )

if __name__ == '__main__':
    app.run(debug=True)
