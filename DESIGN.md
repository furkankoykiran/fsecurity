# fsecurity Visual Identity and Design System Specification

```
|=-----------------------------------------------------------------------------------=|
|  SPEC: VISUAL-FOUNDATION-V1.2  |  STATUS: CANONICAL  |  AUTH: fsecurity CORE       |
|=-----------------------------------------------------------------------------------=|
```

---

## 1. Aesthetic Direction and Principles

`fsecurity` is engineered for security researchers, penetration testers, and security engineers who value technical depth, terminal ergonomics, and explicit operational agency. Modern cybersecurity tooling often obscures critical network state with bloated desktop wrappers, noisy graphs, and speculative automation. `fsecurity` takes the opposite approach.

The visual system is built on five core principles:

1. **Monospace Purity:** Structural character framing, aligned columns, and fixed-width typography over decorative embellishment.
2. **Radical Reduction:** Removing unnecessary chrome and visual noise. Every coordinate tick, bounding caliper, and telemetry node communicates active authorization and machine state.
3. **Native Fidelity:** Treating typography, contrast, and layout as precision systems engineering rather than marketing decoration.
4. **Industrial Precision:** Mathematical grid logic, engineering calipers, coordinate registration marks, and disciplined negative space.
5. **High-Contrast Chiaroscuro:** Deep Obsidian Night backgrounds paired with crisp Glacier White linework and Electric Phosphor / Cyber Azure telemetry accents.

### Boundaries
* No generic AI gradients: No pastel purple or cyan fades, glossy spheres, or soft squircle cards.
* No cyberpunk clichés: No simulated matrix rain, cartoon skulls, or fake hacker clutter.
* No speculative claims: The design reflects an authorized autonomous cybersecurity harness, not a fictional cyber weapon.

---

## 2. Color System

A strict six-token tactical palette with high contrast and zero chromatic noise, rooted in the `ftools` family base system while establishing fsecurity's distinct defensive identity:

```
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
|  OBSIDIAN NIGHT   |  VAULT CHARCOAL   |   BOREAS SLATE    |   GLACIER WHITE   | ELECTRIC PHOSPHOR |    CYBER AZURE    |
|      #080B10      |      #101520      |      #2E384D      |      #E6EDF5      |      #00F59B      |      #38BDF8      |
|  [Canvas Base]    | [Surface Panels]  | [Grid / Caliper]  |  [Type / Vector]  | [Telemetry Node]  | [Protocol Signal] |
+-------------------+-------------------+-------------------+-------------------+-------------------+-------------------+
```

### Color Tokens
| Name | Hex | Semantic Role | Contrast (vs Obsidian Night) |
| :--- | :--- | :--- | :--- |
| **Obsidian Night** | `#080B10` | Primary canvas, terminal background, negative space | Base (1:1) |
| **Vault Charcoal** | `#101520` | Elevated cards, hardware surfaces, modal backgrounds | 1.2:1 |
| **Boreas Slate** | `#2E384D` | Coordinate axes, dimension ticks, structural dividers | 4.6:1 (AA Large) |
| **Glacier White** | `#E6EDF5` | Primary headlines, monospaced vector linework, readouts | 17.5:1 (AAA) |
| **Electric Phosphor** | `#00F59B` | Active telemetry node, authorized perimeter status, primary accent | 14.8:1 (AAA) |
| **Cyber Azure** | `#38BDF8` | Secondary telemetry, protocol indicators, diagnostic highlights | 9.8:1 (AAA) |

---

## 3. Typography System

The typography is engineered for legibility, fixed-grid alignment, and technical authority.

### Monospace (Primary Engine)
* **Recommended Typefaces:** Berkeley Mono, JetBrains Mono, IBM Plex Mono, or Cascadia Code.
* **System Fallback Stack:** `ui-monospace, SFMono-Regular, "Roboto Mono", Menlo, Monaco, Consolas, monospace`.
* **Characteristics:** Slashed zero (`0`), sharp brackets (`[`, `]`), angular serifs on `f` and `l`.

