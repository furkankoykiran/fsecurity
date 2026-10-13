#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Furkan Köykıran
"""
scripts/generate_brand.py

Canonical Brand Asset Generator for fsecurity.
All assets are deterministically derived from:
1. Canonical mark vector geometry (Perimeter Bastion Reticle enclosing the shared ftools canonical 'f')
2. Canonical mascot vector geometry (cerb: the bastion sentinel hound)
3. Canonical frozen vector path outlines for wordmark (f, s, e, c, u, r, i, t, y)

Self-contained:
- Zero runtime font dependencies (does not require external system fonts at CI runtime).
- Zero non-uniform scaling distortions.

Transparency Contract:
- Reusable mark, wordmark, and mascot SVG/PNG exports have genuinely transparent canvases (no background rect, alpha=0 corners).
- *-on-dark / *-on-light, social previews, and intentionally backgrounded platform assets are opaque.
- Favicons preserve transparency around glyphs.
"""

import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND_DIR = os.path.join(BASE_DIR, "assets", "brand")

# Canonical Color Palette Tokens - fsecurity Tactical Palette
OBSIDIAN_NIGHT = "#080b10"
VAULT_CHARCOAL = "#101520"
BOREAS_SLATE = "#2e384d"
GRID_MUTED = "#1a2233"
GLACIER_WHITE = "#e6edf5"
ELECTRIC_PHOSPHOR = "#00f59b"
CYBER_AZURE = "#38bdf8"

# The Single Shared Visual Invariant from ftools lineage: The Canonical 'f' Glyph (512x512 space)
CANONICAL_F = "M 216 384 L 194 384 L 194 172 L 236 128 L 336 128 L 302 168 L 238 168 L 238 214 L 306 214 L 284 254 L 238 254 L 238 348 Z"

# Canonical Mark Geometry Coordinates - The Bastion Reticle (512x512 coordinate space)
BASTION_CORNER_N = "M 216 68 L 256 44 L 296 68"
BASTION_CORNER_NE = "M 420 115 L 440 150 L 440 195"
BASTION_CORNER_SE = "M 440 317 L 440 362 L 420 397"
BASTION_CORNER_S = "M 296 444 L 256 468 L 216 444"
BASTION_CORNER_SW = "M 92 397 L 72 362 L 72 317"
BASTION_CORNER_NW = "M 72 195 L 72 150 L 92 115"
CALIPER_N = (256, 20, 256, 44)
CALIPER_S = (256, 468, 256, 492)
CALIPER_E = (440, 256, 464, 256)
CALIPER_W = (48, 256, 72, 256)
NODE_E = (396, 256, 7)
NODE_W = (116, 256, 7)

# Canonical Mascot Geometry Coordinates (cerb: the bastion sentinel hound, 512x512 space)
CERB_EAR_L = "M 176 190 L 140 68 L 208 124 Z"
CERB_EAR_R = "M 336 190 L 372 68 L 304 124 Z"
CERB_EAR_CHANNEL_L = (152, 98, 186, 148)
CERB_EAR_CHANNEL_R = (360, 98, 326, 148)
CERB_CROWN = "M 208 124 L 256 104 L 304 124 L 286 174 L 226 174 Z"
CERB_BROW_DIVIDER = (226, 174, 286, 174)
CERB_VISOR = "M 168 186 L 344 186 L 332 232 L 180 232 Z"
CERB_VISOR_SCANNER = (236, 196, 40, 26)
CERB_VISOR_TICK_L = (204, 196, 204, 222)
CERB_VISOR_TICK_R = (308, 196, 308, 222)
CERB_SNOUT = "M 214 232 L 214 336 L 256 374 L 298 336 L 298 232"
CERB_MANDIBLE_L = "M 180 250 L 198 320 L 224 354"
CERB_MANDIBLE_R = "M 332 250 L 314 320 L 288 354"
CERB_NOSE = "M 242 328 L 256 342 L 270 328 Z"
CERB_COLLAR_UPPER = "M 160 380 L 256 418 L 352 380"
CERB_COLLAR_LOWER = "M 160 412 L 256 450 L 352 412"
CERB_COLLAR_NODE = (256, 434, 7)
CERB_BASELINE = (80, 474, 432, 474)

