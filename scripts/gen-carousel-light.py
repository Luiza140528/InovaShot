#!/usr/bin/env python3
"""Gera o carrossel Instagram/Facebook no template claro (creme->lilas).
Spec: .claude/skills/inovashot/SKILL.md, secao "Carrossel - template claro".
"""
import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(SCRIPT_DIR, "fonts")
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "marketing", "carrossel-radar-claude")

W = H = 1080
MARGIN = 72
CONTENT_W = W - 2 * MARGIN

CREAM = (246, 241, 234)
LILAC = (230, 222, 243)
DARK = (26, 26, 24)          # #1A1A18
PURPLE = (168, 85, 247)      # #a855f7
WHITE = (255, 255, 255)
LINE_COLOR = (26, 26, 24, 60)

GRAD_COLORS = [(244, 114, 182), (168, 85, 247), (56, 189, 248)]  # pink -> purple -> blue

def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)

F_EXTRABOLD = "Poppins-ExtraBold.ttf"
F_BOLD = "Poppins-Bold.ttf"
F_SEMIBOLD = "Poppins-SemiBold.ttf"
F_MEDIUM = "Poppins-Medium.ttf"
F_REGULAR = "Poppins-Regular.ttf"
F_MONO_BOLD = "SpaceMono-Bold.ttf"


def diag_gradient(w, h, colors):
    """Diagonal (135deg) linear gradient image, w x h, RGBA."""
    w = max(1, w)
    h = max(1, h)
    n = len(colors) - 1
    base = Image.new("RGB", (w, h))
    px = base.load()
    diag = w + h
    for y in range(h):
        for x in range(0, w, 2):  # step 2 for speed, fill neighbor
            t = (x + y) / diag
            t = min(max(t, 0.0), 1.0)
            seg = min(int(t * n), n - 1)
            local_t = t * n - seg
            c0 = colors[seg]
            c1 = colors[seg + 1]
            r = int(c0[0] + (c1[0] - c0[0]) * local_t)
            g = int(c0[1] + (c1[1] - c0[1]) * local_t)
            b = int(c0[2] + (c1[2] - c0[2]) * local_t)
            px[x, y] = (r, g, b)
            if x + 1 < w:
                px[x + 1, y] = (r, g, b)
    return base.convert("RGBA")


def bg_gradient():
    return diag_gradient(W, H, [CREAM, LILAC])


