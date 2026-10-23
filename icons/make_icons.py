#!/usr/bin/env python3
"""Generate the PWA icons from code (no external tools needed).

Design is defined in a 512x512 canvas space and rasterised with analytic
anti-aliasing (signed distance functions), then written as PNG using zlib.

    python3 icons/make_icons.py
"""

import math
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent

SKY_TOP = (67, 184, 196)
SKY_BOTTOM = (168, 230, 200)
BIRD = (247, 201, 72)
BIRD_EDGE = (201, 141, 27)
BELLY = (255, 226, 122)
WING = (255, 243, 196)
EYE = (255, 255, 255)
PUPIL = (32, 38, 43)
BEAK = (242, 131, 46)
BEAK_EDGE = (196, 97, 26)


def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x


def cov(d):
    """Coverage of a shape from a signed distance (negative = inside)."""
    if d <= -0.5:
        return 1.0
    if d >= 0.5:
        return 0.0
    return 0.5 - d


def circle(x, y, cx, cy, r):
    return math.hypot(x - cx, y - cy) - r


def ellipse(x, y, cx, cy, rx, ry, angle=0.0):
    dx, dy = x - cx, y - cy
    if angle:
        ca, sa = math.cos(angle), math.sin(angle)
        dx, dy = dx * ca + dy * sa, -dx * sa + dy * ca
    q = math.hypot(dx / rx, dy / ry)
    return (q - 1.0) * min(rx, ry)


def triangle(x, y, pts):
    """Half-plane signed distance for a convex polygon (clockwise or ccw)."""
    d = -1e9
    n = len(pts)
    # centroid for consistent winding
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    for i in range(n):
        ax, ay = pts[i]
        bx, by = pts[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        # normal pointing away from the centroid
        nx, ny = ey, -ex
        mx, my = (ax + bx) / 2 - cx, (ay + by) / 2 - cy
        if nx * mx + ny * my < 0:
            nx, ny = -nx, -ny
        ln = math.hypot(nx, ny) or 1.0
        nx, ny = nx / ln, ny / ln
        d = max(d, (x - ax) * nx + (y - ay) * ny)
    return d


def rounded_rect(x, y, cx, cy, hw, hh, r):
    dx = abs(x - cx) - (hw - r)
    dy = abs(y - cy) - (hh - r)
    ox, oy = max(dx, 0.0), max(dy, 0.0)
    return math.hypot(ox, oy) + min(max(dx, dy), 0.0) - r


def over(dst, rgb, a):
    """Alpha-composite rgb over dst (both RGBA floats 0..1)."""
    if a <= 0:
        return dst
    na = a + dst[3] * (1 - a)
    if na <= 0:
        return (0.0, 0.0, 0.0, 0.0)
    r = (rgb[0] * a + dst[0] * dst[3] * (1 - a)) / na
    g = (rgb[1] * a + dst[1] * dst[3] * (1 - a)) / na
    b = (rgb[2] * a + dst[2] * dst[3] * (1 - a)) / na
    return (r, g, b, na)


def render(size, content_scale, rounded):
    """Render one icon. Coordinates live in a 512x512 design space."""
    sc = size / 512.0
    k = content_scale
    rows = []
    wing_angle = math.radians(-22)
    beak_pts = [(290, 244), (446, 276), (290, 308)]
    beak_big = [(290 + (px - 342) * 1.10, 276 + (py - 276) * 1.13) for px, py in beak_pts]

    for py in range(size):
        row = bytearray()
        for px in range(size):
            # design-space sample point
            u = (px + 0.5) / sc
            v = (py + 0.5) / sc

            # content (bird) coordinates, optionally shrunk toward the centre
            cu = (u - 256.0) / k + 256.0
            cv = (v - 256.0) / k + 256.0
            kd = k  # distances in content space -> design space

            # --- background ---
            pix = (0.0, 0.0, 0.0, 0.0)
            bg_a = 1.0
            if rounded:
                bg_a = cov(rounded_rect(u, v, 256, 256, 256, 256, 96))
            if bg_a > 0:
                t = clamp((v - 40) / 432.0)
                bg = (
                    (SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * t) / 255.0,
                    (SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * t) / 255.0,
                    (SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * t) / 255.0,
                    1.0,
                )
                pix = over(pix, bg[:3], bg_a)

            # --- beak (drawn first, so the head covers its base) ---
            pix = over(pix, tuple(c / 255.0 for c in BEAK_EDGE),
                       cov(triangle(cu, cv, beak_big) * kd))
            pix = over(pix, tuple(c / 255.0 for c in BEAK),
                       cov(triangle(cu, cv, beak_pts) * kd))

            # --- bird ---
            body_r = 112.0
            pix = over(pix, tuple(c / 255.0 for c in BIRD_EDGE),
                       cov(circle(cu, cv, 238, 262, body_r + 5) * kd))
            pix = over(pix, tuple(c / 255.0 for c in BIRD),
                       cov(circle(cu, cv, 238, 262, body_r) * kd))
            pix = over(pix, tuple(c / 255.0 for c in BELLY),
                       cov(circle(cu, cv, 232, 292, 74) * kd))

            # wing: outline then fill
            pix = over(pix, tuple(c / 255.0 for c in BIRD_EDGE),
                       cov(ellipse(cu, cv, 192, 296, 56, 40, wing_angle) * kd))
            pix = over(pix, tuple(c / 255.0 for c in WING),
                       cov(ellipse(cu, cv, 192, 296, 50, 34, wing_angle) * kd))

            # eye
            pix = over(pix, tuple(c / 255.0 for c in EYE),
                       cov(circle(cu, cv, 282, 214, 44) * kd))
            pix = over(pix, tuple(c / 255.0 for c in PUPIL),
                       cov(circle(cu, cv, 294, 214, 21) * kd))

            row += bytes((
                int(clamp(pix[0]) * 255 + 0.5),
                int(clamp(pix[1]) * 255 + 0.5),
                int(clamp(pix[2]) * 255 + 0.5),
                int(clamp(pix[3]) * 255 + 0.5),
            ))
        rows.append(bytes(row))
    return rows


def write_png(path, size, rows):
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    path.write_bytes(png)
    print(f"{path.name}: {size}x{size}, {len(png)} bytes")


def main():
    targets = [
        ("icon-192.png", 192, 0.94, True),
        ("icon-512.png", 512, 0.94, True),
        ("maskable-512.png", 512, 0.72, False),
        ("apple-touch-icon.png", 180, 0.88, False),
    ]
    for name, size, scale, rounded in targets:
        write_png(HERE / name, size, render(size, scale, rounded))


if __name__ == "__main__":
    main()