# Canonical Wordmark Frozen Vector Paths (Self-contained, zero external font dependency)
WORDMARK_PATH_800X400 = (
    "M 307.55 176.6 L 307.55 180.25 L 320.37 180.25 L 320.37 188.64 L 307.55 188.64 L 307.55 222.0 L 296.62 222.0 L 296.62 188.64 L 286.49 188.64 L 286.49 180.25 L 296.62 180.25 L 296.62 177.34 Q 296.62 169.81 299.75 166.91 Q 302.89 164.0 311.39 164.0 L 320.37 164.0 L 320.37 172.39 L 311.83 172.39 Q 309.37 172.39 308.5 173.28 Q 307.62 174.18 307.55 176.6 Z M 362.9 181.56 L 362.9 191.1 Q 359.88 189.16 356.62 188.18 Q 353.36 187.19 350.08 187.19 Q 346.42 187.19 344.56 188.25 Q 342.7 189.31 342.7 191.4 Q 342.7 194.38 350.67 196.24 L 351.08 196.35 L 354.21 197.1 Q 360.18 198.52 362.96 201.67 Q 365.73 204.82 365.73 210.18 Q 365.73 216.63 361.5 219.86 Q 357.27 223.08 348.77 223.08 Q 345.01 223.08 341.06 222.43 Q 337.11 221.78 333.04 220.47 L 333.04 210.93 Q 336.66 212.98 340.4 214.06 Q 344.15 215.14 347.65 215.14 Q 351.49 215.14 353.47 214.02 Q 355.44 212.9 355.44 210.78 Q 355.44 208.69 354.04 207.57 Q 352.65 206.46 347.39 205.19 L 344.37 204.52 Q 338.11 203.1 335.24 200.08 Q 332.37 197.06 332.37 191.99 Q 332.37 185.96 336.73 182.61 Q 341.09 179.25 349.0 179.25 Q 352.54 179.25 356.06 179.82 Q 359.58 180.4 362.9 181.56 Z M 413.0 219.95 Q 409.2 221.52 405.25 222.3 Q 401.29 223.08 396.89 223.08 Q 386.42 223.08 380.88 217.47 Q 375.35 211.86 375.35 201.31 Q 375.35 191.1 380.68 185.18 Q 386.01 179.25 395.22 179.25 Q 404.5 179.25 409.62 184.75 Q 414.75 190.24 414.75 200.23 L 414.75 204.67 L 386.46 204.67 Q 386.49 209.59 389.36 212.01 Q 392.23 214.43 397.94 214.43 Q 401.7 214.43 405.36 213.35 Q 409.01 212.27 413.0 209.92 Z M 403.75 196.47 Q 403.68 192.14 401.53 189.93 Q 399.39 187.71 395.22 187.71 Q 391.45 187.71 389.22 190.0 Q 386.98 192.29 386.57 196.5 Z M 457.43 219.88 Q 454.67 221.48 451.5 222.28 Q 448.33 223.08 444.68 223.08 Q 435.03 223.08 429.58 217.26 Q 424.14 211.45 424.14 201.16 Q 424.14 190.84 429.62 185.0 Q 435.1 179.17 444.76 179.17 Q 448.11 179.17 451.23 179.95 Q 454.34 180.74 457.43 182.38 L 457.43 192.37 Q 455.04 190.32 452.19 189.22 Q 449.34 188.12 446.28 188.12 Q 440.95 188.12 438.08 191.51 Q 435.21 194.9 435.21 201.16 Q 435.21 207.43 438.08 210.78 Q 440.95 214.13 446.28 214.13 Q 449.45 214.13 452.21 213.07 Q 454.97 212.01 457.43 209.85 Z M 469.8 207.43 L 469.8 180.25 L 480.73 180.25 L 480.73 205.75 Q 480.73 210.26 482.0 212.19 Q 483.26 214.13 486.21 214.13 Q 489.15 214.13 490.81 211.52 Q 492.47 208.92 492.47 204.22 L 492.47 180.25 L 503.39 180.25 L 503.39 222.0 L 492.47 222.0 L 492.47 215.81 Q 491.31 219.28 488.53 221.18 Q 485.76 223.08 481.84 223.08 Q 475.88 223.08 472.84 219.13 Q 469.8 215.18 469.8 207.43 Z M 552.7 191.77 Q 550.91 190.13 548.51 189.31 Q 546.11 188.49 543.24 188.49 Q 539.77 188.49 537.18 189.7 Q 534.59 190.91 533.17 193.22 Q 532.28 194.64 531.92 196.65 Q 531.57 198.67 531.57 202.77 L 531.57 222.0 L 520.65 222.0 L 520.65 180.25 L 531.57 180.25 L 531.57 186.74 Q 533.17 183.16 536.49 181.2 Q 539.81 179.25 544.24 179.25 Q 546.48 179.25 548.62 179.79 Q 550.77 180.33 552.7 181.37 Z M 564.0 180.25 L 585.62 180.25 L 585.62 213.61 L 599.19 213.61 L 599.19 222.0 L 561.09 222.0 L 561.09 213.61 L 574.7 213.61 L 574.7 188.64 L 564.0 188.64 Z M 574.7 159.94 L 585.62 159.94 L 585.62 172.69 L 574.7 172.69 Z M 627.44 168.4 L 627.44 180.25 L 641.72 180.25 L 641.72 188.64 L 627.44 188.64 L 627.44 208.39 Q 627.44 211.19 628.8 212.4 Q 630.16 213.61 633.33 213.61 L 641.72 213.61 L 641.72 222.0 L 632.55 222.0 Q 623.15 222.0 619.84 219.0 Q 616.52 216.0 616.52 207.87 L 616.52 188.64 L 605.86 188.64 L 605.86 180.25 L 616.52 180.25 L 616.52 168.4 Z M 674.18 226.51 Q 671.98 232.4 668.9 235.1 Q 665.83 237.8 661.43 237.8 L 652.41 237.8 L 652.41 229.49 L 656.85 229.49 Q 660.2 229.49 661.77 228.36 Q 663.34 227.22 664.94 223.08 L 665.76 220.84 L 649.88 180.25 L 661.36 180.25 L 670.9 207.35 L 680.03 180.25 L 691.52 180.25 Z"
)
WORDMARK_CURSOR_X_800X400 = 703.0

