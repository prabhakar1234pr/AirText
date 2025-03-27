import streamlit as st
import subprocess
import os

st.set_page_config(page_title="AirText", layout="centered")

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #8e44ad;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #732d91;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✍️ AirText: Draw. Recognize. Generate.")
st.markdown("**Use one finger to draw. Use two fingers to select modes like Draw, Erase, or Color.**")

st.markdown("### Step 1: Draw in Camera Window")
st.write("Click below to open the drawing interface.")

st.write("Click on C to clear your drawing.")
st.write("Click on S to save your drawing before proceeding.")
st.write("Click on esc or Q to exit the drawing interface.")
st.write("Once your drawing is saved, click below to analyze it and generate a matching image.")
if st.button("🎨 Launch Drawing Canvas"):
    subprocess.run(["python", "interactive_draw.py"], shell=True)
    st.success("Canvas closed. Image saved as `airtext_output.png`")

st.markdown("---")
st.markdown("### Step 2: Recognize and Generate")

if st.button("🧠 Analyze Drawing & Generate Image"):
    with st.spinner("Recognizing handwriting and generating image..."):
        result = subprocess.run(
            ["python", "Handwriting_reader.py"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    if result.stdout:
        recognized_text = result.stdout.strip().splitlines()[-1]
        st.markdown(f"📝 **Recognized Text:** {recognized_text}")

    if os.path.exists("airtext_output.png"):
        st.image("airtext_output.png", caption="🖼️ Your Drawing", use_column_width=True)

    if os.path.exists("dalle_output.png"):
        st.image("dalle_output.png", caption="🎨 DALL·E Generated Image", use_column_width=True)

    st.success("Done!")
