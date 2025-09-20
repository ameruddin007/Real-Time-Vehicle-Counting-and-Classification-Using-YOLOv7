# Real-Time Vehicle Counting and Classification Using YOLOv7 🚦

This project is a **real-time traffic monitoring and classification system** built with **YOLOv7**.  
It detects vehicles, bikes, helmets, helmet absence, and number plates from live or recorded video streams,  
and provides an easy-to-use **Flask-based dashboard** for live visualization, statistics, and analysis.  

---

## 📌 Features

- **Vehicle Detection & Classification** – Detects cars, bikes, and more using YOLOv7.
- **Helmet Detection** – Identifies whether riders are wearing helmets.
- **Number Plate Detection** – Extracts license plates for further processing.
- **Real-Time Multi-Object Tracking** – Avoids duplicate counts using OpenCV.
- **Flask Dashboard** – Displays live feed, statistics, and compliance insights.
- **Edge Device Optimized** – Runs on Jetson Nano, Raspberry Pi, or standard PC.
- **High Accuracy** – Achieves >95% mAP with 15–20 FPS on supported devices.

---

## 🛠️ Tech Stack

- **YOLOv7** (Object Detection)
- **OpenCV** (Multi-object tracking, video stream handling)
- **Flask** (Web Interface)
- **Python 3.x**
- **SQLite** (Optional – for logging results)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ameruddin007/Real-Time-Vehicle-Counting-and-Classification-Using-YOLOv7.git
cd Real-Time-Vehicle-Counting-and-Classification-Using-YOLOv7

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Download YOLOv7 Weights

Download pretrained YOLOv7 weights and place them in yolov7/weights/:
	•	YOLOv7 Official Weights

4️⃣ Run the Application
python app.py

5️⃣ Access Dashboard

Open your browser and go to:http://127.0.0.1:5000

## 📊 Example Output

Here is an example of real-time detection and classification using this system:

![Helmet Detection Output](assets/example_output.jpg)


📂 Project Structure
Real-Time-Vehicle-Counting-and-Classification-Using-YOLOv7/
├── yolov7/                # YOLOv7 model & scripts
├── templates/             # Flask HTML templates
├── static/outputs/        # Saved frames, detection images
├── app.py                 # Flask application entry point
├── requirements.txt       # Python dependencies
├── DataBase.db            # (Optional) SQLite DB for logs
└── YoloV7_Custom_Obj_Training Model.ipynb  # Custom training notebook

📈 Future Improvements
	•	Integration with ANPR (Automatic Number Plate Recognition)
	•	Dashboard analytics & reports
	•	Support for traffic violation alerts via SMS/Email

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to add or modify.


📬 Contact

Author: Mohammed Ameruddin
📧 ameruddin524@gmail.com
🔗 GitHub Profile