### Display and Section Framing
* **Recommended Typefaces:** High-contrast grotesque sans-serif in uppercase (Inter, Helvetica Neue, Chivo Mono).
* **Letterspacing:** `+0.12em` to `+0.2em` wide tracking for section tags and coordinate headers.
* **Usage:** Status readouts, coordinates, and phase indicators (for example: `[STATUS: PHASE 0 FOUNDATION]`).

---

## 4. Canonical Mark Geometry: The Bastion Reticle

The primary emblem is **The Bastion Reticle**. It encloses the single invariant inherited from the `ftools` family lineage—the canonical lowercase `f` glyph—within an original, mathematical cybersecurity defense perimeter.

```
                     +---[ CALIPER N ]---+
                     |      256, 20      |
                     |         |         |
                     |     /-- 256, 44 --\
                 [NW] \   /               \   / [NE]
                       \ /                 \ /
                        |   /===========\   |
      [CALIPER W]       |  /   /--------/   |       [CALIPER E]
    48,256 --- 72,256   | /   /             |   440,256 --- 464,256
         (O)            | |  +----------\   |            (O)
     [NODE WEST]        | |  |  +-------/   |        [NODE EAST]
       116, 256         | |  |  |           |          396, 256
                        | |  \---\          |
                       / \ \-----/         / \
                 [SW] /   \               /   \ [SE]
                     |     \-- 256, 468 -/     |
                     |         |         |
                     |      256, 492     |
                     +---[ CALIPER S ]---+
```

### Components of the Bastion Reticle
1. **The Shared ftools Invariant (Canonical `f`):** Razor-cut angular glyph carrying the exact lineage of the family mark, centered within the coordinate space.
2. **Segmented Hexagonal Bastion Perimeter:** Six faceted corner brackets forming an outer defensive bastion ring:
   - **North (`N`):** `M 216 68 L 256 44 L 296 68`
   - **North-East (`NE`):** `M 420 115 L 440 150 L 440 195`
   - **South-East (`SE`):** `M 440 317 L 440 362 L 420 397`
   - **South (`S`):** `M 296 444 L 256 468 L 216 444`
   - **South-West (`SW`):** `M 92 397 L 72 362 L 72 317`
   - **North-West (`NW`):** `M 72 195 L 72 150 L 92 115`
3. **Cardinal Caliper Ticks:** Orthogonal engineering caliper rules at cardinal points:
   - **North Caliper:** Line from `(256, 20)` to `(256, 44)`
   - **South Caliper:** Line from `(256, 468)` to `(256, 492)`
   - **East Caliper:** Line from `(440, 256)` to `(464, 256)`
   - **West Caliper:** Line from `(48, 256)` to `(72, 256)`
4. **Electric Phosphor Telemetry Nodes:** Circular verification nodes indicating active perimeter monitoring and authorized testing bounds:
   - **East Telemetry Node:** Circle centered at `(396, 256)` with radius `7` (`#00F59B`)
   - **West Telemetry Node:** Circle centered at `(116, 256)` with radius `7` (`#00F59B`)

### Mathematical Source of Truth
All mark instances derive from [`assets/brand/fsecurity-mark-master.svg`](assets/brand/fsecurity-mark-master.svg) defined in a 512x512 coordinate space:

* **Canonical f Glyph:** `M 216 384 L 194 384 L 194 172 L 236 128 L 336 128 L 302 168 L 238 168 L 238 214 L 306 214 L 284 254 L 238 254 L 238 348 Z` (stroke-width 14)
* **Bastion Perimeter Brackets:** 6 corner brackets defined by the coordinates above (stroke-width 14, stroke-linecap `square`, stroke-linejoin `miter`)
* **Cardinal Calipers:** 4 line segments at cardinal axes (stroke-width 6, stroke-linecap `square`)
* **Telemetry Nodes:** 2 circles at `(396, 256)` and `(116, 256)` filled with Electric Phosphor (`#00F59B`)

### Deterministic Wordmark Outlines
Brand-critical typography in [`assets/brand/fsecurity-wordmark-master.svg`](assets/brand/fsecurity-wordmark-master.svg) is frozen into vector path outlines. It does not depend on system fonts. Every variant derives from this master file via uniform scaling and translation.

