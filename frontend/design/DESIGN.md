---
name: Apex Predictor
colors:
  surface: '#131314'
  surface-dim: '#131314'
  surface-bright: '#3a393a'
  surface-container-lowest: '#0e0e0f'
  surface-container-low: '#1c1b1c'
  surface-container: '#201f20'
  surface-container-high: '#2a2a2b'
  surface-container-highest: '#353436'
  on-surface: '#e5e2e3'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#e5e2e3'
  inverse-on-surface: '#313031'
  outline: '#849495'
  outline-variant: '#3b494b'
  surface-tint: '#00dbe9'
  primary: '#dbfcff'
  on-primary: '#00363a'
  primary-container: '#00f0ff'
  on-primary-container: '#006970'
  inverse-primary: '#006970'
  secondary: '#ffffff'
  on-secondary: '#223600'
  secondary-container: '#a9f900'
  on-secondary-container: '#496f00'
  tertiary: '#faf3ff'
  on-tertiary: '#3c0090'
  tertiary-container: '#e1d2ff'
  on-tertiary-container: '#7213ff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#7df4ff'
  primary-fixed-dim: '#00dbe9'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#a9f900'
  secondary-fixed-dim: '#94db00'
  on-secondary-fixed: '#121f00'
  on-secondary-fixed-variant: '#334f00'
  tertiary-fixed: '#e9ddff'
  tertiary-fixed-dim: '#d1bcff'
  on-tertiary-fixed: '#23005b'
  on-tertiary-fixed-variant: '#5700c9'
  background: '#131314'
  on-background: '#e5e2e3'
  surface-variant: '#353436'
typography:
  display-lg:
    fontFamily: Archivo Narrow
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Archivo Narrow
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Archivo Narrow
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  title-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: '1.4'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style
The design system is engineered for a high-stakes, high-performance sports analytics environment. It centers on the "AI vs. Human" competitive narrative, creating a digital arena where data meets intuition. The aesthetic is **Modern Glassmorphic**, utilizing deep layers and vibrant accents to simulate a futuristic broadcast command center.

**Target Audience:** Sports enthusiasts, data analysts, and competitive bettors who value precision and speed.
**Emotional Response:** Intense, authoritative, energetic, and technologically advanced.
**Core Style:** A sophisticated dark mode foundation utilizing frosted glass textures, precision borders, and high-energy accent glows to differentiate between machine intelligence and human instinct.

## Colors
The palette is built on a "Total Black" philosophy to maximize the pop of functional accents.

- **Primary (Electric Blue):** Dedicated to AI-driven data, machine predictions, and automated insights.
- **Secondary (Neon Green):** Dedicated to the "Human" element—user inputs, manual predictions, and community polls.
- **Surface Strategy:** Use deep charcoal (`#0A0A0B`) for primary containers. Interactive elements use semi-transparent "glass" fills with 1px borders to maintain clarity against the dark void.
- **Gradients:** Use subtle radial gradients (Primary-to-Transparent) behind AI components to signify "processing" or "intelligence."

## Typography
The typography system prioritizes legibility of dense data and the "impact" of scores.

- **Headlines:** Use **Archivo Narrow** for a condensed, sports-broadcast feel. Bold weights and uppercase styling are mandatory for scores and team names to convey authority.
- **Body:** **Inter** provides a clean, neutral balance for analytical text and descriptions.
- **Data/Labels:** **JetBrains Mono** is used for "Confidence Meters," odds, and technical timestamps, emphasizing the mathematical nature of the app.

## Layout & Spacing
The layout follows a **Fluid Grid** model with high-density information mapping.

- **Mobile First:** Content is stacked vertically in a single column. Scoreboard cards span the full width minus side margins.
- **Desktop Optimization:** A 12-column grid. AI data (Primary) typically occupies the left 6 columns, while Human/User data (Secondary) occupies the right 6 columns to facilitate direct comparison.
- **Rhythm:** An 8px-based spacing system ensures tight, scientific alignment of data tables. Gutters are kept narrow (16px) to maximize the screen real estate for large numeric displays.

## Elevation & Depth
Depth is achieved through **Glassmorphism and Tonal Stacking** rather than traditional shadows.

- **Level 0 (Base):** Solid black canvas (`#050505`).
- **Level 1 (Section):** Deep charcoal cards with a 1px solid border (`#1A1A1B`).
- **Level 2 (Interactive):** Semi-transparent glass (`rgba(255, 255, 255, 0.05)`) with a `blur(12px)` backdrop. 
- **Accent Elevation:** Active states use an outer "Neon Glow" (0px 0px 15px) using either the Primary (AI) or Secondary (Human) color to indicate focus.
- **Dividers:** Use low-opacity lines (`rgba(255, 255, 255, 0.08)`) to separate table rows without adding visual bulk.

## Shapes
The shape language is **Technical and Precise**. 

- **Corners:** Use "Soft" (0.25rem) for small components like chips and inputs. Use "Rounded-lg" (0.5rem) for large scoreboard cards.
- **Clipping:** Flag placeholders should be rendered as "Squarcles" or standard rectangles with subtle rounding—avoid circles to maintain the aggressive, performance-oriented aesthetic.
- **Meters:** Confidence and probability bars use sharp, 0px radius ends to feel like technical readouts.

## Components
Consistent execution of these components ensures the "AI vs Me" hierarchy is maintained.

- **Scoreboard Cards:** Large, high-contrast blocks. The score is `display-lg`. The background uses a subtle radial gradient of the "leading" predictor (e.g., if AI is winning, the card has a faint blue glow).
- **Confidence Meters:** Horizontal bars. The fill color identifies the source: Electric Blue for AI, Neon Green for Human. Include a "delta" indicator showing the percentage difference between the two.
- **Predictor Toggles:** A segmented control that uses a "Glass" background. The active state for "AI" is Blue; "Me" is Green.
- **Data Tables:** High-density rows with `label-sm` headers. Use monospaced numbers for all statistics to ensure vertical alignment of digits.
- **Action Buttons:** Primary buttons are "Pill-shaped" but with high-contrast outlines. AI-actions use the Primary color; User-actions use the Secondary color.