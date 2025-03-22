from dotenv import load_dotenv
import streamlit as st
import os, io, base64
from PIL import Image
import pdf2image
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response=model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_bytes_arr = io.BytesIO()
        first_page.save(img_bytes_arr, format="JPEG")
        img_bytes_arr = img_bytes_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data": base64.b64encode(img_bytes_arr).decode()
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit Interface
st.set_page_config("CVScan - Resume ATS")
st.header("CVScan - Resume Application Tracking System")
job_desc = st.text_area("Enter your Job Description", key="input")     # For user to input Job Description
uploaded_file = st.file_uploader("Upload your Resume (PDF Format).", type=['pdf'])


if uploaded_file is not None:
    st.write("PDF Uploaded successfully")

submit1 = st.button("Tell me about the Resume")
# submit2 = st.button("How can I Optimize this Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, job_desc)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload resume")
if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, job_desc)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload resume")
