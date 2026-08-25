# -*- coding: utf-8 -*-
"""Generator PDF zapisu rozmów — używany przy każdej aktualizacji."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

INK = HexColor("#1b2430"); EMBER = HexColor("#e8590c"); INDIGO = HexColor("#4c5fd5")
GREEN = HexColor("#0ca678"); RED = HexColor("#c92a2a"); GREY = HexColor("#5c6672")
BGU = HexColor("#eef1ff"); BGA = HexColor("#e6fcf5"); BGW = HexColor("#fff4e6")

S = getSampleStyleSheet()
st_title = ParagraphStyle("t", parent=S["Title"], fontName="DejaVuB", textColor=EMBER, fontSize=22, spaceAfter=2)
st_sub = ParagraphStyle("s", parent=S["Normal"], fontName="DejaVu", textColor=GREY, fontSize=10.5, spaceAfter=10)
st_h = ParagraphStyle("h", parent=S["Heading1"], fontName="DejaVuB", textColor=INDIGO, fontSize=14, spaceBefore=14, spaceAfter=6)
st_user_h = ParagraphStyle("uh", parent=S["Normal"], fontName="DejaVuB", textColor=INDIGO, fontSize=10.5)
st_user = ParagraphStyle("u", parent=S["Normal"], fontName="DejaVu", textColor=INK, fontSize=10, leading=14)
st_act_h = ParagraphStyle("ah", parent=S["Normal"], fontName="DejaVuB", textColor=GREEN, fontSize=10.5)
st_act = ParagraphStyle("a", parent=S["Normal"], fontName="DejaVu", textColor=INK, fontSize=10, leading=14)
st_warn = ParagraphStyle("w", parent=S["Normal"], fontName="DejaVu", textColor=INK, fontSize=10, leading=14)


def block(story, header, text, bg, header_style, body_style):
    t = Table([[Paragraph(header, header_style)], [Paragraph(text, body_style)]], colWidths=[168*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (0, 0), 8), ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (0, 1), 2),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]), ("BOX", (0, 0), (-1, -1), 0.75, bg),
    ]))
    story.append(t); story.append(Spacer(1, 7))


def exchange(story, user_txt, action_txt):
    block(story, "► UŻYTKOWNIK (sens wypowiedzi)", user_txt, BGU, st_user_h, st_user)
    block(story, "► MOJE DZIAŁANIA (stan faktyczny)", action_txt, BGA, st_act_h, st_act)
    story.append(Spacer(1, 4))


def build(path, version, date, intro, exchanges, problems):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=16*mm, bottomMargin=16*mm, title=f"LinguaForge — zapis rozmowy {version}")
    story = [Paragraph(f"LinguaForge — zapis rozmowy · {version}", st_title),
             Paragraph(f"Data: {date} · Format: sens wypowiedzi użytkownika → wykonane działania", st_sub),
             HRFlowable(width="100%", color=EMBER, thickness=2), Spacer(1, 10)]
    if intro:
        story.append(Paragraph(intro, st_user)); story.append(Spacer(1, 8))
    for u, a in exchanges:
        exchange(story, u, a)
    story.append(Paragraph("Potencjalne błędy, kłopoty i propozycje rozwiązań", st_h))
    for p in problems:
        block(story, "• " + p[0], p[1], BGW, ParagraphStyle("wh", parent=st_act_h, textColor=RED), st_warn)
    doc.build(story)
    print("PDF:", path)