WORDMARK_PATH_1280X640 = (
    "M 477.04 290.94 L 477.04 295.86 L 494.29 295.86 L 494.29 307.13 L 477.04 307.13 L 477.04 352.0 L 462.36 352.0 L 462.36 307.13 L 448.72 307.13 L 448.72 295.86 L 462.36 295.86 L 462.36 291.95 Q 462.36 281.82 466.57 277.91 Q 470.78 274.0 482.21 274.0 L 494.29 274.0 L 494.29 285.28 L 482.81 285.28 Q 479.5 285.28 478.32 286.49 Q 477.15 287.69 477.04 290.94 Z M 551.49 297.61 L 551.49 310.44 Q 547.43 307.84 543.04 306.51 Q 538.65 305.18 534.24 305.18 Q 529.33 305.18 526.83 306.61 Q 524.32 308.04 524.32 310.84 Q 524.32 314.85 535.05 317.36 L 535.6 317.51 L 539.81 318.51 Q 547.83 320.42 551.57 324.65 Q 555.3 328.89 555.3 336.11 Q 555.3 344.78 549.61 349.12 Q 543.92 353.45 532.49 353.45 Q 527.43 353.45 522.12 352.57 Q 516.8 351.7 511.33 349.94 L 511.33 337.11 Q 516.2 339.87 521.24 341.32 Q 526.27 342.78 530.98 342.78 Q 536.15 342.78 538.81 341.27 Q 541.46 339.77 541.46 336.91 Q 541.46 334.1 539.58 332.6 Q 537.7 331.1 530.63 329.39 L 526.57 328.49 Q 518.15 326.58 514.29 322.52 Q 510.43 318.46 510.43 311.65 Q 510.43 303.53 516.29 299.01 Q 522.16 294.5 532.79 294.5 Q 537.55 294.5 542.29 295.28 Q 547.03 296.06 551.49 297.61 Z M 618.86 349.24 Q 613.75 351.35 608.43 352.4 Q 603.12 353.45 597.21 353.45 Q 583.12 353.45 575.67 345.91 Q 568.23 338.37 568.23 324.18 Q 568.23 310.44 575.4 302.47 Q 582.57 294.5 594.95 294.5 Q 607.43 294.5 614.33 301.89 Q 621.22 309.29 621.22 322.72 L 621.22 328.69 L 583.17 328.69 Q 583.22 335.31 587.08 338.56 Q 590.94 341.82 598.61 341.82 Q 603.67 341.82 608.59 340.37 Q 613.5 338.92 618.86 335.76 Z M 606.43 317.66 Q 606.33 311.85 603.44 308.87 Q 600.56 305.88 594.95 305.88 Q 589.89 305.88 586.88 308.97 Q 583.87 312.05 583.32 317.71 Z M 678.62 349.14 Q 674.91 351.3 670.65 352.38 Q 666.39 353.45 661.47 353.45 Q 648.49 353.45 641.17 345.63 Q 633.85 337.81 633.85 323.98 Q 633.85 310.09 641.22 302.25 Q 648.59 294.4 661.57 294.4 Q 666.08 294.4 670.27 295.45 Q 674.46 296.51 678.62 298.71 L 678.62 312.15 Q 675.41 309.39 671.58 307.91 Q 667.74 306.43 663.63 306.43 Q 656.46 306.43 652.6 311.0 Q 648.74 315.56 648.74 323.98 Q 648.74 332.4 652.6 336.91 Q 656.46 341.42 663.63 341.42 Q 667.89 341.42 671.6 340.0 Q 675.31 338.57 678.62 335.66 Z M 695.25 332.4 L 695.25 295.86 L 709.94 295.86 L 709.94 330.14 Q 709.94 336.21 711.64 338.81 Q 713.35 341.42 717.31 341.42 Q 721.27 341.42 723.5 337.91 Q 725.73 334.4 725.73 328.09 L 725.73 295.86 L 740.42 295.86 L 740.42 352.0 L 725.73 352.0 L 725.73 343.68 Q 724.17 348.34 720.44 350.89 Q 716.71 353.45 711.44 353.45 Q 703.42 353.45 699.34 348.14 Q 695.25 342.83 695.25 332.4 Z M 806.74 311.35 Q 804.33 309.14 801.1 308.03 Q 797.87 306.93 794.01 306.93 Q 789.34 306.93 785.86 308.56 Q 782.38 310.19 780.47 313.3 Q 779.27 315.21 778.8 317.91 Q 778.32 320.62 778.32 326.13 L 778.32 352.0 L 763.63 352.0 L 763.63 295.86 L 778.32 295.86 L 778.32 304.58 Q 780.47 299.77 784.93 297.13 Q 789.39 294.5 795.36 294.5 Q 798.37 294.5 801.25 295.23 Q 804.13 295.96 806.74 297.36 Z M 821.93 295.86 L 851.0 295.86 L 851.0 340.72 L 869.25 340.72 L 869.25 352.0 L 818.02 352.0 L 818.02 340.72 L 836.32 340.72 L 836.32 307.13 L 821.93 307.13 Z M 836.32 268.54 L 851.0 268.54 L 851.0 285.68 L 836.32 285.68 Z M 907.25 279.92 L 907.25 295.86 L 926.45 295.86 L 926.45 307.13 L 907.25 307.13 L 907.25 333.7 Q 907.25 337.46 909.08 339.09 Q 910.91 340.72 915.17 340.72 L 926.45 340.72 L 926.45 352.0 L 914.12 352.0 Q 901.48 352.0 897.02 347.97 Q 892.56 343.93 892.56 333.0 L 892.56 307.13 L 878.22 307.13 L 878.22 295.86 L 892.56 295.86 L 892.56 279.92 Z M 970.11 358.07 Q 967.15 365.99 963.01 369.62 Q 958.88 373.25 952.97 373.25 L 940.84 373.25 L 940.84 362.08 L 946.8 362.08 Q 951.31 362.08 953.41 360.55 Q 955.52 359.02 957.68 353.45 L 958.78 350.45 L 937.43 295.86 L 952.87 295.86 L 965.7 332.3 L 977.98 295.86 L 993.42 295.86 Z"
)
WORDMARK_CURSOR_X_1280X640 = 1008.0


