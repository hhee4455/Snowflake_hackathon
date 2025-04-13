from fpdf import FPDF
from datetime import datetime

def generate_pdf(region: str, year: int, summary: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()

    # Arial fallback (한글 깨질 수 있음)
    pdf.set_font('Arial', '', 13)

    pdf.set_title(f"{region} {year} 젠트리피케이션 리포트")

    pdf.multi_cell(0, 10, f"Gentrification Report\n\nRegion: {region}\nYear: {year}\nGenerated on: {datetime.today().strftime('%Y-%m-%d')}\n\n", align="L")
    pdf.multi_cell(0, 10, summary.strip(), align="L")

    return pdf.output(dest='S').encode('latin1')
