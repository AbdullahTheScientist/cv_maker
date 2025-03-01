import google.generativeai as genai
import os
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def extract_job_description(url):
    """
    Extract job description from URL
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        raise Exception(f"Failed to extract job description: {str(e)}")

def analyze_job_and_score_resume(job_url, resume_content):
    """
    Analyze job description and score resume
    """
    try:
        # Configure Gemini
        genai.configure(api_key="AIzaSyBOygA4Dsti6gaIoPOqY45THz7UT7DeLwE")

        # genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-pro')


        # Extract job description
        job_description = extract_job_description(job_url) if is_valid_url(job_url) else job_url

        analysis_prompt = f"""
        As an ATS (Applicant Tracking System) expert, analyze this job description 
        and the candidate's resume content. Provide the analysis in the following JSON format:
        {{
            "ats_score": <number between 0-100>,
            "missing_keywords": [<list of important keywords from job description missing in resume>],
            "format_issues": [<list of formatting or structure issues>],
            "suggestions": [<list of specific improvement suggestions>]
        }}

        Job Description:
        {job_description}

        Resume Content:
        {resume_content}
        """

        analysis_response = model.generate_content(analysis_prompt)
        analysis = analysis_response.text.strip()

        # Clean up any markdown formatting that might be in the response
        analysis = analysis.replace('```json', '').replace('```', '').strip()
        try:
          analysis = json.loads(analysis)
        except json.JSONDecodeError as e:
          raise Exception(f"Invalid JSON response from Gemini: {analysis}, Error: {e}")


        # Generate ATS-optimized content
        optimization_prompt = f"""
        Based on this job description, enhance the resume content to be more ATS-friendly:

        Job Description:
        {job_description}

        Current Content:
        {resume_content}

        Focus on:
        - Including relevant keywords from the job description
        - Using standardized section headings
        - Quantifying achievements
        - Clear formatting
        """

        optimization_response = model.generate_content(optimization_prompt)
        optimized_content = optimization_response.text.strip()

        return {
            'analysis': analysis,
            'optimized_content': optimized_content
        }

    except Exception as e:
        raise Exception(f"Error analyzing job and scoring resume: {str(e)}")