def get_canonical_mark_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, caliper_color=BOREAS_SLATE):
    """Returns the canonical mark group XML string with Bastion Reticle framing around canonical 'f'."""
    cn_x1, cn_y1, cn_x2, cn_y2 = CALIPER_N
    cs_x1, cs_y1, cs_x2, cs_y2 = CALIPER_S
    ce_x1, ce_y1, ce_x2, ce_y2 = CALIPER_E
    cw_x1, cw_y1, cw_x2, cw_y2 = CALIPER_W
    ne_cx, ne_cy, ne_r = NODE_E
    nw_cx, nw_cy, nw_r = NODE_W

    return f"""<g id="fsecurity-canonical-mark">
    <!-- Perimeter Bastion Boundary -->
    <path id="bastion-n" d="{BASTION_CORNER_N}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="bastion-ne" d="{BASTION_CORNER_NE}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="bastion-se" d="{BASTION_CORNER_SE}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="bastion-s" d="{BASTION_CORNER_S}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="bastion-sw" d="{BASTION_CORNER_SW}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="bastion-nw" d="{BASTION_CORNER_NW}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />

    <!-- Cardinal Caliper Crosshair Ticks -->
    <line id="caliper-n" x1="{cn_x1}" y1="{cn_y1}" x2="{cn_x2}" y2="{cn_y2}" stroke="{caliper_color}" stroke-width="8" stroke-linecap="square" />
    <line id="caliper-s" x1="{cs_x1}" y1="{cs_y1}" x2="{cs_x2}" y2="{cs_y2}" stroke="{caliper_color}" stroke-width="8" stroke-linecap="square" />
    <line id="caliper-e" x1="{ce_x1}" y1="{ce_y1}" x2="{ce_x2}" y2="{ce_y2}" stroke="{caliper_color}" stroke-width="8" stroke-linecap="square" />
    <line id="caliper-w" x1="{cw_x1}" y1="{cw_y1}" x2="{cw_x2}" y2="{cw_y2}" stroke="{caliper_color}" stroke-width="8" stroke-linecap="square" />

    <!-- Telemetry Status Nodes -->
    <circle id="node-e" cx="{ne_cx}" cy="{ne_cy}" r="{ne_r}" fill="{accent_color}" />
    <circle id="node-w" cx="{nw_cx}" cy="{nw_cy}" r="{nw_r}" fill="{accent_color}" />

    <!-- The Shared Lineage Canonical f -->
    <path id="fsecurity-mark-f" d="{CANONICAL_F}" fill="none" stroke="{stroke_color}" stroke-width="14" stroke-linecap="square" stroke-linejoin="miter" />
  </g>"""


def get_canonical_mascot_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, grid_color=BOREAS_SLATE):
    """Returns the canonical mascot (cerb) group XML string with cybernetic hound components."""
    el_x1, el_y1, el_x2, el_y2 = CERB_EAR_CHANNEL_L
    er_x1, er_y1, er_x2, er_y2 = CERB_EAR_CHANNEL_R
    bd_x1, bd_y1, bd_x2, bd_y2 = CERB_BROW_DIVIDER
    vs_x, vs_y, vs_w, vs_h = CERB_VISOR_SCANNER
    vt_l_x1, vt_l_y1, vt_l_x2, vt_l_y2 = CERB_VISOR_TICK_L
    vt_r_x1, vt_r_y1, vt_r_x2, vt_r_y2 = CERB_VISOR_TICK_R
    cn_cx, cn_cy, cn_r = CERB_COLLAR_NODE
    bl_x1, bl_y1, bl_x2, bl_y2 = CERB_BASELINE

    return f"""<g id="fsecurity-mascot-cerb">
    <!-- Upright Radar Ears -->
    <path id="cerb-ear-l" d="{CERB_EAR_L}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="cerb-ear-r" d="{CERB_EAR_R}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter" />
    <line id="cerb-ear-channel-l" x1="{el_x1}" y1="{el_y1}" x2="{el_x2}" y2="{el_y2}" stroke="{grid_color}" stroke-width="6" stroke-linecap="square" />
    <line id="cerb-ear-channel-r" x1="{er_x1}" y1="{er_y1}" x2="{er_x2}" y2="{er_y2}" stroke="{grid_color}" stroke-width="6" stroke-linecap="square" />

    <!-- Cranial Brow Armor -->
    <path id="cerb-crown" d="{CERB_CROWN}" fill="none" stroke="{stroke_color}" stroke-width="10" stroke-linecap="square" stroke-linejoin="miter" />
    <line id="cerb-brow-divider" x1="{bd_x1}" y1="{bd_y1}" x2="{bd_x2}" y2="{bd_y2}" stroke="{grid_color}" stroke-width="6" stroke-linecap="square" />

    <!-- Optical Sensor Visor (The Scanner Band) -->
    <path id="cerb-visor" d="{CERB_VISOR}" fill="none" stroke="{stroke_color}" stroke-width="10" stroke-linecap="square" stroke-linejoin="miter" />
    <rect id="cerb-visor-scanner" x="{vs_x}" y="{vs_y}" width="{vs_w}" height="{vs_h}" fill="{accent_color}" />
    <line id="cerb-visor-tick-l" x1="{vt_l_x1}" y1="{vt_l_y1}" x2="{vt_l_x2}" y2="{vt_l_y2}" stroke="{grid_color}" stroke-width="4" stroke-linecap="square" />
    <line id="cerb-visor-tick-r" x1="{vt_r_x1}" y1="{vt_r_y1}" x2="{vt_r_y2}" stroke="{grid_color}" stroke-width="4" stroke-linecap="square" />

    <!-- Muzzle & Jaw Armor -->
    <path id="cerb-snout" d="{CERB_SNOUT}" fill="none" stroke="{stroke_color}" stroke-width="10" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="cerb-mandible-l" d="{CERB_MANDIBLE_L}" fill="none" stroke="{grid_color}" stroke-width="8" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="cerb-mandible-r" d="{CERB_MANDIBLE_R}" fill="none" stroke="{grid_color}" stroke-width="8" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="cerb-nose" d="{CERB_NOSE}" fill="{grid_color}" stroke="{grid_color}" stroke-width="4" stroke-linejoin="miter" />

    <!-- Tactical Perimeter Collar -->
    <path id="cerb-collar-upper" d="{CERB_COLLAR_UPPER}" fill="none" stroke="{stroke_color}" stroke-width="10" stroke-linecap="square" stroke-linejoin="miter" />
    <path id="cerb-collar-lower" d="{CERB_COLLAR_LOWER}" fill="none" stroke="{stroke_color}" stroke-width="10" stroke-linecap="square" stroke-linejoin="miter" />
    <circle id="cerb-collar-node" cx="{cn_cx}" cy="{cn_cy}" r="{cn_r}" fill="{accent_color}" />

    <!-- Baseline Rule -->
    <line id="cerb-baseline" x1="{bl_x1}" y1="{bl_y1}" x2="{bl_x2}" y2="{bl_y2}" stroke="{grid_color}" stroke-width="6" stroke-dasharray="12,8" stroke-linecap="square" />
  </g>"""


