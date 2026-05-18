from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors
import re
import os

def markdown_to_pdf(markdown_text: str, output_path: str = "report.pdf") -> str:
    """Convert markdown research report to PDF"""
    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=inch,
            leftMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=20
        )
        h1_style = ParagraphStyle(
            'CustomH1',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#16213e'),
            spaceBefore=15,
            spaceAfter=8
        )
        h2_style = ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#0f3460'),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=16,
            spaceAfter=8
        )
        ref_style = ParagraphStyle(
            'RefStyle',
            parent=styles['Normal'],
            fontSize=9,
            leading=14,
            leftIndent=20,
            spaceAfter=4
        )

        story = []
        lines = markdown_text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
                continue

            # Clean markdown formatting
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
            line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', line)

            if line.startswith('# '):
                story.append(Paragraph(line[2:], title_style))
                story.append(HRFlowable(width="100%", thickness=1,
                              color=colors.HexColor('#1a1a2e')))
                story.append(Spacer(1, 10))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], h1_style))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], h2_style))
            elif line.startswith('- ') or line.startswith('* '):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            elif re.match(r'^\d+\.', line):
                story.append(Paragraph(line, body_style))
            elif line.startswith('[') and ']' in line:
                story.append(Paragraph(line, ref_style))
            else:
                try:
                    story.append(Paragraph(line, body_style))
                except:
                    story.append(Paragraph(line.encode('ascii', 'ignore').decode(), body_style))

        doc.build(story)
        return output_path

    except Exception as e:
        return f"PDF generation error: {str(e)}"