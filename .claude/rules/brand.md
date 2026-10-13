---
paths:
  - "assets/**"
---

# Scoped Rule: Brand & Visual Assets Integrity

1. **Color Token Fidelity:** Visual assets must strictly adhere to the approved fsecurity tactical brand palette:
   - Obsidian Night: `#080B10` (primary canvas / terminal backdrop / deep negative space)
   - Vault Charcoal: `#101520` (elevated surface panels / hardware base)
   - Boreas Slate: `#2E384D` (coordinate axes / caliper ticks / structural dividers)
   - Glacier White: `#E6EDF5` (vector strokes / typography / primary readouts)
   - Electric Phosphor: `#00F59B` (telemetry nodes / active authorization state / primary accent)
   - Cyber Azure: `#38BDF8` (secondary telemetry / protocol indicators)
2. **Dimension Standards:**
   - GitHub Social Preview: Strictly 1280 x 640 (2:1 aspect ratio).
   - Avatars and Icons: Strictly 1:1 aspect ratio (1024 x 1024 master, downscaled for 180 x 180, 32 x 32, 16 x 16).
   - Hero Artwork: 16:9 widescreen format.
3. **Canonical Geometry Invariant:** Every logo-bearing asset must derive from the master vector geometry in `assets/brand/fsecurity-mark-master.svg` via uniform scaling and translation. Never redraw or approximate the mark independently per asset.
4. **Vector Wordmark:** Brand-critical text must use frozen vector path outlines. Do not depend on runtime system fonts.
5. **Aesthetic Discipline:**
   - Prohibited: Generic AI SaaS purple or cyan gradients, 3D glossy spheres, cyber-skulls, neon matrix rain.
   - Required: Flat 2D vector clarity, high-contrast chiaroscuro photography, technical coordinate crosshairs.
