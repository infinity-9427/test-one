# Enhanced Rule-Based Specification for “Website Design Scoring & Reporting Tool”

*By a UI/UX Senior Web Developer with 20 years’ experience*

This document refines and extends the core rule-based metrics, adds advanced checks, and prescribes precise scoring rules to yield consistent, actionable, and high-fidelity design evaluations.

---

## 📐 1. Typography & Readability

### 1.1 Metrics & Thresholds

| Metric                      | Ideal Range / Value                | Penalty                                      |
|-----------------------------|------------------------------------|----------------------------------------------|
| **Base font size**          | ≥ 16 px                             | –1 pt per px below 16 px (down to 12 px)     |
| **Line-height ratio**       | 1.4 – 1.6                           | –10 pts if < 1.4 or > 1.6                    |
| **Contrast ratio** (WCAG)   | ≥ 4.5 :1 (body), ≥ 3 :1 (large)     | –30 pts if below threshold                   |
| **Font family fallbacks**   | At least 2 fallbacks declared      | –15 pts if missing                           |
| **Heading hierarchy**       | h1 → h2 → h3 sequentially          | –10 pts per skipped or out-of-order level    |
| **Paragraph length**        | ≤ 75 chars per line (avg)          | –5 pts per 10 chars over                     |

### 1.2 Pseudocode Snippet

```js
let typoScore = 100;

// Base font size
const fs = getComputedStyle('body').fontSizePx;
if (fs < 16) typoScore -= Math.min(4 * (16 - fs), 16);

// Line height
const lhRatio = getComputedStyle('body').lineHeight / fs;
if (lhRatio < 1.4 || lhRatio > 1.6) typoScore -= 10;

// Contrast
const contrast = computeContrast(textColor, bgColor);
if (contrast < (isLargeText ? 3 : 4.5)) typoScore -= 30;

// Fallbacks
const fallbacks = getFontFallbacks('body');
if (fallbacks.length < 2) typoScore -= 15;

// Headings
const headings = document.querySelectorAll('h1, h2, h3, h4').map(h => h.tagName);
if (!isSequential(headings)) typoScore -= 10;


2. Color & Visual Hierarchy
2.1 Metrics & Thresholds
Metric	Ideal Value / Check	Penalty
Primary/accent harmony	Δhue ≤ 30° (analogous) or Δhue ≈ 150°–180°	–25 pts if outside harmony
Saturation moderation	Text saturation ≤ 85 %	–15 pts per violation
Contrast on UI controls	≥ 3 :1 for buttons, links	–20 pts if below
Color consistency	≤ 3 distinct accent colors	–10 pts per extra color
2.2 Pseudocode Snippet

let colorScore = 100;
const palette = extractPalette(); // [{h,s,l},…]

// Harmony
const deltas = pairwiseHueDeltas(palette.primary, palette.accents);
if (!isAnalogousOrComplementary(deltas)) colorScore -= 25;

// Saturation
palette.textColors.forEach(c => {
  if (c.s > 0.85) colorScore -= 15;
});

// Control contrast
controls.forEach(el => {
  const c = computeContrast(getText(el), getBackground(el));
  if (c < 3) colorScore -= 20;
});

📐 3. Layout, Grid & Whitespace
3.1 Metrics & Thresholds
Metric	Ideal Value	Penalty
8 px grid adherence	All margins/paddings multiples of 8 px	–5 pts per misaligned edge
Whitespace ratio	30 % – 50 % of viewport	–30 pts if < 30 %, –15 pts if > 50 %
Section padding	≥ 24 px vertical, ≥ 16 px horizontal	–10 pts per section that violates
Visual balance	Center of mass within central 40 % width	–20 pts if off-center
3.2 Pseudocode Snippet

# Python + Pillow + NumPy
img = load('screenshot.png'); arr = np.array(img)
bg = tuple(arr[0,0])
empty = np.sum(np.all(arr==bg, axis=2))
whitespaceRatio = empty / arr.size

layoutScore = 100
if whitespaceRatio < 0.3: layoutScore -= 30
if whitespaceRatio > 0.5: layoutScore -= 15

# Grid
misaligned = countMisalignedElements(selector, grid=8)
layoutScore -= misaligned * 5

📱 4. Responsiveness & Adaptivity
4.1 Metrics & Thresholds
Metric	Ideal Check	Penalty
Viewport meta tag	<meta name="viewport" content="…">	–25 pts if missing
Breakpoint coverage	≤ 3 layout shifts at common widths	–10 pts per additional shift
Touch target size	≥ 44 × 44 px (buttons/links)	–15 pts per too-small target
Image scaling	Responsive <img srcset> or width:100%	–20 pts if fixed width
4.2 Pseudocode Snippet

let respScore = 100;
if (!document.querySelector('meta[name="viewport"]')) respScore -= 25;
const shifts = getLayoutShifts([320, 768, 1024]);
if (shifts > 3) respScore -= (shifts - 3) * 10;
document.querySelectorAll('a,button').forEach(el => {
  const {width,height} = el.getBoundingClientRect();
  if (width < 44 || height < 44) respScore -= 15;
});

♿ 5. Accessibility & Semantics
5.1 Metrics & Thresholds
Metric	Ideal	Penalty
Alt text on <img>	All decorative & informative images	–10 pts per missing alt
ARIA roles & labels	Buttons, nav, landmarks correctly	–15 pts per missing/incorrect
Semantic HTML	Proper use of <header>, <main>, <footer>	–20 pts if absent
Keyboard focus order	Logical tab sequence	–25 pts if broken
⚡ 6. Performance & SEO (Optional Bonus)
Metrics

    Total page weight: ≤ 1.5 MB (–10 pts per 500 KB over)

    Lighthouse performance score: ≥ 80/100 (–10 pts per 10 pts below)

    Meta tags: <title>, <meta description> present (–20 pts if missing)