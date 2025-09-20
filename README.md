# AirText

Turn mid-air finger writing into text—then turn that text into images.
AirText lets you draw with your fingertip in front of a webcam, auto-captures the sketch, runs AI handwriting recognition, and (optionally) generates a pretty image from your recognized text. It comes with a Streamlit UI plus simple scripts to run the webcam capture and the OCR/generation pipeline.

TL;DR: Wave finger → get PNG → get text → (optionally) get a DALL·E-style image from the text. Minimal fuss.

Table of contents

Why AirText?

Features

Architecture

Project layout

Quick start

Configuration

Running options

Troubleshooting

Roadmap

FAQ

Acknowledgments

License

Why AirText?

Hands-free vibe: Sketch letters/shapes with your finger—no stylus/tablet.

Fast OCR: Push the captured canvas to a vision model for handwriting recognition.

Creative kicker: Pipe recognized text into an image generator for concept art or playful outputs.

Features

Fingertip drawing via webcam using computer vision (e.g., MediaPipe + OpenCV style pipeline).

Live mode switching (draw/erase/clear/save) directly from keyboard or UI controls.

Canvas export to airtext_output.png.

Handwriting OCR (Vision model) that returns clean text.

Text-to-Image generation (DALL·E-style) from the recognized text (optional).

Streamlit web app (streamlit_app.py) for point-and-click uploads or camera flow.

Repo key scripts: interactive_draw.py, Handwriting_reader.py, streamlit_app.py, chatgpt.py, secrets.toml. 
GitHub

Architecture

Capture → Recognize → (Optional) Generate

Capture (interactive_draw.py)

Tracks fingertip → draws onto an in-memory canvas → saves airtext_output.png when you hit save.

Recognize (Handwriting_reader.py)

Sends the PNG to a vision model (e.g., Azure OpenAI GPT-4o/GPT-4 Vision) → returns recognized text.

Generate (Handwriting_reader.py)

Feeds recognized text to an image generator (e.g., DALL·E-style endpoint) → returns image bytes for preview/download.

UI (streamlit_app.py)

One-stop Streamlit interface for upload/capture → OCR → optional image generation; uses chatgpt.py as a thin API wrapper.

Project layout
AirText/
├─ interactive_draw.py       # Webcam fingertip → canvas → save PNG
├─ Handwriting_reader.py     # OCR (vision) and optional text→image generation
├─ streamlit_app.py          # Streamlit UI to run everything in-browser
├─ chatgpt.py                # Helper/wrapper for model calls
├─ secrets.toml              # Streamlit secrets (for Streamlit Cloud)
└─ README.md                 # You’re reading the better one now :)


File names verified directly from the repo file list. 
GitHub

Quick start
1) Create a Python env
# conda (recommended)
conda create -n airtext python=3.10 -y
conda activate airtext

# or venv
python -m venv .venv
source .venv/bin/activate    # on Windows: .venv\Scripts\activate

2) Install dependencies

There’s no requirements.txt in the repo yet, so install the usual suspects:

pip install opencv-python mediapipe streamlit pillow numpy requests python-dotenv
# If you use Azure OpenAI SDKs:
pip install openai==1.* azure-identity azure-core


If you prefer, add a requirements.txt to pin versions.

3) Configure keys (OCR + Image Gen)

See Configuration
. You’ll either use environment variables (.env) locally or secrets.toml for Streamlit Cloud.

Configuration

You can run locally with a .env, or on Streamlit Cloud with .streamlit/secrets.toml.

Option A — Local .env

Create a .env in the project root:

# Azure OpenAI (example)
AZURE_OPENAI_ENDPOINT=https://<your-endpoint>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Vision model (OCR) – pick the deployment/model name you created
AZURE_OCR_DEPLOYMENT=gpt-4o

# Image generation model – your DALL·E-style deployment name
AZURE_IMAGE_DEPLOYMENT=dalle-3


Then load it in code (if not already): from dotenv import load_dotenv; load_dotenv().

Option B — Streamlit Cloud (secrets.toml)

If you deploy on Streamlit Cloud, put secrets in:

.streamlit/secrets.toml


Example:

