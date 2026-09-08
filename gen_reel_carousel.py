#!/usr/bin/env python3
"""
InovaShot - Reel Carousel Generator (Dark format, 1080x1920)
Specs (aprovadas 05/09/2026):
- Canvas 1080x1920
- Background solid #070412
- Footer band height 320px, 35% blend gradient rosa->roxo->azul over #070412
- Kicker/bar start at y=260 (avoid IG top UI collision)
- Ghost number ~950px, ~10% opacity white
- Handle Poppins Bold 46px, pagination Poppins Medium 38px stacked BELOW handle (left)
- Safe zone 480px at bottom - no custom footer content there
- CTA slide: no ghost number, polygon arrow (never emoji)
"""

import sys
import json
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

BG = (7, 4, 18)  # #070412
ROSA = (244, 114, 182)  # #f472b6
ROXO = (168, 85, 247)   # #a855f7
AZUL = (56, 189, 248)   # #38bdf8
KICKER_COLOR = (200, 190, 220)  # #c8bedc
DOT_COLOR = ROXO
TITLE_COLOR = (255, 255, 255)
BODY_COLOR = (220, 215, 230)  # #dcd7e6
FOOTER_HANDLE_COLOR = (235, 232, 240)  # #ebe8f0

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(SCRIPT_DIR, "scripts", "fonts")
F_BOLD = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
F_MEDIUM = os.path.join(FONT_DIR, "Poppins-Medium.ttf")

FOOTER_HEIGHT = 320
SAFE_ZONE = 480  # bottom px reserved for IG reels UI - no custom content here
KICKER_Y = 260


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
    # t in [0,1] across rosa -> roxo -> azul
    if t <= 0.5:
        return lerp_color(ROSA, ROXO, t / 0.5)
    else:
        return lerp_color(ROXO, AZUL, (t - 0.5) / 0.5)


def draw_horizontal_gradient_bar(img_draw, x, y, w, h, opacity=255):
    for i in range(w):
        t = i / max(w - 1, 1)
        color = gradient_3stop(t)
        img_draw.line([(x + i, y), (x + i, y + h)], fill=color + (opacity,) if len(color) == 3 else color)


def draw_kicker(draw, img, label="INOVASHOT · CORTES"):
    dot_r = 9
    dot_x = 90
    dot_y = KICKER_Y + 18
    draw.ellipse(
        [dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r],
        fill=DOT_COLOR,
    )
    kicker_font = font(F_MEDIUM, 34)
    draw.text((dot_x + 24, KICKER_Y), label, font=kicker_font, fill=KICKER_COLOR)

    # gradient bar below kicker
    bar_y = KICKER_Y + 60
    bar_w, bar_h = 110, 9
    bar_img = Image.new("RGB", (bar_w, bar_h))
    bar_draw = ImageDraw.Draw(bar_img)
    for i in range(bar_w):
        t = i / max(bar_w - 1, 1)
        bar_draw.line([(i, 0), (i, bar_h)], fill=gradient_3stop(t))
    img.paste(bar_img, (dot_x - dot_r, bar_y))
    return bar_y + bar_h


def draw_footer(img, draw, page_num, total_pages):
    # footer gradient band: 35% blend of rosa->roxo->azul over BG
    band_top = H - FOOTER_HEIGHT
    band_img = Image.new("RGB", (W, FOOTER_HEIGHT))
    band_draw = ImageDraw.Draw(band_img)
    for i in range(W):
        t = i / max(W - 1, 1)
        grad_c = gradient_3stop(t)
        blended = lerp_color(BG, grad_c, 0.35)
        band_draw.line([(i, 0), (i, FOOTER_HEIGHT)], fill=blended)
    img.paste(band_img, (0, band_top))

    handle_font = font(F_BOLD, 46)
    page_font = font(F_MEDIUM, 38)

    handle_x = 70
    handle_y = band_top + 60
    draw.text((handle_x, handle_y), "@inovashot.cortes", font=handle_font, fill=FOOTER_HANDLE_COLOR)

    page_y = handle_y + 66
    draw.text((handle_x, page_y), f"{page_num:02d}/{total_pages:02d}", font=page_font, fill=FOOTER_HANDLE_COLOR)


