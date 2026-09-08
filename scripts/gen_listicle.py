#!/usr/bin/env python3
"""
InovaShot - Lista (Listicle) Generator (1080x1080)
Specs (aprovadas 05/09/2026, documentadas em DESIGN.md):
- Canvas 1080x1080, fundo #070412
- Kicker "INOVASHOT · CORTES" + barra de gradiente 100x9px
- Subkicker "SALVA PRA DEPOIS" em lilas-apagado (#c8bedc)
- Card de lista: fundo #120d20, linhas separadas por #261e37, circulos
  numerados com cor interpolada do gradiente de marca por item
- Texto: Poppins Medium, peso leve
- Rodape: gradiente + @inovashot.cortes (linha 1) + CTA "Siga pra mais
  atualizacoes" com seta poligonal (linha 2, empilhada, nunca sobreposta)
- Uso: conteudo de valor generico, SEM citar InovaShot no corpo
"""

import sys
import json
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080

BG = (7, 4, 18)         # #070412
CARD_BG = (18, 13, 32)  # #120d20
DIVIDER = (38, 30, 55)  # #261e37
ROSA = (244, 114, 182)  # #f472b6
ROXO = (168, 85, 247)   # #a855f7
AZUL = (56, 189, 248)   # #38bdf8
KICKER_COLOR = (200, 190, 220)  # #c8bedc
SUBKICKER_COLOR = (200, 190, 220)  # #c8bedc
DOT_COLOR = ROXO
TITLE_COLOR = (255, 255, 255)
BODY_COLOR = (220, 215, 230)  # #dcd7e6, texto leve dentro do card
FOOTER_HANDLE_COLOR = (255, 255, 255)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(SCRIPT_DIR, "fonts")
F_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
F_MEDIUM = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

# ponytail: teto fixo, calibrado pro caso comum (headline de 1 linha +
# itens de 1 linha coube até 5; item 6 já cortava no rodapé). Headline
# longo ou itens multi-linha podem estourar mesmo dentro do limite —
# upgrade real seria calcular o máximo a partir do espaço disponível
# depois do headline, não um número fixo. Ver learnings.md.
MAX_ITEMS = 5

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


def draw_kicker(draw, img):
    dot_r = 9
    dot_x = 90
    dot_y = KICKER_Y + 18
    draw.ellipse(
        [dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r],
        fill=DOT_COLOR,
    )
    kicker_font = font(F_MEDIUM, 30)
    draw.text((dot_x + 24, KICKER_Y), "INOVASHOT · CORTES", font=kicker_font, fill=KICKER_COLOR)

    bar_y = KICKER_Y + 52
    bar_w, bar_h = 100, 9
    bar_img = Image.new("RGB", (bar_w, bar_h))
    bar_draw = ImageDraw.Draw(bar_img)
    for i in range(bar_w):
        t = i / max(bar_w - 1, 1)
        bar_draw.line([(i, 0), (i, bar_h)], fill=gradient_3stop(t))
    img.paste(bar_img, (dot_x - dot_r, bar_y))
    return bar_y + bar_h


def draw_footer(img, draw):
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
    cta_font = font(F_MEDIUM, 28)

    handle_x = 70
    line1_y = band_top + 60
    draw.text((handle_x, line1_y), "@inovashot.cortes", font=handle_font, fill=FOOTER_HANDLE_COLOR)

    line2_y = line1_y + 58
    cta_text = "Siga pra mais atualizações"
    draw.text((handle_x, line2_y), cta_text, font=cta_font, fill=FOOTER_HANDLE_COLOR)

    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    arrow_x = handle_x + (bbox[2] - bbox[0]) + 30
    arrow_y = line2_y + (bbox[3] - bbox[1]) // 2
    draw_polygon_arrow(draw, arrow_x, arrow_y, size=16, color=FOOTER_HANDLE_COLOR)


def draw_polygon_arrow(draw, x, y, size=26, color=(255, 255, 255)):
    points = [
        (x, y - size),
        (x, y + size),
        (x + size * 1.3, y),
    ]
    draw.polygon(points, fill=color)


