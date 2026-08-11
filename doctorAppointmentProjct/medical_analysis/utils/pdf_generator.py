from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Image as ReportLabImage
from django.conf import settings
import os
from datetime import datetime


def generate_medical_report(analysis):
    """Generate comprehensive PDF report for medical analysis - Clean version without background color issues"""

    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    # PDF filename with timestamp to avoid caching
    timestamp = int(datetime.now().timestamp())
    filename = f"medical_report_{analysis.id}_{timestamp}.pdf"
    filepath = os.path.join(reports_dir, filename)

    # Create PDF document with proper margins
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()

    # Clean styles without problematic background colors
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        spaceAfter=20,
        alignment=1,
        fontName='Helvetica-Bold'
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.darkblue,
        spaceAfter=8,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )

    normal_text = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        leading=12
    )

    bullet_text = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=3,
        leftIndent=20,
        leading=12
    )

    # Add a small text style for table cells
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        spaceAfter=2
    )

    # Start building content
    story = []

    # Header
    story.append(Paragraph("SYMPWISE Report", title_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_text))
    story.append(Spacer(1, 20))

    # Patient Information Section
    story.append(Paragraph("Patient Information", section_heading))

    patient_data = [
        ["Patient Name:", analysis.user.get_full_name() or analysis.user.username],
        ["Analysis Type:", analysis.get_analysis_type_display()],
        ["Analysis Date:", datetime.now().strftime("%B %d, %Y at %I:%M %p")],
        ["Report Generated:", datetime.now().strftime("%B %d, %Y at %I:%M %p")],
    ]

    # Simple table without background colors
    patient_table = Table(patient_data, colWidths=[2 * inch, 4 * inch])
    patient_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(patient_table)
    story.append(Spacer(1, 16))

    # Symptoms Section
    if analysis.symptoms_text:
        story.append(Paragraph("Reported Symptoms", section_heading))
        story.append(Paragraph(analysis.symptoms_text, normal_text))
        story.append(Spacer(1, 12))

    # Image Section
    if analysis.uploaded_image:
        story.append(Paragraph("Analyzed Image", section_heading))
        try:
            img_path = os.path.join(settings.MEDIA_ROOT, str(analysis.uploaded_image))
            if os.path.exists(img_path):
                img = ReportLabImage(img_path, width=3 * inch, height=2.5 * inch)
                story.append(img)
                story.append(Spacer(1, 12))
        except Exception:
            story.append(Paragraph("Image could not be included in the report.", normal_text))
            story.append(Spacer(1, 12))

    # Analysis Results
    if analysis.analysis_result and 'error' not in analysis.analysis_result:
        result = analysis.analysis_result

        # Visual Observations
        if result.get('visual_observations'):
            story.append(Paragraph("Visual Observations", section_heading))
            for obs in result['visual_observations']:
                story.append(Paragraph(f"• {obs}", bullet_text))
            story.append(Spacer(1, 12))

        # Possible Conditions - FIXED TO PREVENT OVERFLOW
        if result.get('possible_conditions'):
            story.append(Paragraph("Possible Conditions", section_heading))

            # Create table with Paragraph objects for proper text wrapping
            conditions_data = [
                [
                    Paragraph("<b>Rank</b>", table_text),
                    Paragraph("<b>Condition</b>", table_text),
                    Paragraph("<b>Probability</b>", table_text),
                    Paragraph("<b>Description</b>", table_text)
                ]
            ]

            for i, condition in enumerate(result['possible_conditions'], 1):
                name = condition.get('condition', 'N/A')
                prob = str(condition.get('probability', condition.get('confidence', 'N/A')))
                desc = condition.get('description', condition.get('reasoning', 'N/A'))

                # Wrap each cell in a Paragraph for automatic text wrapping
                conditions_data.append([
                    Paragraph(str(i), table_text),
                    Paragraph(name, table_text),
                    Paragraph(prob, table_text),
                    Paragraph(desc, table_text)  # This will now wrap properly
                ])

            conditions_table = Table(conditions_data, colWidths=[0.5 * inch, 1.8 * inch, 1 * inch, 2.7 * inch])
            conditions_table.setStyle(TableStyle([
                # Header styling
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),

                # Data styling
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),

                # General styling
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))

            story.append(conditions_table)
            story.append(Spacer(1, 12))


        # Next Steps
        if result.get('next_steps'):
            story.append(Paragraph("Recommended Next Steps", section_heading))
            for i, step in enumerate(result['next_steps'], 1):
                story.append(Paragraph(f"{i}. {step}", bullet_text))
            story.append(Spacer(1, 12))

    else:
        # Handle errors or missing results
        story.append(Paragraph("Analysis Results", section_heading))
        if analysis.analysis_result and 'error' in analysis.analysis_result:
            error_msg = analysis.analysis_result.get('message', 'Analysis could not be completed.')
            story.append(Paragraph(f"Error: {error_msg}", normal_text))
        else:
            story.append(Paragraph("Analysis is still processing or results are not available.", normal_text))
        story.append(Spacer(1, 12))

    # Medical Disclaimer
    story.append(Spacer(1, 20))
    story.append(Paragraph("Important Medical Disclaimer", section_heading))

    disclaimer = """This report is generated by an AI system for informational purposes only and should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions regarding a medical condition. Never disregard professional medical advice or delay seeking it because of information in this report. If you are experiencing a medical emergency, contact emergency services immediately."""

    # Simple disclaimer without background colors
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.red,
        borderWidth=1,
        borderColor=colors.red,
        borderPadding=8,
        leading=11
    )

    story.append(Paragraph(disclaimer, disclaimer_style))

    # Footer
    story.append(Spacer(1, 10))
    footer = f"Report ID: {analysis.id} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    story.append(Paragraph(footer, footer_style))

    # Build the PDF
    doc.build(story)
    return filepath


