# ✳ AnnotateAI — AI-Powered Object Detection

AnnotateAI is a computer vision web application that detects objects in uploaded images and live camera frames using YOLO and Python.

## ✨ Features

- 🖼️ Upload images for object detection
- 🎯 Display detected objects with bounding boxes
- 📊 View detected object counts and confidence scores
- 📷 Real-time object detection through a live camera
- ⬇️ Download annotated image results
- 💻 Responsive, user-friendly web interface

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **AI / Computer Vision:** Ultralytics YOLO
- **Image Processing:** OpenCV
- **Model:** YOLO11n

## 📁 Project Structure

```text
AnnotateAI/
├── app.py
├── detect.py
├── requirements.txt
├── yolo11n.pt
├── .gitignore
├── static/
└── templates/
    └── index.html
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AnnotateAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open the local address shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

## 📷 How to Use

1. Open AnnotateAI in your browser.
2. Upload an image or start the live camera.
3. View detected objects and their confidence scores.
4. Download the annotated image when available.

## 🎯 Project Goal

The goal of AnnotateAI is to provide a simple and accessible interface for experimenting with AI-powered object detection.

## 👩‍💻 Developer

Developed as a computer vision and AI web application project.