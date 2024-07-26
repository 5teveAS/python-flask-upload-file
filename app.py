from flask import Flask, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <input type=submit value=Upload>
    </form>
    '''

@app.route('/', methods=['POST'])
def upload_file():
    # Eliminar archivo anterior si existe
    previous_files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in previous_files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

    # Subir y guardar nuevo archivo
    file = request.files['file']
    if file and file.filename.endswith('.txt'):
        filename = 'uploaded.txt'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Procesar el archivo
        with open(filepath, 'r') as f:
            lines = f.readlines()

        processed_lines = [line.replace(' CNAME .', '') for line in lines]

        processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.txt')
        with open(processed_filepath, 'w') as f:
            f.writelines(processed_lines)

        return redirect(url_for('display_file'))

    return 'Invalid file type. Only .txt files are allowed.'

@app.route('/display')
def display_file():
    processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.txt')
    with open(processed_filepath, 'r') as f:
        content = f.read()

    return content, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True)