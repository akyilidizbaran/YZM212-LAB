from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from recognizer import classify_sequence, decode_ev_viterbi, load_sample_data


def build_report(output_path: Path) -> None:
    styles = getSampleStyleSheet()
    story = []

    sample_data = load_sample_data()
    viterbi = decode_ev_viterbi(["High", "Low"])
    delta = viterbi["delta"]

    story.append(Paragraph("1.1 - HMM ile Izole Kelime Tanima Sistemi", styles["Title"]))
    story.append(Spacer(1, 12))

    theory_lines = [
        "1. Teorik Cozum",
        "Gozlem dizisi [High, Low] icin baslangicta sadece e durumu mumkundur.",
        f"t1: delta_e={delta[0][0]:.2f}, delta_v={delta[0][1]:.2f}.",
        (
            "t2 icin e durumuna gecis: max(0.70x0.60, 0.00x0.20)x0.30 = "
            f"{delta[1][0]:.3f}."
        ),
        (
            "t2 icin v durumuna gecis: max(0.70x0.40, 0.00x0.80)x0.90 = "
            f"{delta[1][1]:.3f}."
        ),
        (
            "Sonuc olarak en olasi fonem yolu: "
            + " -> ".join(viterbi["best_path"])
            + f" ve olasilik {viterbi['best_probability']:.3f}."
        ),
    ]
    for line in theory_lines:
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph("2. Uygulama Ozeti", styles["Heading2"]))
    app_lines = [
        "EV icin 2 durumlu, OKUL icin 4 durumlu CategoricalHMM modeli tanimlandi.",
        "Gozlemler High=0 ve Low=1 olarak kodlandi.",
        "Temsili egitim dizileri data/sample_data.json dosyasinda tutuldu.",
    ]
    for line in app_lines:
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph("3. Ornek Sonuclar", styles["Heading2"]))
    for sequence in sample_data["test_sequences"]:
        result = classify_sequence(sequence)
        score_text = ", ".join(
            f"{name}={score:.4f}" for name, score in result["scores"].items()
        )
        story.append(
            Paragraph(
                f"{sequence} icin tahmin: {result['predicted_word']} ({score_text})",
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph("4. Analiz", styles["Heading2"]))
    analysis_lines = [
        (
            "Noise, gozlem dagilimini bozar; dogru foneme ait emisyon olasiliklari azalirken "
            "yanlis fonemlerin olasiliklari artar."
        ),
        (
            "Buyuk kelime dagarciginda klasik HMM + Viterbi yaklasimi, ozellik cikarimi ve "
            "durum modelleme acisindan sinirli kalir. Derin ogrenme, daha karmasik akustik "
            "oruntuleri ve uzun baglamlari daha iyi ogrenebilir."
        ),
    ]
    for line in analysis_lines:
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 6))

    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    doc.build(story)


if __name__ == "__main__":
    output = Path(__file__).resolve().parents[1] / "report" / "cozum_anahtari.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    build_report(output)
