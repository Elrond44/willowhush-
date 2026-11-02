#!/usr/bin/env python3
"""Generate the public ebook assets for the Ebook page from the FULL book PDF (which is never committed).

    python3 tools/make_ebook_assets.py /path/to/good-vibrations.pdf

Writes (all safe to publish):
  src/assets/ebook/good-vibrations-sample.pdf   free sample: pages 1-9 (cover, title, contents, introduction,
                                                 all of Chapter 1) + a closing "end of sample" page
  src/assets/images/ebook-cover.webp / -sm.webp  cover rendered from PDF page 1
  src/assets/images/ebook-og.jpg                 1200x630 social card with the cover
  src/assets/images/ebook-page-*.webp            small "look inside" page thumbnails
  src/assets/images/ebook-layers.webp            layered-model diagram from <pdf dir>/img (if present)

Needs poppler-utils (pdftoppm, pdftocairo, pdfunite) and Pillow. The closing page is printed with Playwright
(Chromium) if it is installed; otherwise the sample is just pages 1-9.
NEVER copy the full PDF into src/ or docs/: that would give the paid book away (see .gitignore).
"""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG, EB = ROOT / "src/assets/images", ROOT / "src/assets/ebook"
SAMPLE_PAGES = (1, 9)
THUMB_PAGES = [3, 7, 11, 42, 44]
EBOOK_URL = "elrond44.github.io/willowhush-/ebook.html"

END_PAGE = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Lora:ital@0;1&family=Lato:wght@400;700&display=swap" rel="stylesheet">
<style>@page{{size:6in 9in;margin:0}}html,body{{margin:0}}
body{{width:6in;height:9in;box-sizing:border-box;padding:.9in .75in;font:11pt/1.6 Lora,Georgia,serif;color:#2c2735;
background:radial-gradient(ellipse at 50% 115%,#f4d7c2 0%,#faf6ef 55%);display:flex;flex-direction:column;justify-content:center}}
.k{{font:700 7.5pt Lato,sans-serif;letter-spacing:.25em;text-transform:uppercase;color:#b98d4f;margin:0 0 .9em}}
h1{{font:600 24pt/1.15 Fraunces,Georgia,serif;color:#3a3148;margin:0 0 .6em}}
ul{{padding-left:1.1em;margin:.4em 0 1.4em}}li{{margin:.15em 0}}
.box{{border:1px solid #cfc3dc;border-radius:12px;padding:.9em 1.1em;background:rgba(255,255,255,.6)}}
.box b{{font-family:Fraunces,serif;font-size:13pt;color:#3a3148}}.u{{font:700 10pt Lato,sans-serif;color:#556450}}
.s{{font:8pt/1.5 Lato,sans-serif;color:#6b6475;margin-top:2.2em}}</style></head><body>
<p class="k">End of the free sample</p>
<h1>Thank you for reading the first chapter.</h1>
<p>The full book continues through all five layers of personal vibration, with practices, a 30-day plan and reflection worksheets:</p>
<ul><li>Chapters 2&ndash;9: the layered model; body rhythms; breath &amp; heart; emotions; attention &amp; brainwaves; meaning; sound; people &amp; places</li>
<li>Chapter 10: daily practices, a sample day and a practice menu</li>
<li>Chapter 11: your 30-day plan, one small practice a day</li>
<li>Chapter 12: printable worksheets, journal prompts and checklists</li>
<li>Sources &amp; further reading, grouped by chapter</li></ul>
<div class="box"><b>Get the complete ebook: pay what you want</b><br>52 pages &middot; PDF &middot; First edition 2026<br><span class="u">{EBOOK_URL}</span></div>
<p class="s">This book is for general education and is not medical or psychological advice. Consult a qualified professional about any health concern.</p>
</body></html>"""

def run(*a): subprocess.run(a, check=True, stderr=subprocess.DEVNULL)

def render(pdf, page, width, out):
    run("pdftoppm", "-f", str(page), "-l", str(page), "-scale-to-x", str(width), "-scale-to-y", "-1", "-png", "-singlefile", str(pdf), str(out))
    return Image.open(f"{out}.png").convert("RGB")

def main(pdf):
    pdf = Path(pdf).resolve(); IMG.mkdir(parents=True, exist_ok=True); EB.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cover = render(pdf, 1, 1080, td / "cover")
        cover.resize((720, 1080), Image.LANCZOS).save(IMG / "ebook-cover.webp", quality=84, method=6)
        cover.resize((400, 600), Image.LANCZOS).save(IMG / "ebook-cover-sm.webp", quality=82, method=6)
        # Social card: cover on a soft dusk gradient
        og = Image.new("RGB", (1200, 630), "#3a3148"); d = ImageDraw.Draw(og)
        for y in range(630):
            t = y / 629; c = tuple(int(a + (b - a) * t) for a, b in zip((58, 49, 72), (231, 181, 152)))
            d.line([(0, y), (1200, y)], fill=c)
        bg = cover.resize((1200, 1800)).crop((0, 600, 1200, 1230)).filter(ImageFilter.GaussianBlur(28))
        og = Image.blend(og, bg, .55)
        c = cover.resize((360, 540), Image.LANCZOS)
        sh = Image.new("L", (1200, 630), 0); ImageDraw.Draw(sh).rectangle((430, 60, 790, 600), fill=150)
        og.paste((20, 16, 28), mask=sh.filter(ImageFilter.GaussianBlur(22)))
        og.paste(c, (420, 45)); og.save(IMG / "ebook-og.jpg", quality=86, optimize=True)
        for p in THUMB_PAGES:
            render(pdf, p, 360, td / f"p{p}").save(IMG / f"ebook-page-{p}.webp", quality=78, method=6)
        # Sample PDF: pdftocairo re-writes only the resources these pages use (pdfseparate would drag
        # every image and font of the whole book along).
        first, last = SAMPLE_PAGES
        run("pdftocairo", "-pdf", "-f", str(first), "-l", str(last), str(pdf), str(td / "sample.pdf"))
        parts = [td / "sample.pdf"]
        try:
            from playwright.sync_api import sync_playwright
            (td / "end.html").write_text(END_PAGE)
            with sync_playwright() as pw:
                b = pw.chromium.launch(); pg = b.new_page(); pg.goto((td / "end.html").as_uri()); pg.wait_for_timeout(1500)
                pg.pdf(path=str(td / "end.pdf"), width="6in", height="9in", print_background=True, prefer_css_page_size=True); b.close()
            parts.append(td / "end.pdf")
        except Exception as e:
            print("(no closing page:", e, ")")
        run("pdfunite", *map(str, parts), str(EB / "good-vibrations-sample.pdf"))
    # Illustrations from the book's source folder (optional): the layered-model diagram
    src_img = pdf.parent / "img"
    for name, out, w in [("fig_layers.png", "ebook-layers.webp", 720)]:
        if (src_img / name).exists():
            im = Image.open(src_img / name)
            im = im.convert("RGBA" if im.mode == "RGBA" else "RGB"); im.thumbnail((w, w)); im.save(IMG / out, quality=82, method=6)
    out = EB / "good-vibrations-sample.pdf"
    print("sample:", out, f"{out.stat().st_size/1e6:.2f} MB")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/workspace/ebook/good-vibrations.pdf")
