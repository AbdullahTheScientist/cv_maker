import streamlit as st
import google.generativeai as genai
from utils.resume_generator import generate_resume
# from utils.gemini_helper import enhance_content, enhance_projects
from utils.job_analyzer import analyze_job_and_score_resume
from utils.templates import get_available_templates
import re
import json



st.set_page_config(
    page_title="AI-Powered Resume Builder",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
with open('styles/main.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None


def main():
    st.title("🚀 AI-Powered Resume Builder")

    # Add tabs for different modes
    tab1, tab2 = st.tabs(["Basic Resume", "ATS-Optimized Resume"])

    with tab1:
        create_basic_resume()

    with tab2:
        create_ats_resume()

def create_basic_resume():
    with st.container():
        st.markdown("### Personal Information")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name*", key="basic_name")
            email = st.text_input("Email Address*", key="basic_email")
            if email and not validate_email(email):
                st.error("Please enter a valid email address")

        with col2:
            phone = st.text_input("Phone Number*", key="basic_phone")
            if phone and not validate_phone(phone):
                st.error("Please enter a valid phone number")
            category = st.selectbox(
                "Professional Category*",
                ["Software Development", "Data Science", "Product Management", 
                 "Marketing", "Design", "Business Analysis", "Other"],
                key="basic_category"
            )

    # Template Selection
    template = st.selectbox(
        "Choose Resume Template*",
        get_available_templates(),
        key="basic_template"
    )

    st.markdown("### Skills & Tools")
    skills = st.text_area(
        "Enter your skills (one per line)*",
        height=100,
        help="Enter technical skills, tools, and technologies you're proficient in",
        key="basic_skills"
    ).split('\n')
    skills = [skill.strip() for skill in skills if skill.strip()]

    st.markdown("### Education")
    educations = st.text_area(
        "Enter your skills (one per line)*",
        height=100,
        help="Enter technical skills, tools, and technologies you're proficient in",
        key="basic_education"
    ).split('\n')
    educations = [education.strip() for education in educations if education.strip()]



    st.markdown("### Professional Summary")
    profile_summary = st.text_area(
        "Provide a brief professional summary*",
        height=150,
        help="Write about your professional background, key skills, and career objectives",
        key="basic_summary"
    )

    st.markdown("### Experience")
    with st.expander("Add Work Experience", expanded=True):
        role = st.text_input("Current/Most Recent Role*", key="basic_role")
        experience = st.text_area(
            "Describe your experience and achievements*",
            height=150,
            key="basic_experience"
        )

    st.markdown("### Projects")
    projects = []
    with st.expander("Add Projects", expanded=True):
        num_projects = st.number_input(
            "Number of projects to add",
            min_value=1,
            max_value=5,
            value=1,
            key="basic_num_projects"  # Added unique key
        )

        for i in range(int(num_projects)):
            st.markdown(f"#### Project {i+1}")
            proj_name = st.text_input(f"Project Name*", key=f"basic_proj_name_{i}")
            proj_github = st.text_input(f"GitHub Link (optional)", key=f"basic_proj_github_{i}")
            proj_summary = st.text_area(
                f"Project Summary*",
                height=100,
                help="Describe the project, technologies used, and outcomes",
                key=f"basic_proj_summary_{i}"
            )
            if proj_name and proj_summary:
                projects.append({
                    'name': proj_name,
                    'github_link': proj_github,
                    'summary': proj_summary
                })

    if st.button("Generate Basic Resume", type="primary", key="basic_generate"):
        generate_resume_content(name, email, phone, category, profile_summary, role, experience, projects, template, skills, educations)


def create_ats_resume():
    st.markdown("### Job Details")
    job_url = st.text_input(
        "Enter Job Posting URL or Description*",
        help="Paste the job URL or full job description to optimize your resume"
    )

    with st.container():
        st.markdown("### Personal Information")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name*", key="ats_name")
            email = st.text_input("Email Address*", key="ats_email")
            if email and not validate_email(email):
                st.error("Please enter a valid email address")

        with col2:
            phone = st.text_input("Phone Number*", key="ats_phone")
            if phone and not validate_phone(phone):
                st.error("Please enter a valid phone number")
            category = st.selectbox(
                "Professional Category*",
                ["Software Development", "Data Science", "Product Management", 
                 "Marketing", "Design", "Business Analysis", "Other"],
                key="ats_category"
            )

    # Template Selection
    template = st.selectbox(
        "Choose Resume Template*",
        get_available_templates(),
        key="ats_template"
    )

    st.markdown("### Skills & Tools")
    skills = st.text_area(
        "Enter your skills (one per line)*",
        height=100,
        help="Enter technical skills, tools, and technologies you're proficient in",
        key="ats_skills"
    ).split('\n')
    skills = [skill.strip() for skill in skills if skill.strip()]



    st.markdown("### Education")
    educations = st.text_area(
        "Enter your skills (one per line)*",
        height=100,
        help="Enter technical skills, tools, and technologies you're proficient in",
        key="ats_education"
    ).split('\n')
    educations = [education.strip() for education in educations if education.strip()]



    st.markdown("### Professional Summary")
    profile_summary = st.text_area(
        "Provide a brief professional summary*",
        height=150,
        help="Write about your professional background, key skills, and career objectives",
        key="ats_summary"
    )

    st.markdown("### Experience")
    with st.expander("Add Work Experience", expanded=True):
        role = st.text_input("Current/Most Recent Role*", key="ats_role")
        experience = st.text_area(
            "Describe your experience and achievements*",
            height=150,
            key="ats_experience"
        )

    st.markdown("### Projects")
    projects = []
    with st.expander("Add Projects", expanded=True):
        num_projects = st.number_input(
            "Number of projects to add",
            min_value=1,
            max_value=5,
            value=1,
            key="ats_num_projects"  # Added unique key
        )

        for i in range(int(num_projects)):
            st.markdown(f"#### Project {i+1}")
            proj_name = st.text_input(f"Project Name*", key=f"ats_proj_name_{i}")
            proj_github = st.text_input(f"GitHub Link (optional)", key=f"ats_proj_github_{i}")
            proj_summary = st.text_area(
                f"Project Summary*",
                height=100,
                help="Describe the project, technologies used, and outcomes",
                key=f"ats_proj_summary_{i}"
            )
            if proj_name and proj_summary:
                projects.append({
                    'name': proj_name,
                    'github_link': proj_github,
                    'summary': proj_summary
                })

    if st.button("Generate ATS-Optimized Resume", type="primary", key="ats_generate"):
        if not job_url:
            st.error("Please provide a job posting URL or description")
            return

        if not all([name, email, phone, category, profile_summary, role, experience, projects, skills]):
            st.error("Please fill in all required fields marked with *")
            return

        with st.spinner("🤖 Analyzing job and optimizing resume..."):
            try:
                # Combine all content for analysis
                resume_content = f"""
                Professional Summary:
                {profile_summary}

                Current Role: {role}

                Experience:
                {experience}

                Projects:
                {projects}
                """

                # Get ATS analysis and optimization
                result = analyze_job_and_score_resume(job_url, resume_content)

                try:
                    # Clean up any markdown formatting that might be in the response
                    analysis_json = result['analysis'].replace('```json', '').replace('```', '').strip()
                    analysis = json.loads(analysis_json)

                    # Display ATS Analysis
                    st.markdown("### ATS Analysis Results")
                    st.metric("ATS Score", f"{analysis['ats_score']}%")

                    with st.expander("View Detailed Analysis"):
                        if analysis.get('missing_keywords'):
                            st.markdown("#### Missing Keywords")
                            st.write(", ".join(analysis['missing_keywords']))

                        if analysis.get('format_issues'):
                            st.markdown("#### Format Issues")
                            for issue in analysis['format_issues']:
                                st.write(f"• {issue}")

                        if analysis.get('suggestions'):
                            st.markdown("#### Improvement Suggestions")
                            for suggestion in analysis['suggestions']:
                                st.write(f"• {suggestion}")

                    # Generate optimized resume
                    optimized_summary = result['optimized_content']
                    pdf_file = generate_resume(
                        name=name,
                        email=email,
                        phone=phone,
                        category=category,
                        summary=optimized_summary,
                        role=role,
                        experience=experience,
                        projects=projects,
                        template_name=template,
                        skills=skills,
                        educations=educations
                    )

                    st.success("✨ Your ATS-optimized resume has been generated!")
                    st.download_button(
                        label="Download ATS-Optimized Resume",
                        data=pdf_file,
                        file_name=f"{name.lower().replace(' ', '_')}_ats_resume.pdf",
                        mime="application/pdf"
                    )

                except json.JSONDecodeError as je:
                    st.error(f"Error processing ATS analysis. Please try again.")
                    print(f"JSON parsing error: {str(je)}")
                    print(f"Raw analysis: {result['analysis']}")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                print(f"Error details: {str(e)}")

# In the imports section at the top of main.py:
from utils.gemini_helper import enhance_content, enhance_project_descriptions, enhance_skills, enhance_education

# Then update the generate_resume_content function:
def generate_resume_content(name, email, phone, category, profile_summary, role, experience, projects, template, skills, educations):
    if not all([name, email, phone, category, profile_summary, role, experience, projects, skills, educations]):
        st.error("Please fill in all required fields marked with *")
        return

    with st.spinner("🤖 AI is crafting your professional resume..."):
        try:
            # Enhance content using Gemini Pro
            enhanced_summary = enhance_content(profile_summary, "professional summary")
            enhanced_experience = enhance_content(experience, "work experience")
            enhanced_projects = enhance_project_descriptions(projects)
            enhanced_skills = enhance_skills(skills)
            enhanced_educations = enhance_education(educations)
            
            # Generate resume
            pdf_file = generate_resume(
                name=name,
                email=email,
                phone=phone,
                category=category,
                summary=enhanced_summary,
                role=role,
                experience=enhanced_experience,
                projects=enhanced_projects,
                template_name=template,
                skills=enhanced_skills,
                educations=enhanced_educations
            )

            st.success("✨ Your resume has been generated successfully!")
            st.download_button(
                label="Download Resume",
                data=pdf_file,
                file_name=f"{name.lower().replace(' ', '_')}_resume.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
if __name__ == "__main__":
    main()