AZURE_OPENAI_ENDPOINT = "https://<your-endpoint>.openai.azure.com/"
AZURE_OPENAI_API_KEY  = "<your-key>"
AZURE_OPENAI_API_VERSION = "2024-02-15-preview"
AZURE_OCR_DEPLOYMENT = "gpt-4o"
AZURE_IMAGE_DEPLOYMENT = "dalle-3"


There’s a secrets.toml in the repo root now, but Streamlit Cloud reads from .streamlit/secrets.toml, so consider moving it. 
GitHub

Running options
Option 1 — Streamlit app (recommended)

Launch the full UI:

streamlit run streamlit_app.py


Typical flow:

Upload a canvas image OR click “Open camera” (if implemented on your platform).

Click Recognize to run OCR.

(Optional) Click Generate Image to create a DALL·E-style image from the recognized text.

The app entrypoint is streamlit_app.py. 
GitHub

Option 2 — Direct capture (webcam)
python interactive_draw.py


Controls (typical pattern):

Draw with your fingertip in front of the camera.

S to save → writes airtext_output.png to the project root.

C to clear, E to erase mode, Q to quit.
(If your keybindings differ, print help in the script or check the on-screen hints.)

Script name verified from repo. If you changed keybindings, update this section. 
GitHub

Option 3 — OCR & generation (CLI)
# OCR only
python Handwriting_reader.py --image airtext_output.png --task ocr

# OCR + image generation
python Handwriting_reader.py --image airtext_output.png --task generate


Flags you’ll typically support:

--image: path to a PNG/JPG file (default: airtext_output.png)

--task: ocr or generate

Script name verified from repo. Fill in any extra flags you support (e.g., --prompt, --out). 
GitHub

How it works (under the hood)

Fingertip tracking: A hand-landmark detector finds the index fingertip; the tip’s 2D coordinates draw onto an in-memory canvas, which is periodically displayed and can be saved to disk.

OCR: The captured canvas is sent to a vision model (Azure OpenAI vision-capable deployment). The script parses the JSON/text response to extract the best-guess transcription.

Image Generation (optional): Recognized text is used as a prompt and sent to a DALL·E-style image endpoint; image bytes are saved or streamed back to the UI.

chatgpt.py: Small helper to keep API calls in one place (endpoint, headers, models), so your app code stays clean.

Troubleshooting

Black or laggy camera feed
Close other apps using the webcam, reduce resolution/frame rate in code, ensure correct camera index (0/1).

No fingertip detected
Light your hand well; keep a contrasting background; move a bit slower; adjust CV thresholds.

OCR is off / gibberish
Use darker strokes + thicker lines; try white background + black writing; ensure the canvas is not mirrored.

Image generation returns an error
Check your model deployment name and region; verify your API version; confirm billing is active for the image model.

Streamlit cannot see secrets
On Streamlit Cloud, put them in .streamlit/secrets.toml (not root). Locally, use .env or export your env vars.

Roadmap

 One-click “Live camera → OCR → Generate” pipeline in Streamlit

 Eraser thickness & brush color controls in the capture script

 Undo/redo support on the canvas

 Batch OCR for multiple images

 Export PDF of recognized text + generated images

 On-device OCR fallback (Tesseract) for offline mode

FAQ

Q: Do I need Azure for this?
A: The repo is set up with Azure OpenAI style envs. You can swap to OpenAI or another provider by editing chatgpt.py and the calls in Handwriting_reader.py.

Q: Can I use a mouse instead of my finger?
A: Yes—trivially. Replace fingertip coordinates with mouse events on a simple GUI canvas.

Q: Is training required?
A: No—you’re calling foundation models. Just supply an image and get text/back an image.

Acknowledgments

The fingertip tracking approach is inspired by common MediaPipe hand-landmark pipelines and OpenCV drawing techniques.

The Streamlit UI makes everything runnable in the browser with minimal setup.

Vision & image generation via Azure OpenAI (or compatible providers).

License

Pick one and add it as LICENSE:

MIT (most permissive/common)

Apache-2.0

GPL-3.0 (copyleft)

Maintainer

Prabhakar Elavala — feel free to open issues or PRs.
