#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Furkan Köykıran
"""
scripts/verify_brand.py

Automated Brand System Verification Suite for fsecurity.
Enforces the 7 core brand invariants and the strict Transparency Contract:
1. Canonical Mark Geometry: all mark instances use the exact master coordinates without distortion.
2. Canonical Mascot Geometry: all mascot instances use the exact master coordinates of sentinel hound 'cerb'.
3. Uniform Transforms: all scaling is uniform (sx == sy), preserving angles and proportions.
4. Zero <text> Tags: brand-critical text is strictly frozen vector path outlines.
5. Avatar Mark Placement: square and circle avatars have mathematically identical mark placement.
6. Dimension and Format Integrity: all raster and vector assets match specified dimensions and valid XML.
7. Alpha & Transparency Contract:
   - Reusable mark, wordmark, and mascot transparent exports have alpha=0 corners and >20% transparent area.
   - Transparent SVGs contain NO full-canvas background <rect>.
   - Opaque exports (*-on-dark, *-on-light, avatars, social previews) have opaque corners and explicit backgrounds.
   - Circular avatars preserve transparent corner bounds around the circular badge.
   - Favicons preserve transparency for web bookmarks, while touch icons have solid backgrounds.
   - Every filename accurately communicates its background semantics.
"""

import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND_DIR = os.path.join(BASE_DIR, "assets", "brand")

# Canonical coordinate invariants - Mark
CANONICAL_F = "M 216 384 L 194 384 L 194 172 L 236 128 L 336 128 L 302 168 L 238 168 L 238 214 L 306 214 L 284 254 L 238 254 L 238 348 Z"
BASTION_CORNER_N = "M 216 68 L 256 44 L 296 68"
BASTION_CORNER_NE = "M 420 115 L 440 150 L 440 195"
BASTION_CORNER_SE = "M 440 317 L 440 362 L 420 397"
BASTION_CORNER_S = "M 296 444 L 256 468 L 216 444"
BASTION_CORNER_SW = "M 92 397 L 72 362 L 72 317"
BASTION_CORNER_NW = "M 72 195 L 72 150 L 92 115"
CALIPER_N = 'x1="256" y1="20" x2="256" y2="44"'
CALIPER_S = 'x1="256" y1="468" x2="256" y2="492"'
CALIPER_E = 'x1="440" y1="256" x2="464" y2="256"'
CALIPER_W = 'x1="48" y1="256" x2="72" y2="256"'
NODE_E = 'cx="396" cy="256" r="7"'
NODE_W = 'cx="116" cy="256" r="7"'

# Canonical coordinate invariants - Mascot 'cerb'
CERB_EAR_L = "M 176 190 L 140 68 L 208 124 Z"
CERB_EAR_R = "M 336 190 L 372 68 L 304 124 Z"
CERB_EAR_CHANNEL_L = 'x1="152" y1="98" x2="186" y2="148"'
CERB_EAR_CHANNEL_R = 'x1="360" y1="98" x2="326" y2="148"'
CERB_CROWN = "M 208 124 L 256 104 L 304 124 L 286 174 L 226 174 Z"
CERB_BROW_DIVIDER = 'x1="226" y1="174" x2="286" y2="174"'
CERB_VISOR = "M 168 186 L 344 186 L 332 232 L 180 232 Z"
CERB_VISOR_SCANNER = 'x="236" y="196" width="40" height="26"'
CERB_SNOUT = "M 214 232 L 214 336 L 256 374 L 298 336 L 298 232"
CERB_MANDIBLE_L = "M 180 250 L 198 320 L 224 354"
CERB_MANDIBLE_R = "M 332 250 L 314 320 L 288 354"
CERB_NOSE = 'd="M 242 328 L 256 342 L 270 328 Z"'
CERB_COLLAR_UPPER = "M 160 380 L 256 418 L 352 380"
CERB_COLLAR_LOWER = "M 160 412 L 256 450 L 352 412"
CERB_COLLAR_NODE = 'cx="256" cy="434" r="7"'
CERB_BASELINE = 'x1="80" y1="474" x2="432" y2="474"'


def verify_svg_xml_and_no_text():
    """Invariant 1: Valid XML and zero <text> tags in brand SVGs."""
    print("Checking Invariant 1: Valid XML and Zero <text> tags in brand SVGs...")
    svg_files = [f for f in sorted(os.listdir(BRAND_DIR)) if f.endswith(".svg")]
    if not svg_files:
        raise AssertionError("No SVG files found in assets/brand/")

    for f in svg_files:
        path = os.path.join(BRAND_DIR, f)
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except Exception as e:
            raise AssertionError(f"Invalid XML in {f}: {e}")

        text_elements = root.findall(".//{http://www.w3.org/2000/svg}text") + root.findall(".//text")
        if text_elements:
            raise AssertionError(
                f"Prohibited <text> element found in {f}. Brand SVGs must use frozen vector outlines."
            )
        print(f"  [PASS] {f}: valid XML, 0 <text> tags")


