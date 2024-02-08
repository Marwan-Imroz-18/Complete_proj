from flask import Flask, request, jsonify, render_template
import os
import cv2
import numpy as np
from tempfile import mkdtemp
from werkzeug.utils import secure_filename
from detection import detect_image_difference

app = Flask(__name__)

# Set upload folder and allowed extensions
UPLOAD_FOLDER = mkdtemp()
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect_differences", methods=["POST"])
def detect_differences():
    # Check if two images were uploaded
    if "image1" not in request.files or "image2" not in request.files:
        return jsonify({"error": "Two images must be uploaded."}), 400

    image1 = request.files["image1"]
    image2 = request.files["image2"]

    # Check if filenames are empty
    if image1.filename == "" or image2.filename == "":
        return jsonify({"error": "Filenames cannot be empty."}), 400

    # Check if file extensions are allowed
    if not allowed_file(image1.filename) or not allowed_file(image2.filename):
        return jsonify({"error": "File extensions not allowed."}), 400

    # Save uploaded images
    filename1 = secure_filename(image1.filename)
    filename2 = secure_filename(image2.filename)
    filepath1 = os.path.join(app.config["UPLOAD_FOLDER"], filename1)
    filepath2 = os.path.join(app.config["UPLOAD_FOLDER"], filename2)
    image1.save(filepath1)
    image2.save(filepath2)

    # Perform image difference detection
    output_image, similarity_score = detect_image_difference(filepath1, filepath2)
    output_image_list = output_image.tolist()
    output_image_path = "static/output.png"
    cv2.imwrite(output_image_path, output_image)

    # Return the output image and similarity score as JSON
    return jsonify(
        {"output_image": output_image_list, "similarity_score": similarity_score}
    )
    # Remove uploaded images
    os.remove(filepath1)
    os.remove(filepath2)

    return jsonify({"output_image": output_image, "similarity_score": similarity_score})


if __name__ == "__main__":
    app.run(debug=True)
