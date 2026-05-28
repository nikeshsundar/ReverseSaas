---
name: ReverseSaaS Visual Language
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#bbcabf'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#86948a'
  outline-variant: '#3c4a42'
  surface-tint: '#4edea3'
  primary: '#4edea3'
  on-primary: '#003824'
  primary-container: '#10b981'
  on-primary-container: '#00422b'
  inverse-primary: '#006c49'
  secondary: '#89ceff'
  on-secondary: '#00344d'
  secondary-container: '#00a2e6'
  on-secondary-container: '#00344e'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#e29100'
  on-tertiary-container: '#523200'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6ffbbe'
  primary-fixed-dim: '#4edea3'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005236'
  secondary-fixed: '#c9e6ff'
  secondary-fixed-dim: '#89ceff'
  on-secondary-fixed: '#001e2f'
  on-secondary-fixed-variant: '#004c6e'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-base:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-page: 40px
  panel-padding: 16px
  stack-gap: 8px
---

## Brand & Style

The design system is engineered for high-performance reverse-engineering, blending the technical density of developer tools with the premium, atmospheric aesthetics of modern gaming interfaces. The personality is "Tactical Intelligence"—sophisticated, precise, and authoritative.

The aesthetic fuses **Glassmorphism** with **Technical Minimalism**. It utilizes deep obsidian surfaces, high-fidelity backdrop blurs, and hyper-thin borders to create a sense of infinite depth. The "Obsidian Minecraft" influence manifests through subtle geometric patterns and "voxel" elevation—where elements feel like floating monolithic slabs. The experience is designed to feel like a high-end command center: dark, focused, and powerful.

## Colors

The palette is strictly dark-mode, anchored by a "True Obsidian" base. 

- **Base Layer:** `#050505` serves as the canvas, providing maximum contrast for glass effects.
- **Surface Layer:** `#0a0a0a` is used for elevated panels and containers.
- **Accents:** Emerald Green is the primary action color (Success/Active), Diamond Blue is for secondary telemetry (Info/Selection), and Gold is reserved for critical insights or "Premium" discoveries.
- **Borders:** Surfaces are defined by 1px "Glass" borders (white at 8-12% opacity) rather than solid colors, allowing background textures to bleed through the edges.

## Typography

Typography follows a dual-purpose hierarchy: **Inter** handles the interface logic and structural hierarchy, while **JetBrains Mono** is utilized for all data-driven, terminal, and metadata elements.

- **Inter:** Used for all navigation, headings, and descriptive text. Weights should stay between 400 and 700.
- **JetBrains Mono:** Applied to ID strings, hex codes, code snippets, and utility labels. This reinforces the "Developer Tool" utility.
- **Hierarchy:** High contrast in size is used for "Discovery" screens, while dense, tightly-packed JetBrains Mono is preferred for "Analysis" views.

## Layout & Spacing

The layout uses a **Strict Grid System** inspired by technical blueprints. 

- **Grid:** A 12-column fluid grid for main content areas, with fixed-width sidebars (typically 240px or 280px) for navigation and inspection panels.
- **Rhythm:** An 8px linear scale (referenced as units of 4px) ensures alignment across dense data tables and complex forms.
- **Reflow:** On mobile, sidebars collapse into a bottom-anchored "Command Bar," and complex data tables transition into "Voxel Cards" that stack vertically.

## Elevation & Depth

Depth is the core differentiator of this design system. It uses a **Multi-Layer Glass** approach:

1.  **Level 0 (Floor):** Pure `#050505` with a subtle 32px grid pattern (1% opacity white).
2.  **Level 1 (Panels):** `#0a0a0a` with a 12px backdrop blur and a 1px inner glass border.
3.  **Level 2 (Floating/Modals):** Subtle translucency (85% opacity) with a "Voxel Shadow"—a high-fidelity, multi-stage shadow that feels heavy and grounded.
4.  **Interaction Glows:** Active elements emit a soft, 20px radius outer glow in the primary accent color (Emerald or Diamond) at very low opacity (10%), simulating a powered-on hardware light.

## Shapes

The shape language is "Precision-Cut." We avoid high-radius "pill" shapes to maintain a professional, architectural feel. 

- **Corners:** A consistent `0.25rem` (4px) radius is applied to almost all containers and buttons. This creates a "softened-sharp" look.
- **45-Degree Accents:** Use 45-degree chamfered edges on decorative elements, such as tag corners or "active" indicators on tabs, to evoke the pixel-geometric aesthetic without being literal "blocks."

## Components

- **Buttons:** Primary buttons use a solid Emerald fill with black text. Secondary buttons are "Ghost" style: 1px glass borders with no fill until hover.
- **Input Fields:** Dark backgrounds (`#000000`) with JetBrains Mono text. On focus, the border glows with a subtle Diamond Blue neon line.
- **Voxel Cards:** Containers for startup data. They feature a 1px top-highlight (simulating light hitting the edge) and a deep shadow.
- **Status Chips:** Small, rectangular labels using JetBrains Mono. Success uses Emerald text with a 5% fill; Warning uses Gold.
- **The Terminal:** A dedicated component for raw data output. Uses a pure black background, no border-radius, and a subtle scanning line animation.
- **Breadcrumbs:** Technical paths (e.g., `Project > Module > Function`) separated by 45-degree forward slashes.