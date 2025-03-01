from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

def modern_template(pdf, width, height, name, email, phone, category, y_position):
    """
    Modern template with clean layout and black accents
    """
    # Set default font
    pdf.setFont("Helvetica-Bold", 24)

    # Header - Name
    pdf.drawCentredString(width/2, y_position, name)
    y_position -= 0.3*inch

    # Contact Information
    pdf.setFont("Helvetica", 10)
    contact_info = f"{email} | {phone}"
    if category:
        contact_info += f" | {category}"
    pdf.drawCentredString(width/2, y_position, contact_info)

    return y_position - inch  # Return updated y position

def professional_template(pdf, width, height, name, email, phone, category, y_position):
    """
    Professional template with traditional layout
    """
    # Header with name
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(inch, y_position, name.upper())

    # Draw a line under the name
    y_position -= 0.2*inch
    pdf.setLineWidth(1)
    pdf.setStrokeColor(colors.black)
    pdf.line(inch, y_position, width - inch, y_position)

    # Contact information in right corner
    pdf.setFont("Helvetica", 9)
    y_contact = y_position + 0.7*inch
    pdf.drawRightString(width - inch, y_contact, email)
    pdf.drawRightString(width - inch, y_contact - 12, phone)
    if category:
        pdf.drawRightString(width - inch, y_contact - 24, category)

    return y_position - inch  # Return updated y position

def get_template_function(template_name):
    """
    Returns the appropriate template function based on template name
    """
    templates = {
        "Modern": modern_template,
        "Professional": professional_template
    }
    return templates.get(template_name, modern_template)

def get_available_templates():
    """
    Returns list of available template names
    """
    return ["Modern", "Professional"]