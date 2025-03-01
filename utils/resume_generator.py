# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib import colors
# import io
# from utils.templates import get_template_function

# def generate_resume(name, email, phone, category, summary, role, experience, projects, template_name="Modern", skills=None):
#     """
#     Generate a professionally formatted resume using ReportLab
#     """
#     try:
#         # Create a buffer for the PDF
#         buffer = io.BytesIO()

#         # Create the PDF object
#         pdf = canvas.Canvas(buffer)  # Remove pagesize to allow multiple pages
#         width, height = letter

#         # Get the template function
#         template_func = get_template_function(template_name)

#         # Starting y position
#         y_position = height - inch

#         # Draw template header and get updated y position
#         y_position = template_func(pdf, width, height, name, email, phone, category, y_position)

#         # Draw vertical line for skills section
#         pdf.setLineWidth(2)
#         pdf.setStrokeColor(colors.black)
#         pdf.line(2.5*inch, y_position, 2.5*inch, 2*inch)

#         # Draw skills section on the left
#         pdf.setFont("Helvetica-Bold", 14)
#         pdf.drawString(0.75*inch, y_position - 0.5*inch, "Skills")
#         y_skills = y_position - inch

#         # Add skills with bullet points
#         pdf.setFont("Helvetica", 10)
#         for skill in skills or []:
#             pdf.drawString(0.95*inch, y_skills, "•")
#             pdf.drawString(1.25*inch, y_skills, skill)
#             y_skills -= 20

#         # Start main content area
#         x_position = 3*inch
#         content_width = width - 3.5*inch
#         y_content = y_position - 0.5*inch

#         # Professional Summary
#         pdf.setFont("Helvetica-Bold", 14)
#         pdf.drawString(x_position, y_content, "Professional Summary")
#         y_content -= 25

#         # Summary content
#         pdf.setFont("Helvetica", 11)
#         summary_lines = _wrap_text(summary, pdf, content_width)
#         for line in summary_lines:
#             pdf.drawString(x_position, y_content, line)
#             y_content -= 15

#         # Professional Experience
#         y_content -= 20
#         pdf.setFont("Helvetica-Bold", 14)
#         pdf.drawString(x_position, y_content, "Professional Experience")
#         y_content -= 25

#         # Current Role
#         pdf.setFont("Helvetica-Bold", 12)
#         pdf.drawString(x_position, y_content, role)
#         y_content -= 20

#         # Experience details
#         pdf.setFont("Helvetica", 11)
#         experience_lines = _wrap_text(experience, pdf, content_width)
#         for line in experience_lines:
#             if y_content < 2*inch:
#                 pdf.showPage()
#                 y_content = height - inch
#                 # Redraw vertical line on new page
#                 pdf.setLineWidth(2)
#                 pdf.setStrokeColor(colors.black)
#                 pdf.line(2.5*inch, height - inch, 2.5*inch, 2*inch)

#             pdf.drawString(x_position, y_content, line)
#             y_content -= 15

#         # Projects Section
#         y_content -= 20
#         pdf.setFont("Helvetica-Bold", 14)
#         pdf.drawString(x_position, y_content, "Key Projects")
#         y_content -= 5

#         # Process each project
#         for project in projects:
#             if y_content < 3.5*inch:
#                 pdf.showPage()
#                 y_content = height - inch
#                 # Redraw vertical line on new page
#                 pdf.setLineWidth(2)
#                 pdf.setStrokeColor(colors.black)
#                 pdf.line(2.5*inch, height - inch, 2.5*inch, 2*inch)

#             # Project title
#             pdf.setFont("Helvetica-Bold", 12)
#             title = project.get('name', '')
#             pdf.drawString(x_position, y_content, title)

#             # GitHub link
#             if project.get('github_link'):
#                 pdf.setFont("Helvetica", 9)
#                 pdf.setFillColor(colors.blue)
#                 link_x = x_position + pdf.stringWidth(title, "Helvetica-Bold", 12) + 10
#                 pdf.drawString(link_x, y_content, "[GitHub]")
#                 pdf.setFillColor(colors.black)

#             y_content -= 15

