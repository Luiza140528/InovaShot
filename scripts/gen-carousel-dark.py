#!/usr/bin/env python3
"""Gera o carrossel Instagram/Facebook no template ESCURO (oficial).
Spec: DESIGN.md, secao "Social Media Carousel (Instagram @inovashot.cortes)".

NOTA: este arquivo substitui gen-carousel-light.py. O template claro
(creme->lilas) foi testado em 30/08/2026 e definitivamente descartado —
nao deve ser reintroduzido sem confirmacao explicita da Luiza.
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(SCRIPT_DIR, "fonts")
CONTENT_DIR = os.path.join(SCRIPT_DIR, "carousel-content")
DEFAULT_CONTENT_PATH = os.path.join(CONTENT_DIR, "radar-claude.json")
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "marketing", "carrossel-radar-claude")

W = H = 1080
MARGIN = 72
CONTENT_W = W - 2 * MARGIN

BG = (7, 4, 18)              # #070412 - fundo oficial, permanente
WHITE = (255, 255, 255)
TEXT_BODY = (220, 215, 230)  # lilas-apagado sobre fundo escuro
FOOTER_TEXT = (235, 232, 240)  # branco quase puro - handle precisa de alto contraste
KICKER_TEXT = (200, 190, 220)

GRAD_COLORS = [(244, 114, 182), (168, 85, 247), (56, 189, 248)]  # pink -> purple -> blue

def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)

F_BOLD = "Poppins-Bold.ttf"
F_MEDIUM = "Poppins-Medium.ttf"
F_REGULAR = "Poppins-Regular.ttf"
# Sem segunda familia tipografica (sem Space Mono) - The Single-Typeface Rule


def diag_gradient(w, h, colors, angle_horizontal=True):
    """Linear gradient image, w x h, RGBA. Horizontal (90deg) por padrao,
    usado na barra fina e na faixa da base do slide."""
    w = max(1, w)
    h = max(1, h)
    n = len(colors) - 1
    span = w if angle_horizontal else (w + h)
    lut = []
    for s in range(span):
        t = min(max(s / span, 0.0), 1.0)
        seg = min(int(t * n), n - 1)
        local_t = t * n - seg
        c0 = colors[seg]
        c1 = colors[seg + 1]
        r = int(c0[0] + (c1[0] - c0[0]) * local_t)
        g = int(c0[1] + (c1[1] - c0[1]) * local_t)
        b = int(c0[2] + (c1[2] - c0[2]) * local_t)
        lut.append((r, g, b))
    base = Image.new("RGB", (w, h))
    if angle_horizontal:
        base.putdata([lut[x] for y in range(h) for x in range(w)])
    else:
        base.putdata([lut[x + y] for y in range(h) for x in range(w)])
    return base.convert("RGBA")


def draw_spaced_text(draw, xy, text, fnt, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w = draw.textlength(ch, font=fnt)
        x += w + tracking
    return x - xy[0]


def wrap_tokens(draw, tokens, fnt, max_width):
    """tokens: list of (text, is_gradient). Nao usado mais para gradiente no
    titulo (titulo agora e sempre branco puro), mantido para wrap generico."""
    space_w = draw.textlength(" ", font=fnt)
    lines = []
    cur = []
    cur_w = 0
    for tok_text, is_grad in tokens:
        tw = draw.textlength(tok_text, font=fnt)
        add_w = tw if not cur else tw + space_w
        if cur and cur_w + add_w > max_width:
            lines.append(cur)
            cur = [(tok_text, is_grad, tw)]
            cur_w = tw
        else:
            cur.append((tok_text, is_grad, tw))
            cur_w += add_w
    if cur:
        lines.append(cur)
    return lines


def headline_tokens(text):
    return [(w, False) for w in text.split(" ") if w]


def fit_headline(draw, text, max_width, max_height, start_size=68, min_size=38):
    def layout(size):
        fnt = font(F_BOLD, size)
        tokens = headline_tokens(text)
        lines = wrap_tokens(draw, tokens, fnt, max_width)
        line_h = int(size * 1.18)
        total_h = line_h * len(lines)
        widest = max((tw for line in lines for (_, _, tw) in line), default=0)
        return fnt, lines, line_h, total_h, widest

    size = start_size
    while size >= min_size:
        fnt, lines, line_h, total_h, widest = layout(size)
        if total_h <= max_height and len(lines) <= 4 and widest <= max_width:
            return fnt, lines, line_h, total_h
        size -= 2

    while size > 10:
        fnt, lines, line_h, total_h, widest = layout(size)
        if widest <= max_width:
            return fnt, lines, line_h, total_h
        size -= 2
    fnt, lines, line_h, total_h, _ = layout(size)
    return fnt, lines, line_h, total_h


def wrap_plain(draw, text, fnt, max_width):
    words = text.split(" ")
    lines = []
    cur = []
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


def draw_bg_number(img, number, size=780, opacity=26):
    """Numero gigante desfocado no canto inferior direito. Omitido no slide
    de CTA (cover=True nao chama esta funcao)."""
    layer = Image.new("L", (W, H), 0)
    ldraw = ImageDraw.Draw(layer)
    fnt = font(F_BOLD, size)
    bbox = ldraw.textbbox((0, 0), number, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx, cy = W - 300, H - 260
    ldraw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), number, font=fnt, fill=255)
    mask = layer.point(lambda p: int(p * opacity / 255))
    white_layer = Image.new("RGB", (W, H), WHITE)
    base_rgb = img.convert("RGB")
    base_rgb.paste(white_layer, (0, 0), mask)
    img.paste(base_rgb.convert("RGBA"), (0, 0))


def draw_gradient_bar(img, x, y, w, h):
    grad = diag_gradient(w, h, GRAD_COLORS, angle_horizontal=True)
    img.paste(grad, (x, y))


def draw_base_band(img, band_h=220, blend=0.35):
    """Faixa de gradiente sutil (~35% blend) na base do slide."""
    grad = diag_gradient(W, band_h, GRAD_COLORS, angle_horizontal=True)
    band_bg = Image.new("RGB", (W, band_h), BG)
    blended = Image.blend(band_bg, grad.convert("RGB"), blend)
    img.paste(blended, (0, H - band_h))


def draw_footer(draw, page_label):
    handle_fnt = font(F_BOLD, 30)
    draw.text((MARGIN, H - 90), "@inovashot.cortes", font=handle_fnt, fill=FOOTER_TEXT)
    page_fnt = font(F_MEDIUM, 28)
    bbox = draw.textbbox((0, 0), page_label, font=page_fnt)
    tw = bbox[2] - bbox[0]
    draw.text((W - MARGIN - tw, H - 88), page_label, font=page_fnt, fill=TEXT_BODY)


def draw_polygon_arrow(draw, x, y, size=32):
    color = GRAD_COLORS[1]  # roxo-sinal
    points = [(x, y - size / 2), (x + size, y), (x, y + size / 2)]
    draw.polygon(points, fill=color)


def render_slide(path, kicker, headline, body, page_label, number=None, is_cta=False):
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw = ImageDraw.Draw(img)

    if number and not is_cta:
        draw_bg_number(img, number)
        draw = ImageDraw.Draw(img)

    draw_base_band(img)
    draw = ImageDraw.Draw(img)

    y = 90
    kicker_fnt = font(F_MEDIUM, 30)
    dot_r = 5
    draw.ellipse([MARGIN, y + 10, MARGIN + dot_r * 2, y + 10 + dot_r * 2], fill=GRAD_COLORS[1])
    draw.text((MARGIN + 24, y), kicker, font=kicker_fnt, fill=KICKER_TEXT)

    bar_y = y + 60
    draw_gradient_bar(img, MARGIN, bar_y, 90, 8)
    draw = ImageDraw.Draw(img)

    headline_top = bar_y + 55
    max_headline_h = 420 if is_cta else 340
    hfnt, hlines, line_h, headline_h = fit_headline(draw, headline, CONTENT_W, max_headline_h)

    yy = headline_top
    for line in hlines:
        x = MARGIN
        space_w = draw.textlength(" ", font=hfnt)
        for tok_text, _, tw in line:
            draw.text((x, yy), tok_text, font=hfnt, fill=WHITE)
            x += tw + space_w
        yy += line_h

    if body:
        yy += 40
        body_fnt = font(F_MEDIUM, 44 if not is_cta else 42)
        body_lines = wrap_plain(draw, body, body_fnt, CONTENT_W)
        line_h_b = int(body_fnt.size * 1.3)
        for line in body_lines:
            draw.text((MARGIN, yy), line, font=body_fnt, fill=TEXT_BODY)
            yy += line_h_b

    if is_cta:
        yy += 50
        draw_polygon_arrow(draw, MARGIN, yy + 18, size=36)
        small_fnt = font(F_MEDIUM, 34)
        draw.text((MARGIN + 50, yy), "Link na bio", font=small_fnt, fill=WHITE)

    draw_footer(draw, page_label)
    img.convert("RGB").save(path, "PNG")
    print("saved", path)


def load_slides(content_path):
    with open(content_path, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    # usage: gen-carousel-dark.py [content.json] [out_dir]
    content_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONTENT_PATH
    out_dir = sys.argv[2] if len(sys.argv) > 2 else OUT_DIR
    slides = load_slides(content_path)
    total = len(slides)
    os.makedirs(out_dir, exist_ok=True)
    for i, s in enumerate(slides, start=1):
        is_cta = s.get("cover", False) or i == total
        page_label = f"{i:02d}/{total:02d}"
        render_slide(
            os.path.join(out_dir, f"slide-{i}.png"),
            kicker=s.get("eyebrow", "INOVASHOT \u00b7 CORTES"),
            headline=s["headline"],
            body=s.get("body", ""),
            page_label=page_label,
            number=str(i),
            is_cta=is_cta,
        )
