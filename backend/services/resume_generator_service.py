"""
Resume Generator Service for creating PDF and DOCX resumes.
"""

import os
import uuid
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from models.resume import ResumeData
from core.config import settings


class ResumeGeneratorService:
    """Service for generating ATS-friendly PDF and DOCX resumes."""

    @staticmethod
    def _ensure_generated_dir():
        """Ensure the generated directory exists."""
        os.makedirs(settings.GENERATED_DIR, exist_ok=True)

    @classmethod
    def generate_pdf(cls, resume_data: ResumeData) -> str:
        """
        Generate an ATS-friendly PDF resume from ResumeData.

        Args:
            resume_data: The resume data to generate PDF from.

        Returns:
            The relative path to the generated PDF file (from backend root).
        """
        cls._ensure_generated_dir()

        # Generate a unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.pdf"
        filepath = os.path.join(settings.GENERATED_DIR, filename)

        # Create the PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Get default styles and create custom ones
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            alignment=1  # Center alignment
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            spaceBefore=12
        )
        normal_style = styles['Normal']
        normal_style.fontSize = 11
        normal_style.spaceAfter = 6

        # Build the story (content)
        story = []

        # Contact Info
        contact_info = resume_data.contact_info
        if contact_info:
            # Assuming contact_info is a dict with keys like 'name', 'email', 'phone', etc.
            contact_lines = []
            if 'name' in contact_info:
                contact_lines.append(f"<b>{contact_info['name']}</b>")
            if 'email' in contact_info:
                contact_lines.append(contact_info['email'])
            if 'phone' in contact_info:
                contact_lines.append(contact_info['phone'])
            if 'location' in contact_info:
                contact_lines.append(contact_info['location'])

            contact_text = " | ".join(contact_lines)
            story.append(Paragraph(contact_text, title_style))
            story.append(Spacer(1, 12))

        # Summary
        if resume_data.summary:
            story.append(Paragraph("Professional Summary", heading_style))
            story.append(Paragraph(resume_data.summary, normal_style))
            story.append(Spacer(1, 12))

        # Experience
        if resume_data.experience:
            story.append(Paragraph("Experience", heading_style))
            for exp in resume_data.experience:
                # Job title and company
                job_title = f"<b>{exp.title}</b> - <b>{exp.company}</b>"
                story.append(Paragraph(job_title, normal_style))
                # Dates
                date_range = f"{exp.start_date}"
                if exp.end_date:
                    date_range += f" - {exp.end_date}"
                else:
                    date_range += " - Present"
                story.append(Paragraph(date_range, normal_style))
                story.append(Spacer(1, 6))

                # Description bullets
                if exp.description:
                    bullet_items = []
                    for desc in exp.description:
                        bullet_items.append(ListItem(Paragraph(desc, normal_style)))
                    story.append(ListFlowable(bullet_items, bulletType='bullet', start='•'))
                story.append(Spacer(1, 12))

        # Education
        if resume_data.education:
            story.append(Paragraph("Education", heading_style))
            for edu in resume_data.education:
                edu_text = f"<b>{edu.degree}</b> - <b>{edu.institution}</b>"
                story.append(Paragraph(edu_text, normal_style))
                date_text = edu.graduation_year
                if edu.gpa:
                    date_text += f" | GPA: {edu.gpa}"
                story.append(Paragraph(date_text, normal_style))
                story.append(Spacer(1, 12))

        # Skills
        if resume_data.skills:
            story.append(Paragraph("Skills", heading_style))
            # Create a comma-separated list of skills
            skills_text = ", ".join(resume_data.skills)
            story.append(Paragraph(skills_text, normal_style))
            story.append(Spacer(1, 12))

        # Achievements
        if resume_data.achievements:
            story.append(Paragraph("Achievements", heading_style))
            bullet_items = []
            for ach in resume_data.achievements:
                bullet_items.append(ListItem(Paragraph(ach, normal_style)))
            story.append(ListFlowable(bullet_items, bulletType='bullet', start='•'))
            story.append(Spacer(1, 12))

        # Build the PDF
        doc.build(story)

        # Return the relative path from the backend directory
        return os.path.join(settings.GENERATED_DIR, filename)

    @classmethod
    def generate_docx(cls, resume_data: ResumeData) -> str:
        """
        Generate an ATS-friendly DOCX resume from ResumeData.

        Args:
            resume_data: The resume data to generate DOCX from.

        Returns:
            The relative path to the generated DOCX file (from backend root).
        """
        cls._ensure_generated_dir()

        # Generate a unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.docx"
        filepath = os.path.join(settings.GENERATED_DIR, filename)

        # Create the document
        doc = Document()

        # Set margins (optional, but good practice)
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.75)
            section.bottom_margin = Inches(0.75)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)

        # Add content

        # Contact Info
        contact_info = resume_data.contact_info
        if contact_info:
            contact_parts = []
            if 'name' in contact_info:
                contact_parts.append(contact_info['name'])
            if 'email' in contact_info:
                contact_parts.append(contact_info['email'])
            if 'phone' in contact_info:
                contact_parts.append(contact_info['phone'])
            if 'location' in contact_info:
                contact_parts.append(contact_info['location'])

            contact_line = " | ".join(contact_parts)
            p = doc.add_paragraph(contact_line)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Make the name bold (if we have it)
            # Note: This is a simple approach; for more control, we could use runs.
            # For simplicity, we'll just make the whole line bold if there's a name.
            # But let's not overcomplicate for now.
            doc.add_paragraph()  # Add a blank line after contact

        # Summary
        if resume_data.summary:
            doc.add_heading('Professional Summary', level=2)
            doc.add_paragraph(resume_data.summary)
            doc.add_paragraph()  # Blank line

        # Experience
        if resume_data.experience:
            doc.add_heading('Experience', level=2)
            for exp in resume_data.experience:
                # Job title and company
                p = doc.add_paragraph()
                p.add_run(f"{exp.title} - {exp.company}").bold = True
                # Dates
                date_range = f"{exp.start_date}"
                if exp.end_date:
                    date_range += f" - {exp.end_date}"
                else:
                    date_range += " - Present"
                p.add_run(f"\t{date_range}").italic = True
                p.add_run('\n')

                # Description bullets
                if exp.description:
                    for desc in exp.description:
                        bullet = doc.add_paragraph(desc, style='List Bullet')
                doc.add_paragraph()  # Blank line between jobs

        # Education
        if resume_data.education:
            doc.add_heading('Education', level=2)
            for edu in resume_data.education:
                p = doc.add_paragraph()
                p.add_run(f"{edu.degree} - {edu.institution}").bold = True
                edu_text = edu.graduation_year
                if edu.gpa:
                    edu_text += f" | GPA: {edu.gpa}"
                p.add_run(f"\t{edu_text}").italic = True
                doc.add_paragraph()  # Blank line

        # Skills
        if resume_data.skills:
            doc.add_heading('Skills', level=2)
            skills_text = ", ".join(resume_data.skills)
            doc.add_paragraph(skills_text)
            doc.add_paragraph()  # Blank line

        # Achievements
        if resume_data.achievements:
            doc.add_heading('Achievements', level=2)
            for ach in resume_data.achievements:
                doc.add_paragraph(ach, style='List Bullet')

        # Save the document
        doc.save(filepath)

        # Return the relative path from the backend directory
        return os.path.join(settings.GENERATED_DIR, filename)