#             # Project summary
#             pdf.setFont("Helvetica", 11)
#             summary_lines = _wrap_text(project.get('summary', ''), pdf, content_width)
#             for line in summary_lines:
#                 if y_content < 2*inch:
#                     pdf.showPage()
#                     y_content = height - inch
#                     # Redraw vertical line on new page
#                     pdf.setLineWidth(2)
#                     pdf.setStrokeColor(colors.black)
#                     pdf.line(2.5*inch, height - inch, 2.5*inch, 2*inch)

#                 pdf.drawString(x_position + 15, y_content, "• " + line)
#                 y_content -= 15

#             y_content -= 15

#         # Save the PDF
#         pdf.save()

#         # Get the value from the buffer
#         buffer.seek(0)
#         return buffer.getvalue()

#     except Exception as e:
#         print(f"Error generating resume PDF: {str(e)}")  # Add logging
#         raise Exception(f"Failed to generate resume PDF: {str(e)}")

# def _wrap_text(text, pdf, max_width):
#     """Helper function to wrap text within specified width"""
#     if not text:
#         return []

#     text = text.replace('*', '').strip()  # Remove any markdown formatting
#     words = text.split()
#     lines = []
#     current_line = []

#     for word in words:
#         current_line.append(word)
#         line_width = pdf.stringWidth(' '.join(current_line), "Helvetica", 11)
#         if line_width > max_width:
#             if len(current_line) > 1:
#                 current_line.pop()
#                 lines.append(' '.join(current_line))
#                 current_line = [word]
#             else:
#                 lines.append(word)
#                 current_line = []

#     if current_line:
#         lines.append(' '.join(current_line))

#     return lines







from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import io
from utils.templates import get_template_function


