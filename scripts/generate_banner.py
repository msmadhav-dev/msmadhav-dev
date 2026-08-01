#!/usr/bin/env python3
"""
generate_banner.py — builds assets/madhav.svg

A self-contained, self-typing ASCII banner styled to look exactly like a
GitHub code block. No third-party services, no runtime requests: the animation
is SMIL (<animate>) inside the file, which GitHub executes.

Animation cannot live in the README itself — GitHub's sanitiser strips <style>
and <script> from markdown, so characters written directly in the file are
permanently static. An SVG is the only way to make ASCII type itself out.

Standard library only. Run:  python3 scripts/generate_banner.py
"""

import os

# --- the word, in ANSI-Shadow block letters -------------------------------
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
# Monospace advance is 0.600 em in DejaVu Sans Mono, Liberation Mono and Noto
# Sans Mono; Consolas (Windows) is ~0.55, and box-drawing glyphs sometimes fall
# back to a wider face. Text is left-anchored and every wipe overshoots to the
# right, so a wider font still gets fully revealed instead of being clipped.
W, H = 880, 292
PAD = 32

FS = 20                       # banner
CW = FS * 0.600               # 12.0 px/char
COLS = len(ROWS[0])           # 57
FS_S = 14                     # prompt + tagline
CW_S = FS_S * 0.600

OVERSHOOT = 1.14              # worst-case advance ~0.68 em

Y_PROMPT = 46
Y0, LH = 94, 22               # first banner baseline, line height
Y_TAG = 250

MONO = ("ui-monospace,'SFMono-Regular','DejaVu Sans Mono',"
        "'Liberation Mono',Menlo,Consolas,monospace")

# --- timeline -------------------------------------------------------------
T_PROMPT, D_PROMPT = 0.25, 0.85
T_ROWS = 1.25                 # first banner row
STAGGER = 0.30
D_ROW = 0.85
T_TAG = T_ROWS + STAGGER * (len(ROWS) - 1) + D_ROW + 0.25
D_TAG = 1.30


def steps(start, span, n):
    """Discrete values list — a character-at-a-time wipe, not a smooth one."""
    return ";".join(str(round(start + span * i / n, 2)) for i in range(n + 1))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


SPAN_B = round(COLS * CW * OVERSHOOT, 2)
SPAN_P = round(len(PROMPT) * CW_S * OVERSHOOT, 2)
SPAN_T = round(len(TAGLINE) * CW_S * OVERSHOOT, 2)

out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
  f'height="{H}" fill="none" role="img" aria-label="MADHAV — full stack '
  f'developer, UI/UX designer, building AI-powered applications">')
A('<title>MADHAV</title>')

A('<defs>')
A('<linearGradient id="ink" x1="0" y1="0" x2="1" y2="0.35">'
  '<stop offset="0" stop-color="#C4B5FD"/>'
  '<stop offset="0.5" stop-color="#A78BFA"/>'
  '<stop offset="1" stop-color="#818CF8"/></linearGradient>')

# one clip per line, so each row types independently, top to bottom
A('<clipPath id="cp">')
A(f'<rect x="{PAD}" y="{Y_PROMPT - 14}" width="0" height="20">'
  f'<animate attributeName="width" calcMode="discrete" '
  f'values="{steps(0, SPAN_P, len(PROMPT))}" dur="{D_PROMPT}s" '
  f'begin="{T_PROMPT}s" fill="freeze"/></rect>')
A('</clipPath>')

for i in range(len(ROWS)):
    begin = round(T_ROWS + i * STAGGER, 2)
    A(f'<clipPath id="cr{i}">')
    A(f'<rect x="{PAD}" y="{Y0 + i*LH - 18}" width="0" height="{LH + 4}">'
      f'<animate attributeName="width" calcMode="discrete" '
      f'values="{steps(0, SPAN_B, COLS)}" dur="{D_ROW}s" begin="{begin}s" '
      f'fill="freeze"/></rect>')
    A('</clipPath>')

