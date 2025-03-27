from openai import AzureOpenAI
import base64
import openai
from chatgpt import generate_image

# Use secrets
api_key = st.secrets["OPENAI_API_KEY"]
azure_key = st.secrets["AZURE_OPENAI_KEY"]
azure_endpoint = st.secrets["AZURE_ENDPOINT"]
api_version = st.secrets["AZURE_API_VERSION"]


# Configure Azure OpenAI
client = AzureOpenAI(
    api_key=azure_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)


with open("airtext_output.png", "rb") as f:
    base64_image = base64.b64encode(f.read()).decode("utf-8")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "This is a user-drawn image. If there's handwriting, transcribe it. If it's a doodle, describe it."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]
        }
    ],
    max_tokens=300
)

recognized_text = response.choices[0].message.content
print(recognized_text)  # ✅ So Streamlit can capture it

generate_image(recognized_text, client)
