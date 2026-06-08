"""Generate an animated WebP for the ClinOmics AI hero section.

Visualizes:
  • Central glowing droplet (liquid biopsy sample)
  • Pulsing protein structure inside the droplet (proteomics)
  • Orbiting data particles flowing inward (sample → analysis)
  • AI neural-network constellation forming around it (machine learning)
  • Three nodes that pulse brighter in sequence (identifying the right patients)

Output: images/hero-animation.webp — a seamless 4-second loop at 30fps.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 800
N_FRAMES = 60        # 60 frames @ 33.3ms = 2s loop, looks smooth
LOOP_MS = 4000       # total loop duration in ms
FRAME_MS = LOOP_MS // N_FRAMES

# Brand palette (from logo)
INDIGO    = (67, 102, 216)
SKY       = (80, 169, 237)
PALE_SKY  = (159, 211, 245)
DEEP_BG_1 = (12, 18, 50)     # top-left of background
DEEP_BG_2 = (22, 30, 90)     # bottom-right of background
WHITE     = (255, 255, 255)


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))


def smooth_pulse(t, phase=0):
    """Smooth sinusoidal pulse 0 → 1 → 0, t∈[0,1], with phase offset."""
    return 0.5 + 0.5 * math.sin(2 * math.pi * (t + phase) - math.pi / 2)


def make_background():
    """Diagonal indigo gradient background, generated once."""
    img = Image.new("RGB", (W, H), DEEP_BG_1)
    pixels = img.load()
    for y in range(H):
        for x in range(W):
            t = (x + y) / (W + H)
            r = clamp(lerp(DEEP_BG_1[0], DEEP_BG_2[0], t))
            g = clamp(lerp(DEEP_BG_1[1], DEEP_BG_2[1], t))
            b = clamp(lerp(DEEP_BG_1[2], DEEP_BG_2[2], t))
            pixels[x, y] = (r, g, b)
    return img


def add_glow(img, draw_callable, blur_radius=18, opacity=0.6):
    """Render something onto a transparent overlay, blur it, composite as glow."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    draw_callable(gd)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    # scale opacity
    alpha = glow.split()[3]
    alpha = alpha.point(lambda a: int(a * opacity))
    glow.putalpha(alpha)
    img.alpha_composite(glow)


