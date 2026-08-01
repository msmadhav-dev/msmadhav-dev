#!/usr/bin/env python3
"""
generate_banner.py — builds assets/madhav.svg

A self-contained, self-typing ASCII banner. No third-party services, no runtime
requests: the animation is SMIL (<animate>) inside the file, which GitHub does
execute. Scripts and <style> blocks are stripped by GitHub's sanitiser, so all
styling is done with presentation attributes.

Standard library only.
"""

import os

# --- the word, in ANSI-Shadow block letters -------------------------------
# Every row is exactly the same character count, so one clip rectangle can
# wipe across all six rows in lockstep.
ROWS = [
    "███╗   ███╗  █████╗  ██████╗  ██╗  ██╗  █████╗  ██╗   ██╗",
    "████╗ ████║ ██╔══██╗ ██╔══██╗ ██║  ██║ ██╔══██╗ ██║   ██║",
    "██╔████╔██║ ███████║ ██║  ██║ ███████║ ███████║ ██║   ██║",
    "██║╚██╔╝██║ ██╔══██║ ██║  ██║ ██╔══██║ ██╔══██║ ╚██╗ ██╔╝",
    "██║ ╚═╝ ██║ ██║  ██║ ██████╔╝ ██║  ██║ ██║  ██║  ╚████╔╝ ",
    "╚═╝     ╚═╝ ╚═╝  ╚═╝ ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═══╝  ",
]

PROMPT = "msmadhav-dev@github:~$ whoami"
TAGLINE = "full stack developer · ui/ux designer · building ai-powered applications"

# --- geometry -------------------------------------------------------------
# Monospace advance width is 0.600 em in DejaVu Sans Mono, Liberation Mono and
# Noto Sans Mono. Consolas (what Windows lands on) is ~0.55, so a Windows
# visitor sees the block ~7% narrower. Because each row is a single <text>
# element rather than a per-character grid, that scales cleanly instead of
# breaking alignment.
W, H = 900, 300
FS = 20                      # banner font size
CW = FS * 0.600              # 12.0 px per character
COLS = len(ROWS[0])          # 57
BANNER_W = COLS * CW         # 684
X0 = round((W - BANNER_W) / 2)
CX = W / 2                   # everything is centre-anchored, so a font with a
                             # different advance width grows symmetrically
                             # instead of drifting off one edge

# Wipe a little wider than the nominal text box. If a visitor's machine falls
# back to a font with a wider advance (Consolas, or a fallback for the box
# drawing glyphs), the tail of the word still gets revealed instead of being
# clipped off forever.
OVER_BANNER = 1.10
OVER_TEXT = 1.06
Y0, LH = 86, 21              # first baseline, line height

FS_SMALL = 13
CW_SMALL = FS_SMALL * 0.600
Y_PROMPT = 46
Y_TAG = 240
Y_RULE = 264

MONO = ("ui-monospace,'SFMono-Regular','DejaVu Sans Mono',"
        "'Liberation Mono',Menlo,Consolas,monospace")


def discrete(start, step, count):
    """Values list for a character-by-character (not smooth) wipe."""
    return ";".join(str(round(start + step * i, 2)) for i in range(count + 1))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --- timeline -------------------------------------------------------------
T_PROMPT = 0.30
D_PROMPT = 0.90
T_BANNER = T_PROMPT + D_PROMPT + 0.25          # 1.45
D_BANNER = 1.90
T_TAG = T_BANNER + D_BANNER + 0.25             # 3.60
D_TAG = 1.60
T_RULE = T_TAG + D_TAG + 0.10                  # 5.30

n_prompt = len(PROMPT)
n_tag = len(TAGLINE)

SPAN_B = round(BANNER_W * OVER_BANNER, 2)
SPAN_P = round(n_prompt * CW_SMALL * OVER_TEXT, 2)
SPAN_T = round(n_tag * CW_SMALL * OVER_TEXT, 2)

LB = round(CX - SPAN_B / 2, 2)   # left edge of each wipe
LP = round(CX - SPAN_P / 2, 2)
LT = round(CX - SPAN_T / 2, 2)

out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
  f'height="{H}" fill="none" role="img" aria-label="MADHAV — full stack '
  f'developer, UI/UX designer, building AI-powered applications">')
A('<title>MADHAV</title>')

# defs -------------------------------------------------------------------
A('<defs>')
A('<linearGradient id="ink" x1="0" y1="0" x2="1" y2="0.4">'
  '<stop offset="0" stop-color="#818CF8"/>'
  '<stop offset="0.45" stop-color="#A78BFA"/>'
  '<stop offset="1" stop-color="#C084FC"/></linearGradient>')
A('<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
  '<stop offset="0" stop-color="#7C3AED"/>'
  '<stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></linearGradient>')
A('<radialGradient id="glow" cx="0.5" cy="0.45" r="0.6">'
  '<stop offset="0" stop-color="#7C3AED" stop-opacity="0.30"/>'
  '<stop offset="1" stop-color="#7C3AED" stop-opacity="0"/></radialGradient>')

# one clip for all six rows -> a single vertical cursor can ride the edge
A('<clipPath id="cbanner">')
A(f'<rect x="{LB}" y="{Y0 - 18}" width="0" height="{LH * len(ROWS) + 12}">')
A(f'<animate attributeName="width" calcMode="discrete" '
  f'values="{discrete(0, SPAN_B / COLS, COLS)}" dur="{D_BANNER}s" '
  f'begin="{T_BANNER}s" fill="freeze"/>')
