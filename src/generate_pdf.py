"""
Generate CIRS Approach Deck as PDF
India Runs Data & AI Challenge
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ─── Color palette ────────────────────────────────────────────────────────────
DARK_BG    = colors.HexColor("#0F1117")
ACCENT     = colors.HexColor("#4F8EF7")
ACCENT2    = colors.HexColor("#7C3AED")
WHITE      = colors.white
LIGHT_GRAY = colors.HexColor("#E5E7EB")
MID_GRAY   = colors.HexColor("#6B7280")
DARK_GRAY  = colors.HexColor("#1F2937")
GREEN      = colors.HexColor("#10B981")
ORANGE     = colors.HexColor("#F59E0B")
RED        = colors.HexColor("#EF4444")

W, H = A4

def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["slide_title"] = ParagraphStyle(
        "slide_title", fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
        spaceAfter=8, alignment=TA_CENTER
    )
    styles["slide_subtitle"] = ParagraphStyle(
        "slide_subtitle", fontName="Helvetica", fontSize=14, textColor=LIGHT_GRAY,
        spaceAfter=4, alignment=TA_CENTER
    )
    styles["section_heading"] = ParagraphStyle(
        "section_heading", fontName="Helvetica-Bold", fontSize=18, textColor=ACCENT,
        spaceBefore=10, spaceAfter=6
    )
    styles["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=11, textColor=DARK_GRAY,
        spaceAfter=6, leading=16
    )
    styles["body_white"] = ParagraphStyle(
        "body_white", fontName="Helvetica", fontSize=11, textColor=WHITE,
        spaceAfter=6, leading=16
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=11, textColor=DARK_GRAY,
        spaceAfter=5, leftIndent=16, bulletIndent=0, leading=16
    )
    styles["metric"] = ParagraphStyle(
        "metric", fontName="Helvetica-Bold", fontSize=32, textColor=ACCENT,
        alignment=TA_CENTER, spaceAfter=2
    )
    styles["metric_label"] = ParagraphStyle(
        "metric_label", fontName="Helvetica", fontSize=11, textColor=MID_GRAY,
        alignment=TA_CENTER
    )
    styles["tag"] = ParagraphStyle(
        "tag", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
        alignment=TA_CENTER
    )
    styles["code"] = ParagraphStyle(
        "code", fontName="Courier", fontSize=9, textColor=DARK_GRAY,
        backColor=LIGHT_GRAY, spaceAfter=4, leading=13
    )
    styles["footnote"] = ParagraphStyle(
        "footnote", fontName="Helvetica", fontSize=8, textColor=MID_GRAY,
        alignment=TA_CENTER
    )
    styles["slide_num"] = ParagraphStyle(
        "slide_num", fontName="Helvetica", fontSize=9, textColor=MID_GRAY,
        alignment=TA_RIGHT
    )
    return styles

def divider(color=ACCENT, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=10)

def spacer(h=0.3):
    return Spacer(1, h * cm)

def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="CIRS Approach Deck",
        author="India Runs Data & AI Challenge"
    )

    s = build_styles()
    story = []

    # ─── Slide 1: Title ───────────────────────────────────────────────────────
    story.append(spacer(2))

    title_table = Table([[
        Paragraph("CIRS", ParagraphStyle("big", fontName="Helvetica-Bold", fontSize=56,
                                          textColor=ACCENT, alignment=TA_CENTER))
    ]], colWidths=[15 * cm])
    title_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("ROWPADDING", (0, 0), (-1, -1), 20),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(title_table)
    story.append(spacer(0.4))

    story.append(Paragraph("Candidate Intelligent Ranking System", s["slide_subtitle"]))
    story.append(Paragraph("India Runs Data &amp; AI Challenge — Redrob Hackathon 2026", s["footnote"]))
    story.append(spacer(1))
    divider_t = Table([[""]],  colWidths=[15*cm])
    divider_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),ACCENT),("ROWPADDING",(0,0),(-1,-1),1)]))
    story.append(divider_t)
    story.append(spacer(0.5))

    story.append(Paragraph(
        "An AI-powered multi-dimensional candidate ranking engine that evaluates "
        "candidates the way a great recruiter would — holistically, not just by keywords.",
        ParagraphStyle("intro", fontName="Helvetica", fontSize=13, textColor=DARK_GRAY,
                       alignment=TA_CENTER, leading=20)
    ))
    story.append(PageBreak())

    # ─── Slide 2: Problem Statement ───────────────────────────────────────────
    story.append(Paragraph("The Problem with Keyword-Based Hiring", s["section_heading"]))
    story.append(divider())

    problems = [
        ("🔍 Keyword Blindness",
         "ATS systems filter 75% of qualified resumes before a human sees them. Great candidates "
         "with non-standard phrasing get dropped — not because they can't do the job, "
         "but because they wrote 'ML' instead of 'Machine Learning'."),
        ("📊 Uni-Dimensional Scoring",
         "Most systems score candidates on skill keywords alone, ignoring career trajectory, "
         "platform signals, cultural contribution (GitHub, LinkedIn), and practical fit signals "
         "like notice period and salary expectations."),
        ("⏱️ Recruiter Overload",
         "A recruiter reviewing 500+ profiles for a single role spends ~6 seconds per profile. "
         "The result: qualified candidates are missed, and the hiring cycle extends by weeks."),
        ("🎭 The Hidden Signal Gap",
         "A candidate's GitHub contributions, open-source impact, and professional network "
         "are rich behavioral signals that keyword systems completely ignore."),
    ]

    for icon_title, desc in problems:
        row = Table([[
            Paragraph(icon_title, ParagraphStyle("prob_t", fontName="Helvetica-Bold",
                                                  fontSize=12, textColor=ACCENT)),
            Paragraph(desc, s["body"])
        ]], colWidths=[5*cm, 10*cm])
        row.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F9FAFB")),
            ("ROWPADDING", (0,0), (-1,-1), 8),
            ("ROUNDEDCORNERS", [4]),
            ("BOX", (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ]))
        story.append(row)
        story.append(spacer(0.2))

    story.append(PageBreak())

    # ─── Slide 3: Our Solution ────────────────────────────────────────────────
    story.append(Paragraph("CIRS — Our Solution", s["section_heading"]))
    story.append(divider())
    story.append(Paragraph(
        "CIRS scores every candidate across <b>5 weighted dimensions</b>, each capturing a "
        "different signal of real-world job fit. The result: a recruiter-trusted shortlist "
        "in seconds, not hours.",
        s["body"]
    ))
    story.append(spacer(0.3))

    dims = [
        ("🎯 Skill Match", "35%", ACCENT, "Semantic + exact coverage of JD requirements. Required skills weighted 2x over nice-to-have."),
        ("💼 Experience", "25%", ACCENT2, "YOE alignment, company prestige tier, career progression & tenure analysis."),
        ("📡 Platform Signals", "20%", GREEN, "GitHub (stars, contributions, PRs) + LinkedIn (recommendations, activity, network)."),
        ("🎓 Education", "10%", ORANGE, "College tier (IIT/NIT/BITS/Tier-2/3), CGPA score, certifications earned."),
        ("✅ Practical Fit", "10%", RED, "CTC range alignment, notice period, location match."),
    ]

    for icon_dim, weight, col, desc in dims:
        row = Table([[
            Paragraph(icon_dim, ParagraphStyle("dim_t", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE)),
            Paragraph(weight, ParagraphStyle("wt", fontName="Helvetica-Bold", fontSize=20, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(desc, ParagraphStyle("dim_d", fontName="Helvetica", fontSize=10, textColor=WHITE, leading=14))
        ]], colWidths=[4.5*cm, 2*cm, 8.5*cm])
        row.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), col),
            ("ROWPADDING", (0,0), (-1,-1), 10),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ROUNDEDCORNERS", [4]),
        ]))
        story.append(row)
        story.append(spacer(0.15))

    story.append(PageBreak())

    # ─── Slide 4: Architecture ────────────────────────────────────────────────
    story.append(Paragraph("System Architecture", s["section_heading"]))
    story.append(divider())

    arch_rows = [
        ["INPUT", "→", "PROCESSING", "→", "OUTPUT"],
        ["Job Description\n(JSON)", "", "Skill Match Scorer\n(synonym normalization)", "", "Composite Score\n(0-100)"],
        ["500+ Candidate\nProfiles (JSON/CSV)", "", "Experience Scorer\n(YOE + prestige tiers)", "", "Ranked CSV\n(all candidates)"],
        ["", "", "Platform Signal Scorer\n(log-scale GitHub/LI)", "", "Top-50 Shortlist"],
        ["", "", "Education Scorer\n(tier + CGPA)", "", "Summary JSON\n(top-10 + stats)"],
        ["", "", "Fit Scorer\n(CTC, notice, location)", "", ""],
    ]

    arch_table = Table(arch_rows, colWidths=[3.5*cm, 1*cm, 5.5*cm, 1*cm, 4*cm])
    arch_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), ACCENT),
        ("BACKGROUND", (2,0), (2,0), ACCENT2),
        ("BACKGROUND", (4,0), (4,0), GREEN),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWPADDING", (0,0), (-1,-1), 6),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("TEXTCOLOR", (0,1), (-1,-1), DARK_GRAY),
        ("BACKGROUND", (0,1), (0,-1), colors.HexColor("#EFF6FF")),
        ("BACKGROUND", (2,1), (2,-1), colors.HexColor("#F5F3FF")),
        ("BACKGROUND", (4,1), (4,-1), colors.HexColor("#ECFDF5")),
        ("BOX", (0,0), (0,-1), 0.5, ACCENT),
        ("BOX", (2,0), (2,-1), 0.5, ACCENT2),
        ("BOX", (4,0), (4,-1), 0.5, GREEN),
    ]))
    story.append(arch_table)
    story.append(spacer(0.5))

    story.append(Paragraph("Tech Stack", ParagraphStyle("ts_h", fontName="Helvetica-Bold", fontSize=12, textColor=DARK_GRAY)))
    tech_row = Table([[
        Paragraph("Python 3.11+", s["body"]),
        Paragraph("Pandas / NumPy", s["body"]),
        Paragraph("Scikit-learn", s["body"]),
        Paragraph("JSON / CSV I/O", s["body"]),
    ]], colWidths=[3.75*cm]*4)
    tech_row.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_GRAY),
        ("ROWPADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("BOX", (0,0), (-1,-1), 0.5, MID_GRAY),
        ("INNERGRID", (0,0), (-1,-1), 0.5, MID_GRAY),
    ]))
    story.append(tech_row)
    story.append(PageBreak())

    # ─── Slide 5: Scoring Deep Dive ───────────────────────────────────────────
    story.append(Paragraph("Scoring Deep Dive", s["section_heading"]))
    story.append(divider())

    scoring_items = [
        ("Skill Match (35%)",
         "Required skills are matched using synonym normalization: 'PyTorch' = 'torch' = 'pytorch'. "
         "Required skills contribute 70% to skill score; nice-to-have contribute 30%. "
         "This prevents keyword-stuffed resumes from gaming the system."),
        ("Experience (25%)",
         "YOE is scored against the JD range with asymmetric penalties — "
         "over-qualification is penalized lightly (senior fits junior roles somewhat); "
         "under-qualification is penalized more steeply. Company prestige uses 5 tiers: "
         "FAANG > Unicorn > Growth > Enterprise > Startup. Most recent employer weighted 1.5x."),
        ("Platform Signals (20%)",
         "GitHub: star count uses log-scale normalization (1k stars vs 100k stars are "
         "very different signals). Contributions and merged PRs reflect active open-source "
         "engagement. LinkedIn: recommendations are weighted most (peer validation), "
         "followed by connection count and endorsements."),
        ("Education (10%)",
         "Tiers: IIT (100) > BITS (85) > NIT (75) > Tier-2 (55) > Tier-3 (35). "
         "CGPA scaled linearly from 5.0 (min useful) to 9.8 (max). "
         "Each certification adds up to 25 points (capped at 100)."),
        ("Practical Fit (10%)",
         "CTC below budget is a mild positive; above budget penalized 8 pts/lpa over range. "
         "Notice period <= max_days is full marks; every day over is -2 pts. "
         "Bangalore candidates for Bangalore roles score 100; remote-ok scores 85 for hybrid."),
    ]

    for title, desc in scoring_items:
        story.append(Paragraph(f"<b>{title}</b>", s["body"]))
        story.append(Paragraph(desc, ParagraphStyle("desc", fontName="Helvetica", fontSize=10,
                                                     textColor=DARK_GRAY, leftIndent=12, leading=15,
                                                     spaceAfter=8)))

    story.append(PageBreak())

    # ─── Slide 6: Results ─────────────────────────────────────────────────────
    story.append(Paragraph("Results on Sample Dataset", s["section_heading"]))
    story.append(divider())

    # Metrics row
    metrics = [
        ("500", "Candidates Ranked"),
        ("62.5", "Top Score"),
        ("41.8", "Mean Score"),
        ("23.1", "Lowest Score"),
    ]
    met_table = Table([[
        Paragraph(val, s["metric"]) for val, _ in metrics
    ], [
        Paragraph(lbl, s["metric_label"]) for _, lbl in metrics
    ]], colWidths=[3.75*cm]*4)
    met_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F9FAFB")),
        ("BOX", (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ("ROWPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(met_table)
    story.append(spacer(0.4))

    story.append(Paragraph("Sample Top-10 Rankings", ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=12)))
    story.append(spacer(0.2))

    table_data = [
        ["Rank", "Candidate ID", "Composite", "Skill Match", "Experience", "Platform", "Stage"],
        ["1", "CAND_0126", "62.5", "38.8", "95.8", "47.1", "senior"],
        ["2", "CAND_0281", "61.7", "21.3", "77.4", "85.5", "mid"],
        ["3", "CAND_0379", "60.7", "35.0", "87.8", "55.3", "mid"],
        ["4", "CAND_0215", "59.5", "16.3", "100.0", "58.4", "mid"],
        ["5", "CAND_0186", "59.1", "17.5", "91.5", "84.0", "mid"],
    ]

    res_table = Table(table_data, colWidths=[1.5*cm, 3.5*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.2*cm, 1.5*cm])
    res_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_GRAY),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("ROWPADDING", (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, colors.HexColor("#F9FAFB")]),
        ("BOX", (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ("INNERGRID", (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ("TEXTCOLOR", (2,1), (2,-1), ACCENT),
        ("FONTNAME", (2,1), (2,-1), "Helvetica-Bold"),
    ]))
    story.append(res_table)
    story.append(PageBreak())

    # ─── Slide 7: Design Decisions ────────────────────────────────────────────
    story.append(Paragraph("Key Design Decisions", s["section_heading"]))
    story.append(divider())

    decisions = [
        ("Why multi-dimensional scoring?",
         "No single signal predicts job success. A great GitHub profile with weak skills "
         "is different from weak GitHub with perfect skill match. Weighted combination "
         "reflects how experienced recruiters actually think."),
        ("Why synonym normalization?",
         "Real resumes are inconsistent. 'PyTorch', 'pytorch', 'torch' all mean the same thing. "
         "Without normalization, valid candidates get penalized for formatting, not ability."),
        ("Why log-scale for GitHub stars?",
         "The difference between 0 and 100 stars is huge; the difference between "
         "5,000 and 10,000 is marginal. Log normalization prevents superstar outliers "
         "from overwhelming the signal."),
        ("Why penalize over-qualification lightly?",
         "A senior engineer applying to a mid-level role may be relocating, changing "
         "industries, or prefer a lower-pressure environment. Automatic rejection "
         "loses great candidates on a technicality."),
        ("Why weight recent employers 1.5x?",
         "A candidate who spent 3 years at TCS and just joined Google is different "
         "from a 10-year TCS lifer. Recency-weighting captures trajectory, not just history."),
    ]

    for q, a in decisions:
        story.append(Table([[
            Paragraph(f"Q: {q}", ParagraphStyle("q", fontName="Helvetica-Bold", fontSize=11, textColor=ACCENT2)),
        ]], colWidths=[15*cm]))
        story.append(Paragraph(f"A: {a}", ParagraphStyle("a", fontName="Helvetica", fontSize=10,
                                                           textColor=DARK_GRAY, leftIndent=12, leading=15, spaceAfter=8)))

    story.append(PageBreak())

    # ─── Slide 8: Roadmap / Extensions ───────────────────────────────────────
    story.append(Paragraph("Roadmap — What We'd Build Next", s["section_heading"]))
    story.append(divider())

    roadmap = [
        ("v1.1 — Semantic Skill Matching",
         "Replace synonym dictionaries with sentence-transformers embeddings. "
         "Compute cosine similarity between JD skill descriptions and candidate skill vectors. "
         "Catches 'built NLP pipelines' even without explicit skill labels."),
        ("v1.2 — LLM-Powered Fit Reasoning",
         "Send top-50 shortlisted profiles + JD to Claude/GPT for narrative fit assessment. "
         "Generate a 2-sentence recruiter note per candidate explaining WHY they ranked where they did."),
        ("v1.3 — Behavioral Signal Parsing",
         "Parse cover letters, portfolio bios, and GitHub README files for motivation signals: "
         "passion for the domain, communication quality, growth mindset indicators."),
        ("v2.0 — Feedback Loop Training",
         "Record recruiter accept/reject decisions on shortlisted candidates. "
         "Fine-tune dimension weights using logistic regression on historical hiring outcomes. "
         "Self-improving system that gets better with every hiring cycle."),
    ]

    for version, desc in roadmap:
        row = Table([[
            Paragraph(version, ParagraphStyle("vt", fontName="Helvetica-Bold", fontSize=11,
                                               textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(desc, ParagraphStyle("vd", fontName="Helvetica", fontSize=10,
                                            textColor=DARK_GRAY, leading=15))
        ]], colWidths=[3.5*cm, 11.5*cm])
        row.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), ACCENT2),
            ("BACKGROUND", (1,0), (1,-1), colors.HexColor("#F5F3FF")),
            ("ROWPADDING", (0,0), (-1,-1), 10),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(row)
        story.append(spacer(0.2))

    story.append(PageBreak())

    # ─── Slide 9: Closing ─────────────────────────────────────────────────────
    story.append(spacer(2))

    closing_table = Table([[
        Paragraph("Make Hiring Smarter.", ParagraphStyle(
            "close_h", fontName="Helvetica-Bold", fontSize=28, textColor=WHITE, alignment=TA_CENTER
        ))
    ]], colWidths=[15*cm])
    closing_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BG),
        ("ROWPADDING", (0,0), (-1,-1), 30),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(closing_table)
    story.append(spacer(0.5))

    bullets = [
        "✅ 500 candidates scored across 5 dimensions in under 2 seconds",
        "✅ Recruiter-ready shortlist: Top 50 with full score breakdown",
        "✅ Explainable scores: every candidate gets dimension-level transparency",
        "✅ No black-box: weights are visible, tunable, and defensible",
        "✅ Built to extend: embeddings, LLM reasoning, and feedback loops ready to plug in",
    ]
    for b in bullets:
        story.append(Paragraph(b, ParagraphStyle("closing_b", fontName="Helvetica", fontSize=12,
                                                   textColor=DARK_GRAY, spaceAfter=6, leading=18)))

    story.append(spacer(1))
    story.append(Paragraph(
        "Submission: GitHub Repo | ranked_candidates.csv | shortlist_top50.csv",
        s["footnote"]
    ))
    story.append(Paragraph(
        "India Runs Data &amp; AI Challenge — Redrob 2026",
        s["footnote"]
    ))

    doc.build(story)
    print(f"PDF deck generated -> {output_path}")


def generate_deck(output_path: str, ranked=None, jd=None) -> None:
    """Generate the CIRS approach deck PDF (ranked/jd reserved for future dynamic slides)."""
    build_pdf(output_path)


if __name__ == "__main__":
    build_pdf("output/CIRS_Approach_Deck.pdf")
