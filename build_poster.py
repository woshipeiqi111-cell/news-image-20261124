#!/usr/bin/env python3
"""Build the news-image-20261124 front page (1024x1024 PNG).

Composes the six generated illustrations with real rendered text, so every
word on the page is crisp and exactly as written. Run from the repo root:
    python3 build_poster.py
Writes entry.png next to this script. Deterministic: same inputs, same bytes
(PNG encoder is deterministic; no timestamps are embedded).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 22, 22)
GREY = (92, 88, 80)
RED = (166, 30, 30)
RULE = (22, 22, 22)
CARD = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt, max_w, max_h, start_size, path, min_size=12):
    """Draw wrapped text, shrinking the font until it fits max_h. Returns lines."""
    size = start_size
    while size >= min_size:
        f = font(path, size)
        lines = wrap(draw, text, f, max_w)
        total = sum(draw.textbbox((0, 0), l, font=f)[3] for l in lines) + int(size * 0.25) * (len(lines) - 1)
        if total <= max_h:
            return f, lines
        size -= 1
    f = font(path, min_size)
    return f, wrap(draw, text, f, max_w)


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def cover(im, w, h):
    """Center-crop an image to fill w x h."""
    iw, ih = im.size
    s = max(w / iw, h / ih)
    im = im.resize((round(iw * s), round(ih * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def img(name):
    for f in sorted(os.listdir(ASSETS)):
        if f.startswith(name) and f.endswith(".png"):
            return Image.open(os.path.join(ASSETS, f)).convert("RGB")
    raise FileNotFoundError(name)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    MX = 36  # side margin

    # ---- masthead ----
    d.text((MX, 20), "THE WORLD IN ONE DAY", font=font(SERIF, 58), fill=INK)
    d.line([(MX, 96), (W - MX, 96)], fill=RULE, width=3)
    d.text((MX, 106), "TUESDAY, 24 NOVEMBER 2026", font=font(SANS_B, 32), fill=RED)
    d.text((W - MX - d.textlength("SIX STORIES THAT DEFINED THE DAY", font=font(SANS_B, 19)), 114),
           "SIX STORIES THAT DEFINED THE DAY", font=font(SANS_B, 19), fill=GREY)
    d.line([(MX, 152), (W - MX, 152)], fill=RULE, width=2)

    # ---- lead story: Nvidia ----
    ly = 164
    lead_img = cover(img("media-generation-nvidia-chip"), 440, 220)
    page.paste(lead_img, (MX, ly))
    d.rectangle([MX, ly, MX + 440, ly + 220], outline=INK, width=2)
    tx = MX + 460
    d.text((tx, ly + 2), "TECH  ·  MARKETS", font=font(SANS_B, 19), fill=RED)
    d.text((tx, ly + 30), "Huang is back", font=font(SERIF, 44), fill=INK)
    d.text((tx, ly + 78), "at Nvidia", font=font(SERIF, 44), fill=INK)
    body = ("Nvidia's board reinstates Jensen Huang as chief "
            "executive after pressure from President Trump. "
            "Shares jump 31% in a day, their best since 2003, "
            "and the S&P 500 gains 4.7%.")
    draw_wrapped(d, tx, ly + 132, body, font(SANS, 20), W - MX - tx, INK)
    d.line([(MX, ly + 236), (W - MX, ly + 236)], fill=RULE, width=2)

    # ---- grid: 3 cols x 2 rows ----
    gy = 412
    gw = 304
    gap = 20
    gh = 246
    stories = [
        ("WAR  ·  LIBYA", "Ukraine sinks Russian warship off Libya",
         "Seven sea drones sink the corvette Merkury in Benghazi harbour; a cargo ship carrying weapons is also hit, Kyiv says.",
         "media-generation-merkury-ship"),
        ("MIDDLE EAST", "Iran claims three tankers hit mines in Hormuz",
         "Tehran says the tankers caught fire after striking mines; the claim is unverified and the US has not responded.",
         "media-generation-hormuz-tanker"),
        ("SPACE  ·  CHINA", "China names Shenzhou-24 crew",
         "Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali — the first foreign astronaut to visit Tiangong. Launch 25 Nov.",
         "media-generation-shenzhou-rocket"),
        ("GAZA", "Israeli strike kills Hamas security chief",
         "Naeem Abu Nahel and six others are killed in Gaza City, medics and police say, as strikes continue across the territory.",
         "media-generation-gaza-city"),
        ("TECH  ·  LAW", "Two US states sue Musk over Grok images",
         "Virginia and Oregon accuse SpaceX of stripping safeguards from Grok's image tool, spreading sexualised deepfakes.",
         "media-generation-grok-court"),
        (None, None, None, None),  # markets panel
    ]
    for i, (kicker, head, body, asset) in enumerate(stories):
        col = i % 3
        row = i // 3
        x = MX + col * (gw + gap)
        y = gy + row * (gh + gap)
        if asset is None:
            # markets panel
            d.rectangle([x, y, x + gw, y + gh], fill=(22, 22, 22))
            d.text((x + 16, y + 14), "MARKETS", font=font(SANS_B, 18), fill=(255, 255, 255))
            d.text((x + 16, y + 44), "S&P 500", font=font(SANS, 22), fill=(200, 200, 200))
            d.text((x + 16, y + 72), "+4.7%", font=font(SANS_B, 40), fill=(120, 220, 130))
            d.text((x + 16, y + 126), "Nasdaq", font=font(SANS, 22), fill=(200, 200, 200))
            d.text((x + 16, y + 154), "+6.4%", font=font(SANS_B, 40), fill=(120, 220, 130))
            d.text((x + 16, y + 206), "Nvidia  +31%", font=font(SANS_B, 22), fill=(255, 255, 255))
            continue
        im = cover(img(asset), gw, 110)
        page.paste(im, (x, y))
        d.rectangle([x, y, x + gw, y + 110], outline=INK, width=1)
        d.text((x, y + 118), kicker, font=font(SANS_B, 15), fill=RED)
        f, lines = fit_text(d, head, font(SERIF, 24), gw, 56, 24, SERIF)
        yy = y + 138
        for ln in lines:
            d.text((x, yy), ln, font=f, fill=INK)
            yy += int(f.size * 1.12)
        draw_wrapped(d, x, yy + 2, body, font(SANS, 15), gw, GREY, leading=19)

    # ---- footer ----
    fy = gy + 2 * gh + gap + 8
    d.line([(MX, fy), (W - MX, fy)], fill=RULE, width=2)
    also = ("ALSO TODAY  —  Zaporizhzhia strike kills 2, wounds 40  ·  "
            "EU 22nd sanctions package on Russia  ·  "
            "Spain amnesties Puigdemont")
    draw_wrapped(d, MX, fy + 10, also, font(SANS, 16), W - 2 * MX, INK, leading=21)
    d.text((MX, H - 30), "Sources: Reuters, AP, WSJ, Al Jazeera, Xinhua, SCMP — reported 24 November 2026",
           font=font(SANS, 14), fill=GREY)

    page.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote", os.path.join(HERE, "entry.png"),
          os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")


if __name__ == "__main__":
    main()