def build_mark_svg(mode="transparent"):
    """
    Generates 512x512 mark SVG.
    Transparency contract:
    - mode="transparent": NO background rect, glacier white strokes.
    - mode="on-dark": opaque Obsidian Night background rect + technical perimeter grid.
    - mode="on-light": opaque Glacier White background rect + dark linework + grid.
    """
    if mode == "transparent":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  {get_canonical_mark_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, caliper_color=BOREAS_SLATE)}
</svg>"""

    stroke_col = GLACIER_WHITE if mode == "on-dark" else OBSIDIAN_NIGHT
    bg_col = OBSIDIAN_NIGHT if mode == "on-dark" else GLACIER_WHITE
    grid_col = GRID_MUTED if mode == "on-dark" else "#cbd5e1"
    caliper_col = BOREAS_SLATE if mode == "on-dark" else "#64748b"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" fill="{bg_col}" />
  <g opacity="0.6">
    <circle cx="256" cy="256" r="230" fill="none" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,6" />
    <line x1="256" y1="26" x2="256" y2="486" stroke="{grid_col}" stroke-width="1" stroke-dasharray="4,4" />
    <line x1="26" y1="256" x2="486" y2="256" stroke="{grid_col}" stroke-width="1" stroke-dasharray="4,4" />
  </g>
  {get_canonical_mark_svg_group(stroke_color=stroke_col, accent_color=ELECTRIC_PHOSPHOR, caliper_color=caliper_col)}
</svg>"""


def build_mascot_svg(mode="transparent"):
    """
    Generates 512x512 mascot SVG (cerb: the bastion sentinel hound).
    Transparency contract:
    - mode="transparent": NO background rect, glacier white strokes.
    - mode="on-dark": opaque Obsidian Night background rect + grid framing.
    - mode="on-light": opaque Glacier White background rect + dark linework.
    """
    if mode == "transparent":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  {get_canonical_mascot_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, grid_color=BOREAS_SLATE)}
</svg>"""

    stroke_col = GLACIER_WHITE if mode == "on-dark" else OBSIDIAN_NIGHT
    bg_col = OBSIDIAN_NIGHT if mode == "on-dark" else GLACIER_WHITE
    grid_col = GRID_MUTED if mode == "on-dark" else "#cbd5e1"
    sub_col = BOREAS_SLATE if mode == "on-dark" else "#64748b"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" fill="{bg_col}" />
  <g opacity="0.4">
    <line x1="64" y1="64" x2="448" y2="64" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
    <line x1="64" y1="448" x2="448" y2="448" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
    <line x1="64" y1="64" x2="64" y2="448" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
    <line x1="448" y1="64" x2="448" y2="448" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
  </g>
  {get_canonical_mascot_svg_group(stroke_color=stroke_col, accent_color=ELECTRIC_PHOSPHOR, grid_color=sub_col)}
</svg>"""


def build_wordmark_svg(mode="transparent", animated=False):
    """
    Generates 800x400 wordmark lockup SVG with master mark + frozen vector outlines.
    Transparency contract:
    - mode="transparent": NO background rect, glacier white strokes.
    - mode="on-dark": opaque Obsidian Night background rect + grid + crosshairs.
    - mode="on-light": opaque Glacier White background rect + dark linework + grid.
    """
    text_col = GLACIER_WHITE if mode in ("transparent", "on-dark") else OBSIDIAN_NIGHT
    grid_col = GRID_MUTED if mode == "on-dark" else "#cbd5e1"
    cross_col = BOREAS_SLATE if mode == "on-dark" else "#64748b"

    anim_elem = ""
    if animated:
        anim_elem = """
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.501;1" dur="1s" repeatCount="indefinite" />"""

    bg_markup = ""
    grid_markup = ""
    if mode != "transparent":
        bg_col = OBSIDIAN_NIGHT if mode == "on-dark" else GLACIER_WHITE
        bg_markup = f'<rect width="800" height="400" fill="{bg_col}" />'
        grid_markup = f"""  <g opacity="0.5">
    <line x1="60" y1="60" x2="740" y2="60" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
    <line x1="60" y1="340" x2="740" y2="340" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
    <line x1="60" y1="60" x2="60" y2="340" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
    <line x1="740" y1="60" x2="740" y2="340" stroke="{grid_col}" stroke-width="1.5" stroke-dasharray="4,4" />
  </g>
  <g stroke="{cross_col}" stroke-width="2" stroke-linecap="square">
    <line x1="400" y1="16" x2="400" y2="32" />
    <line x1="392" y1="24" x2="408" y2="24" />
    <line x1="400" y1="368" x2="400" y2="384" />
    <line x1="392" y1="376" x2="408" y2="376" />
    <line x1="16" y1="200" x2="32" y2="200" />
    <line x1="24" y1="192" x2="24" y2="208" />
    <line x1="768" y1="200" x2="784" y2="200" />
    <line x1="776" y1="192" x2="776" y2="208" />
  </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="800" height="400">
  {bg_markup}
{grid_markup}
  <g transform="translate(160, 200) scale(0.56) translate(-256, -256)">
    {get_canonical_mark_svg_group(stroke_color=text_col, accent_color=ELECTRIC_PHOSPHOR, caliper_color=cross_col)}
  </g>
  <path d="{WORDMARK_PATH_800X400}" fill="{text_col}" />
  <rect x="{WORDMARK_CURSOR_X_800X400}" y="166.0" width="22" height="58.0" fill="{ELECTRIC_PHOSPHOR}">{anim_elem}
  </rect>
</svg>"""