---

## 5. Canonical Mascot: cerb (The Bastion Sentinel Hound)

Developer tools earn cultural resonance when they possess an authentic, memorable companion. `cerb` is an original cybernetic sentinel hound constructed entirely from terminal character geometry and perimeter defense iconography.

```
                      /\                     /\
                     /  \                   /  \
                    / |  \                 /  | \
                   /  |   \_______________/   |  \
                  |   |    \             /    |   |
                  |   |     |---[===]---|     |   |
                  |          \_________/          |
                   \                             /
                    \      +-------------+      /
                     \     |[===========]|     /
                      \    +-------------+    /
                       \      \       /      /
                        \      \  V  /      /
                         \______\___/______/
                             |  ( O )  |
                        =====+=========+=====
```

### Anatomical Grammar
* **Radar Ears:** Dual faceted angular scanning ears (`CERB_EAR_L`: `M 176 190 L 140 68 L 208 124 Z`, `CERB_EAR_R`: `M 336 190 L 372 68 L 304 124 Z`) with inner telemetry channels (`x1="152" y1="98" x2="186" y2="148"`, `x1="360" y1="98" x2="326" y2="148"`).
* **Cranial Crown & Brow Divider:** Faceted skull plate (`M 208 124 L 256 104 L 304 124 L 286 174 L 226 174 Z`) and horizontal brow divider (`x1="226" y1="174" x2="286" y2="174"`).
* **Transverse Optical Scanner Visor:** Panoramic sensor visor (`M 168 186 L 344 186 L 332 232 L 180 232 Z`) housing an active Electric Phosphor scanner band (`x="236" y="196" width="40" height="26"` fill `#00F59B`).
* **Snout & Faceted Mandibles:** Articulated muzzle line (`M 214 232 L 214 336 L 256 374 L 298 336 L 298 232`), left mandible (`M 180 250 L 198 320 L 224 354`), right mandible (`M 332 250 L 314 320 L 288 354`), and triangular olfactory sensor (`d="M 242 328 L 256 342 L 270 328 Z"`).
* **Tactical Collar & Perimeter Telemetry Node:** Dual-band armored collar (`M 160 380 L 256 418 L 352 380`, `M 160 412 L 256 450 L 352 412`) centered with an Electric Phosphor node (`cx="256" cy="434" r="7"`).
* **Terminal Baseline Perch:** Dashed monospaced terminal baseline rule from `(80, 474)` to `(432, 474)`.

### Operational Role
In the runtime architecture, `cerb` serves as the visible agent state indicator:
* **Idle / Scope Validation:** Optical visor scanner pulses at 1.0 Hz cadence.
* **Perimeter Scanning:** Ear telemetry channels and snout scanner illuminate during reconnaissance mapping.
* **Sandbox Execution:** Collar telemetry node glows during ephemeral sandbox probe cycles.
* **Scope Enforced:** Scanner band locks solid Electric Phosphor upon successful verified assessment delivery.

---

## 6. The Transparency Contract

To eliminate asset friction across dark mode, light mode, website documentation, and social embeds, `fsecurity` enforces the strict `ftools` Transparency Contract:

### Rules of Canvas Transparency
1. **Reusable Transparent Exports:** Standalone marks, wordmarks, and mascot assets (`*-transparent.svg`, `*-transparent.png`, `fsecurity-mark.svg`, `fsecurity-wordmark.svg`, `fsecurity-mascot.svg`) MUST have genuinely transparent canvases.
2. **Zero SVG Background Rects:** Transparent SVGs must contain no full-canvas background rect elements.
3. **Corner Alpha Invariant:** Transparent PNG exports must have `alpha = 0` across all four corner pixels and maintain over 20% transparent area.
4. **Opaque Ground Variants:** Variants tagged `*-on-dark` or `*-on-light` must contain explicit, solid background rects (`#080B10` or `#E6EDF5`).
5. **Circular Avatars:** Avatars with circular badges preserve transparent corner bounds outside the circular mask for seamless integration into host platforms.
6. **Filename Semantics:** Every asset filename must communicate its background contract unambiguously.

---

## 7. Asset Generation and Verification Tooling

