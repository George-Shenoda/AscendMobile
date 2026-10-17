#!/usr/bin/env python3
"""Generate Ascend app icons: SVG by hand, PNGs via PIL."""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "www", "icons")
os.makedirs(OUT, exist_ok=True)

BG = (9, 13, 22)          # #090d16
EMERALD = (16, 185, 129)  # #10b981
TEAL = (45, 212, 191)     # #2dd4bf
SLATE = (51, 65, 85)      # #334155 accent arcs


def draw_icon(size, safe=1.0, opaque=True):
    """Draw the icon at `size`px. safe=0.8 keeps content in maskable zone.
    opaque=False renders on a transparent canvas (for adaptive-icon foregrounds)."""
    img = Image.new("RGBA", (size, size), BG + (255,) if opaque else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    u = size / 512.0
    pad = (1 - safe) / 2 * size

    # Rising bars ( Keystone habits / growth ) emerald -> teal
    bars = [
        (0.18, 0.62, EMERALD),
        (0.40, 0.46, (20, 196, 148)),
        (0.62, 0.30, TEAL),
    ]
    bar_w = 0.14 * size * safe
    base_y = 0.80 * size * safe + pad
    for i, (fx, fy, color) in enumerate(bars):
        x0 = pad + fx * size * safe + i * bar_w * 0.5
        y0 = pad + fy * size * safe + (1 - safe) * 0
        # stagger horizontally: left bar, middle, right
        x0 = pad + (0.14 + i * 0.26) * size * safe
        y0 = base_y - (0.14 + i * 0.14) * size * safe
        d.rounded_rectangle([x0, y0, x0 + bar_w, base_y],
                            radius=max(2, int(8 * u)), fill=color)

    # Ascending arrow above the bars
    ax0 = pad + 0.22 * size * safe
    ay0 = pad + 0.44 * size * safe
    ax1 = pad + 0.78 * size * safe
    ay1 = pad + 0.16 * size * safe
    lw = max(3, int(22 * u * safe))
    d.line([(ax0, ay0), (ax1, ay1)], fill=EMERALD, width=lw)
    head = max(4, int(70 * u * safe))
    d.polygon([(ax1 + lw * 0.2, ay1 - head * 0.35),
               (ax1 + head * 0.75, ay1 - head * 0.2 + head * 0.1),
               (ax1 - head * 0.15, ay1 + head * 0.75)], fill=EMERALD)
    return img


# Standard icons (content may extend to edges)
for s in (48, 72, 96, 144, 192, 256, 512):
    draw_icon(s, safe=1.0).save(os.path.join(OUT, f"icon-{s}.png"))

# Maskable icon: 80% safe zone (background fills the whole tile)
draw_icon(512, safe=0.62).save(os.path.join(OUT, "icon-maskable-512.png"))

svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#090d16"/>
  <rect x="72" y="326" width="72" height="86" rx="12" fill="#10b981"/>
  <rect x="200" y="254" width="72" height="158" rx="12" fill="#14c494"/>
  <rect x="328" y="172" width="72" height="240" rx="12" fill="#2dd4bf"/>
  <polyline points="112,226 240,172 364,120" fill="none" stroke="#10b981"
    stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>
  <polygon points="400,86 438,104 402,140" fill="#10b981"/>
</svg>
"""
with open(os.path.join(OUT, "icon.svg"), "w") as f:
    f.write(svg)

# Android adaptive-icon foregrounds (transparent, content in center 66%)
RES = os.path.join(os.path.dirname(__file__), "..", "android", "app", "src", "main", "res")
FG_SIZES = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}
LAUNCHER_SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for density, s in FG_SIZES.items():
    draw_icon(s, safe=0.66, opaque=False).save(
        os.path.join(RES, f"mipmap-{density}", "ic_launcher_foreground.png"))
for density, s in LAUNCHER_SIZES.items():
    draw_icon(s, safe=1.0).save(os.path.join(RES, f"mipmap-{density}", "ic_launcher.png"))
    draw_icon(s, safe=1.0).save(os.path.join(RES, f"mipmap-{density}", "ic_launcher_round.png"))

print("icons written:", sorted(os.listdir(OUT)))
print("android mipmaps updated:", ", ".join(FG_SIZES))