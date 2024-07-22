import streamlit as st
import google.generativeai as genai
from PIL import Image
import fitz  # PyMuPDF
import io
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def convert_pdf_to_image(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page = pdf_document.load_page(0)  # Load the first page
    pix = page.get_pixmap()
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    pdf_parts = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }
    ]
    return pdf_parts

# Setup Streamlit app
st.set_page_config(page_title="Resume Application Tracking System", layout="wide")
st.markdown("""
    <style>
        .main-title {
            color: #4CAF50;
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 20px;
        }
        .sub-header {
            color: #2196F3;
            font-size: 1.5em;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
        }
        .stTextArea textarea {
            font-size: 16px;
        }
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">📄 Resume Application Tracking System (ATS) Using Google Gemini Pro 🚀</h1>', unsafe_allow_html=True)

st.markdown('<div class="centered">', unsafe_allow_html=True)
input_text = st.text_area("📝 Enter your Job Description text here", key="input")
uploaded_file = st.file_uploader("📂 Upload your Resume", type="pdf", key="file")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    st.write("✅ Uploaded Resume Successfully.")

submit_1 = st.button("🔍 Tell Me about the Resume")
submit_2 = st.button("💡 How can I Improve my Skillset")
submit_3 = st.button("🔑 What Keywords are Missing in my Resume")
submit_4 = st.button("📊 Percentage Match between Resume and Job Description")

input_prompt1 = """
You are an experienced Technical Human Resource Manager with tech experience in any one field of data analysis, data science, machine learning engineering, AI engineering, DevOps, cloud computing, or cybersecurity. 
Your task is to review the provided resume against the job description for these profiles. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a career development coach with extensive knowledge in the fields of data analysis, data science, machine learning engineering, AI engineering, DevOps, cloud computing, or cybersecurity. 
Your task is to review the provided resume and job description, and then suggest ways the candidate can improve their skillset to better align with the job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one field of data analysis, data science, machine learning engineering, AI engineering, DevOps, cloud computing, or cybersecurity, and deep ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. 
First, provide the output as a percentage, then list the missing keywords, and finally, give your final thoughts.
"""

input_prompt4 = """
You are an experienced ATS (Applicant Tracking System) specialist with deep knowledge of keyword optimization in resumes. 
Your task is to review the provided resume and job description, and identify which important keywords are missing from the resume.
"""

if submit_1:
    if uploaded_file is not None:
        pdf_content = convert_pdf_to_image(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.markdown('<h2 class="sub-header">🔍 Resume Evaluation</h2>', unsafe_allow_html=True)
        st.write(response)
    else:
        st.write("📂 Upload your Resume to get the result")

elif submit_2:
    if uploaded_file is not None:
        pdf_content = convert_pdf_to_image(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.markdown('<h2 class="sub-header">💡 Skillset Improvement Suggestions</h2>', unsafe_allow_html=True)
        st.write(response)
    else:
        st.write("📂 Upload your Resume to get the result")

elif submit_3:
    if uploaded_file is not None:
        pdf_content = convert_pdf_to_image(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt4)
        st.markdown('<h2 class="sub-header">🔑 Missing Keywords</h2>', unsafe_allow_html=True)
        st.write(response)
    else:
        st.write("📂 Upload your Resume to get the result")

elif submit_4:
    if uploaded_file is not None:
        pdf_content = convert_pdf_to_image(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.markdown('<h2 class="sub-header">📊 Percentage Match</h2>', unsafe_allow_html=True)
        st.write(response)
    else:
        st.write("📂 Upload your Resume to get the result")