Brand integrity is guaranteed by automated code rather than manual export pipelines:

* **Generator Script:** [`scripts/generate_brand.py`](scripts/generate_brand.py) generates all derivative SVGs, PNGs, avatars, favicons, and motion assets directly from master vector geometry.
* **Verification Suite:** [`scripts/verify_brand.py`](scripts/verify_brand.py) tests all seven core invariants:
  1. **Canonical Mark Geometry:** Exact coordinate matches for the Bastion Reticle and canonical `f`.
  2. **Canonical Mascot Geometry:** Exact coordinate matches for `cerb` anatomical components.
  3. **Uniform Transforms:** Prohibits non-uniform aspect scaling.
  4. **Zero `<text>` Tags:** Guarantees frozen vector outlines across all SVGs.
  5. **Avatar Placement Parity:** Exact coordinate and scale match between square and circular avatars.
  6. **Dimension and Format Integrity:** Pixel-perfect dimensions and valid XML.
  7. **Transparency and Alpha Contract:** Automated corner alpha checks, transparent area ratio verification, and background rect validation.

---

## 8. Usage Rules, Clear Space, and Motion Language

### Clear Space
The minimum clear space surrounding the mark must equal at least half the width of the outer bastion bracket on all sides. No text, decorative borders, or third-party marks may intrude into this zone.

### Avatars
* **Square Mark Profile (GitHub organizations, Slack):** [`assets/brand/fsecurity-avatar-square.png`](assets/brand/fsecurity-avatar-square.png) (1024x1024).
* **Circular Mark Profile (Discord, X):** [`assets/brand/fsecurity-avatar-circle.png`](assets/brand/fsecurity-avatar-circle.png) (1024x1024).
* **Mascot Avatar Profile:** [`assets/brand/fsecurity-mascot-avatar.png`](assets/brand/fsecurity-mascot-avatar.png) (1024x1024).

### Motion Cadence
Terminal motion is strictly digital with zero spring physics or interpolation blur:
* **Cadence:** Exactly 1.0 Hz (1000ms loop).
* **Duty Cycle:** 500ms active node visible (`#00F59B`), 500ms dimmed.
* **Easing:** `step-end` instantaneous transition.
* **Reference Asset:** [`assets/brand/fsecurity-motion-pulse.gif`](assets/brand/fsecurity-motion-pulse.gif) and [`assets/brand/fsecurity-motion-pulse.svg`](assets/brand/fsecurity-motion-pulse.svg).

---

## 9. Inventory of Brand Assets

All official brand assets reside in [`assets/brand/`](assets/brand/):

### Master Definitions
* [`fsecurity-mark-master.svg`](assets/brand/fsecurity-mark-master.svg): Canonical master vector mark on transparent canvas (512x512).
* [`fsecurity-wordmark-master.svg`](assets/brand/fsecurity-wordmark-master.svg): Canonical master wordmark lockup on transparent canvas (800x400).
* [`fsecurity-mascot-master.svg`](assets/brand/fsecurity-mascot-master.svg): Canonical master mascot vector (`cerb`) on transparent canvas (512x512).

### Transparent Exports
* [`fsecurity-mark.svg`](assets/brand/fsecurity-mark.svg), [`fsecurity-mark-transparent.svg`](assets/brand/fsecurity-mark-transparent.svg): Mark vector on transparent canvas.
* [`fsecurity-mark.png`](assets/brand/fsecurity-mark.png), [`fsecurity-mark-transparent.png`](assets/brand/fsecurity-mark-transparent.png): 512x512 mark raster on transparent canvas.
* [`fsecurity-wordmark.svg`](assets/brand/fsecurity-wordmark.svg), [`fsecurity-wordmark-transparent.svg`](assets/brand/fsecurity-wordmark-transparent.svg): Wordmark vector on transparent canvas.
* [`fsecurity-wordmark.png`](assets/brand/fsecurity-wordmark.png), [`fsecurity-wordmark-transparent.png`](assets/brand/fsecurity-wordmark-transparent.png): 800x400 wordmark raster on transparent canvas.
* [`fsecurity-mascot.svg`](assets/brand/fsecurity-mascot.svg), [`fsecurity-mascot-transparent.svg`](assets/brand/fsecurity-mascot-transparent.svg): Mascot vector on transparent canvas.
* [`fsecurity-mascot.png`](assets/brand/fsecurity-mascot.png), [`fsecurity-mascot-transparent.png`](assets/brand/fsecurity-mascot-transparent.png): 512x512 mascot raster on transparent canvas.
* [`favicon-32x32.png`](assets/brand/favicon-32x32.png), [`favicon-16x16.png`](assets/brand/favicon-16x16.png): Web favicons with transparent backgrounds.

