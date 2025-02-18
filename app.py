import streamlit as st
import google.generativeai as gai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
gai.configure(api_key=os.getenv('GENAI_API_KEY'))

# Function to get Gemini response
def get_gemini_response(text):
    model = gai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    return getattr(response, "text", "Error: No response")

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:  # Avoid NoneType errors
            text += extracted_text + "\n"

    return text.strip()

# Prompt Template
prompt_template = """
Analyze the following resume against the given job description and provide a structured analysis.

**Expected Output Format:**
Match Percentage: (Numeric value from 0-100%)  
Missing Keywords: (List of missing important keywords)  
Suggestions: (Actionable improvements for keyword integration and content refinement)  
ATS Compliance Issues: (Formatting, readability, and structure suggestions for better ATS compatibility)  
Optimized Resume: (An improved, ATS-friendly version of the resume)

Resume:
{text}

Job Description:
{jd}
"""

# Streamlit UI
st.title("📄 Resume Analysis Tool")
st.text("Upload your resume and compare it with the job description.")

jd = st.text_area("✍️ Job Description", placeholder="Paste the job description here")
uploaded_file = st.file_uploader("📂 Choose a file", type=['pdf'], help="Upload your resume in PDF format")
submit = st.button("🚀 Submit")

# Handle submission
if submit:
    if uploaded_file is not None:
        st.text("🔄 Extracting text from PDF...")
        text = input_pdf_text(uploaded_file)
        
        if text:
            st.text("✅ Successfully extracted text from the PDF.")
            full_prompt = prompt_template + "\nResume:\n" + text + "\n\nJob Description:\n" + jd
            response = get_gemini_response(full_prompt)
            
            st.subheader("📊 Analysis Results")
            st.write(response)  # Display structured output
            
        else:
            st.error("❌ Failed to extract text from the PDF. Try a different file.")
    
    else:
        st.warning("⚠️ Please upload a resume before submitting.")

