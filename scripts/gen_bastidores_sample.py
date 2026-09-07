#!/usr/bin/env python3
"""
InovaShot - Bastidores Generator (1080x1080)
Specs (aprovadas 05/09/2026, documentadas em DESIGN.md):
- Canvas 1080x1080
- Background: preto puro (diferente do #070412 do formato Dark)
- Kicker "INOVASHOT · BASTIDORES" com ponto colorido (roxo-sinal)
- Frase em destaque estilo citação, Poppins Bold ~72px, alinhada à esquerda,
  centralizada verticalmente acima da faixa de rodapé
- Numero de fundo (~10% opacidade) ao fundo
- Rodape: faixa de gradiente rosa->roxo->azul + @inovashot.cortes
"""

import sys
import json
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080

BG = (0, 0, 0)  # preto puro
ROSA = (244, 114, 182)  # #f472b6
ROXO = (168, 85, 247)   # #a855f7
AZUL = (56, 189, 248)   # #38bdf8
KICKER_COLOR = (200, 190, 220)  # #c8bedc
DOT_COLOR = ROXO
TITLE_COLOR = (255, 255, 255)
FOOTER_HANDLE_COLOR = (235, 232, 240)  # #ebe8f0

FONT_DIR = "/usr/share/fonts/truetype/google-fonts"
F_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
F_MEDIUM = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

FOOTER_HEIGHT = 220
KICKER_Y = 90


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=fnt)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def gradient_3stop(t):
    if t <= 0.5:
        return lerp_color(ROSA, ROXO, t / 0.5)
    else:
        return lerp_color(ROXO, AZUL, (t - 0.5) / 0.5)


def draw_kicker(draw, img, label="INOVASHOT · BASTIDORES"):
    dot_r = 9
    dot_x = 90
    dot_y = KICKER_Y + 18
    draw.ellipse(
        [dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r],
        fill=DOT_COLOR,
    )
    kicker_font = font(F_MEDIUM, 30)
    draw.text((dot_x + 24, KICKER_Y), label, font=kicker_font, fill=KICKER_COLOR)

    bar_y = KICKER_Y + 52
    bar_w, bar_h = 90, 8
    bar_img = Image.new("RGB", (bar_w, bar_h))
    bar_draw = ImageDraw.Draw(bar_img)
    for i in range(bar_w):
        t = i / max(bar_w - 1, 1)
        bar_draw.line([(i, 0), (i, bar_h)], fill=gradient_3stop(t))
    img.paste(bar_img, (dot_x - dot_r, bar_y))
    return bar_y + bar_h


def draw_footer(img, draw, page_num, total_pages):
    band_top = H - FOOTER_HEIGHT
    band_img = Image.new("RGB", (W, FOOTER_HEIGHT))
    band_draw = ImageDraw.Draw(band_img)
    for i in range(W):
        t = i / max(W - 1, 1)
        grad_c = gradient_3stop(t)
        blended = lerp_color(BG, grad_c, 0.35)
        band_draw.line([(i, 0), (i, FOOTER_HEIGHT)], fill=blended)
    img.paste(band_img, (0, band_top))

    handle_font = font(F_BOLD, 34)
    page_font = font(F_MEDIUM, 28)

    handle_x = 70
    handle_y = band_top + (FOOTER_HEIGHT - 34) // 2
    draw.text((handle_x, handle_y), "@inovashot.cortes", font=handle_font, fill=FOOTER_HANDLE_COLOR)

    page_text = f"{page_num:02d}/{total_pages:02d}"
    bbox = draw.textbbox((0, 0), page_text, font=page_font)
    page_x = W - 70 - (bbox[2] - bbox[0])
    page_y = band_top + (FOOTER_HEIGHT - 28) // 2
    draw.text((page_x, page_y), page_text, font=page_font, fill=FOOTER_HANDLE_COLOR)


def draw_ghost_number(img, number):
    ghost_font = font(F_BOLD, 780)
    ghost_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(ghost_layer)
    text = str(number)
    bbox = gdraw.textbbox((0, 0), text, font=ghost_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = W - tw - 40 - bbox[0]
    y = H - FOOTER_HEIGHT - th - 20 - bbox[1]
    gdraw.text((x, y), text, font=ghost_font, fill=(255, 255, 255, 26))
    img.paste(ghost_layer, (0, 0), ghost_layer)


def new_canvas():
    return Image.new("RGB", (W, H), BG)


def bastidores_slide(data, out_path, page_num, total_pages):
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    if not data.get("no_ghost"):
        draw_ghost_number(img, page_num)
        draw = ImageDraw.Draw(img)

    draw_kicker(draw, img, data.get("eyebrow", "INOVASHOT · BASTIDORES"))

    # Frase em destaque: alinhada a esquerda, centralizada verticalmente
    # acima da faixa de rodape
    max_w = W - 160
    quote_font = font(F_BOLD, 72)
    lines = wrap_text(draw, data["quote"], quote_font, max_w)

    line_heights = []
    total_h = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        lh = (bbox[3] - bbox[1]) + 20
        line_heights.append(lh)
        total_h += lh

    available_top = 0
    available_bottom = H - FOOTER_HEIGHT
    center_y = (available_top + available_bottom) // 2
    y = center_y - total_h // 2

    for line, lh in zip(lines, line_heights):
        draw.text((80, y), line, font=quote_font, fill=TITLE_COLOR)
        y += lh

    draw_footer(img, draw, page_num, total_pages)
    img.save(out_path)


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 gen_bastidores_sample.py [json-path] [output-dir]")
        sys.exit(1)

    json_path = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        slides = json.load(f)

    total = len(slides)
    for idx, slide in enumerate(slides, start=1):
        out_path = os.path.join(out_dir, f"slide-{idx}.png")
        bastidores_slide(slide, out_path, idx, total)
        print(f"Gerado: {out_path}")


if __name__ == "__main__":
    main()
