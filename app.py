from flask import Flask, render_template, request, send_file, flash
import os
from bookworks.core.publisher import process_markdown_content, UPLOAD_FOLDER
import logging
from typing import Any

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index() -> Any:
    if request.method == "POST":
        markdown_content = request.form.get("markdown_content")
        uploaded_file = request.files.get("markdown_file")
        author = request.form.get("author", "Anonymous")

        if not markdown_content and not uploaded_file:
            flash("Please provide either markdown content or upload a file")
            return render_template("index.html")

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
        else:
            content = markdown_content

        logger.debug(f"Processing markdown content with author: {author}")
        output_file, error = process_markdown_content(content, author=author)

        if error:
            logger.error(f"Error processing markdown: {error}")
            flash(error)
            return render_template("index.html")

        if not output_file or not os.path.exists(output_file):
            logger.error(f"Output file not found at {output_file}")
            flash("Error: Output file was not created")
            return render_template("index.html")

        logger.debug(f"Sending file: {output_file}")
        try:
            return send_file(
                output_file,
                as_attachment=True,
                download_name=os.path.basename(output_file),
            )
        finally:
            # Clean up the file after sending
            if os.path.exists(output_file):
                os.remove(output_file)

    return render_template("index.html")


@app.route("/audiobook")
def audiobook() -> Any:
    return render_template("audiobook.html")


@app.route("/about")
def about() -> Any:
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