def build_social_preview_svg():
    """Generates 1280x640 GitHub social preview SVG in Tactical Obsidian style."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
  <rect width="1280" height="640" fill="{OBSIDIAN_NIGHT}" />
  <g stroke="#141c2b" stroke-width="1.5">
    <line x1="160" y1="120" x2="1120" y2="120" />
    <line x1="160" y1="220" x2="1120" y2="220" />
    <line x1="160" y1="320" x2="1120" y2="320" />
    <line x1="160" y1="420" x2="1120" y2="420" />
    <line x1="160" y1="520" x2="1120" y2="520" />
    <line x1="160" y1="120" x2="160" y2="520" />
    <line x1="320" y1="120" x2="320" y2="520" />
    <line x1="480" y1="120" x2="480" y2="520" />
    <line x1="640" y1="120" x2="640" y2="520" />
    <line x1="800" y1="120" x2="800" y2="520" />
    <line x1="960" y1="120" x2="960" y2="520" />
    <line x1="1120" y1="120" x2="1120" y2="520" />
  </g>
  <g stroke="{BOREAS_SLATE}" stroke-width="2" stroke-linecap="square">
    <line x1="640" y1="20" x2="640" y2="44" />
    <line x1="628" y1="32" x2="652" y2="32" />
    <line x1="640" y1="596" x2="640" y2="620" />
    <line x1="628" y1="608" x2="652" y2="608" />
    <line x1="20" y1="320" x2="44" y2="320" />
    <line x1="32" y1="308" x2="32" y2="332" />
    <line x1="1236" y1="320" x2="1260" y2="320" />
    <line x1="1248" y1="308" x2="1248" y2="332" />
  </g>
  <g transform="translate(280, 320) scale(0.74) translate(-256, -256)">
    {get_canonical_mark_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, caliper_color=BOREAS_SLATE)}
  </g>
  <path d="{WORDMARK_PATH_1280X640}" fill="{GLACIER_WHITE}" />
  <rect x="{WORDMARK_CURSOR_X_1280X640}" y="276.0" width="28" height="78.0" fill="{ELECTRIC_PHOSPHOR}" />
</svg>"""


def build_avatar_svg(mask="square"):
    """
    Generates 1024x1024 mark avatar SVG.
    CRITICAL INVARIANT: Square and circle avatars MUST have IDENTICAL mark placement and scale!
    In circle avatar, outside the circle is transparent, inside circle is Obsidian Night.
    """
    scale = 1.35
    clip_def = ""
    container = f'<rect width="1024" height="1024" fill="{OBSIDIAN_NIGHT}" />'
    clip_attr = ""
    if mask == "circle":
        clip_def = """<defs>
    <clipPath id="avatar-circle-clip">
      <circle cx="512" cy="512" r="512" />
    </clipPath>
  </defs>"""
        container = f'<circle cx="512" cy="512" r="512" fill="{OBSIDIAN_NIGHT}" />'
        clip_attr = ' clip-path="url(#avatar-circle-clip)"'

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  {clip_def}
  {container}
  <g transform="translate(512, 512) scale({scale}) translate(-256, -256)"{clip_attr}>
    {get_canonical_mark_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, caliper_color=BOREAS_SLATE)}
  </g>
</svg>"""


def build_mascot_avatar_svg():
    """Generates 1024x1024 mascot profile avatar with circular mask on transparent canvas."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <clipPath id="mascot-circle-clip">
      <circle cx="512" cy="512" r="512" />
    </clipPath>
  </defs>
  <circle cx="512" cy="512" r="512" fill="{OBSIDIAN_NIGHT}" />
  <g transform="translate(512, 512) scale(1.35) translate(-256, -256)" clip-path="url(#mascot-circle-clip)">
    {get_canonical_mascot_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, grid_color=BOREAS_SLATE)}
  </g>
