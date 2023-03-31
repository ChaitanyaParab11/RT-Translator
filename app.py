from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from Cam_Trans import *
from Pdf_Trans import *
from Take_Trans import *
from Text_Trans import *

# Set up Flask app
app = Flask(__name__)

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for text translation
@app.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        text = request.form['text']
        translation = texttranslate(text)
        return render_template('text.html', translation=translation)
    else:
        return render_template('text.html')

# Route for file translation
@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if filename.endswith('.txt'):
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as f:
                    text = f.read()
                    translation = pdftranslate(text, target_language=target_language)['translatedText']
                    return render_template('file.html', translation=translation)
            elif filename.endswith('.pdf'):
                translation = pdftranslate(file_path) 
                os.remove(file_path)
                return render_template('file.html', translation=translation)
            elif filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.gif'):
                # TODO: Implement PDF and image translation
                return render_template('file.html', error='PDF and image translation coming soon!')
        else:
            return render_template('file.html', error='Invalid file type')
    else:
        return render_template('file.html')

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)