def draw_spaced_text(draw, xy, text, fnt, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w = draw.textlength(ch, font=fnt)
        x += w + tracking
    return x - xy[0]


def spaced_text_width(draw, text, fnt, tracking):
    total = 0
    for ch in text:
        total += draw.textlength(ch, font=fnt) + tracking
    return total - tracking if text else 0


def paste_gradient_text(img, draw, xy, text, fnt, colors):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 4
    mask_img = Image.new("L", (tw + pad * 2, th + pad * 2), 0)
    mdraw = ImageDraw.Draw(mask_img)
    mdraw.text((pad - bbox[0], pad - bbox[1]), text, font=fnt, fill=255)
    grad = diag_gradient(mask_img.width, mask_img.height, colors)
    img.paste(grad, (int(xy[0]) - pad, int(xy[1] + bbox[1]) - pad), mask_img)


def wrap_tokens(draw, tokens, fnt, max_width):
    """tokens: list of (text, is_gradient). Greedy wrap, tokens are atomic units."""
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


def headline_tokens(text, grad_phrase):
    if grad_phrase and grad_phrase in text:
        before, after = text.split(grad_phrase, 1)
        toks = [(w, False) for w in before.strip().split(" ") if w]
        toks.append((grad_phrase, True))
        toks += [(w, False) for w in after.strip().split(" ") if w]
        return toks
    return [(w, False) for w in text.split(" ") if w]


def fit_headline(draw, text, grad_phrase, max_width, max_height, start_size=64, min_size=38):
    size = start_size
    while size >= min_size:
        fnt = font(F_EXTRABOLD, size)
        tokens = headline_tokens(text, grad_phrase)
        lines = wrap_tokens(draw, tokens, fnt, max_width)
        line_h = int(size * 1.22)
        total_h = line_h * len(lines)
        if total_h <= max_height and len(lines) <= 4:
            return fnt, lines, line_h, total_h
        size -= 2
    fnt = font(F_EXTRABOLD, min_size)
    tokens = headline_tokens(text, grad_phrase)
    lines = wrap_tokens(draw, tokens, fnt, max_width)
    line_h = int(min_size * 1.22)
    return fnt, lines, line_h, line_h * len(lines)


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


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_logo(img, draw, x, y):
    mark_size = 60
    grad = diag_gradient(mark_size, mark_size, GRAD_COLORS)
    mask = Image.new("L", (mark_size, mark_size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, mark_size - 1, mark_size - 1], radius=16, fill=255)
    img.paste(grad, (x, y), mask)
    ifnt = font(F_EXTRABOLD, 34)
    ibbox = draw.textbbox((0, 0), "I", font=ifnt)
    iw = ibbox[2] - ibbox[0]
    ih = ibbox[3] - ibbox[1]
    draw.text((x + mark_size / 2 - iw / 2 - ibbox[0], y + mark_size / 2 - ih / 2 - ibbox[1]), "I", font=ifnt, fill=WHITE)

    word_fnt = font(F_EXTRABOLD, 34)
    wbbox = draw.textbbox((0, 0), "InovaShot", font=word_fnt)
    wh = wbbox[3] - wbbox[1]
    wy = y + mark_size / 2 - wh / 2 - wbbox[1]
    draw.text((x + mark_size + 16, wy), "InovaShot", font=word_fnt, fill=DARK)
    return mark_size


def draw_footer(img, draw):
    line_y = 946
    # img.convert("RGB") at save time discards alpha without compositing, so a
    # translucent fill drawn straight on img would render fully opaque. Blend
    # it against the actual background on a separate layer first.
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).line([(MARGIN, line_y), (W - MARGIN, line_y)], fill=(26, 26, 24, 70), width=2)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay), (0, 0))

    text_y = line_y + 26
    mono_fnt = font(F_MONO_BOLD, 20)
    handle = "SIGA @INOVASHOT.CORTES"
    draw_spaced_text(draw, (MARGIN, text_y), handle, mono_fnt, PURPLE, tracking=1.5)

    pill_fnt = font(F_BOLD, 18)
    pill_text = "O INOVASHOT"
    tw = draw.textlength(pill_text, font=pill_fnt)
    pad_x = 22
    pill_h = 40
    pill_w = tw + pad_x * 2
    pill_x1 = W - MARGIN
    pill_x0 = pill_x1 - pill_w
    pill_y0 = text_y - 8
    pill_y1 = pill_y0 + pill_h

    grad = diag_gradient(int(pill_w), pill_h, GRAD_COLORS)
    mask = Image.new("L", (int(pill_w), pill_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, int(pill_w) - 1, pill_h - 1], radius=pill_h // 2, fill=255)
    img.paste(grad, (int(pill_x0), int(pill_y0)), mask)

    tbbox = draw.textbbox((0, 0), pill_text, font=pill_fnt)
    th = tbbox[3] - tbbox[1]
    tx = pill_x0 + pad_x
    ty = pill_y0 + pill_h / 2 - th / 2 - tbbox[1]
    draw.text((tx, ty), pill_text, font=pill_fnt, fill=DARK)


def render_slide(path, eyebrow, headline, grad_phrase, body, cover=False):
    img = bg_gradient()
    draw = ImageDraw.Draw(img)

    footer_top = 946
    top_zone_top = 64
    top_zone_bottom = footer_top - 40

    # --- pass 1: measure block height (logo + eyebrow + headline + chip) ---
    logo_h = 60
    eb_fnt = font(F_MONO_BOLD, 24)
    eb_h = 24

    headline_size = 68 if cover else 58
    max_headline_h = 520
    hfnt, hlines, line_h, headline_h = fit_headline(
        draw, headline, grad_phrase, CONTENT_W, max_headline_h, start_size=headline_size
    )

    chip_h = 0
    pad = 36
    body_fnt = font(F_REGULAR, 29)
    body_lines = []
    line_h_b = 40
    if body:
        body_lines = wrap_plain(draw, body, body_fnt, CONTENT_W - pad * 2)
        chip_h = pad * 2 + len(body_lines) * line_h_b

    gap_logo_eb = 44
    gap_eb_headline = 30
    gap_headline_chip = 36

    block_h = logo_h + gap_logo_eb + eb_h + gap_eb_headline + headline_h
    if body:
        block_h += gap_headline_chip + chip_h

    avail_h = top_zone_bottom - top_zone_top
    y = top_zone_top + max(0, (avail_h - block_h) // 2)

    # --- pass 2: draw ---
    mark_h = draw_logo(img, draw, MARGIN, y)
    y += mark_h + gap_logo_eb

    draw_spaced_text(draw, (MARGIN, y), eyebrow, eb_fnt, PURPLE, tracking=2)
    y += eb_h + gap_eb_headline

    for line in hlines:
        x = MARGIN
        space_w = draw.textlength(" ", font=hfnt)
        for tok_text, is_grad, tw in line:
            if is_grad:
                paste_gradient_text(img, draw, (x, y), tok_text, hfnt, GRAD_COLORS)
            else:
                draw.text((x, y), tok_text, font=hfnt, fill=DARK)
            x += tw + space_w
        y += line_h

    if body:
        y += gap_headline_chip
        chip_top = y
        chip_bottom = chip_top + chip_h
        rounded_rect(draw, [MARGIN, chip_top, W - MARGIN, chip_bottom], 24, DARK)
        ty = chip_top + pad
        for line in body_lines:
            draw.text((MARGIN + pad, ty), line, font=body_fnt, fill=WHITE)
            ty += line_h_b

    draw_footer(img, draw)
    img.convert("RGB").save(path, "PNG")
    print("saved", path)


slides = [
    dict(
        eyebrow="RADAR CLAUDE",
        headline="O criador do Claude Code gravou 28 minutos que valem mais que curso pago",
        grad_phrase="curso pago",
        body=None,
        cover=True,
    ),
    dict(
        eyebrow="PONTO 1",
        headline="Cada erro vira regra permanente",
        grad_phrase="regra permanente",
        body="Toda vez que o Claude erra numa tarefa, ele escreve a correção no arquivo CLAUDE.md. Da próxima vez, o Claude já sabe não repetir aquele erro.",
    ),
    dict(
        eyebrow="PONTO 2",
        headline="Várias sessões rodando ao mesmo tempo",
        grad_phrase="ao mesmo tempo",
        body="Em vez de esperar uma tarefa terminar pra começar a próxima, ele mantém várias sessões do Claude abertas em paralelo, cada uma com seu próprio contexto.",
    ),
    dict(
        eyebrow="PONTO 3",
        headline="Dar ao Claude um jeito de conferir o próprio trabalho",
        grad_phrase="próprio trabalho",
        body="Essa é a regra que ele mais repete: quando o Claude consegue testar o que fez sozinho, o resultado melhora muito.",
    ),
    dict(
        eyebrow="PONTO 4",
        headline="Tarefa repetida vira atalho automático",
        grad_phrase="atalho automático",
        body="Toda ação que ele faz mais de uma vez por dia, ele transforma em comando pronto — economiza tempo todos os dias depois.",
    ),
    dict(
        eyebrow="RESUMO",
        headline="Não é sobre prompt mágico. É sobre montar um sistema",
        grad_phrase="montar um sistema",
        body="Siga @inovashot.cortes pra mais achados reais sobre Claude.",
    ),
]

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for i, s in enumerate(slides, start=1):
        render_slide(os.path.join(OUT_DIR, f"slide-{i}.png"), s["eyebrow"], s["headline"], s["grad_phrase"], s["body"], cover=s.get("cover", False))