def verify_canonical_geometry():
    """Invariant 2: Canonical mark geometry exact coordinate match."""
    print("Checking Invariant 2: Canonical Mark Geometry exact coordinates...")
    mark_svgs = [
        "fsecurity-mark-master.svg",
        "fsecurity-mark.svg",
        "fsecurity-mark-transparent.svg",
        "fsecurity-mark-on-dark.svg",
        "fsecurity-mark-on-light.svg",
        "fsecurity-mark-light.svg",
        "fsecurity-wordmark-master.svg",
        "fsecurity-wordmark.svg",
        "fsecurity-wordmark-transparent.svg",
        "fsecurity-wordmark-on-dark.svg",
        "fsecurity-wordmark-on-light.svg",
        "fsecurity-wordmark-light.svg",
        "fsecurity-social-preview-1280x640.svg",
        "fsecurity-motion-pulse.svg",
    ]

    for f in mark_svgs:
        path = os.path.join(BRAND_DIR, f)
        with open(path, "r", encoding="utf-8") as fp:
            content = fp.read()

        if CANONICAL_F not in content:
            raise AssertionError(f"{f} missing canonical angular f coordinate!")
        if BASTION_CORNER_N not in content:
            raise AssertionError(f"{f} missing canonical bastion north bracket!")
        if BASTION_CORNER_NE not in content:
            raise AssertionError(f"{f} missing canonical bastion north-east bracket!")
        if BASTION_CORNER_SE not in content:
            raise AssertionError(f"{f} missing canonical bastion south-east bracket!")
        if BASTION_CORNER_S not in content:
            raise AssertionError(f"{f} missing canonical bastion south bracket!")
        if BASTION_CORNER_SW not in content:
            raise AssertionError(f"{f} missing canonical bastion south-west bracket!")
        if BASTION_CORNER_NW not in content:
            raise AssertionError(f"{f} missing canonical bastion north-west bracket!")
        if CALIPER_N not in content:
            raise AssertionError(f"{f} missing canonical north caliper tick!")
        if CALIPER_S not in content:
            raise AssertionError(f"{f} missing canonical south caliper tick!")
        if CALIPER_E not in content:
            raise AssertionError(f"{f} missing canonical east caliper tick!")
        if CALIPER_W not in content:
            raise AssertionError(f"{f} missing canonical west caliper tick!")
        if NODE_E not in content:
            raise AssertionError(f"{f} missing canonical east telemetry node!")
        if NODE_W not in content:
            raise AssertionError(f"{f} missing canonical west telemetry node!")

        print(f"  [PASS] {f}: exact canonical mark geometry verified")


def verify_mascot_geometry():
    """Invariant 3: Canonical mascot 'cerb' geometry coordinates."""
    print("Checking Invariant 3: Canonical Mascot 'cerb' Geometry exact coordinates...")
    mascot_svgs = [
        "fsecurity-mascot-master.svg",
        "fsecurity-mascot.svg",
        "fsecurity-mascot-transparent.svg",
        "fsecurity-mascot-on-dark.svg",
        "fsecurity-mascot-on-light.svg",
    ]

    for f in mascot_svgs:
        path = os.path.join(BRAND_DIR, f)
        with open(path, "r", encoding="utf-8") as fp:
            content = fp.read()

        if CERB_EAR_L not in content:
            raise AssertionError(f"{f} missing canonical mascot left ear!")
        if CERB_EAR_R not in content:
            raise AssertionError(f"{f} missing canonical mascot right ear!")
        if CERB_EAR_CHANNEL_L not in content:
            raise AssertionError(f"{f} missing canonical mascot left ear channel!")
        if CERB_EAR_CHANNEL_R not in content:
            raise AssertionError(f"{f} missing canonical mascot right ear channel!")
        if CERB_CROWN not in content:
            raise AssertionError(f"{f} missing canonical mascot cranial crown!")
        if CERB_BROW_DIVIDER not in content:
            raise AssertionError(f"{f} missing canonical mascot brow divider!")
        if CERB_VISOR not in content:
            raise AssertionError(f"{f} missing canonical mascot optical visor!")
        if CERB_VISOR_SCANNER not in content:
            raise AssertionError(f"{f} missing canonical mascot visor scanner band!")
        if CERB_SNOUT not in content:
            raise AssertionError(f"{f} missing canonical mascot snout contour!")
        if CERB_MANDIBLE_L not in content:
            raise AssertionError(f"{f} missing canonical mascot left mandible bracket!")
        if CERB_MANDIBLE_R not in content:
            raise AssertionError(f"{f} missing canonical mascot right mandible bracket!")
        if CERB_NOSE not in content:
            raise AssertionError(f"{f} missing canonical mascot nose sensor!")
        if CERB_COLLAR_UPPER not in content:
            raise AssertionError(f"{f} missing canonical mascot upper collar rim!")
        if CERB_COLLAR_LOWER not in content:
            raise AssertionError(f"{f} missing canonical mascot lower collar rim!")
        if CERB_COLLAR_NODE not in content:
            raise AssertionError(f"{f} missing canonical mascot collar telemetry node!")
        if CERB_BASELINE not in content:
            raise AssertionError(f"{f} missing canonical mascot baseline perch rule!")

        print(f"  [PASS] {f}: exact canonical mascot geometry verified")


