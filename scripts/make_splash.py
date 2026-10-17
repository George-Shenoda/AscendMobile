#!/usr/bin/env python3
"""Generate branded dark splash screens for every Android drawable density."""
import os
from PIL import Image, ImageDraw

RES = os.path.join(os.path.dirname(__file__), "..", "android", "app", "src", "main", "res")
BG = (9, 13, 22)  # #090d16

# density -> (portrait size, landscape size) taken from template files
SIZES = {
    "mdpi": ((320, 480), (480, 320)),
    "hdpi": ((480, 800), (800, 480)),
    "xhdpi": ((720, 1280), (1280, 720)),
    "xxhdpi": ((960, 1600), (1600, 960)),
    "xxxhdpi": ((1280, 1920), (1920, 1280)),
}

ICON = (16, 185, 129)      # emerald bars
ICON2 = (45, 212, 191)     # teal
ARROW = (16, 185, 129)


def draw_logo(img):
    """Center a scaled version of the Ascend mark on the splash."""
    d = ImageDraw.Draw(img)
    w, h = img.size
    # logo is ~40% of the smaller dimension, vertically centered
    unit = min(w, h) * 0.34
    cx, cy = w / 2, h / 2

    bars = [(-0.34, 0.10), (0.0, 0.24), (0.34, 0.40)]  # (x offset, height factor)
    bar_w = unit * 0.16
    base_y = cy + unit * 0.42
    colors = [ICON, (20, 196, 148), ICON2]
    for (xo, hf), color in zip(bars, colors):
        x0 = cx + xo * unit - bar_w / 2
        y0 = base_y - hf * unit * 2.1
        d.rounded_rectangle([x0, y0, x0 + bar_w, base_y], radius=max(2, int(bar_w * 0.18)),
                            fill=color)

    # rising arrow
    lw = max(3, int(unit * 0.10))
    ax0, ay0 = cx - unit * 0.46, cy - unit * 0.34
    ax1, ay1 = cx + unit * 0.44, cy - unit * 0.86
    d.line([(ax0, ay0), (ax1, ay1)], fill=ARROW, width=lw)
    hl = unit * 0.36
    d.polygon([(ax1 + lw * 0.3, ay1 - hl * 0.15),
               (ax1 + hl * 0.55, ay1 + hl * 0.45),
               (ax1 - hl * 0.35, ay1 + hl * 0.55)], fill=ARROW)


for density, (port, land) in SIZES.items():
    for folder, size in ((f"drawable-port-{density}", port),
                         (f"drawable-land-{density}", land)):
        img = Image.new("RGB", size, BG)
        draw_logo(img)
        path = os.path.join(RES, folder, "splash.png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        img.save(path)

# generic drawable/splash.png (template default 480x320)
img = Image.new("RGB", (480, 320), BG)
draw_logo(img)
img.save(os.path.join(RES, "drawable", "splash.png"))

print("splash screens written")