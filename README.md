# AirText

Turn mid-air finger writing into text — then turn that text into images.  
**AirText** lets you draw with your fingertip in front of a webcam, auto-captures the sketch, runs AI handwriting recognition, and (optionally) generates a pretty image from your recognized text.  

It comes with a **Streamlit UI** plus simple scripts to run the webcam capture and the OCR/generation pipeline.

**TL;DR**  
👉 Wave finger → get PNG → get text → (optionally) get a DALL·E-style image from the text. Minimal fuss.

---

## 📑 Table of Contents
- [Why AirText?](#-why-airtext)
- [Features](#-features)
- [Architecture](#-architecture)
- [Project Layout](#-project-layout)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Running Options](#-running-options)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [FAQ](#-faq)
- [Acknowledgments](#-acknowledgments)
- [License](#-license)

---

## 🚀 Why AirText?

- **Hands-free vibe**: Sketch letters/shapes with your finger — no stylus/tablet.
- **Fast OCR**: Push the captured canvas to a vision model for handwriting recognition.
- **Creative kicker**: Pipe recognized text into an image generator for concept art or playful outputs.

---

## ✨ Features

- Fingertip drawing via **webcam** (MediaPipe + OpenCV style pipeline).  
- **Mode switching**: draw / erase / clear / save.  
- **Canvas export** → `airtext_output.png`.  
- **OCR** with Vision model → recognized text.  
- **Text-to-Image** (DALL·E-style).  
- **Streamlit web app** (`streamlit_app.py`) for uploads/camera workflow.  

---

## 🛠 Architecture

**Capture → Recognize → (Optional) Generate**

1. **Capture** (`interactive_draw.py`)  
   Tracks fingertip → draws onto canvas → saves PNG.  

2. **Recognize** (`Handwriting_reader.py`)  
   OCR via Vision model → returns text.  

3. **Generate** (optional)  
   Text prompt → DALL·E-style generator → output image.  

4. **UI** (`streamlit_app.py`)  
   One-stop Streamlit interface tying it together.  

---

AirText/
├─ interactive_draw.py # Webcam fingertip → canvas → PNG
├─ Handwriting_reader.py # OCR + optional text→image
├─ streamlit_app.py # Streamlit UI
├─ chatgpt.py # API helper
├─ secrets.toml # Keys (for Streamlit Cloud)
└─ README.md


---

## ⚡ Quick Start

### 1. Environment
```bash
conda create -n airtext python=3.10 -y
conda activate airtext
```

##Install dependencies
pip install opencv-python mediapipe streamlit pillow numpy requests python-dotenv
pip install openai azure-identity azure-core   # if using Azure

3. Configure keys

Use .env locally or .streamlit/secrets.toml in Streamlit Cloud.
(See Configuration
 below.)

⚙️ Configuration
Local .env
AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OCR_DEPLOYMENT=gpt-4o
AZURE_IMAGE_DEPLOYMENT=dalle-3

Streamlit Cloud (.streamlit/secrets.toml)
AZURE_OPENAI_ENDPOINT = "https://<your-endpoint>.openai.azure.com/"
AZURE_OPENAI_API_KEY  = "<your-key>"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_OCR_DEPLOYMENT = "gpt-4o"
AZURE_IMAGE_DEPLOYMENT = "dalle-3"

▶️ Running Options
1. Streamlit app (recommended)
streamlit run streamlit_app.py

2. Direct capture
python interactive_draw.py

3. OCR & generation
python Handwriting_reader.py --image airtext_output.png --task ocr
python Handwriting_reader.py --image airtext_output.png --task generate

🐞 Troubleshooting

Black camera feed → ensure correct webcam index.

No fingertip detected → improve lighting & background contrast.

OCR errors → thicker strokes / black on white canvas.

Secrets not found → use .env locally, .streamlit/secrets.toml on cloud.

🗺 Roadmap

 One-click “camera → OCR → generate” in Streamlit.

 Brush/eraser thickness + color options.

 Undo/redo support.

 Batch OCR.

 Export PDF with text + images.

❓ FAQ

Q: Do I need Azure?
A: Repo is Azure-ready, but you can swap to OpenAI API easily.

Q: Can I use a mouse?
A: Yes — change fingertip tracking → mouse events.

Q: Any training required?
A: No — foundation models handle OCR & image generation.

🙏 Acknowledgments

MediaPipe + OpenCV for hand tracking.

Streamlit for easy UI.

Azure OpenAI for vision + image generation.

📜 License

MIT / Apache-2.0 / GPL — choose one and add LICENSE fil



