from flask import Flask, request, render_template, send_from_directory, url_for, redirect, make_response
from PIL import Image
from werkzeug.utils import secure_filename
import os, uuid, base64
from ml_compression import enhance_image  # Add this import

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# --- Helpers ---
def unique_filename(filename):
    filename = secure_filename(filename)
    name, ext = os.path.splitext(filename)
    uid = uuid.uuid4().hex[:8]
    return f"{name}_{uid}{ext}", f"{name}_{uid}.jpg"

def compress_image(input_path, output_path, max_size_mb=1, max_dimension=2048):
    try:
        # First, enhance image using ML
        enhanced_path = input_path.replace(".", "_enhanced.")
        enhance_image(input_path, enhanced_path)
        img = Image.open(enhanced_path)
        img.thumbnail((max_dimension, max_dimension))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        quality = 85
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        while os.path.getsize(output_path) > max_size_mb * 1024 * 1024 and quality > 10:
            quality -= 5
            img.save(output_path, "JPEG", quality=quality, optimize=True)
        return True
    except Exception as e:
        print(f"Compression failed: {e}")
        return False

def get_file_size_kb(path):
    return round(os.path.getsize(path) / 1024, 2) if os.path.exists(path) else None

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == "":
            return render_template("index.html", error="No file selected")

        original_filename, compressed_filename = unique_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, original_filename)
        output_path = os.path.join(DOWNLOAD_FOLDER, compressed_filename)
        file.save(input_path)

        if compress_image(input_path, output_path):
            return redirect(url_for("compare", original=original_filename, compressed=compressed_filename, display_name=file.filename))
        else:
            return render_template("index.html", error="Compression failed")

    return render_template("index.html")

@app.route("/compare")
def compare():
    original = request.args.get("original")
    compressed = request.args.get("compressed")
    display_name = request.args.get("display_name", original)

    return render_template(
        "compare.html",
        original=url_for("uploaded_file", filename=original),
        compressed=url_for("compressed_file", filename=compressed),
        original_size=get_file_size_kb(os.path.join(UPLOAD_FOLDER, original)),
        compressed_size=get_file_size_kb(os.path.join(DOWNLOAD_FOLDER, compressed)),
        compressed_filename=compressed,
        original_name=display_name
    )

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)

@app.route("/compressed/<filename>")
def compressed_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=False)

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route("/download_html")
def download_html():
    original = request.args.get("original")
    compressed = request.args.get("compressed")

    def img_to_data_uri(path):
        ext = os.path.splitext(path)[1][1:].lower()
        with open(path, "rb") as img_file:
            data = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/{ext};base64,{data}"

    original_path = os.path.join(UPLOAD_FOLDER, original)
    compressed_path = os.path.join(DOWNLOAD_FOLDER, compressed)

    original_data_uri = img_to_data_uri(original_path)
    compressed_data_uri = img_to_data_uri(compressed_path)

    rendered = render_template(
        "compare.html",
        original=original_data_uri,
        compressed=compressed_data_uri,
        original_size=get_file_size_kb(original_path),
        compressed_size=get_file_size_kb(compressed_path),
        compressed_filename=compressed,
        original_name=original
    )

    response = make_response(rendered)
    response.headers["Content-Disposition"] = "attachment; filename=comparison.html"
    response.headers["Content-Type"] = "text/html"
    return response

if __name__ == "__main__":
    app.run(debug=True)
