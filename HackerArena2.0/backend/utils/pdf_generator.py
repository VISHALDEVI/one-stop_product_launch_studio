import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY = colors.HexColor("#1a1a2e")
ACCENT = colors.HexColor("#e94560")
LIGHT_BG = colors.HexColor("#f0f0f0")
WHITE = colors.white
DARK_TEXT = colors.HexColor("#2d2d2d")


def _styles():
    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", fontSize=22, textColor=WHITE,
                                fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4),
        "subtitle": ParagraphStyle("subtitle", fontSize=11, textColor=colors.HexColor("#cccccc"),
                                   fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2),
        "section": ParagraphStyle("section", fontSize=13, textColor=WHITE,
                                  fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=4),
        "body": ParagraphStyle("body", fontSize=9, textColor=DARK_TEXT,
                               fontName="Helvetica", leading=14, spaceAfter=3),
        "label": ParagraphStyle("label", fontSize=9, textColor=DARK_TEXT,
                                fontName="Helvetica-Bold", spaceAfter=2),
        "small": ParagraphStyle("small", fontSize=8, textColor=colors.grey,
                                fontName="Helvetica", spaceAfter=2),
    }


def _section_header(title: str, style) -> list:
    tbl = Table([[Paragraph(f"  {title}", style["section"])]], colWidths=[17 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PRIMARY]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return [Spacer(1, 0.3 * cm), tbl, Spacer(1, 0.2 * cm)]


def _kv_table(rows: list, col_widths=None) -> Table:
    col_widths = col_widths or [5 * cm, 12 * cm]
    style = _styles()
    data = [[Paragraph(str(k), style["label"]), Paragraph(str(v), style["body"])]
            for k, v in rows]
    tbl = Table(data, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def _safe(val, default="N/A"):
    if val is None:
        return default
    if isinstance(val, dict):
        return ", ".join(f"{k}: {v}" for k, v in val.items()) if val else default
    if isinstance(val, list):
        return " | ".join(str(i) for i in val) if val else default
    return str(val) or default


def generate_pdf(analysis: dict, record_id: int) -> str:
    os.makedirs("exports/pdfs", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = f"exports/pdfs/product_report_{record_id}_{timestamp}.pdf"

    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    style = _styles()
    story = []

    # ── Cover Banner ──────────────────────────────────────────────────────────
    cover = Table([[Paragraph("AI Product Launch Studio", style["title"]),],
                   [Paragraph("Automated Marketplace-Ready Product Report", style["subtitle"])],
                   [Paragraph(f"Generated: {datetime.utcnow().strftime('%d %B %Y, %H:%M UTC')}  |  Report ID: {record_id}",
                              style["subtitle"])]],
                  colWidths=[17 * cm])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(cover)
    story.append(Spacer(1, 0.4 * cm))

    # ── 1. Vision Analysis ────────────────────────────────────────────────────
    va = analysis.get("vision_analysis", {})
    story.extend(_section_header("1. Vision Analysis", style))
    rows = [
        ("Product Name", _safe(va.get("product_name"))),
        ("Category", _safe(va.get("product_category"))),
        ("Type", _safe(va.get("product_type"))),
        ("Brand", _safe(va.get("brand"))),
        ("Material", _safe(va.get("material"))),
        ("Primary Color", _safe(va.get("primary_color"))),
        ("Secondary Colors", _safe(va.get("secondary_colors"))),
        ("Dimensions", _safe(va.get("estimated_dimensions"))),
        ("Weight", _safe(va.get("estimated_weight"))),
        ("Key Features", _safe(va.get("key_features"))),
        ("Confidence Score", f"{va.get('confidence_score', 0):.0%}"),
    ]
    story.append(_kv_table(rows))

    # ── 2. Listing ────────────────────────────────────────────────────────────
    li = analysis.get("listing", {})
    story.extend(_section_header("2. Listing Generation", style))
    rows = [
        ("SEO Title", _safe(li.get("seo_optimized_title"))),
        ("Description", _safe(li.get("product_description"))),
        ("Bullet Points", _safe(li.get("bullet_points"))),
        ("SEO Keywords", _safe(li.get("seo_keywords"))),
        ("Category", _safe(li.get("marketplace_category"))),
        ("Search Tags", _safe(li.get("search_tags"))),
    ]
    story.append(_kv_table(rows))

    # ── 3. Packaging ──────────────────────────────────────────────────────────
    pk = analysis.get("packaging", {})
    story.extend(_section_header("3. Packaging Suggestions", style))
    rows = [
        ("Packaging Type", _safe(pk.get("recommended_packaging_type"))),
        ("Box Size", _safe(pk.get("recommended_box_size"))),
        ("Protective Materials", _safe(pk.get("protective_material"))),
        ("Shipping", _safe(pk.get("shipping_recommendations"))),
    ]
    story.append(_kv_table(rows))

    # ── 4. Compliance ─────────────────────────────────────────────────────────
    co = analysis.get("compliance", {})
    story.extend(_section_header("4. Compliance Report", style))
    rows = [
        ("BIS Requirement", _safe(co.get("bis_requirement"))),
        ("FSSAI Requirement", _safe(co.get("fssai_requirement"))),
        ("Barcode Requirement", _safe(co.get("barcode_requirement"))),
        ("MRP Label", _safe(co.get("mrp_label_requirement"))),
        ("Product Label Info", _safe(co.get("product_label_information"))),
    ]
    story.append(_kv_table(rows))

    # ── 5. Pricing ────────────────────────────────────────────────────────────
    pr = analysis.get("pricing", {})
    story.extend(_section_header("5. Pricing Analysis", style))

    def fmt_price(p):
        if isinstance(p, dict):
            return f"₹{p.get('amount', 'N/A')} ({p.get('label', '')})"
        return _safe(p)

    rows = [
        ("Low Price", fmt_price(pr.get("low_price"))),
        ("Recommended Price", fmt_price(pr.get("recommended_selling_price"))),
        ("Premium Price", fmt_price(pr.get("premium_price"))),
        ("Pricing Analysis", _safe(pr.get("pricing_analysis"))),
    ]
    story.append(_kv_table(rows))

    # Pricing card visual
    prices = [
        ("Budget", fmt_price(pr.get("low_price")), colors.HexColor("#27ae60")),
        ("Recommended", fmt_price(pr.get("recommended_selling_price")), ACCENT),
        ("Premium", fmt_price(pr.get("premium_price")), colors.HexColor("#8e44ad")),
    ]
    card_data = [[Paragraph(f"<b>{lbl}</b><br/>{val}", ParagraphStyle(
        "card", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold",
        alignment=TA_CENTER, leading=16)) for lbl, val, _ in prices]]
    card_tbl = Table(card_data, colWidths=[5.5 * cm] * 3, rowHeights=[1.5 * cm])
    card_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), prices[0][2]),
        ("BACKGROUND", (1, 0), (1, 0), prices[1][2]),
        ("BACKGROUND", (2, 0), (2, 0), prices[2][2]),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, WHITE),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(card_tbl)

    # ── 6. Competitor Analysis ────────────────────────────────────────────────
    ca = analysis.get("competitor_analysis", {})
    story.extend(_section_header("6. Competitor Analysis", style))
    rows = [
        ("Avg Market Price", _safe(ca.get("average_market_price"))),
        ("Competitor Count", _safe(ca.get("competitor_count"))),
        ("Market Position", _safe(ca.get("market_position"))),
        ("Suggested Improvements", _safe(ca.get("suggested_improvements"))),
    ]
    story.append(_kv_table(rows))

    # ── 7. Marketing Content ──────────────────────────────────────────────────
    mk = analysis.get("marketing_content", {})
    story.extend(_section_header("7. Marketing Content", style))
    for platform, key in [("Instagram", "instagram_post"), ("Facebook", "facebook_post"),
                           ("WhatsApp", "whatsapp_promotion"), ("Email Campaign", "email_campaign")]:
        story.append(Paragraph(f"<b>{platform}</b>", style["label"]))
        story.append(Paragraph(_safe(mk.get(key)), style["body"]))
        story.append(HRFlowable(width="100%", thickness=0.3, color=colors.HexColor("#dddddd")))
        story.append(Spacer(1, 0.15 * cm))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=PRIMARY))
    story.append(Paragraph(
        "Generated by AI Product Launch Studio Agent  •  Powered by Zapier AI",
        ParagraphStyle("footer", fontSize=7, textColor=colors.grey,
                       fontName="Helvetica", alignment=TA_CENTER, spaceBefore=4)
    ))

    doc.build(story)
    return path
