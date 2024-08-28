from flask import Flask, render_template, flash, redirect, url_for, send_file
from config import Config
from forms import UploadPDFForm
from utils import save_file, create_folders
from ocr.pdf_processing import convert_to_text, convert_to_word, convert_to_pdf
import os

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    create_folders()

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadPDFForm()
    if form.validate_on_submit():
        file_path = save_file(form.pdf.data, 'UPLOAD_FOLDER')
        result_text = convert_to_text(file_path)
        result_word = file_path.replace('.pdf', '.docx')
        result_pdf = file_path.replace('.pdf', '_converted.pdf')
        convert_to_word(file_path, result_word)
        convert_to_pdf(file_path, result_pdf)
        flash('File successfully converted!', 'success')
        return render_template('result.html', text=result_text, word=result_word, pdf=result_pdf)
    return render_template('home.html', form=form)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['RESULT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
