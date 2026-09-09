#!/usr/bin/env python3
"""Gera slides de Reel nativo (1080x1920) pro template Bastidores.
Specs oficiais: preto puro, kicker y=260, ghost number ~950px @10% opacidade,
footer band ~320px com blend 35%, paginacao empilhada sob o handle."""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
MARGIN = 72

BG = (0, 0, 0)
WHITE = (255, 255, 255)
KICKER_COLOR = (200, 190, 220)      # #c8bedc
DOT_COLOR = (168, 85, 247)          # #a855f7
HANDLE_COLOR = (235, 232, 240)      # #ebe8f0
GRAD = [(244, 114, 182), (168, 85, 247), (56, 189, 248)]  # #f472b6 -> #a855f7 -> #38bdf8

FONT_DIR = "/usr/share/fonts/truetype/google-fonts/"
F_BOLD = FONT_DIR + "Poppins-Bold.ttf"
F_MEDIUM = FONT_DIR + "Poppins-Medium.ttf"


def hgradient(w, h, colors):
    n = len(colors) - 1
    lut = []
    for x in range(w):
        t = x / max(1, w - 1)
        seg = min(int(t * n), n - 1)
        local_t = t * n - seg
        c0, c1 = colors[seg], colors[seg + 1]
        lut.append(tuple(int(c0[i] + (c1[i] - c0[i]) * local_t) for i in range(3)))
    img = Image.new("RGB", (w, h))
    img.putdata([lut[x] for _y in range(h) for x in range(w)])
    return img


def wrap_text(draw, text, fnt, max_width):
    words = text.split(" ")
    lines, cur = [], []
    for w in words:
        test = " ".join(cur + [w])
        if draw.textlength(test, font=fnt) <= max_width or not cur:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_ghost_number(img, number, size=950, opacity=0.10):
    layer = Image.new("L", (W, H), 0)
    ldraw = ImageDraw.Draw(layer)
    right_margin = 40
    max_w = W - right_margin - 20  # deixa uma folga minima na esquerda tambem
    fnt = ImageFont.truetype(F_BOLD, size)
    bbox = ldraw.textbbox((0, 0), number, font=fnt)
    tw = bbox[2] - bbox[0]
    while tw > max_w and size > 200:
        size -= 20
        fnt = ImageFont.truetype(F_BOLD, size)
        bbox = ldraw.textbbox((0, 0), number, font=fnt)
        tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = W - tw - right_margin - bbox[0]
    y = H - th - 260 - bbox[1]
    ldraw.text((x, y), number, font=fnt, fill=int(255 * opacity))
    white = Image.new("RGB", (W, H), WHITE)
    base = img.convert("RGB")
    base.paste(white, (0, 0), layer)
    return base.convert("RGB")


def draw_footer_band(img, band_h=320, blend=0.35):
    grad = hgradient(W, band_h, GRAD)
    band_bg = Image.new("RGB", (W, band_h), BG)
    blended = Image.blend(band_bg, grad, blend)
    img.paste(blended, (0, H - band_h))


def make_slide(out_path, kicker, title, page_label):
    img = Image.new("RGB", (W, H), BG)

    # ghost number (numero da pagina) - camada composta antes do resto
    number = page_label.split("/")[0]
    img = draw_ghost_number(img, number)

    draw_footer_band(img)
    draw = ImageDraw.Draw(img)

    # kicker (y fixo = 260, evita UI nativa do Instagram)
    ky = 260
    kfnt = ImageFont.truetype(F_MEDIUM, 30)
    dot_r = 5
    draw.ellipse([MARGIN, ky + 10, MARGIN + dot_r * 2, ky + 10 + dot_r * 2], fill=DOT_COLOR)
    draw.text((MARGIN + 24, ky), kicker, font=kfnt, fill=KICKER_COLOR)

    # barra gradiente 90x8
    bar = hgradient(90, 8, GRAD)
    img.paste(bar, (MARGIN, ky + 60))
    draw = ImageDraw.Draw(img)

    # titulo
    tfnt = ImageFont.truetype(F_BOLD, 72)
    max_w = W - 2 * MARGIN
    lines = wrap_text(draw, title, tfnt, max_w)
    line_h = int(72 * 1.2)
    ty = ky + 140
    for line in lines:
        draw.text((MARGIN, ty), line, font=tfnt, fill=WHITE)
        ty += line_h

    # footer: handle + paginacao empilhada
    hfnt = ImageFont.truetype(F_BOLD, 46)
    draw.text((MARGIN, H - 260), "@inovashot.cortes", font=hfnt, fill=HANDLE_COLOR)
    pfnt = ImageFont.truetype(F_MEDIUM, 38)
    draw.text((MARGIN, H - 195), page_label, font=pfnt, fill=KICKER_COLOR)

    img.save(out_path)
    print("saved", out_path)


if __name__ == "__main__":
    content_path = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    with open(content_path, encoding="utf-8") as f:
        slides = json.load(f)
    default_total = len(slides)
    for idx, s in enumerate(slides, start=1):
        i = s.get("index", idx)
        total = s.get("total", default_total)
        make_slide(
            os.path.join(out_dir, f"reel-slide-{i}.png"),
            kicker=s.get("kicker", "INOVASHOT \u00b7 BASTIDORES"),
            title=s["title"],
            page_label=f"{i:02d}/{total:02d}",
        )
