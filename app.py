import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()  # load all our environment variables

# Configure the API key
genai.configure(api_key="AIzaSyDC7F-hQU1SKv_0h7JxRfOdFN0_qCvMxNk")

# Function to get the Gemini response
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from the uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt template for Gemini
input_prompt = """
Hey, Act like a skilled or very experienced ATS (Application Tracking System) with a deep understanding of tech fields, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description. You must consider that the job market is very competitive, and you should provide the best assistance for improving the resume. Assign the percentage matching based on JD and the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string with the structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit app setup
st.title("Smart ATS")
st.text("Improve Your Resume ATS")

# User inputs: Job description and resume upload
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

# When the submit button is pressed
if submit:
    if uploaded_file is not None:
        # Extract text from the uploaded resume
        text = input_pdf_text(uploaded_file)
        
        # Format the input prompt with job description and resume text
        formatted_prompt = input_prompt.format(text=text, jd=jd)
        
        # Get the response from Gemini API
        response = get_gemini_response(formatted_prompt)
        
        # Display the response
        try:
            # Try parsing the response if it's JSON formatted
            response_json = json.loads(response)
            st.subheader("JD Match: " + response_json.get("JD Match", "N/A"))
            st.write("Missing Keywords: " + str(response_json.get("MissingKeywords", [])))
            st.write("Profile Summary: " + response_json.get("Profile Summary", "N/A"))
        except json.JSONDecodeError:
            # In case response is not in JSON format, just show the raw response
            st.subheader("Raw Response:")
            st.write(response)
    else:
        st.write("Please upload the resume")
