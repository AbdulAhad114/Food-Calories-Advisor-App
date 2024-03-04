from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(image, prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Food Calories Advisor App")
st.header("Food Calories Advisor App")

# Input for API Key
api_key = st.text_input("Enter your Google Gemini API Key:", type="password")

input_prompt = """
            You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               Finally you can also mention whether the food is healthy or not and 
               also mention
               the percentage split of the ratio of carbohydrates, fats, fibers, sugaar 
               and other important things required in our diet. 
               If the food is unhealthy, gave user the options if these
               items were remove or replace with a healthy food. It help their diet.
"""

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

## If submit button is clicked
if submit:
    if api_key:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(image_data, input_prompt, api_key)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.error("Please enter your Google Gemini API Key.")
