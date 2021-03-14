"""python app.py"""
from flask import Flask, render_template, request, url_for, send_from_directory, jsonify, send_file
import os
import PyCertGen
import common_utils

# "templates" this is for plain html files or "Great_Templates" this is for complex css + imgs +js +html+sass
TEMPLATES = "Great_Templates"

app = Flask(__name__, static_folder="assets", template_folder=TEMPLATES)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Standard File Size
ROOT_DIR = os.getcwd()

# Reloading
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


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
        DocxFileSavePath = os.path.join(
            ROOT_DIR, "TempSaved", "Generated.docx")
        f.save(DocxFileSavePath)
        # return str(f.filename) + 'file uploaded successfully'
        document = PyCertGen.DocxLoader(DocxFileSavePath)
        ParsedResults = PyCertGen.parser(document, v=0)
        CleanParsed = PyCertGen.cleanParsed(ParsedResults)
        return render_template('uploadsuccess.html', UploadFileMessage=str(f.filename) + ' file uploaded successfully', data=CleanParsed)


@app.route('/reuploadsuccess', methods=['GET', 'POST'])
def reupload_file():
    if request.method == 'POST':
        f = request.files['reuploadfile']
        # f.save(f.filename)
        # Perform Some File Validation so that only DOCX File Can be uploaded
        DocxFileSavePath = os.path.join(
            ROOT_DIR, "TempSaved", "Generated.docx")
        f.save(DocxFileSavePath)
        # return str(f.filename) + 'file uploaded successfully'
        document = PyCertGen.DocxLoader(DocxFileSavePath)
        ParsedResults = PyCertGen.parser(document, v=0)
        CleanParsed = PyCertGen.cleanParsed(ParsedResults)
        return render_template('uploadsuccess.html', UploadFileMessage=str(f.filename) + ' file uploaded successfully', data=CleanParsed)


@app.route('/uploadexcel')
def upload_excel_file():
    return render_template('uploadexcel.html')


@app.route('/uploadexcelsuccess', methods=['GET', 'POST'])
def uploadexcelsuccess():
    if request.method == 'POST':
        f = request.files['ExcelFile']
        # f.save(f.filename)
        # Perform Some File Validation so that only EXCEL File Can be uploaded
        ExcelFileSavePath = os.path.join(ROOT_DIR, "TempSaved", "Data.xlsx")
        f.save(ExcelFileSavePath)
        DocxFileSavePath = os.path.join(
            ROOT_DIR, "TempSaved", "Generated.docx")
        # return str(f.filename) + 'file uploaded successfully'
        SaveFolder = os.path.join(ROOT_DIR, "TempSaved", "TempFiles")
        # Clean First
        common_utils.DeleteFolderContents(SaveFolder)
        PyCertGen.CertGenEngine(
            DocxFileSavePath, ExcelFileSavePath, SaveFolder)

        SaveFolderPath = os.path.join("TempSaved", "TempFiles")
        # SaveZipFilePath = os.path.join(ROOT_DIR, "TempSaved", "CertGen.zip")
        SaveZipFilePath = os.path.join("TempZipSaved", "CertGen.zip")
        common_utils.zipper(SaveFolderPath, SaveZipFilePath)
        # Processing
        return render_template('run.html', value="CertGen.zip")


@app.route('/download/<filename>')
def return_files_tut(filename):
    ZipFilePath = os.path.join("TempZipSaved", filename)
    return send_file(ZipFilePath, as_attachment=True, mimetype='application/zip',
                     attachment_filename='CertGenResults.zip')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'assets', 'favicons'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(debug=True)
