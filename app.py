"""python app.py"""
from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
import os
import PyCertGen

app = Flask(__name__, static_folder="assets")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ROOT_DIR = os.getcwd()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/gencert')
def base():
    return render_template('uploadtemp.html')
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/


@app.route('/uploadsuccess', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(f.filename)
        # Perform Some File Validation so that only DOCX File Can be uploaded
        FileSavePath = os.path.join(ROOT_DIR, "TempSaved", "Generated.docx")
        f.save(FileSavePath)
        # return str(f.filename) + 'file uploaded successfully'
        document = PyCertGen.DocxLoader(FileSavePath)
        ParsedResults = PyCertGen.parser(document)
        return render_template('uploadsuccess.html', UploadFileMessage=str(f.filename) + ' file uploaded successfully', data=ParsedResults)


if __name__ == "__main__":
    app.run(debug=True)
