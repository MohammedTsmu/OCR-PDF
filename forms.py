from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

class UploadPDFForm(FlaskForm):
    pdf = FileField('Upload PDF', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Convert')
