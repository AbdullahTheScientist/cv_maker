import google.generativeai as genai
import os


import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def enhance_content(content, content_type):
    """
    Enhance content using Google Gemini Pro
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv('GOOGLE_API_KEY')

        if not api_key:
            raise ValueError("API key is missing. Ensure it is set in the .env file.")

        # Configure API key
        genai.configure(api_key=api_key)
        print(api_key)

        # Initialize Gemini Pro
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        You are enhancing {content_type} for a resume. Your response will be directly included in the resume, so do not ask clarifying questions or assume a conversation.

        If only a job title (e.g., "Data Scientist") is provided, generate a professional summary based on industry standards and key responsibilities.

        As a professional resume writer, improve the following {content_type} by making it more impactful and professional while ensuring accuracy and authenticity. Focus on:

        - Strong action verbs  
        - Quantifiable achievements  
        - Clear and concise language  
        - Professional and compelling tone  
        - Must be more than 30 words
        - Avoid using []
        Original content:  
        {content}
        """

        response = model.generate_content(prompt)
        enhanced_content = response.text.strip()

        return enhanced_content

    except Exception as e:
        raise Exception(f"Error enhancing {content_type}: {str(e)}")


    
def enhance_project_descriptions(projects):
    """
    Enhances project descriptions using Google's Gemini AI.
    
    Args:
        projects (list of dict): A list of project dictionaries, each containing 
                                'name', 'github_link' (optional), and 'summary' keys.
        
    Returns:
        list of dict: Enhanced projects with AI-improved summaries.
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv('GOOGLE_API_KEY')

        if not api_key:
            raise ValueError("API key is missing. Ensure it is set in the .env file.")

        # Configure API key
        genai.configure(api_key=api_key)

        # Initialize Gemini Pro
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        enhanced_projects = []
        
        for project in projects:
            github_info = f"\nGitHub Link: {project['github_link']}" if project.get('github_link') else ""
            
            prompt = f"""
            As a professional resume writer, enhance the following project description to make it more impactful for a resume:
            
            Project Name: {project['name']}{github_info}
            Original Description: {project['summary']}
            
            Enhance this description by:
            1. Using strong action verbs
            2. Highlighting specific technical skills used
            3. Emphasizing measurable outcomes or achievements
            4. Keeping it concise (4-5 lines maximum)
            5. Making it ATS-friendly with relevant keywords
            6. Don't add GitHub link in description
            
            Return only the enhanced description without any additional text, explanations, or bullet points.
            """
            
            response = model.generate_content(prompt)
            enhanced_summary = response.text.strip()
            
            enhanced_projects.append({
                'name': project['name'],
                'github_link': project.get('github_link', ''),
                'summary': enhanced_summary
            })
        
        return enhanced_projects

    except Exception as e:
        print(f"Error enhancing project descriptions: {str(e)}")
        # Return original projects if enhancement fails
        return projects
    
    
def enhance_skills(skills_list):
    """
    Enhances and formats a list of skills for a professional resume.
    Properly capitalizes technology names, expands abbreviations, and ensures consistent formatting.
    
    Args:
        skills_list (list): A list of skill strings to be enhanced
        
    Returns:
        list: Enhanced and properly formatted skills
    """
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError("API key is missing. Ensure it is set in the .env file.")
            
        # Configure API key
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convert list to string for processing
        skills_str = "\n".join(skills_list)
        
        prompt = f"""
        Format and enhance the following list of technical skills for a professional resume.
        For each skill:
        1. Use proper capitalization for technologies, languages, and frameworks (e.g., "Python", "JavaScript", "React.js")
        2. Expand common abbreviations (e.g., "ml" to "Machine Learning", "ai" to "Artificial Intelligence")
        3. Format consistently and professionally
        4. Keep domain-specific terminology intact
        
        Original skills list:
        {skills_str}
        
        Return only the enhanced list, with one skill per line, without numbering or bullet points.
        """
        
        response = model.generate_content(prompt)
        enhanced_skills_text = response.text.strip()
        
        # Convert back to list
        enhanced_skills = [skill.strip() for skill in enhanced_skills_text.split('\n') if skill.strip()]
        
        return enhanced_skills
        
    except Exception as e:
        print(f"Error enhancing skills: {str(e)}")
        # Return original skills if enhancement fails
        return skills_list


def enhance_education(education_list):
    """
    Enhances and formats education entries for a professional resume.
    Properly formats degree abbreviations, institution names, and ensures consistent formatting.
    
    Args:
        education_list (list): A list of education entry strings
        
    Returns:
        list: Enhanced and properly formatted education entries
    """
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError("API key is missing. Ensure it is set in the .env file.")
            
        # Configure API key
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Convert list to string for processing
        education_str = "\n".join(education_list)
        
        prompt = f"""
        Format and enhance the following list of education entries for a professional resume.
        For each entry:
        1. Use proper degree abbreviations (e.g., "BS" to "B.S.", "MBA", "Ph.D.")
        2. Ensure proper capitalization of institution names and fields of study
        3. Format consistently and professionally
        4. If years or GPAs are included, keep them in a standard format
        
        Original education list:
        {education_str}
        
        Return only the enhanced list, with one education entry per line, without numbering or bullet points.
        """
        
        response = model.generate_content(prompt)
        enhanced_education_text = response.text.strip()
        
        # Convert back to list
        enhanced_education = [edu.strip() for edu in enhanced_education_text.split('\n') if edu.strip()]
        
        return enhanced_education
        
    except Exception as e:
        print(f"Error enhancing education entries: {str(e)}")
        # Return original education list if enhancement fails
        return education_list