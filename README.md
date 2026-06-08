# ClinOmics AI — Website

Single-page marketing site built from the **ClinOmicsAI website sample - 28mar2026** PowerPoint deck.

## Files

```
ClinomicsAI/
├── index.html          Main page — 9 sections
├── styles.css          Brand styles, typography, all section/component CSS
├── script.js           Mobile nav, sticky nav, scroll-reveal, form handling
├── README.md           This file
├── images/             (empty — drop real assets here)
└── design-refs/        7 PNGs extracted from the source PPTX (one per slide)
```

## Sections (mapped to deck slides)

| # | Section | Source slide |
|---|---------|--------------|
| 1 | **Hero** — *Accelerating the Treatments of Tomorrow Through Liquid Biopsy Intelligence* + 4 KPI stats | Slide 1 |
| 2 | **The Challenge** — *Why Do 90% of Drugs Fail* + $41K stat + 3 problem cards (Heterogeneity / Imaging / AMD Graveyard) | Slide 2 |
| 3 | **Our Approach** — *Engineering Success with Liquid Biopsy Proteomics* + 3 outcome cards with stats | Slide 3 |
| 4 | **TEMPO™ Molecure™ Platform** (dark) — 4-step workflow + Molecure Report dashboard features | Slide 4 |
| 5 | **Solutions / Framework** — A Phased Framework for Asset Value Creation + Lazarus Effect rescue card | Slide 5 |
| 6 | **Leadership Team** (dark) — Co-founders Dr. David R.P. Almeida + Dr. Vinit B. Mahajan with bios, credentials, education | Live site /leadership-team |
| 7 | **Pipeline** (cream) — *Pioneering Precision Ophthalmology Trials* + trial table + 5 country site cards | Slide 6 |
| 8 | **Partner With Us** (dark) — Locations + inquiry form | Slide 7 |
| 9 | Footer | — |

## Brand system

| Token | Value | Use |
|-------|-------|-----|
| `--ink` | `#0a1628` | Deep navy hero / CTA / dark sections |
| `--cyan` | `#2cb9e0` | Primary AI accent — the "Omics AI" italics, CTA buttons, gradient text |
| `--teal` | `#4fd6c8` | Secondary accent — gradient pair end |
| `--cream` | `#f6efe2` | Warm editorial section background (Pipeline) |
| `--paper` | `#ffffff` | Light section / card surface |
| Headlines | **DM Serif Display** (italic emphasis) | Section h1/h2/h3 |
| Body | **Inter** | All UI / body text |
| Tags / codes | **JetBrains Mono** | Step numbers, table headers |

## Key interactions

- **Sticky nav** turns more opaque on scroll
- **Mobile menu** at ≤ 900px (hamburger → fullscreen dropdown)
- **Scroll-reveal** fade-up using IntersectionObserver (one-shot, respects `prefers-reduced-motion`)
- **Smooth in-page anchor scrolling** with sticky-nav offset
- **Form** validates name + email client-side; falls back to opening a `mailto:` draft with all field values pre-populated (no backend wired in this template)
- **Hero grid** — 9 pulsing "sample cell" tiles in the right pane (purely decorative, brand-on)

## To view

Open `index.html` in any modern browser. No build step.

## Hooking the form to a real backend

In `script.js`, replace the `mailto:` fallback inside the submit handler with a `fetch()` POST to your endpoint (Formspree, Netlify Forms, Jotform iframe — same patterns as the prior projects).

## Images

Four real assets pulled from **clinomicsai.com** are now wired in:

| File | Source | Use |
|------|--------|-----|
| `images/hero-home.jpg` | Getty (`img1.wsimg.com/.../1646106148`) — blue medical-AI scene with hexagonal icons + circuit-cross | Hero background |
| `images/about-hero.jpg` | Getty (`img1.wsimg.com/.../2216264126`) — teal DNA helix + node network | Leadership section background texture |
| `images/dr-almeida.png` | Live site (`/blob-cdea1ee.png`) | Dr. Almeida headshot |
| `images/dr-mahajan.jpg` | Live site (`/vinit.jpg`) | Dr. Mahajan headshot |

The previous CSS-driven "pulsing sample cells" hero treatment has been replaced with the real Getty image + a 100°-angled dark-navy overlay (heavy on the left for headline legibility, fading to ~15% opacity on the right where the AI cross + ECG lines are featured).

## Updating copy

All section text lives in `index.html`. The deck's copy is intact — every stat, headline, and phase narrative is preserved verbatim (numerical thousands separators normalized).
