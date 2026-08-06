#!/usr/bin/env python3
"""
Regenerate every logo asset for Chatham Epoxy Flooring.

    python tools/make-logo.py

DIFFERENT FROM EVERY OTHER CITY IN THIS NETWORK. Grimsby's master held two
lockups side by side and its script split them left/right. Sarnia and Welland
shipped a supplied circular badge and their scripts cropped it vertically.

There is no supplied Chatham artwork, so this script DRAWS the lockup instead
of cropping one. Everything is vector-ish: filled polygons and text rendered
at 8x and downsampled, so the 16px favicon stays clean.

The mark is three stacked parallelograms reading as a coated slab receding in
perspective - the wet edge of a pour. The top bar is amber, the lower two are
graphite, which is the whole brand palette in one shape and still legible as
two tones at 16px. Do NOT add detail to the mark: anything finer than these
three bars turns to mush at favicon sizes.

Outputs (filenames must not change - build.py references them directly)
    icon-{16,32,48,64,96,180,192,512}.png   header logo + favicons
    favicon.ico                             multi-resolution, legacy browsers
    logo.png                                512px icon, for schema.org
    wordmark-{300,600}.png                  dark lockup, for light backgrounds
    wordmark-light-{300,600}.png            reversed lockup, for the footer

The wordmark is 300x82 (3.66:1). build.py hardcodes those numbers on the
footer <img> so the box is reserved before the image loads. If this ratio
changes, change build.py to match or the footer will shift on load.
"""
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG  = os.path.join(ROOT, "site", "images")

SS = 8  # supersample factor - draw big, downsample with LANCZOS

GRAPHITE = (34, 38, 44, 255)
SLATE    = (74, 82, 94, 255)
AMBER    = (216, 150, 20, 255)
WHITE    = (255, 255, 255, 255)
PALE     = (226, 230, 236, 255)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:\\Windows\\Fonts\\arialbd.ttf",
]


def font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def bars(d, x, y, w, h, colours):
    """Three stacked parallelograms, each narrower than the one below, slanted
    right. Reads as a slab in perspective at large sizes and as a two-tone
    stack at 16px."""
    n = len(colours)
    gap = h * 0.13
    bh = (h - gap * (n - 1)) / n
    skew = w * 0.20
    for i, col in enumerate(colours):
        top = y + i * (bh + gap)
        inset = (n - 1 - i) * w * 0.13   # top bar is the narrowest
        left = x + inset
        right = x + w - inset * 0.15
        d.polygon([(left + skew, top),
                   (right, top),
                   (right - skew, top + bh),
                   (left, top + bh)], fill=col)


def make_icon(side, on_dark=False):
    S = side * SS
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = int(S * 0.22)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=r,
                        fill=WHITE if on_dark else GRAPHITE)
    pad = S * 0.20
    bars(d, pad, S * 0.26, S - pad * 2, S * 0.48,
         [AMBER, PALE if not on_dark else SLATE,
          (150, 158, 170, 255) if not on_dark else GRAPHITE])
    return im.resize((side, side), Image.LANCZOS)


def make_wordmark(w, light=False):
    """CHATHAM over a rule over EPOXY FLOORING, with the mark on the left."""
    h = round(w * 82 / 300)
    W, H = w * SS, h * SS
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    ink   = WHITE if light else GRAPHITE
    quiet = PALE if light else (90, 99, 112, 255)

    mark = int(H * 0.86)
    my = (H - mark) // 2
    d.rounded_rectangle([0, my, mark, my + mark], radius=int(mark * 0.22),
                        fill=WHITE if light else GRAPHITE)
    pad = mark * 0.20
    bars(d, pad, my + mark * 0.26, mark - pad * 2, mark * 0.48,
         [AMBER,
          SLATE if light else PALE,
          GRAPHITE if light else (150, 158, 170, 255)])

    tx = mark + int(W * 0.045)

    f1 = font(int(H * 0.40))
    d.text((tx, H * 0.10), "CHATHAM", font=f1, fill=ink)
    b1 = d.textbbox((tx, H * 0.10), "CHATHAM", font=f1)

    ry = b1[3] + H * 0.075
    d.rectangle([tx, ry, b1[2], ry + max(2, H * 0.022)], fill=AMBER)

    f2 = font(int(H * 0.185))
    tracked = " ".join("EPOXY FLOORING")
    d.text((tx, ry + H * 0.115), tracked, font=f2, fill=quiet)

    return im.resize((w, h), Image.LANCZOS)


def save_png(img, path):
    img.save(path, optimize=True)


def main():
    os.makedirs(IMG, exist_ok=True)

    for size in (512, 192, 180, 96, 64, 48, 32, 16):
        save_png(make_icon(size), os.path.join(IMG, "icon-%d.png" % size))
        print("  icon-%d.png" % size)

    save_png(make_icon(512), os.path.join(IMG, "logo.png"))
    make_icon(256).save(os.path.join(IMG, "favicon.ico"),
                        sizes=[(16, 16), (32, 32), (48, 48),
                               (64, 64), (128, 128), (256, 256)])
    print("  favicon.ico, logo.png")

    for w in (600, 300):
        save_png(make_wordmark(w), os.path.join(IMG, "wordmark-%d.png" % w))
        save_png(make_wordmark(w, light=True),
                 os.path.join(IMG, "wordmark-light-%d.png" % w))
        print("  wordmark-%d.png, wordmark-light-%d.png" % (w, w))

    print("\nDone. Run 'python build.py' to refresh the cache fingerprints.")


if __name__ == "__main__":
    main()