def draw_frame(bg, t):
    """Draw a single frame at time t∈[0,1]. Returns RGBA image."""
    img = bg.convert("RGBA").copy()

    # === Central droplet (right side, leaves left clean for text) ===
    cx, cy = int(W * 0.70), int(H * 0.50)
    base_r = 110
    droplet_pulse = math.sin(2 * math.pi * t) * 8
    r = base_r + droplet_pulse

    # Outer glow halo
    def draw_halo(gd):
        for i in range(6):
            radius = r + 30 + i * 14
            opacity = max(0, 60 - i * 10)
            gd.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                       fill=(SKY[0], SKY[1], SKY[2], opacity))
    add_glow(img, draw_halo, blur_radius=30, opacity=0.7)

    # Droplet body (translucent)
    drop_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(drop_layer)
    dd.ellipse([cx - r, cy - r, cx + r, cy + r],
               fill=(SKY[0], SKY[1], SKY[2], 75),
               outline=(PALE_SKY[0], PALE_SKY[1], PALE_SKY[2], 200), width=2)
    # Inner highlight (gives a glassy 3D feel)
    hr = r * 0.55
    hx, hy = cx - r * 0.30, cy - r * 0.30
    dd.ellipse([hx - hr * 0.4, hy - hr * 0.3, hx + hr * 0.4, hy + hr * 0.3],
               fill=(255, 255, 255, 60))
    img.alpha_composite(drop_layer)

    # === Protein structure inside droplet (twisting helix / lattice) ===
    # Small lattice of points that rotates slowly inside the droplet
    helix_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(helix_layer)
    rotation = 2 * math.pi * t
    n_helix = 16
    for i in range(n_helix):
        angle = (i / n_helix) * 4 * math.pi + rotation
        height = (i / (n_helix - 1) - 0.5) * 1.4
        px = cx + math.cos(angle) * r * 0.35
        py = cy + height * r * 0.5
        # Two strands offset
        pulse = smooth_pulse(t, phase=i / n_helix)
        sz = 2 + pulse * 3
        hd.ellipse([px - sz, py - sz, px + sz, py + sz],
                   fill=(255, 255, 255, 200))
        # Mirror strand
        px2 = cx + math.cos(angle + math.pi) * r * 0.35
        hd.ellipse([px2 - sz, py - sz, px2 + sz, py + sz],
                   fill=(PALE_SKY[0], PALE_SKY[1], PALE_SKY[2], 180))
    img.alpha_composite(helix_layer)

    # === Orbiting data particles flowing inward ===
    orbit_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(orbit_layer)
    n_orbit = 36
    for i in range(n_orbit):
        # Each particle has its own offset phase; together they form a spiraling current
        base_angle = (i / n_orbit) * 2 * math.pi
        # Particle progress around its orbit (loop continuously)
        prog = ((t * 1.5) + i / n_orbit) % 1.0
        # Spiral inward then reset
        spiral_r = lerp(r + 280, r + 50, prog ** 0.7)
        ang = base_angle + prog * 2 * math.pi * 0.6  # slight rotational drift
        px = cx + math.cos(ang) * spiral_r
        py = cy + math.sin(ang) * spiral_r * 0.85  # slight ellipse
        # Fade as it approaches the droplet
        alpha = int(220 * (1 - prog) ** 1.3 + 30 * (1 - prog))
        sz = lerp(1.5, 3.5, prog)
        color = SKY if i % 3 == 0 else PALE_SKY
        od.ellipse([px - sz, py - sz, px + sz, py + sz],
                   fill=(color[0], color[1], color[2], alpha))
    img.alpha_composite(orbit_layer)

    # === AI neural-network constellation ===
    # Fixed positions around the droplet, with connection lines that pulse
    nodes = []
    n_nodes = 9
    for i in range(n_nodes):
        ang = (i / n_nodes) * 2 * math.pi + 0.2  # offset so it doesn't align with orbits
        dist = r + 240 + (i % 3) * 18  # slight tiered distance
        nx = cx + math.cos(ang) * dist
        ny = cy + math.sin(ang) * dist * 0.85
        nodes.append((nx, ny, i))

    # Three "patient identified" nodes that pulse brighter in sequence
    highlight_indices = [1, 4, 7]
    # cycle through which node is brightest
    cycle_t = (t * 1.0) % 1.0
    active_idx = highlight_indices[int(cycle_t * 3) % 3]

    # Connection lines (drawn first, behind nodes)
    line_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ll = ImageDraw.Draw(line_layer)
    for i, (nx, ny, idx) in enumerate(nodes):
        # Connect each node to the next 2 in the ring
        for offset in (1, 2):
            j = (i + offset) % n_nodes
            mx, my, _ = nodes[j]
            # Pulse the line opacity
            pulse_phase = (i + offset) / n_nodes
            pulse = smooth_pulse(t, phase=pulse_phase)
            opacity = int(40 + pulse * 80)
            ll.line([(nx, ny), (mx, my)],
                    fill=(INDIGO[0], INDIGO[1], INDIGO[2], opacity), width=1)
        # Also connect to droplet center (very faint)
        ll.line([(nx, ny), (cx, cy)],
                fill=(SKY[0], SKY[1], SKY[2], 22), width=1)
    img.alpha_composite(line_layer)

    # Nodes (with glow on active ones)
    node_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(node_layer)
    for nx, ny, idx in nodes:
        is_active = (idx == active_idx)
        if is_active:
            # Brighter glow + larger size
            for halo_r in (28, 18, 10):
                halo_alpha = int(60 if halo_r == 28 else 120 if halo_r == 18 else 200)
                nd.ellipse([nx - halo_r, ny - halo_r, nx + halo_r, ny + halo_r],
                           fill=(PALE_SKY[0], PALE_SKY[1], PALE_SKY[2], halo_alpha))
            nd.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=WHITE + (255,))
        else:
            nd.ellipse([nx - 11, ny - 11, nx + 11, ny + 11],
                       fill=(INDIGO[0], INDIGO[1], INDIGO[2], 70))
            nd.ellipse([nx - 5, ny - 5, nx + 5, ny + 5],
                       fill=(SKY[0], SKY[1], SKY[2], 220))
            nd.ellipse([nx - 2.5, ny - 2.5, nx + 2.5, ny + 2.5],
                       fill=WHITE + (240,))
    # Blur the active glows lightly for softness
    node_layer_blurred = node_layer.filter(ImageFilter.GaussianBlur(radius=1.5))
    img.alpha_composite(node_layer_blurred)
    img.alpha_composite(node_layer)

    # === Subtle drifting background motes (depth) ===
    motes_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ml = ImageDraw.Draw(motes_layer)
    n_motes = 40
    for i in range(n_motes):
        # Deterministic positions per index
        seed_x = (i * 137) % 1000 / 1000.0
        seed_y = (i * 251) % 1000 / 1000.0
        # Slow drift
        drift = ((t * 0.3) + i / n_motes) % 1.0
        mx = (seed_x * W + drift * 40) % W
        my = seed_y * H
        twinkle = smooth_pulse(t, phase=i / n_motes)
        a = int(40 + twinkle * 120)
        sz = 1 + twinkle * 1.5
        ml.ellipse([mx - sz, my - sz, mx + sz, my + sz],
                   fill=(PALE_SKY[0], PALE_SKY[1], PALE_SKY[2], a))
    img.alpha_composite(motes_layer)

    return img


def main():
    print("Generating background gradient...")
    bg = make_background()

    print(f"Rendering {N_FRAMES} frames...")
    frames = []
    for f in range(N_FRAMES):
        t = f / N_FRAMES
        frame = draw_frame(bg, t)
        # Convert to RGB for WebP/GIF compatibility, keep small palette
        frame_rgb = frame.convert("RGB")
        frames.append(frame_rgb)
        if (f + 1) % 10 == 0:
            print(f"  {f + 1}/{N_FRAMES}")

    out_path = os.path.join("images", "hero-animation.webp")
    print(f"\nSaving animated WebP to {out_path}...")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,            # infinite loop
        duration=FRAME_MS,
        quality=80,
        method=6,          # max compression effort
    )
    size = os.path.getsize(out_path)
    print(f"Done. File size: {size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