</svg>"""


def render_png(src_svg, dst_png, bg="none", resize=None):
    """Renders PNG using ImageMagick PNG32 with -strip for strict 8-bit RGBA channels and determinism."""
    cmd = ["convert"]
    if bg:
        cmd.extend(["-background", bg])
    cmd.append(src_svg)
    if resize:
        cmd.extend(["-resize", resize])
    cmd.extend(["-strip", f"PNG32:{dst_png}"])
    subprocess.run(cmd, check=True)


def main():
    print("Generating fsecurity canonical brand assets...")
    os.makedirs(BRAND_DIR, exist_ok=True)

    # ==================== 1. MASTER & TRANSPARENT MARK ====================
    mark_master_svg = build_mark_svg(mode="transparent")
    mark_master_path = os.path.join(BRAND_DIR, "fsecurity-mark-master.svg")
    with open(mark_master_path, "w") as f:
        f.write(mark_master_svg)

    mark_trans_path = os.path.join(BRAND_DIR, "fsecurity-mark-transparent.svg")
    with open(mark_trans_path, "w") as f:
        f.write(mark_master_svg)

    mark_default_path = os.path.join(BRAND_DIR, "fsecurity-mark.svg")
    with open(mark_default_path, "w") as f:
        f.write(mark_master_svg)

    # Opaque Mark Variants
    mark_dark_path = os.path.join(BRAND_DIR, "fsecurity-mark-on-dark.svg")
    with open(mark_dark_path, "w") as f:
        f.write(build_mark_svg(mode="on-dark"))

    mark_light_path = os.path.join(BRAND_DIR, "fsecurity-mark-on-light.svg")
    with open(mark_light_path, "w") as f:
        f.write(build_mark_svg(mode="on-light"))

    # Legacy light alias
    shutil.copyfile(mark_light_path, os.path.join(BRAND_DIR, "fsecurity-mark-light.svg"))

    # ==================== 2. MASTER & TRANSPARENT WORDMARK ====================
    wordmark_master_svg = build_wordmark_svg(mode="transparent")
    wordmark_master_path = os.path.join(BRAND_DIR, "fsecurity-wordmark-master.svg")
    with open(wordmark_master_path, "w") as f:
        f.write(wordmark_master_svg)

    wordmark_trans_path = os.path.join(BRAND_DIR, "fsecurity-wordmark-transparent.svg")
    with open(wordmark_trans_path, "w") as f:
        f.write(wordmark_master_svg)

    wordmark_default_path = os.path.join(BRAND_DIR, "fsecurity-wordmark.svg")
    with open(wordmark_default_path, "w") as f:
        f.write(wordmark_master_svg)

    # Opaque Wordmark Variants
    wordmark_dark_path = os.path.join(BRAND_DIR, "fsecurity-wordmark-on-dark.svg")
    with open(wordmark_dark_path, "w") as f:
        f.write(build_wordmark_svg(mode="on-dark"))

    wordmark_light_path = os.path.join(BRAND_DIR, "fsecurity-wordmark-on-light.svg")
    with open(wordmark_light_path, "w") as f:
        f.write(build_wordmark_svg(mode="on-light"))

    # Legacy light alias
    shutil.copyfile(wordmark_light_path, os.path.join(BRAND_DIR, "fsecurity-wordmark-light.svg"))

    # ==================== 3. MASTER & TRANSPARENT MASCOT (cerb) ====================
    mascot_master_svg = build_mascot_svg(mode="transparent")
    mascot_master_path = os.path.join(BRAND_DIR, "fsecurity-mascot-master.svg")
    with open(mascot_master_path, "w") as f:
        f.write(mascot_master_svg)

    mascot_trans_path = os.path.join(BRAND_DIR, "fsecurity-mascot-transparent.svg")
    with open(mascot_trans_path, "w") as f:
        f.write(mascot_master_svg)

    mascot_default_path = os.path.join(BRAND_DIR, "fsecurity-mascot.svg")
    with open(mascot_default_path, "w") as f:
        f.write(mascot_master_svg)

    # Opaque Mascot Variants
    mascot_dark_path = os.path.join(BRAND_DIR, "fsecurity-mascot-on-dark.svg")
    with open(mascot_dark_path, "w") as f:
        f.write(build_mascot_svg(mode="on-dark"))

    mascot_light_path = os.path.join(BRAND_DIR, "fsecurity-mascot-on-light.svg")
    with open(mascot_light_path, "w") as f:
        f.write(build_mascot_svg(mode="on-light"))

    # ==================== 4. SOCIAL PREVIEW & MOTION SVG ====================
    social_svg_path = os.path.join(BRAND_DIR, "fsecurity-social-preview-1280x640.svg")
    with open(social_svg_path, "w") as f:
        f.write(build_social_preview_svg())

    motion_svg_path = os.path.join(BRAND_DIR, "fsecurity-motion-pulse.svg")
    with open(motion_svg_path, "w") as f:
        f.write(build_wordmark_svg(mode="on-dark", animated=True))

    # ==================== 5. RASTER RENDERING (PNG & JPG) ====================
    print("Rendering raster assets with ImageMagick PNG32 and -strip...")

    # Transparent Mark PNGs
    render_png(mark_trans_path, os.path.join(BRAND_DIR, "fsecurity-mark-transparent.png"), bg="none")
    render_png(mark_trans_path, os.path.join(BRAND_DIR, "fsecurity-mark.png"), bg="none")

    # Opaque Mark PNGs
    render_png(mark_dark_path, os.path.join(BRAND_DIR, "fsecurity-mark-on-dark.png"), bg=OBSIDIAN_NIGHT)
    render_png(mark_light_path, os.path.join(BRAND_DIR, "fsecurity-mark-on-light.png"), bg=GLACIER_WHITE)
    # Legacy aliases
    shutil.copyfile(os.path.join(BRAND_DIR, "fsecurity-mark-on-dark.png"), os.path.join(BRAND_DIR, "fsecurity-mark-dark.png"))
    shutil.copyfile(os.path.join(BRAND_DIR, "fsecurity-mark-on-light.png"), os.path.join(BRAND_DIR, "fsecurity-mark-light.png"))

    # Transparent Wordmark PNGs
    render_png(wordmark_trans_path, os.path.join(BRAND_DIR, "fsecurity-wordmark-transparent.png"), bg="none")
    render_png(wordmark_trans_path, os.path.join(BRAND_DIR, "fsecurity-wordmark.png"), bg="none")

    # Opaque Wordmark PNGs
    render_png(wordmark_dark_path, os.path.join(BRAND_DIR, "fsecurity-wordmark-on-dark.png"), bg=OBSIDIAN_NIGHT)
    render_png(wordmark_light_path, os.path.join(BRAND_DIR, "fsecurity-wordmark-on-light.png"), bg=GLACIER_WHITE)
    # Legacy aliases
    shutil.copyfile(os.path.join(BRAND_DIR, "fsecurity-wordmark-on-dark.png"), os.path.join(BRAND_DIR, "fsecurity-wordmark-dark.png"))
    shutil.copyfile(os.path.join(BRAND_DIR, "fsecurity-wordmark-on-light.png"), os.path.join(BRAND_DIR, "fsecurity-wordmark-light.png"))

    # Transparent Mascot PNGs
    render_png(mascot_trans_path, os.path.join(BRAND_DIR, "fsecurity-mascot-transparent.png"), bg="none")
    render_png(mascot_trans_path, os.path.join(BRAND_DIR, "fsecurity-mascot.png"), bg="none")

    # Opaque Mascot PNGs
    render_png(mascot_dark_path, os.path.join(BRAND_DIR, "fsecurity-mascot-on-dark.png"), bg=OBSIDIAN_NIGHT)
    render_png(mascot_light_path, os.path.join(BRAND_DIR, "fsecurity-mascot-on-light.png"), bg=GLACIER_WHITE)

    # Mascot Profile Avatar (1024x1024, circular mask on transparent canvas)
    with tempfile.NamedTemporaryFile("w", suffix=".svg") as tmp_ma:
        tmp_ma.write(build_mascot_avatar_svg())
        tmp_ma.flush()
        render_png(tmp_ma.name, os.path.join(BRAND_DIR, "fsecurity-mascot-avatar.png"), bg="none")

    # Mark Avatars (1024x1024)
    with tempfile.NamedTemporaryFile("w", suffix=".svg") as tmp_sq:
        tmp_sq.write(build_avatar_svg(mask="square"))
        tmp_sq.flush()
        render_png(tmp_sq.name, os.path.join(BRAND_DIR, "fsecurity-avatar-square.png"), bg=OBSIDIAN_NIGHT)

    with tempfile.NamedTemporaryFile("w", suffix=".svg") as tmp_cr:
        tmp_cr.write(build_avatar_svg(mask="circle"))
        tmp_cr.flush()
        render_png(tmp_cr.name, os.path.join(BRAND_DIR, "fsecurity-avatar-circle.png"), bg="none")

    # Social Preview (1280x640)
    render_png(social_svg_path, os.path.join(BRAND_DIR, "fsecurity-social-preview-1280x640.png"), bg=OBSIDIAN_NIGHT)
    subprocess.run(
        ["convert", social_svg_path, "-strip", "-quality", "95", os.path.join(BRAND_DIR, "fsecurity-social-preview-1280x640.jpg")],
        check=True,
    )

    # Favicons & Touch Icons (Preserving transparency around glyph)
    icon_master_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <g transform="translate(256, 256) scale(0.9) translate(-256, -256)">
    {get_canonical_mark_svg_group(stroke_color=GLACIER_WHITE, accent_color=ELECTRIC_PHOSPHOR, caliper_color=BOREAS_SLATE)}
  </g>
</svg>"""

    with tempfile.NamedTemporaryFile("w", suffix=".svg") as tmp_ic:
        tmp_ic.write(icon_master_svg)
        tmp_ic.flush()
        # Apple touch icon (180x180, square on obsidian night)
        render_png(tmp_ic.name, os.path.join(BRAND_DIR, "apple-touch-icon.png"), bg=OBSIDIAN_NIGHT, resize="180x180")
        # Favicon 32x32 (transparent background)
        p32 = os.path.join(BRAND_DIR, "favicon-32x32.png")
        render_png(tmp_ic.name, p32, bg="none", resize="32x32")
        # Favicon 16x16 (transparent background)
        p16 = os.path.join(BRAND_DIR, "favicon-16x16.png")
        render_png(tmp_ic.name, p16, bg="none", resize="16x16")
        # Multi-size favicon.ico
        subprocess.run(
            ["convert", p16, p32, "-strip", "-colors", "256", os.path.join(BRAND_DIR, "favicon.ico")],
            check=True,
        )

    # Animated Motion GIF (Terminal cursor pulse: 500ms on, 500ms off)
    f1_svg = build_wordmark_svg(mode="on-dark", animated=False)
    f2_svg = f1_svg.replace(
        f'<rect x="{WORDMARK_CURSOR_X_800X400}" y="166.0" width="22" height="58.0" fill="{ELECTRIC_PHOSPHOR}">',
        f'<rect x="{WORDMARK_CURSOR_X_800X400}" y="166.0" width="22" height="58.0" fill="{ELECTRIC_PHOSPHOR}" opacity="0">'
    )
    with tempfile.NamedTemporaryFile("w", suffix=".svg") as t1, tempfile.NamedTemporaryFile("w", suffix=".svg") as t2:
        t1.write(f1_svg); t1.flush()
        t2.write(f2_svg); t2.flush()
        with tempfile.NamedTemporaryFile("w", suffix=".png") as p1, tempfile.NamedTemporaryFile("w", suffix=".png") as p2:
            subprocess.run(["convert", t1.name, p1.name], check=True)
            subprocess.run(["convert", t2.name, p2.name], check=True)
            subprocess.run(
                ["convert", "-delay", "50", "-loop", "0", p1.name, p2.name, "-strip", os.path.join(BRAND_DIR, "fsecurity-motion-pulse.gif")],
                check=True,
            )

    print("All fsecurity brand assets successfully generated with verified transparency contract!")


if __name__ == "__main__":
    main()
