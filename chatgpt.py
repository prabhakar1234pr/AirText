# dalle_generator.py

from openai import AzureOpenAI

# Azure OpenAI Configuration
# Use secrets
api_key = st.secrets["OPENAI_API_KEY"]
azure_key = st.secrets["AZURE_OPENAI_KEY"]
azure_endpoint = st.secrets["AZURE_ENDPOINT"]
api_version = st.secrets["AZURE_API_VERSION"]
deployment_name = st.secrets["AZURE_DEPLOYMENT_NAME"]

# Configure Azure OpenAI
client = AzureOpenAI(
    api_key=azure_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)


def generate_image(prompt, client):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url


    # Save the image locally
    import requests
    dalle_img = requests.get(image_url).content
    with open("dalle_output.png", "wb") as f:
        f.write(dalle_img)
        print("✅ DALL·E image saved as dalle_output.png",dalle_img)

    return image_url