def draw_numbered_circle(draw, cx, cy, r, number, total_items):
    t = (number - 1) / max(total_items - 1, 1)
    color = gradient_3stop(t)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    num_font = font(F_BOLD, int(r * 1.1))
    text = str(number)
    bbox = draw.textbbox((0, 0), text, font=num_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=num_font, fill=(255, 255, 255))


def new_canvas():
    return Image.new("RGB", (W, H), BG)


def lista_slide(data, out_path):
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    content_top = draw_kicker(draw, img)

    max_w = W - 160

    # Title
    title_font = font(F_BOLD, 56)
    title_lines = wrap_text(draw, data["headline"], title_font, max_w)
    ty = content_top + 50
    for line in title_lines:
        draw.text((80, ty), line, font=title_font, fill=TITLE_COLOR)
        bbox = draw.textbbox((0, 0), line, font=title_font)
        ty += (bbox[3] - bbox[1]) + 16

    # Subkicker
    sub_font = font(F_MEDIUM, 26)
    ty += 10
    draw.text((80, ty), "SALVA PRA DEPOIS", font=sub_font, fill=SUBKICKER_COLOR)
    bbox = draw.textbbox((0, 0), "SALVA PRA DEPOIS", font=sub_font)
    ty += (bbox[3] - bbox[1]) + 40

    # Card de lista
    items = data["items"]
    if len(items) > MAX_ITEMS:
        print(f"Aviso: {len(items)} itens excede o máximo de {MAX_ITEMS}; truncando.")
        items = items[:MAX_ITEMS]
    card_x0 = 80
    card_x1 = W - 80
    card_y0 = ty
    card_bottom_limit = H - FOOTER_HEIGHT - 40
    card_height = card_bottom_limit - card_y0

    draw.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y0 + card_height],
        radius=24,
        fill=CARD_BG,
    )

    circle_r = 34
    item_font = font(F_MEDIUM, 32)
    row_pad_v = 28  # vertical padding inside each row
    text_x = card_x0 + 30 + circle_r * 2 + 30
    text_max_w = card_x1 - 30 - text_x

    # First pass: compute wrapped lines and natural row heights
    rows_data = []
    line_gap = 6
    for item in items:
        lines = wrap_text(draw, item, item_font, text_max_w)
        heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=item_font)
            heights.append((bbox[3] - bbox[1]) + line_gap)
        text_block_h = sum(heights)
        row_h = max(circle_r * 2 + row_pad_v, text_block_h + row_pad_v)
        rows_data.append((lines, heights, row_h))

    # Scale rows proportionally to fill card_height exactly
    natural_total = sum(r[2] for r in rows_data)
    # Nunca encolhe abaixo do tamanho natural de cada linha (senão o
    # conteúdo desenhado - círculo + texto - passa a se sobrepor); só
    # estica pra preencher o card quando sobra espaço.
    scale = max(card_height / natural_total, 1.0) if natural_total > 0 else 1

    y_cursor = card_y0
    for i, (lines, heights, row_h) in enumerate(rows_data):
        scaled_row_h = row_h * scale
        row_top = y_cursor
        row_center = row_top + scaled_row_h / 2

        if i > 0:
            draw.line([(card_x0 + 30, row_top), (card_x1 - 30, row_top)], fill=DIVIDER, width=2)

        circle_cx = card_x0 + 30 + circle_r
        draw_numbered_circle(draw, circle_cx, row_center, circle_r, i + 1, len(items))

        line_h_total = sum(heights)
        ly = row_center - line_h_total / 2
        for line, lh in zip(lines, heights):
            draw.text((text_x, ly), line, font=item_font, fill=BODY_COLOR)
            ly += lh

        y_cursor += scaled_row_h

    draw_footer(img, draw)
    img.save(out_path)


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 gen_listicle.py [json-path] [output-dir]")
        sys.exit(1)

    json_path = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        slides = json.load(f)

    for idx, slide in enumerate(slides, start=1):
        out_path = os.path.join(out_dir, f"slide-{idx}.png")
        lista_slide(slide, out_path)
        print(f"Gerado: {out_path}")


if __name__ == "__main__":
    main()
