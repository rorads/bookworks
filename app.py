from flask import Flask, render_template, request, send_file, flash
import os
from bookworks.md_publish import process_markdown_content
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        markdown_content = request.form.get('markdown_content')
        uploaded_file = request.files.get('markdown_file')
        author = request.form.get('author', 'Anonymous')

        if not markdown_content and not uploaded_file:
            flash('Please provide either markdown content or upload a file')
            return render_template('index.html')

        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
        else:
            content = markdown_content

        output_file, error = process_markdown_content(content, author=author)
        
        if error:
            flash(error)
            return render_template('index.html')
        
        return send_file(output_file, as_attachment=True, download_name=os.path.basename(output_file))

    return render_template('index.html')

@app.route('/audiobook')
def audiobook():
    return render_template('audiobook.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True) 