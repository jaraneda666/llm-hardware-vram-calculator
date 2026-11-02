import subprocess
import os
import re
import pymupdf

def generar_pdf_oscuro():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    html_src = os.path.join(base_dir, "output", "informe_hardware_llm_bbb.html")
    pdf_out = os.path.join(base_dir, "output", "informe_hardware_llm_bbb_dark.pdf")
    temp_html = os.path.join(base_dir, "output", "informe_dark_temp.html")
    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    with open(html_src, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Estilos de impresión para modo oscuro
    dark_print_css = """
    @media print {
      :root {
        --bg-body: #0b0f19 !important;
        --bg-surface: #111827 !important;
        --bg-surface-elevated: #1f2937 !important;
        --bg-card: #111827 !important;
        --border-color: rgba(255, 255, 255, 0.12) !important;
        --text-main: #f3f4f6 !important;
        --text-muted: #9ca3af !important;
        --text-dim: #6b7280 !important;
        --primary: #06b6d4 !important;
        --secondary: #8b5cf6 !important;
        --accent: #10b981 !important;
        --code-bg: #030712 !important;
      }

      @page {
        margin: 1.2cm 1cm;
        size: A4 portrait;
      }

      *, *::before, *::after {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }

      html, body {
        background-color: #0b0f19 !important;
        color: #f3f4f6 !important;
        font-size: 9.5pt !important;
        line-height: 1.45 !important;
      }

      .top-nav, .sidebar, .btn-copy {
        display: none !important;
      }

      .main-layout {
        display: block !important;
      }

      .content-area {
        max-width: 100% !important;
        padding: 0 !important;
      }

      h1, h2, h3, h4 {
        color: #f3f4f6 !important;
        page-break-after: avoid !important;
        break-after: avoid !important;
      }

      h1 { font-size: 18pt !important; margin-bottom: 0.5rem !important; }
      h2 { font-size: 13.5pt !important; margin-top: 1.25rem !important; margin-bottom: 0.65rem !important; border-bottom: 2px solid #06b6d4 !important; padding-bottom: 0.3rem !important; }
      h3 { font-size: 11pt !important; margin-top: 1rem !important; margin-bottom: 0.4rem !important; }
      h4 { font-size: 10pt !important; }

      p, li {
        color: #d1d5db !important;
        orphans: 3;
        widows: 3;
      }

      a {
        color: #38bdf8 !important;
        text-decoration: underline !important;
      }

      .hero-subtitle {
        color: #9ca3af !important;
      }

      .meta-bar {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #9ca3af !important;
        padding: 0.65rem 1rem !important;
        margin-bottom: 1.5rem !important;
        font-size: 8.5pt !important;
      }
      .meta-item strong {
        color: #f3f4f6 !important;
      }

      .calculator-widget {
        display: block !important;
        background: #111827 !important;
        border: 1.5px solid #06b6d4 !important;
        border-radius: 8px !important;
        padding: 1rem 1.25rem !important;
        margin: 1.25rem 0 !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        box-shadow: none !important;
      }
      .calc-header h3 {
        color: #06b6d4 !important;
      }
      .calc-controls {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 0.65rem 1rem !important;
        margin-bottom: 0.85rem !important;
      }
      .control-group label {
        color: #9ca3af !important;
      }
      .control-group select {
        background: #1f2937 !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
      }
      .calc-results {
        background: #1f2937 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
      }
      .result-box .label {
        color: #9ca3af !important;
      }
      .result-box .val {
        color: #06b6d4 !important;
        font-weight: 700 !important;
      }
      .vram-meter {
        background: #374151 !important;
      }
      .vram-fill {
        background: #06b6d4 !important;
      }
      .calc-verdict {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #34d399 !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
      }

      .lab-box, .screenshot-card, .tier-card {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: none !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }

      .screenshot-header {
        background: #1f2937 !important;
        color: #f3f4f6 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
        font-size: 8pt !important;
        padding: 0.4rem 0.75rem !important;
      }

      .screenshot-caption {
        background: #111827 !important;
        color: #9ca3af !important;
        font-size: 8pt !important;
        padding: 0.5rem 0.75rem !important;
      }

      .badge-benchmark {
        padding: 0.15rem 0.45rem !important;
        font-size: 7pt !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
      }
      .badge-gpu { background: rgba(6, 182, 212, 0.2) !important; color: #38bdf8 !important; }
      .badge-cpu { background: rgba(245, 158, 11, 0.2) !important; color: #fbbf24 !important; }
      .badge-ultra { background: rgba(16, 185, 129, 0.2) !important; color: #34d399 !important; }

      .table-responsive {
        box-shadow: none !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        overflow: visible !important;
        margin: 0.85rem 0 !important;
      }

      table {
        width: 100% !important;
        table-layout: auto !important;
        font-size: 7.5pt !important;
      }

      tr {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }

      th {
        background: #1f2937 !important;
        color: #f3f4f6 !important;
        border-bottom: 2px solid #06b6d4 !important;
        padding: 0.4rem 0.45rem !important;
      }

      td {
        color: #e5e7eb !important;
        background: #111827 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        padding: 0.4rem 0.45rem !important;
      }

      .callout {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        padding: 0.85rem 1rem !important;
        margin: 1rem 0 !important;
      }
      .callout-caution {
        background: rgba(239, 68, 68, 0.12) !important;
        border-left: 4px solid #ef4444 !important;
      }
      .callout-tip {
        background: rgba(16, 185, 129, 0.12) !important;
        border-left: 4px solid #10b981 !important;
      }
      .callout-warning {
        background: rgba(245, 158, 11, 0.12) !important;
        border-left: 4px solid #f59e0b !important;
      }
      .callout-info {
        background: rgba(6, 182, 212, 0.12) !important;
        border-left: 4px solid #06b6d4 !important;
      }

      .code-box {
        background: #030712 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
      }
      pre {
        padding: 0.65rem 0.85rem !important;
        font-size: 8pt !important;
        overflow: visible !important;
        white-space: pre-wrap !important;
        word-break: break-all !important;
        color: #e2e8f0 !important;
        background: #030712 !important;
      }
      code {
        color: #38bdf8 !important;
        background: #1f2937 !important;
      }

      .checklist-item {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
      }

      .diagram-container {
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: #111827 !important;
      }

      .flow-step {
        background: #1f2937 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
      }

      .flow-step .title {
        color: #f3f4f6 !important;
      }

      footer {
        color: #9ca3af !important;
      }
    }
    """

    # Reemplazar el bloque @media print existente
    html_dark = re.sub(r'@media print\s*\{.*?\n\s*\}\s*</style>', dark_print_css + "\n  </style>", html_content, flags=re.DOTALL)

    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_dark)

    temp_url = "file:///" + temp_html.replace(os.sep, "/")
    cmd = [
        edge_bin,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_out}",
        "--no-pdf-header-footer",
        temp_url
    ]

    print("1. Ejecutando Edge headless...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
    print("   Return code:", res.returncode)

    if os.path.exists(temp_html):
        os.remove(temp_html)

    if not os.path.exists(pdf_out):
        print("Error: No se pudo generar el archivo PDF inicial.")
        return False

    print("2. Aplicando sangrado completo (full-bleed) de fondo oscuro para eliminar bordes blancos...")
    # Color de fondo slate oscuro exacto: #0b0f19 -> (11/255, 15/255, 25/255)
    bg_color = (11 / 255.0, 15 / 255.0, 25 / 255.0)

    doc = pymupdf.open(pdf_out)
    for i, page in enumerate(doc):
        # Dibujar rectángulo en el fondo (overlay=False) cubriendo todo el lienzo de la página (page.rect)
        page.draw_rect(page.rect, color=bg_color, fill=bg_color, overlay=False)

    doc.save(pdf_out, incremental=True, encryption=pymupdf.PDF_ENCRYPT_KEEP)
    doc.close()

    print(f"3. PDF en Modo Oscuro generado con éxito sin bordes blancos: {pdf_out}")
    print(f"   Tamaño final: {os.path.getsize(pdf_out)} bytes")
    return True

if __name__ == "__main__":
    generar_pdf_oscuro()