def draw_ghost_number(img, number):
    ghost_font = font(F_BOLD, 950)
    ghost_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(ghost_layer)
    text = str(number)
    bbox = gdraw.textbbox((0, 0), text, font=ghost_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = W - tw - 40 - bbox[0]
    y = H - FOOTER_HEIGHT - th - 40 - bbox[1]
    gdraw.text((x, y), text, font=ghost_font, fill=(255, 255, 255, 26))  # ~10% opacity
    img.paste(ghost_layer, (0, 0), ghost_layer)


def draw_polygon_arrow(draw, x, y, size=28, color=(255, 255, 255)):
    # simple right-pointing triangle/arrow polygon (never emoji)
    points = [
        (x, y - size),
        (x, y + size),
        (x + size * 1.3, y),
    ]
    draw.polygon(points, fill=color)


def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    return img


def cover_slide(data, out_path, page_num, total_pages):
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    draw_ghost_number(img, page_num)
    draw = ImageDraw.Draw(img)

    content_top = draw_kicker(draw, img, data.get("eyebrow", "INOVASHOT · CORTES"))

    title_font = font(F_BOLD, 78)
    max_w = W - 160
    title_lines = wrap_text(draw, data["headline"], title_font, max_w)
    ty = content_top + 70
    for line in title_lines:
        draw.text((80, ty), line, font=title_font, fill=TITLE_COLOR)
        bbox = draw.textbbox((0, 0), line, font=title_font)
        ty += (bbox[3] - bbox[1]) + 28

    if data.get("body"):
        body_font = font(F_MEDIUM, 46)
        body_lines = wrap_text(draw, data["body"], body_font, max_w)
        ty += 30
        # nunca desenha dentro da safe zone reservada pra UI do Reels
        content_limit = H - SAFE_ZONE
        for line in body_lines:
            bbox = draw.textbbox((0, 0), line, font=body_font)
            line_h = (bbox[3] - bbox[1]) + 20
            if ty + line_h > content_limit:
                print("Aviso: corpo do cover_slide truncado — não cabia antes da safe zone.")
                break
            draw.text((80, ty), line, font=body_font, fill=BODY_COLOR)
            ty += line_h

    draw_footer(img, draw, page_num, total_pages)
    img.save(out_path)


def body_slide(data, out_path, page_num, total_pages):
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    draw_ghost_number(img, page_num)
    draw = ImageDraw.Draw(img)

    content_top = draw_kicker(draw, img, data.get("eyebrow", "INOVASHOT · CORTES"))

    max_w = W - 160
    y_start = content_top + 70
    # nunca desenha dentro da safe zone reservada pra UI do Reels
    content_limit = H - SAFE_ZONE

    item_title_font = font(F_BOLD, 52)
    body_font = font(F_MEDIUM, 40)

    # Pré-calcula a altura natural de cada item (title + text + espaço),
    # só inclui item por item enquanto couber antes da safe zone — igual
    # à estratégia usada em gen_listicle.py pro mesmo tipo de bug.
    all_items = data["items"]
    rows = []
    for item in all_items:
        title_lines = wrap_text(draw, item["title"], item_title_font, max_w)
        title_heights = [
            (draw.textbbox((0, 0), line, font=item_title_font)[3]
             - draw.textbbox((0, 0), line, font=item_title_font)[1]) + 16
            for line in title_lines
        ]
        text_lines = wrap_text(draw, item["text"], body_font, max_w)
        text_heights = [
            (draw.textbbox((0, 0), line, font=body_font)[3]
             - draw.textbbox((0, 0), line, font=body_font)[1]) + 14
            for line in text_lines
        ]
        item_h = sum(title_heights) + sum(text_heights) + 50
        rows.append((title_lines, title_heights, text_lines, text_heights, item_h))

    kept = []
    total_h = 0
    for row in rows:
        if kept and y_start + total_h + row[4] > content_limit:
            break
        kept.append(row)
        total_h += row[4]

    if len(kept) < len(all_items):
        print(
            f"Aviso: {len(all_items)} itens não cabem antes da safe zone; "
            f"truncando pra {len(kept)}."
        )

    y = y_start
    for title_lines, title_heights, text_lines, text_heights, item_h in kept:
        for line, lh in zip(title_lines, title_heights):
            draw.text((80, y), line, font=item_title_font, fill=TITLE_COLOR)
            y += lh
        for line, lh in zip(text_lines, text_heights):
            draw.text((80, y), line, font=body_font, fill=BODY_COLOR)
            y += lh
        y += 50  # spacing between items

    draw_footer(img, draw, page_num, total_pages)
    img.save(out_path)


def cta_slide(data, out_path, page_num, total_pages, cta_label="Link na bio"):
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    # no ghost number on CTA slide
    content_top = draw_kicker(draw, img, data.get("eyebrow", "INOVASHOT · CORTES"))

    max_w = W - 160
    title_font = font(F_BOLD, 72)

    # cta_label passa por wrap_text — sem isso, um label longo vazava
    # pra fora do canvas em vez de quebrar linha. Calculado ANTES do
    # headline pra saber a altura real do CTA (pode ser mais de 1
    # linha) e nunca deixar essa altura invadir o rodapé.
    cta_font = font(F_BOLD, 50)
    cta_max_w = W - 160 - 100  # deixa espaço pra seta depois do texto
    cta_lines = wrap_text(draw, cta_label, cta_font, cta_max_w)
    cta_line_heights = []
    for line in cta_lines:
        bbox = draw.textbbox((0, 0), line, font=cta_font)
        cta_line_heights.append((bbox[3] - bbox[1]) + 14)
    cta_total_h = sum(cta_line_heights)

    cta_y_default = H - FOOTER_HEIGHT - 140  # posição-alvo, perto do rodapé
    footer_top = H - FOOTER_HEIGHT
    # nunca deixa a última linha do CTA invadir o rodapé, mesmo com
    # label longo (múltiplas linhas)
    cta_y = min(cta_y_default, footer_top - cta_total_h - 20)

    # Pré-calcula as linhas do headline e só desenha o que couber antes
    # do CTA (que agora já reflete a altura real dele) — sem isso,
    # headline longo atropela a linha do CTA. Mesma estratégia de
    # body_slide/cover_slide.
    all_title_lines = wrap_text(draw, data["headline"], title_font, max_w)
    title_heights = []
    for line in all_title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        title_heights.append((bbox[3] - bbox[1]) + 28)

    title_start = content_top + 100
    title_limit = cta_y - 40  # margem mínima antes do CTA
    kept_lines, kept_heights, total_h = [], [], 0
    for line, lh in zip(all_title_lines, title_heights):
        if kept_lines and title_start + total_h + lh > title_limit:
            break
        kept_lines.append(line)
        kept_heights.append(lh)
        total_h += lh

    if len(kept_lines) < len(all_title_lines):
        print(
            f"Aviso: headline do CTA com {len(all_title_lines)} linhas não "
            f"cabe antes do CTA; truncando pra {len(kept_lines)}."
        )

    ty = title_start
    for line, lh in zip(kept_lines, kept_heights):
        draw.text((80, ty), line, font=title_font, fill=TITLE_COLOR)
        ty += lh

    # CTA row with polygon arrow (drawn above footer, not in safe zone)
    line_y = cta_y
    last_bbox = None
    for line in cta_lines:
        draw.text((80, line_y), line, font=cta_font, fill=TITLE_COLOR)
        last_bbox = draw.textbbox((0, 0), line, font=cta_font)
        last_line_y = line_y
        line_y += (last_bbox[3] - last_bbox[1]) + 14

    arrow_x = 80 + (last_bbox[2] - last_bbox[0]) + 50
    arrow_y = last_line_y + (last_bbox[3] - last_bbox[1]) // 2
    draw_polygon_arrow(draw, arrow_x, arrow_y, size=26, color=TITLE_COLOR)

    draw_footer(img, draw, page_num, total_pages)
    img.save(out_path)


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 gen_reel_carousel.py [json-path] [output-dir]")
        sys.exit(1)

    json_path = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        slides = json.load(f)

    total = len(slides)
    for idx, slide in enumerate(slides, start=1):
        out_path = os.path.join(out_dir, f"slide-{idx}.png")
        stype = slide.get("type", "body")
        if stype == "cover":
            cover_slide(slide, out_path, idx, total)
        elif stype == "cta":
            cta_slide(slide, out_path, idx, total, cta_label=slide.get("cta_label", "Link na bio"))
        else:
            body_slide(slide, out_path, idx, total)
        print(f"Gerado: {out_path}")


if __name__ == "__main__":
    main()
