"""
File: pdf_generator.py

Purpose: Takes the model's JSON output and converts it into a PDF.

Note: This is AI-generated code because the specific layout and formatting for the PDF is difficult to design manually.
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(data: dict, output_path: Path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )
    
    list_style = ParagraphStyle(
        'ListText',
        parent=body_style,
        leftIndent=20,
        spaceAfter=4
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=body_style,
        fontSize=9,
        textColor=colors.HexColor('#718096')
    )

    story = []
    
    story.append(Paragraph("InferR Execution Report", title_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Problem Summary", h2_style))
    story.append(Paragraph(data.get("problem_summary", "N/A"), body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Solution Pathway", h2_style))
    pathway = data.get("solution_pathway", [])
    if isinstance(pathway, list):
        for step in pathway:
            story.append(Paragraph(f"• {step}", list_style))
    else:
        story.append(Paragraph(str(pathway), body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Evidence & Grounding", h2_style))
    evidence = data.get("evidence", [])
    if isinstance(evidence, list):
        for item in evidence:
            story.append(Paragraph(f"• {item}", list_style))
    else:
        story.append(Paragraph(str(evidence), body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Final Conclusion", h2_style))
    story.append(Paragraph(f"<b>Answer:</b> {data.get('final_answer', 'N/A')}", body_style))
    story.append(Spacer(1, 15))
    
    confidence = data.get("confidence_score", "N/A")
    story.append(Paragraph(f"System Confidence Score: {confidence}%", meta_style))
    
    doc.build(story)