A('<clipPath id="ct">')
A(f'<rect x="{PAD}" y="{Y_TAG - 14}" width="0" height="22">'
  f'<animate attributeName="width" calcMode="discrete" '
  f'values="{steps(0, SPAN_T, len(TAGLINE))}" dur="{D_TAG}s" '
  f'begin="{T_TAG}s" fill="freeze"/></rect>')
A('</clipPath>')
A('</defs>')

# panel — matches a GitHub dark-mode code block
A(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" '
  f'fill="#161B22" stroke="#30363D"/>')

# prompt line
A(f'<g clip-path="url(#cp)"><text x="{PAD}" y="{Y_PROMPT}" '
  f'font-family="{MONO}" font-size="{FS_S}" fill="#8B949E" '
  f'xml:space="preserve">{esc(PROMPT)}</text></g>')
A(f'<rect x="{PAD}" y="{Y_PROMPT - 11}" width="{round(CW_S, 2)}" height="14" '
  f'fill="#C4B5FD" opacity="0">'
  f'<set attributeName="opacity" to="0.9" begin="{T_PROMPT}s"/>'
  f'<animate attributeName="x" calcMode="discrete" '
  f'values="{steps(PAD, SPAN_P, len(PROMPT))}" dur="{D_PROMPT}s" '
  f'begin="{T_PROMPT}s" fill="freeze"/>'
  f'<set attributeName="opacity" to="0" '
  f'begin="{round(T_PROMPT + D_PROMPT, 2)}s"/></rect>')

# banner rows, each typing in turn with its own cursor
for i, row in enumerate(ROWS):
    y = Y0 + i * LH
    begin = round(T_ROWS + i * STAGGER, 2)
    A(f'<g clip-path="url(#cr{i})"><text x="{PAD}" y="{y}" '
      f'font-family="{MONO}" font-size="{FS}" fill="url(#ink)" '
      f'xml:space="preserve">{esc(row)}</text></g>')
    A(f'<rect x="{PAD}" y="{y - 15}" width="6" height="19" fill="#C4B5FD" '
      f'opacity="0">'
      f'<set attributeName="opacity" to="0.85" begin="{begin}s"/>'
      f'<animate attributeName="x" calcMode="discrete" '
      f'values="{steps(PAD, SPAN_B, COLS)}" dur="{D_ROW}s" begin="{begin}s" '
      f'fill="freeze"/>'
      f'<set attributeName="opacity" to="0" '
      f'begin="{round(begin + D_ROW, 2)}s"/></rect>')

# tagline
A(f'<g clip-path="url(#ct)"><text x="{PAD}" y="{Y_TAG}" '
  f'font-family="{MONO}" font-size="{FS_S}" fill="#A78BFA" '
  f'xml:space="preserve">{esc(TAGLINE)}</text></g>')

# trailing cursor: rides the tagline, then blinks forever
A(f'<rect x="{PAD}" y="{Y_TAG - 11}" width="{round(CW_S, 2)}" height="14" '
  f'fill="#C4B5FD" opacity="0">'
  f'<set attributeName="opacity" to="0.9" begin="{T_TAG}s"/>'
  f'<animate attributeName="x" calcMode="discrete" '
  f'values="{steps(PAD, SPAN_T, len(TAGLINE))}" dur="{D_TAG}s" '
  f'begin="{T_TAG}s" fill="freeze"/>'
  f'<animate attributeName="opacity" values="0.9;0.9;0;0" dur="1.1s" '
  f'begin="{round(T_TAG + D_TAG, 2)}s" repeatCount="indefinite"/></rect>')

A('</svg>')

svg = "\n".join(out)
os.makedirs("assets", exist_ok=True)
with open("assets/madhav.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"assets/madhav.svg — {len(svg.encode('utf-8'))/1024:.1f} KB, "
      f"typing finishes at {round(T_TAG + D_TAG, 2)}s")
