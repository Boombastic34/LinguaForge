# -*- coding: utf-8 -*-
"""Generator katalogu materiałów LinguaForge w PDF (czytelny, kolorowy)."""
import os
import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, PageBreak,
                                KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
if os.path.exists(FONT_DIR):
    pdfmetrics.registerFont(TTFont("DV", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DVB", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DVI", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf")))

INK = HexColor("#1b2430")
EMBER = HexColor("#e8590c")
INDIGO = HexColor("#4c5fd5")
TEAL = HexColor("#0ca678")
VIOLET = HexColor("#7048e8")
GOLD = HexColor("#e8a202")
GREY = HexColor("#5c6672")
LIGHT = HexColor("#f4f7fa")
LINE = HexColor("#dde5ec")

S = getSampleStyleSheet()
st_h1 = ParagraphStyle("h1", parent=S["Title"], fontName="DVB", fontSize=26,
                       textColor=EMBER, spaceAfter=4, alignment=0)
st_sub = ParagraphStyle("sub", parent=S["Normal"], fontName="DV", fontSize=10.5,
                        textColor=GREY, spaceAfter=14)
st_sec = ParagraphStyle("sec", parent=S["Heading1"], fontName="DVB", fontSize=17,
                        textColor=INDIGO, spaceBefore=6, spaceAfter=8)
st_sub2 = ParagraphStyle("sub2", parent=S["Heading2"], fontName="DVB", fontSize=12.5,
                         textColor=INK, spaceBefore=10, spaceAfter=5)
st_body = ParagraphStyle("body", parent=S["Normal"], fontName="DV", fontSize=9.5,
                         leading=13.5, textColor=INK)
st_small = ParagraphStyle("small", parent=st_body, fontSize=8.5, textColor=GREY, leading=11.5)
st_cell = ParagraphStyle("cell", parent=st_body, fontSize=9, leading=12)
st_cell_b = ParagraphStyle("cellb", parent=st_cell, fontName="DVB")
st_toc = ParagraphStyle("toc", parent=st_body, fontSize=11, leading=18)


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Cat(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, pagesize=A4, leftMargin=17 * mm,
                                 rightMargin=17 * mm, topMargin=16 * mm,
                                 bottomMargin=16 * mm, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self._deco)])
        self.section = ""

    def _deco(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(EMBER)
        canvas.rect(0, A4[1] - 8 * mm, A4[0], 8 * mm, stroke=0, fill=1)
        canvas.setFont("DV", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(17 * mm, 9 * mm, "LinguaForge — katalog materiałów")
        canvas.drawRightString(A4[0] - 17 * mm, 9 * mm, f"strona {doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "sec":
            self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))


def band(title, subtitle, color):
    t = Table([[Paragraph(f'<font color="#ffffff"><b>{esc(title)}</b></font>', st_sec),
                Paragraph(f'<font color="#ffffff">{esc(subtitle)}</font>', st_small)]],
              colWidths=[110 * mm, 66 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    return t


def table(rows, widths, header=None, zebra=True):
    data = []
    if header:
        data.append([Paragraph(f"<b>{esc(h)}</b>", st_cell) for h in header])
    data += rows
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "DV"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), HexColor("#e9eef5"))]
    if zebra:
        for i in range(1 if header else 0, len(data), 2):
            style.append(("BACKGROUND", (0, i), (-1, i), HexColor("#fbfcfe")))
    t.setStyle(TableStyle(style))
    return t