### Opaque Ground Exports
* [`fsecurity-mark-on-dark.svg`](assets/brand/fsecurity-mark-on-dark.svg), [`fsecurity-mark-on-dark.png`](assets/brand/fsecurity-mark-on-dark.png): 512x512 mark on Obsidian Night with engineering grid framing.
* [`fsecurity-mark-on-light.svg`](assets/brand/fsecurity-mark-on-light.svg), [`fsecurity-mark-on-light.png`](assets/brand/fsecurity-mark-on-light.png): 512x512 mark on Glacier White for light documentation.
* [`fsecurity-wordmark-on-dark.svg`](assets/brand/fsecurity-wordmark-on-dark.svg), [`fsecurity-wordmark-on-dark.png`](assets/brand/fsecurity-wordmark-on-dark.png): 800x400 wordmark on Obsidian Night.
* [`fsecurity-wordmark-on-light.svg`](assets/brand/fsecurity-wordmark-on-light.svg), [`fsecurity-wordmark-on-light.png`](assets/brand/fsecurity-wordmark-on-light.png): 800x400 wordmark on Glacier White.
* [`fsecurity-mascot-on-dark.svg`](assets/brand/fsecurity-mascot-on-dark.svg), [`fsecurity-mascot-on-dark.png`](assets/brand/fsecurity-mascot-on-dark.png): 512x512 mascot on Obsidian Night.
* [`fsecurity-mascot-on-light.svg`](assets/brand/fsecurity-mascot-on-light.svg), [`fsecurity-mascot-on-light.png`](assets/brand/fsecurity-mascot-on-light.png): 512x512 mascot on Glacier White.
* [`fsecurity-social-preview-1280x640.png`](assets/brand/fsecurity-social-preview-1280x640.png), [`fsecurity-social-preview-1280x640.jpg`](assets/brand/fsecurity-social-preview-1280x640.jpg): 1280x640 GitHub social preview.
* [`apple-touch-icon.png`](assets/brand/apple-touch-icon.png): 180x180 solid iOS/macOS web clip icon.

### Profile Avatars and Animation
* [`fsecurity-avatar-square.png`](assets/brand/fsecurity-avatar-square.png): 1024x1024 square mark avatar.
* [`fsecurity-avatar-circle.png`](assets/brand/fsecurity-avatar-circle.png): 1024x1024 circular mark badge on transparent canvas.
* [`fsecurity-mascot-avatar.png`](assets/brand/fsecurity-mascot-avatar.png): 1024x1024 circular mascot badge on transparent canvas.
* [`fsecurity-motion-pulse.gif`](assets/brand/fsecurity-motion-pulse.gif): 1.0s loop terminal telemetry animation.
* [`fsecurity-motion-pulse.svg`](assets/brand/fsecurity-motion-pulse.svg): Pure vector animated SVG with CSS keyframe pulse.
* [`favicon.ico`](assets/brand/favicon.ico): Multi-resolution container icon.

### Atmospheric and Concept Visuals ([`assets/atmospheric/`](assets/atmospheric/))
* [`fsecurity-hero-workspace.jpg`](assets/atmospheric/fsecurity-hero-workspace.jpg): 1920x1080 terminal UI product concept preview illustrating target scope validation, scanner orchestration, vulnerability proof, and rate-limit monitoring.
* [`fsecurity-architecture-harness.jpg`](assets/atmospheric/fsecurity-architecture-harness.jpg): 16:9 systems engineering diagram illustrating the scope-synthesized security harness pipeline.

