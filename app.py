from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from models.generate import generate_image_from_prompt, convert_image_to_ghibli

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_image():
    """Generate an image from a text prompt"""
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    image_url = generate_image_from_prompt(prompt)
    
    if image_url:
        return jsonify({"image_url": image_url})
    else:
        return jsonify({"error": "Failed to generate image"}), 500

@app.route("/upload", methods=["POST"])
def upload_image():
    """Convert an uploaded image to Ghibli style"""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)

    image_url = convert_image_to_ghibli(file_path)
    
    if image_url:
        return jsonify({"image_url": image_url})
    else:
        return jsonify({"error": "Failed to convert image"}), 500

if __name__ == "__main__":
    app.run(debug=True)