def build_catalog(path, data, meta):
    """data: dict z gotowymi sekcjami; meta: informacje nagłówkowe."""
    doc = Cat(path, title="LinguaForge — katalog materiałów")
    S = []
    stamp = datetime.date.today().isoformat()

    # ---------- okładka ----------
    S.append(Paragraph("LinguaForge", st_h1))
    S.append(Paragraph(f"Katalog materiałów dydaktycznych · wersja aplikacji {meta['version']} · {stamp}", st_sub))
    S.append(HRFlowable(width="100%", color=EMBER, thickness=2.5))
    S.append(Spacer(1, 10))
    S.append(Paragraph(
        "Ten dokument zawiera <b>wszystkie treści</b> zapisane w aplikacji: słówka, ćwiczenia gramatyczne, "
        "zdania do tłumaczenia, dyktanda, teksty do czytania, zadania pisemne, scenki dialogowe, artykuły teorii "
        "oraz strukturę kursu. Każda pozycja ma <b>numer</b> — ten sam, który widać w aplikacji, np. <b>[30]</b> — "
        "dzięki czemu łatwo wskazać, co poprawić lub rozbudować.", st_body))
    S.append(Spacer(1, 8))
    S.append(Paragraph(
        "<b>Chcesz dopisać własne materiały?</b> Na końcu dokumentu znajduje się rozdział "
        "„Jak dodać nowe treści” z gotowymi wzorami. Do edycji służy paczka ZIP pobierana z panelu "
        "administratora (przycisk „Pobierz paczkę do edycji”) — wystarczy uzupełnić plik szablonu "
        "i odesłać go z powrotem. <b>Nagrań nie trzeba dostarczać: lektor generowany jest automatycznie "
        "z tekstu.</b>", st_body))
    S.append(Spacer(1, 14))

    counts = [[Paragraph(f"<b>{esc(k)}</b>", st_cell), Paragraph(str(v), st_cell)]
              for k, v in meta["counts"].items()]
    S.append(Paragraph("Zawartość w liczbach", st_sub2))
    S.append(table(counts, [110 * mm, 30 * mm], header=["Rodzaj materiału", "Liczba"]))
    S.append(PageBreak())

    # ---------- SŁOWNICTWO ----------
    for group in data["vocab_files"]:
        S.append(band(f"🃏 {group['label']}", f"{len(group['items'])} pozycji · kategoria: {group['theme']}", EMBER))
        S.append(Spacer(1, 6))
        rows = []
        for it in group["items"]:
            rows.append([Paragraph(f"<b>{it['nr']}</b>", st_cell),
                         Paragraph(esc(it["en"]), st_cell_b),
                         Paragraph(esc(it["pl"]), st_cell),
                         Paragraph(esc(it.get("example") or it.get("hint") or ""), st_small)])
        S.append(table(rows, [12 * mm, 40 * mm, 48 * mm, 76 * mm],
                       header=["Nr", "Angielski", "Polski", "Przykład / uwaga"]))
        S.append(Spacer(1, 12))
    S.append(PageBreak())

    # ---------- CZASOWNIKI ODMIANA ----------
    if data.get("verbs"):
        S.append(band("⚙️ Czasowniki — odmiana przez czasy", f"{len(data['verbs'])} czasowników", TEAL))
        S.append(Spacer(1, 6))
        rows = []
        for v in data["verbs"]:
            rows.append([Paragraph(f"<b>{v['nr']}</b>", st_cell),
                         Paragraph(f"{esc(v['en'])} → {esc(v['past'])} → {esc(v['perf'])}", st_cell_b),
                         Paragraph(esc(v["pl_inf"]), st_cell),
                         Paragraph(f"{esc(v['pl_past'][0])} · {esc(v['pl_pres'])} · {esc(v['pl_fut'][0])}", st_small)])
        S.append(table(rows, [12 * mm, 52 * mm, 40 * mm, 72 * mm],
                       header=["Nr", "Formy angielskie", "Znaczenie", "Polskie formy (przeszły · teraźniejszy · przyszły)"]))
        S.append(PageBreak())

    # ---------- GRAMATYKA ----------
    S.append(band("📐 Gramatyka", f"{len(data['grammar'])} tematów", INDIGO))
    S.append(Spacer(1, 6))
    for t in data["grammar"]:
        S.append(Paragraph(f"{esc(t['name'])} <font size=9 color='#5c6672'>({t['level']}, "
                           f"{len(t['exercises'])} ćwiczeń · plik: {esc(t['file'])})</font>", st_sub2))
        if t.get("rule"):
            S.append(Paragraph(f"<b>Reguła:</b> {esc(t['rule'])}", st_small))
            S.append(Spacer(1, 4))
        rows = []
        for e in t["exercises"]:
            ans = e.get("answer_text", "")
            rows.append([Paragraph(f"<b>{e.get('nr','')}</b>", st_cell),
                         Paragraph(esc(e.get("text", "")), st_cell),
                         Paragraph(esc(ans), st_cell_b),
                         Paragraph(esc(e.get("pl", "")) + ("<br/><i>" + esc(e.get("explain", "")) + "</i>"
                                                           if e.get("explain") else ""), st_small)])
        S.append(table(rows, [10 * mm, 58 * mm, 30 * mm, 78 * mm],
                       header=["Nr", "Ćwiczenie", "Odpowiedź", "Tłumaczenie i wyjaśnienie"]))
        S.append(Spacer(1, 10))
    S.append(PageBreak())

    # ---------- TŁUMACZENIA ----------
    S.append(band("🌐 Zdania do tłumaczenia PL → EN", f"{len(data['translations'])} zdań", TEAL))
    S.append(Spacer(1, 6))
    rows = [[Paragraph(f"<b>{i.get('nr','')}</b>", st_cell),
             Paragraph(esc(i["pl"]), st_cell),
             Paragraph(esc(i.get("en_ref", "")), st_cell_b),
             Paragraph(esc(i.get("tense_name", "")) + f" · {i.get('level','')}", st_small)]
            for i in data["translations"]]
    S.append(table(rows, [10 * mm, 58 * mm, 66 * mm, 42 * mm],
                   header=["Nr", "Polski", "Wzorcowe tłumaczenie", "Czas / poziom"]))
    S.append(Spacer(1, 12))

    # ---------- DYKTANDA ----------
    S.append(band("🎧 Dyktanda (słuchanie)", f"{len(data['listening'])} zdań · lektor automatyczny", VIOLET))
    S.append(Spacer(1, 6))
    rows = [[Paragraph(f"<b>{i.get('nr','')}</b>", st_cell),
             Paragraph(esc(i.get("en", "")), st_cell_b),
             Paragraph(esc(i.get("pl", "")), st_cell),
             Paragraph(esc(i.get("level", "")), st_small)]
            for i in data["listening"]]
    S.append(table(rows, [10 * mm, 76 * mm, 76 * mm, 14 * mm],
                   header=["Nr", "Angielski (czytany głosem)", "Polski", "Poz."]))
    S.append(PageBreak())

    # ---------- CZYTANIE ----------
    S.append(band("📖 Teksty do czytania", f"{len(data['reading'])} tekstów", VIOLET))
    for t in data["reading"]:
        block = [Paragraph(f"{esc(t['title'])} <font size=9 color='#5c6672'>({t['level']}, "
                           f"{len(t['text'].split())} słów)</font>", st_sub2),
                 Paragraph(esc(t["text"]).replace("\n", "<br/>"), st_body),
                 Spacer(1, 5),
                 Paragraph("<b>Tłumaczenie:</b> " + esc(t.get("text_pl", "")).replace("\n", "<br/>"), st_small),
                 Spacer(1, 5)]
        rows = []
        for q in t.get("questions", []):
            opts = " · ".join(f"{'✔ ' if j == q['answer'] else ''}{esc(o)}"
                              for j, o in enumerate(q["options"]))
            rows.append([Paragraph(esc(q["text"]), st_cell), Paragraph(opts, st_small)])
        if rows:
            block.append(table(rows, [66 * mm, 110 * mm], header=["Pytanie", "Odpowiedzi (✔ poprawna)"]))
        block.append(Spacer(1, 12))
        S += block
    S.append(PageBreak())

    # ---------- PISANIE ----------
    S.append(band("✍️ Zadania pisemne", f"{len(data['writing'])} tematów", GOLD))
    S.append(Spacer(1, 6))
    for w in data["writing"]:
        S.append(KeepTogether([
            Paragraph(f"{esc(w['title'])} <font size=9 color='#5c6672'>({w['level']}, min. "
                      f"{w.get('min_words', 40)} słów)</font>", st_sub2),
            Paragraph(esc(w["brief"]), st_body),
            Paragraph("<b>Wymagane elementy:</b> " + esc(", ".join(w.get("must_pl", []))), st_small),
            Spacer(1, 3),
            Paragraph("<b>Wzorzec:</b> <i>" + esc(w.get("model", "")) + "</i>", st_small),
            Spacer(1, 10)]))
    S.append(PageBreak())

    # ---------- ROZMOWY ----------
    S.append(band("💬 Rozmowy (scenki dialogowe)", f"{len(data['dialogs'])} scenek · lektor automatyczny", TEAL))
    for d in data["dialogs"]:
        S.append(Paragraph(f"{esc(d['name'])} <font size=9 color='#5c6672'>({d['level']}, "
                           f"{len(d['nodes'])} kwestii)</font>", st_sub2))
        S.append(Paragraph(esc(d.get("desc", "")), st_small))
        S.append(Spacer(1, 4))
        for n in d["nodes"]:
            rows = [[Paragraph("<b>Rozmówca</b>", st_cell),
                     Paragraph(esc(n["npc_en"]) + f"<br/><font color='#5c6672'>{esc(n.get('npc_pl',''))}</font>", st_cell)]]
            if n.get("mode") == "choice":
                for o in n.get("options", []):
                    mark = "✔" if o.get("good") else "✘"
                    rows.append([Paragraph(mark, st_cell),
                                 Paragraph(f"<b>{esc(o['en'])}</b><br/>"
                                           f"<font color='#5c6672'>{esc(o.get('pl',''))}</font><br/>"
                                           f"<font size=8><i>{esc(o.get('feedback',''))}</i></font>", st_cell)])
            else:
                w = n.get("write", {})
                rows.append([Paragraph("✍️", st_cell),
                             Paragraph(f"Uczeń pisze samodzielnie. Wzorzec: <b>{esc(w.get('model',''))}</b>", st_cell)])
            S.append(table(rows, [16 * mm, 160 * mm], zebra=False))
            S.append(Spacer(1, 5))
        S.append(Spacer(1, 8))
    S.append(PageBreak())

    # ---------- TEORIA ----------
    S.append(band("📘 Baza wiedzy — artykuły teorii", f"{len(data['knowledge'])} artykułów", INDIGO))
    for a in data["knowledge"]:
        S.append(Paragraph(f"{esc(a['name'])} <font size=9 color='#5c6672'>({a['level']})</font>", st_sub2))
        S.append(Paragraph(esc(a["what"]), st_body))
        f = a.get("form", {})
        frows = [[Paragraph(esc(k), st_cell), Paragraph(esc(v), st_cell)]
                 for k, v in [("Twierdzenie", f.get("plus", "")), ("Przeczenie", f.get("minus", "")),
                              ("Pytanie", f.get("question", ""))] if v and v != "—"]
        if frows:
            S.append(Spacer(1, 4))
            S.append(table(frows, [30 * mm, 146 * mm], zebra=False))
        exs = a.get("examples", [])
        if exs:
            S.append(Spacer(1, 4))
            S.append(table([[Paragraph(esc(e[0]), st_cell_b), Paragraph(esc(e[1]), st_cell)] for e in exs],
                           [88 * mm, 88 * mm], header=["Przykład", "Tłumaczenie"]))
        if a.get("mistakes"):
            S.append(Spacer(1, 3))
            S.append(Paragraph("<b>Typowe błędy:</b> " + esc(" · ".join(a["mistakes"])), st_small))
        S.append(Spacer(1, 10))
    S.append(PageBreak())

    # ---------- LEKCJE ----------
    if data.get("lessons"):
        S.append(band("📚 Lekcje (podręcznik)", f"{len(data['lessons'])} działów", VIOLET))
        for u in data["lessons"]:
            S.append(Paragraph(f"{esc(u['name'])} ({u['level']})", st_sub2))
            rows = [[Paragraph(esc(c["name"]), st_cell),
                     Paragraph(f"{len(c.get('exercises', []))} ćw. · {len(c.get('homework', []))} zad. dom. · "
                               f"{len(c.get('quiz', []))} pyt. quizu", st_small)] for c in u["chapters"]]
            rows.append([Paragraph("<b>Sprawdzian końcowy</b>", st_cell),
                         Paragraph(f"{len(u.get('exam', {}).get('questions', []))} pytań", st_small)])
            S.append(table(rows, [96 * mm, 80 * mm], header=["Rozdział", "Zawartość"]))
            S.append(Spacer(1, 8))

    # ---------- ŚCIEŻKA ----------
    S.append(band("🧭 Ścieżka nauki — struktura kursu",
                  f"{sum(len(l['links']) for l in data['path'])} ogniw", EMBER))
    for lvl in data["path"]:
        S.append(Paragraph(esc(lvl["name"]), st_sub2))
        rows = [[Paragraph(esc(ln.get("section", "")), st_small),
                 Paragraph(esc(ln["name"]), st_cell),
                 Paragraph(esc(ln["type"]), st_small)] for ln in lvl["links"]]
        S.append(table(rows, [56 * mm, 88 * mm, 32 * mm], header=["Rozdział", "Ogniwo", "Typ"]))
        S.append(Spacer(1, 8))
    S.append(PageBreak())

    # ---------- INSTRUKCJA ----------
    S.append(band("🛠 Jak dodać nowe treści", "instrukcja dla osoby przygotowującej materiały", GOLD))
    S.append(Spacer(1, 8))
    for para in meta["instructions"].split("\n\n"):
        if not para.strip():
            continue
        if para.startswith("## "):
            S.append(Paragraph(esc(para[3:]), st_sub2))
        elif para.startswith("# "):
            continue
        else:
            S.append(Paragraph(esc(para).replace("\n", "<br/>"), st_body))
            S.append(Spacer(1, 5))

    S.append(Spacer(1, 8))
    S.append(Paragraph("Pliki źródłowe (do edycji)", st_sub2))
    rows = [[Paragraph(f"<b>{esc(f['label'])}</b>", st_cell),
             Paragraph(f"data/{esc(f['path'])}", st_small),
             Paragraph(str(f["items"]), st_cell)] for f in meta["files"]]
    S.append(table(rows, [66 * mm, 90 * mm, 20 * mm], header=["Materiał", "Plik", "Pozycji"]))

    doc.build(S)
    return path