def verify_uniform_transforms():
    """Invariant 4: All transforms on mark and mascot groups must be uniform scaling."""
    print("Checking Invariant 4: Uniform transforms only (no non-uniform stretching)...")
    for f in sorted(os.listdir(BRAND_DIR)):
        if not f.endswith(".svg"):
            continue
        path = os.path.join(BRAND_DIR, f)
        with open(path, "r", encoding="utf-8") as fp:
            content = fp.read()

        transforms = re.findall(r'transform="([^"]+)"', content)
        for t in transforms:
            scales = re.findall(r'scale\(([^)]+)\)', t)
            for sc in scales:
                parts = [p.strip() for p in sc.split(",")]
                if len(parts) == 2:
                    if float(parts[0]) != float(parts[1]):
                        raise AssertionError(
                            f"Non-uniform scale {sc} found in {f} transform: {t}"
                        )
        print(f"  [PASS] {f}: transforms are uniform")


def verify_avatar_parity():
    """Invariant 5: Square and circular avatars must have identical mark scale and placement."""
    print("Checking Invariant 5: Square and Circle avatar placement parity...")
    sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
    from generate_brand import build_avatar_svg

    sq_svg = build_avatar_svg(mask="square")
    cr_svg = build_avatar_svg(mask="circle")

    sq_match = re.search(r'<g transform="([^"]+)"', sq_svg)
    cr_match = re.search(r'<g transform="([^"]+)"', cr_svg)

    if not sq_match or not cr_match:
        raise AssertionError("Avatar mark transform group not found!")

    if sq_match.group(1) != cr_match.group(1):
        raise AssertionError(
            f"Avatar mark transforms differ!\nSquare: {sq_match.group(1)}\nCircle: {cr_match.group(1)}"
        )

    print(f"  [PASS] Avatar mark transforms match identically: {sq_match.group(1)}")


def verify_raster_dimensions():
    """Invariant 6: Raster dimensions match exact pixel specifications."""
    print("Checking Invariant 6: Raster dimensions match specifications...")
    expected_dims = {
        "fsecurity-social-preview-1280x640.png": "1280x640",
        "fsecurity-social-preview-1280x640.jpg": "1280x640",
        "fsecurity-avatar-square.png": "1024x1024",
        "fsecurity-avatar-circle.png": "1024x1024",
        "fsecurity-mascot-avatar.png": "1024x1024",
        "fsecurity-mark-transparent.png": "512x512",
        "fsecurity-mark.png": "512x512",
        "fsecurity-mark-on-dark.png": "512x512",
        "fsecurity-mark-dark.png": "512x512",
        "fsecurity-mark-on-light.png": "512x512",
        "fsecurity-mark-light.png": "512x512",
        "fsecurity-mascot-transparent.png": "512x512",
        "fsecurity-mascot.png": "512x512",
        "fsecurity-mascot-on-dark.png": "512x512",
        "fsecurity-mascot-on-light.png": "512x512",
        "fsecurity-wordmark-transparent.png": "800x400",
        "fsecurity-wordmark.png": "800x400",
        "fsecurity-wordmark-on-dark.png": "800x400",
        "fsecurity-wordmark-dark.png": "800x400",
        "fsecurity-wordmark-on-light.png": "800x400",
        "fsecurity-wordmark-light.png": "800x400",
        "apple-touch-icon.png": "180x180",
        "favicon-32x32.png": "32x32",
        "favicon-16x16.png": "16x16",
    }

    for filename, expected in expected_dims.items():
        path = os.path.join(BRAND_DIR, filename)
        if not os.path.exists(path):
            raise AssertionError(f"Missing raster file {filename}!")

        out = subprocess.check_output(["identify", "-format", "%wx%h", path]).decode().strip()
        if out != expected:
            raise AssertionError(
                f"Dimension mismatch for {filename}: expected {expected}, got {out}"
            )
        print(f"  [PASS] {filename}: {out} (matches {expected})")

    ico_path = os.path.join(BRAND_DIR, "favicon.ico")
    if not os.path.exists(ico_path) or os.path.getsize(ico_path) == 0:
        raise AssertionError("favicon.ico is missing or empty!")
    print(f"  [PASS] favicon.ico: present ({os.path.getsize(ico_path)} bytes)")

    gif_path = os.path.join(BRAND_DIR, "fsecurity-motion-pulse.gif")
    if not os.path.exists(gif_path) or os.path.getsize(gif_path) == 0:
        raise AssertionError("fsecurity-motion-pulse.gif is missing or empty!")
    print(f"  [PASS] fsecurity-motion-pulse.gif: present ({os.path.getsize(gif_path)} bytes)")