def generate_resume(name, email, phone, category, summary, role, experience, projects, template_name="Modern", skills=None, educations=None):
    """
    Generate a professionally formatted resume using ReportLab
    """
    try:
        # Create a buffer for the PDF
        buffer = io.BytesIO()

        # Create the PDF object
        pdf = canvas.Canvas(buffer)  
        width, height = letter

        # Get the template function
        template_func = get_template_function(template_name)

        # Starting y position
        y_position = height - inch

        # Draw template header and get updated y position
        y_position = template_func(pdf, width, height, name, email, phone, category, y_position)

        # Draw vertical line for skills section
        pdf.setLineWidth(2)
        pdf.setStrokeColor(colors.black)
        pdf.line(2.4*inch, y_position, 2.4*inch, 2*inch)

        # # Draw skills section
        # pdf.setFont("Helvetica-Bold", 14)
        # pdf.drawString(0.50*inch, y_position - 0.5*inch, "Skills")
        # y_skills = y_position - inch

        # pdf.setFont("Helvetica", 10)
        # for skill in skills or []:
        #     pdf.drawString(0.50*inch, y_skills, "•")
        #     pdf.drawString(0.72*inch, y_skills, skill)
        #     y_skills -= 20


        # pdf.setFont("Helvetica-Bold", 14)
        # pdf.drawString(0.75*inch, y_position - 0.75*inch, "Educations")
        # y_educations = y_position - inch

        # pdf.setFont("Helvetica", 10)
        # for education in educations or []:
        #     pdf.drawString(0.50*inch, y_educations, "•")
        #     pdf.drawString(0.72*inch, y_educations, education)
        #     y_educations -= 20




        # Draw Education Section First
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(0.50*inch, y_position - 0.5*inch, "Education")
        y_education = y_position - inch  

        pdf.setFont("Helvetica", 10)
        for edu in educations or []:
            if y_education < 2.5 * inch:  # Check if we need a new page
                pdf.showPage()
                y_education = height - inch  # Reset y_position for new page
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(0.50*inch, y_education, "Education")
                y_education -= 20

            pdf.drawString(0.50*inch, y_education, "•")
            pdf.drawString(0.72*inch, y_education, edu)
            y_education -= 20

        # Adjust y_position to the last education entry before starting Skills
        y_skills = y_education - 30  

        # Draw Skills Section
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(0.50*inch, y_skills, "Skills")
        y_skills -= 20

        pdf.setFont("Helvetica", 10)
        for skill in skills or []:
            if y_skills < 2.5 * inch:  # Check if we need a new page
                pdf.showPage()
                y_skills = height - inch
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(0.50*inch, y_skills, "Skills")
                y_skills -= 20

            pdf.drawString(0.50*inch, y_skills, "•")
            pdf.drawString(0.72*inch, y_skills, skill)
            y_skills -= 20



      
        # Main content area
        x_position = 2.6*inch
        content_width = width - 3.5*inch
        y_content = y_position - 0.5*inch

        # Professional Summary
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x_position, y_content, "Professional Summary")
        y_content -= 20

        pdf.setFont("Helvetica", 11)
        summary_lines = _wrap_text(summary, pdf, content_width)
        for line in summary_lines:
            pdf.drawString(x_position, y_content, line)
            y_content -= 15

        # Professional Experience
        y_content -= 20
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x_position, y_content, "Professional Experience")
        y_content -= 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x_position, y_content, role)
        y_content -= 15

        pdf.setFont("Helvetica", 11)
        experience_lines = _wrap_text(experience, pdf, content_width)
        for line in experience_lines:
            if y_content < 1.5*inch:  # Adjusted Page Break Threshold
                pdf.showPage()
                y_content = height - inch
                pdf.setLineWidth(2)
                pdf.setStrokeColor(colors.black)
                pdf.line(2.5*inch, height - inch, 2.5*inch, 2*inch)

            pdf.drawString(x_position, y_content, line)
            y_content -= 15

            
        first_page = True  # Track if it's the first page
        MIN_SPACE_BEFORE_NEW_PAGE = 30  # Space for two lines
        NEW_PAGE_START_Y = height - 0.2 * inch  # Adjust starting position on a new page

        y_content -= 25
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x_position, y_content, "Key Projects")
        y_content -= 20

        for project in projects:
            # Ensure at least two lines of space before page break
            if y_content < MIN_SPACE_BEFORE_NEW_PAGE:
                pdf.showPage()
                y_content = NEW_PAGE_START_Y  # Start next page closer to the top

                # Draw vertical line for skills section on new page
                pdf.setLineWidth(2)
                pdf.setStrokeColor(colors.black)
                # pdf.line(2.2 * inch, height - inch, 2.2 * inch, 2 * inch)
                pdf.line(2.2 * inch, height - 0.1 * inch, 2.2 * inch, 1.5 * inch)  


                # Add "Key Projects" only on the first page
                if first_page:
                    pdf.setFont("Helvetica-Bold", 14)
                    pdf.drawString(x_position, y_content, "Key Projects")
                    y_content -= 20
                    first_page = False  # Ensure it's not repeated on next pages

            # Project Name
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(x_position, y_content, project.get('name', ''))

            # GitHub Link
            if project.get('github_link'):
                pdf.setFont("Helvetica", 9)
                pdf.setFillColor(colors.blue)
                link_x = x_position + pdf.stringWidth(project.get('name', ''), "Helvetica-Bold", 12) + 10
                pdf.drawString(link_x, y_content, "[GitHub]")
                pdf.linkURL(project.get('github_link'), (link_x, y_content, link_x + 40, y_content + 10))
                pdf.setFillColor(colors.black)

            y_content -= 20  # Move down for summary

            # Project Summary
            pdf.setFont("Helvetica", 11)
            summary_lines = _wrap_text(project.get('summary', ''), pdf, content_width)

            for line in summary_lines:
                if y_content < MIN_SPACE_BEFORE_NEW_PAGE:
                    pdf.showPage()
                    y_content = NEW_PAGE_START_Y  # Start new page at correct position

                    # Draw vertical line for skills section on new page
                    pdf.setLineWidth(2)
                    pdf.setStrokeColor(colors.black)
                    pdf.line(2.2 * inch, height - 0.2 * inch, 2.2 * inch, 0.5 * inch)


                pdf.drawString(x_position + 10, y_content, line)
                y_content -= 15  # Line spacing

        # Ensure only 2 lines of space at the bottom before new page
        if y_content < MIN_SPACE_BEFORE_NEW_PAGE:
            pdf.showPage()

            


        y_content -= 25


        pdf.save()
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        print(f"Error generating resume PDF: {str(e)}")  
        raise Exception(f"Failed to generate resume PDF: {str(e)}")

def _wrap_text(text, pdf, max_width):
    """Helper function to wrap text within specified width"""
    if not text:
        return []

    text = text.replace('*', '').strip()
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        line_width = pdf.stringWidth(' '.join(current_line), "Helvetica", 11)
        if line_width > max_width:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []

    if current_line:
        lines.append(' '.join(current_line))

    return lines