A('</rect></clipPath>')

A('<clipPath id="cprompt">')
A(f'<rect x="{LP}" y="{Y_PROMPT - 14}" width="0" height="20">')
A(f'<animate attributeName="width" calcMode="discrete" '
  f'values="{discrete(0, SPAN_P / n_prompt, n_prompt)}" dur="{D_PROMPT}s" '
  f'begin="{T_PROMPT}s" fill="freeze"/>')
A('</rect></clipPath>')

A('<clipPath id="ctag">')
A(f'<rect x="{LT}" y="{Y_TAG - 14}" width="0" height="22">')
A(f'<animate attributeName="width" calcMode="discrete" '
  f'values="{discrete(0, SPAN_T / n_tag, n_tag)}" dur="{D_TAG}s" '
  f'begin="{T_TAG}s" fill="freeze"/>')
A('</rect></clipPath>')
A('</defs>')

# card -------------------------------------------------------------------
A(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
  f'fill="#0B0A14" stroke="#241C46"/>')
A(f'<ellipse cx="{W/2}" cy="{H*0.42}" rx="{W*0.42}" ry="{H*0.5}" '
  f'fill="url(#glow)"/>')

# corner brackets
b, o, s = 18, 16, 1.4
for cx, cy, sx, sy in ((o, o, 1, 1), (W-o, o, -1, 1),
                       (o, H-o, 1, -1), (W-o, H-o, -1, -1)):
    A(f'<path d="M{cx} {cy + sy*b} L{cx} {cy} L{cx + sx*b} {cy}" '
      f'stroke="#3B2E6E" stroke-width="{s}" stroke-linecap="square"/>')

# prompt line ------------------------------------------------------------
A(f'<g clip-path="url(#cprompt)">'
  f'<text x="{CX}" y="{Y_PROMPT}" text-anchor="middle" font-family="{MONO}" '
  f'font-size="{FS_SMALL}" fill="#6E6A8A" xml:space="preserve">{esc(PROMPT)}'
  f'</text></g>')
A(f'<rect x="{LP}" y="{Y_PROMPT - 11}" width="{round(CW_SMALL, 2)}" height="14" '
  f'fill="#C084FC" opacity="0">'
  f'<set attributeName="opacity" to="0.9" begin="{T_PROMPT}s"/>'
  f'<animate attributeName="x" calcMode="discrete" '
  f'values="{discrete(LP, SPAN_P / n_prompt, n_prompt)}" dur="{D_PROMPT}s" '
  f'begin="{T_PROMPT}s" fill="freeze"/>'
  f'<set attributeName="opacity" to="0" begin="{T_PROMPT + D_PROMPT}s"/></rect>')

# banner -----------------------------------------------------------------
A('<g clip-path="url(#cbanner)" fill="url(#ink)" '
  f'font-family="{MONO}" font-size="{FS}" xml:space="preserve">')
for i, row in enumerate(ROWS):
    A(f'<text x="{CX}" y="{Y0 + i*LH}" text-anchor="middle">{esc(row)}</text>')
A('</g>')

# vertical cursor riding the banner wipe edge
A(f'<rect x="{LB}" y="{Y0 - 17}" width="7" height="{LH * len(ROWS) + 8}" '
  f'fill="#C084FC" opacity="0">'
  f'<set attributeName="opacity" to="0.85" begin="{T_BANNER}s"/>'
  f'<animate attributeName="x" calcMode="discrete" '
  f'values="{discrete(LB, SPAN_B / COLS, COLS)}" dur="{D_BANNER}s" '
  f'begin="{T_BANNER}s" fill="freeze"/>'
  f'<set attributeName="opacity" to="0" begin="{T_BANNER + D_BANNER}s"/></rect>')

# tagline ----------------------------------------------------------------
A(f'<g clip-path="url(#ctag)">'
  f'<text x="{CX}" y="{Y_TAG}" text-anchor="middle" font-family="{MONO}" '
  f'font-size="{FS_SMALL}" fill="#A78BFA" xml:space="preserve">{esc(TAGLINE)}'
  f'</text></g>')

# trailing cursor: rides the tagline, then blinks forever
A(f'<rect x="{LT}" y="{Y_TAG - 11}" width="{round(CW_SMALL, 2)}" height="14" '
  f'fill="#C084FC" opacity="0">'
  f'<set attributeName="opacity" to="0.9" begin="{T_TAG}s"/>'
  f'<animate attributeName="x" calcMode="discrete" '
  f'values="{discrete(LT, SPAN_T / n_tag, n_tag)}" dur="{D_TAG}s" '
  f'begin="{T_TAG}s" fill="freeze"/>'
  f'<animate attributeName="opacity" values="0.9;0.9;0;0" dur="1.1s" '
  f'begin="{T_TAG + D_TAG}s" repeatCount="indefinite"/></rect>')

# rule -------------------------------------------------------------------
A(f'<rect x="{LB}" y="{Y_RULE}" width="0" height="1.5" fill="url(#rule)">'
  f'<animate attributeName="width" values="0;{SPAN_B}" dur="0.7s" '
  f'begin="{T_RULE}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
  f'keySplines="0.2 0.8 0.2 1"/></rect>')

A('</svg>')

svg = "\n".join(out)
os.makedirs("assets", exist_ok=True)
with open("assets/madhav.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"assets/madhav.svg  —  {len(svg.encode('utf-8')) / 1024:.1f} KB, "
      f"{COLS} cols x {len(ROWS)} rows, ends at {T_RULE + 0.7:.1f}s")
