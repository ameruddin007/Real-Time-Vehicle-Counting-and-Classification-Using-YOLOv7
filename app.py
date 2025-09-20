import os
import cv2
import torch
import sqlite3
import pytz
import base64
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from werkzeug.utils import secure_filename
import uuid

# Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/outputs"

# Allowed extensions
ALLOWED_EXTENSIONS = {
    "image": {"jpg", "jpeg", "png", "bmp", "gif"},
}

def allowed_file(filename, filetype):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS[filetype]

# Load YOLOv7 Model
model = torch.hub.load("yolov7", "custom", source="local",
                       path_or_model="yolov7/Trained_Model/weights/best.pt",
                       force_reload=True)
class_names = model.names

# Ensure DB exists
def init_db():
    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS Image (
            Time TEXT,
            Date TEXT,
            Label TEXT,
            Image BLOB
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Insert detection crop into DB
def insert_image(Time, Date_, crop_file, label_name):
    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    with open(crop_file, "rb") as f:
        crop_binary = f.read()
    c.execute("INSERT INTO Image (Time, Date, Label, Image) VALUES (?, ?, ?, ?)",
              (Time, Date_, label_name, crop_binary))
    conn.commit()
    conn.close()

# YOLOv7 Detection (for frames)
def detect_and_save_frame(frame, save_prefix="output"):
    height, width = frame.shape[:2]
    results = model(frame)
    print(results.xyxyn)
    labels, cords = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    for i in range(len(labels)):
        x1, y1, x2, y2 = int(cords[i][0]*width), int(cords[i][1]*height), int(cords[i][2]*width), int(cords[i][3]*height)
        conf = float(cords[i][4])
        label_name = class_names[int(labels[i])]

        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{label_name} {conf:.2f}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Save crop
        crop = frame[y1:y2, x1:x2]
        if crop.size != 0:
            crop_file = os.path.join(app.config["UPLOAD_FOLDER"], f"{save_prefix}_{label_name}_{uuid.uuid4().hex}.jpg")
            cv2.imwrite(crop_file, crop)

            now = datetime.now(pytz.timezone("Asia/Kolkata"))
            insert_image(now.strftime("%H:%M:%S"), now.strftime("%d/%m/%Y"), crop_file, label_name)

    return frame

# Process Image
def process_image(filepath):
    frame = cv2.imread(filepath)
    frame = detect_and_save_frame(frame, "image")
    output_file = os.path.join(app.config["UPLOAD_FOLDER"], f"output_image_{uuid.uuid4().hex}.jpg")
    cv2.imwrite(output_file, frame)
    return os.path.basename(output_file)


# Process Webcam
def process_webcam():
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20

    output_file = os.path.join(app.config["UPLOAD_FOLDER"], f"output_webcam_{uuid.uuid4().hex}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    frame_count = 0
    while frame_count < 200:  # limit capture
        ret, frame = cap.read()
        if not ret:
            break
        frame = detect_and_save_frame(frame, "webcam")
        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()
    return os.path.basename(output_file)

# Main Route
@app.route("/", methods=["GET", "POST"])
def index():
    output_file = None
    if request.method == "POST":
        option = request.form.get("option")

        if option in ["image"]:
            file = request.files.get("file")
            if not file or file.filename == "":
                return redirect(request.url)  # no file selected

            if not allowed_file(file.filename, option):
                return f"Invalid {option} file type.", 400

            # Generate safe, unique filename
            original_name = secure_filename(file.filename)
            filename = f"{uuid.uuid4().hex}_{original_name}"
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Process file
            if option == "image":
                output_file = process_image(filepath)

        elif option == "webcam":
            output_file = process_webcam()

    return render_template("index.html", output_file=output_file)

# Gallery Route

@app.route("/gallery", methods=["GET"])
def gallery():
    selected_label = request.args.get("label", "all")  # default = all

    conn = sqlite3.connect("DataBase.db")
    c = conn.cursor()
    if selected_label == "all":
        c.execute("SELECT Time, Date, Label, Image FROM Image ORDER BY ROWID DESC LIMIT 100")
    else:
        c.execute("SELECT Time, Date, Label, Image FROM Image WHERE Label=? ORDER BY ROWID DESC LIMIT 100", (selected_label,))
    rows = c.fetchall()
    conn.close()

    images = []
    for time, date, label, img_blob in rows:
        img_base64 = base64.b64encode(img_blob).decode("utf-8")
        images.append({"time": time, "date": date, "label": label, "image": img_base64})

    return render_template("gallery.html", images=images, selected_label=selected_label)

# Run Flask
if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)