def verify_transparency_contract():
    """Invariant 7: Rigorous Transparency and Alpha Semantics Contract."""
    print("Checking Invariant 7: Transparency and Alpha Semantics Contract...")

    # 1. Transparent PNG exports must have alpha=0 corner pixels and meaningful transparency area (> 20%)
    transparent_pngs = [
        "fsecurity-mark-transparent.png",
        "fsecurity-mark.png",
        "fsecurity-wordmark-transparent.png",
        "fsecurity-wordmark.png",
        "fsecurity-mascot-transparent.png",
        "fsecurity-mascot.png",
        "favicon-32x32.png",
        "favicon-16x16.png",
    ]

    for fname in transparent_pngs:
        path = os.path.join(BRAND_DIR, fname)
        if not os.path.exists(path):
            raise AssertionError(f"Missing transparent PNG {fname}")

        corner_cmd = [
            "convert", path,
            "-format", "%[pixel:p{0,0}] %[pixel:p{w-1,0}] %[pixel:p{0,h-1}] %[pixel:p{w-1,h-1}]",
            "info:"
        ]
        corners = subprocess.check_output(corner_cmd).decode().strip().split()
        for i, c in enumerate(corners):
            if not (",0)" in c or c == "none" or ",0.0)" in c):
                raise AssertionError(
                    f"{fname}: Corner {i} is not transparent! Value: {c}"
                )

        ratio_cmd = [
            "convert", path,
            "-alpha", "extract",
            "-format", "%[fx:1.0 - mean]",
            "info:"
        ]
        ratio_str = subprocess.check_output(ratio_cmd).decode().strip()
        trans_ratio = float(ratio_str)
        if trans_ratio < 0.20:
            raise AssertionError(
                f"{fname}: Transparency ratio too low ({trans_ratio:.2%}), expected > 20% transparent canvas"
            )

        print(f"  [PASS] Transparent PNG {fname}: alpha=0 on all corners, {trans_ratio:.1%} transparent canvas")

    # 2. Circular avatar badges: transparent corner bounding box, solid opaque disc center
    circular_avatars = [
        "fsecurity-avatar-circle.png",
        "fsecurity-mascot-avatar.png",
    ]

    for fname in circular_avatars:
        path = os.path.join(BRAND_DIR, fname)
        if not os.path.exists(path):
            raise AssertionError(f"Missing circular avatar {fname}")

        # Corners must be transparent
        corner_cmd = [
            "convert", path,
            "-format", "%[pixel:p{0,0}] %[pixel:p{w-1,0}] %[pixel:p{0,h-1}] %[pixel:p{w-1,h-1}]",
            "info:"
        ]
        corners = subprocess.check_output(corner_cmd).decode().strip().split()
        for i, c in enumerate(corners):
            if not (",0)" in c or c == "none" or ",0.0)" in c):
                raise AssertionError(
                    f"{fname}: Avatar outer corner {i} is not transparent! Value: {c}"
                )

        # Center disc must be solid
        center_cmd = ["convert", path, "-format", "%[pixel:p{512,512}]", "info:"]
        center_px = subprocess.check_output(center_cmd).decode().strip()
        if ",0)" in center_px or center_px == "none":
            raise AssertionError(
                f"{fname}: Avatar center pixel is not opaque! Value: {center_px}"
            )

        print(f"  [PASS] Circular avatar {fname}: transparent canvas corners, solid badge interior")

    # 3. Opaque PNG / JPG exports must have opaque corner pixels (alpha=1)
    opaque_rasters = [
        "fsecurity-mark-on-dark.png",
        "fsecurity-mark-dark.png",
        "fsecurity-mark-on-light.png",
        "fsecurity-mark-light.png",
        "fsecurity-wordmark-on-dark.png",
        "fsecurity-wordmark-dark.png",
        "fsecurity-wordmark-on-light.png",
        "fsecurity-wordmark-light.png",
        "fsecurity-mascot-on-dark.png",
        "fsecurity-mascot-on-light.png",
        "fsecurity-avatar-square.png",
        "fsecurity-social-preview-1280x640.png",
        "fsecurity-social-preview-1280x640.jpg",
        "apple-touch-icon.png",
    ]

    for fname in opaque_rasters:
        path = os.path.join(BRAND_DIR, fname)
        if not os.path.exists(path):
            raise AssertionError(f"Missing opaque raster {fname}")

        corner_cmd = [
            "convert", path,
            "-format", "%[pixel:p{0,0}] %[pixel:p{w-1,0}] %[pixel:p{0,h-1}] %[pixel:p{w-1,h-1}]",
            "info:"
        ]
        corners = subprocess.check_output(corner_cmd).decode().strip().split()
        for i, c in enumerate(corners):
            if ",0)" in c or c == "none":
                raise AssertionError(
                    f"{fname}: Opaque file has unexpected transparent corner {i}! Value: {c}"
                )

        print(f"  [PASS] Opaque raster {fname}: solid corner pixels confirmed ({corners[0]})")

    # 4. Transparent SVGs must NOT contain full-canvas background rects
    transparent_svgs = [
        "fsecurity-mark-master.svg",
        "fsecurity-mark.svg",
        "fsecurity-mark-transparent.svg",
        "fsecurity-wordmark-master.svg",
        "fsecurity-wordmark.svg",
        "fsecurity-wordmark-transparent.svg",
        "fsecurity-mascot-master.svg",
        "fsecurity-mascot.svg",
        "fsecurity-mascot-transparent.svg",
    ]

    for fname in transparent_svgs:
        path = os.path.join(BRAND_DIR, fname)
        tree = ET.parse(path)
        root = tree.getroot()

        svg_w = root.get("width")
        svg_h = root.get("height")

        rects = root.findall("{http://www.w3.org/2000/svg}rect") + root.findall("rect")
        for r in rects:
            rw = r.get("width")
            rh = r.get("height")
            if rw in ("100%", svg_w) and rh in ("100%", svg_h):
                raise AssertionError(
                    f"Transparent SVG {fname} contains prohibited full-canvas background rect ({rw}x{rh})!"
                )

        print(f"  [PASS] Transparent SVG {fname}: zero background rects, genuinely transparent canvas")

    # 5. Opaque SVGs must contain explicit background rects
    opaque_svgs = [
        "fsecurity-mark-on-dark.svg",
        "fsecurity-mark-on-light.svg",
        "fsecurity-mark-light.svg",
        "fsecurity-wordmark-on-dark.svg",
        "fsecurity-wordmark-on-light.svg",
        "fsecurity-wordmark-light.svg",
        "fsecurity-mascot-on-dark.svg",
        "fsecurity-mascot-on-light.svg",
        "fsecurity-social-preview-1280x640.svg",
    ]

    for fname in opaque_svgs:
        path = os.path.join(BRAND_DIR, fname)
        tree = ET.parse(path)
        root = tree.getroot()

        svg_w = root.get("width")
        svg_h = root.get("height")

        rects = root.findall("{http://www.w3.org/2000/svg}rect") + root.findall("rect")
        has_bg = any(
            (r.get("width") in ("100%", svg_w) and r.get("height") in ("100%", svg_h))
            for r in rects
        )
        if not has_bg:
            raise AssertionError(
                f"Opaque SVG {fname} missing required full-canvas background rect!"
            )

        print(f"  [PASS] Opaque SVG {fname}: explicit full-canvas background rect confirmed")


def main():
    print("==================================================")
    print("Running fsecurity Brand System Verification Suite")
    print("==================================================")
    try:
        verify_svg_xml_and_no_text()
        verify_canonical_geometry()
        verify_mascot_geometry()
        verify_uniform_transforms()
        verify_avatar_parity()
        verify_raster_dimensions()
        verify_transparency_contract()
        print("==================================================")
        print("ALL BRAND INVARIANTS VERIFIED SUCCESSFULLY (100% PASS)")
        print("==================================================")
    except AssertionError as e:
        print(f"\n[FAIL] Assertion Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

