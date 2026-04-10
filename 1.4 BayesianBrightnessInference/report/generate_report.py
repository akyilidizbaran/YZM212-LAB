#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from bayesian_brightness_analysis import PRIOR_LABELS, REPORT_DIR, run_full_analysis


def build_report(output_path: Path) -> None:
    bundle = run_full_analysis()
    constants = bundle["constants"]
    results = bundle["results"]
    analysis_text = bundle["analysis_text"]
    figure_paths = bundle["figure_paths"]
    rows = bundle["base_table_rows"]

    styles = getSampleStyleSheet()
    body = styles["BodyText"]
    body.leading = 14
    heading = styles["Heading2"]
    heading.spaceAfter = 8
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        spaceAfter=16,
    )

    story = []
    story.append(Paragraph("1.4 BayesianBrightnessInference", title_style))
    story.append(Paragraph("YZM212 Makine Ogrenmesi Dersi 4. Laboratuvar Odevi", styles["Heading2"]))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Bu rapor, gurultulu astronomi gozlemlerinden bir gok cisminin gercek parlakligini "
            "ve olcum hatasini Bayesyen cikarim ile tahmin etmek icin hazirlanmistir.",
            body,
        )
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Problem ve Parametreler", heading))
    story.append(
        Paragraph(
            (
                f"Temel senaryoda true_mu={constants['true_mu']}, true_sigma={constants['true_sigma']}, "
                f"n_obs={constants['n_obs']}, seed={constants['seed']}, n_walkers={constants['n_walkers']}, "
                f"n_steps={constants['n_steps']}, burn_in={constants['burn_in']} ve thin={constants['thin']} kullanildi."
            ),
            body,
        )
    )
    story.append(
        Paragraph(
            f"Temel prior siniri: {PRIOR_LABELS['wide']}. Dar prior deneyinde ise {PRIOR_LABELS['narrow_mu']}.",
            body,
        )
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Temel Sonuclar Tablosu", heading))
    table_data = [
        [
            "Degisken",
            "Gercek",
            "Median",
            "Alt Sinir (%16)",
            "Ust Sinir (%84)",
            "Mutlak Hata",
        ]
    ]
    for row in rows:
        table_data.append(
            [
                row["Degisken"],
                f"{row['Gercek Deger']:.3f}",
                f"{row['Tahmin Edilen (Median)']:.3f}",
                f"{row['Alt Sinir (%16)']:.3f}",
                f"{row['Ust Sinir (%84)']:.3f}",
                f"{row['Mutlak Hata']:.3f}",
            ]
        )

    table = Table(table_data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b5cad")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eef4fb")]),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("3. Analiz ve Yorum", heading))
    for key in ["accuracy", "prior_effect", "sample_size", "precision", "correlation"]:
        story.append(Paragraph(analysis_text[key], body))
        story.append(Spacer(1, 6))

    story.append(Paragraph("4. Grafikler", heading))
    figure_order = [
        ("Temel corner plot", figure_paths["base_corner"]),
        ("Temel trace plot", figure_paths["base_trace"]),
        ("Dar prior etkisi", figure_paths["prior_corner"]),
        ("Az veri senaryosu", figure_paths["sample_size_corner"]),
        ("Senaryo karsilastirma ozeti", figure_paths["comparison"]),
    ]
    for caption, path in figure_order:
        story.append(Paragraph(caption, styles["Heading3"]))
        story.append(Image(str(path), width=16 * cm, height=11.5 * cm))
        story.append(Spacer(1, 10))

    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    doc.build(story)


if __name__ == "__main__":
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    build_report(REPORT_DIR / "bayesian_brightness_report.pdf")
