#!/usr/bin/env python3
"""Generate the self-contained CoverMyMeds Marp theme CSS.

Every value comes from the authoritative "CMM Master" PowerPoint theme
(CoverMyMeds_PowerPointTemplate_2026.potx): palette from ppt/theme/theme1.xml
clrScheme, fonts from its fontScheme (Georgia headings / Arial body, i.e.
titleStyle=+mj-lt, bodyStyle=+mn-lt), chrome geometry from the content layouts
(wordmark ~6%/83% x, ~89% y; content inset 6%). Nothing is invented.

The wordmark and ring frame are base64-embedded so this one file is the entire
brand: deck.md + this CSS renders identically anywhere with nothing to resolve.
Regenerate with .claude/assets/marp/gen_theme.py if the marks change.
"""
import base64

assets = "/Users/owinkler/Projects/tools/.claude/assets/marp"


def data_uri(path, mime):
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode("ascii")


logo = data_uri(f"{assets}/covermymeds-logo.png", "image/png")
rings = data_uri(f"{assets}/covermymeds-rings.png", "image/png")

css = f"""/* @theme covermymeds */
/*
 * CoverMyMeds Marp theme. Authoritative source: CoverMyMeds_PowerPointTemplate_2026.potx
 * ("CMM Master" theme). Do not eyeball values; pull them from that .potx.
 *
 * Design intent: the .md stays clean and diff-friendly. All brand styling lives
 * here. A standard slide needs nothing but a heading and content; the wordmark,
 * page number, fonts, and palette apply automatically. The only styling an
 * author writes is a per-slide class directive, and only when a slide differs:
 *
 *   <!-- _class: title -->    cover slide (ring frame + big wordmark)
 *   <!-- _class: section -->  navy section divider
 *   <!-- _class: lead -->     centered single idea / quote
 *   <!-- _class: invert -->   orange emphasis slide
 *   <!-- _class: columns -->  auto-flow the slide's content into two columns
 *
 * Eyebrow and footer are Marp's native directives, not custom syntax:
 *   header: 'CoverMyMeds'                         (eyebrow, top-left)
 *   footer: '(c) 2026 CoverMyMeds ... CONFIDENTIAL'  (bottom-left)
 *
 * Colored group panels (the one place a little structure is unavoidable) use
 * semantic class names so color never touches the content. Requires html: true.
 *   <div class="cols"><div class="card orange">### Header ...</div>
 *                     <div class="card magenta">### Header ...</div></div>
 * Authoritative pairs: orange->peach, magenta->pink (accent1/5, accent2/6).
 */

@import 'default';

:root {{
  /* Palette (theme1.xml clrScheme) */
  --cmm-orange:  #FF8F1C;  /* accent1 */
  --cmm-magenta: #EC0868;  /* accent2 / hyperlink */
  --cmm-blue:    #1E91D6;  /* accent3 */
  --cmm-navy:    #01426A;  /* accent4 */
  --cmm-peach:   #FFF2EB;  /* accent5 tint (pairs with orange) */
  --cmm-pink:    #FDE8F1;  /* accent6 tint (pairs with magenta) */
  --cmm-ink:     #1D2329;  /* dk1 / dk2 */
  --cmm-mist:    #F7F7F7;  /* lt2 */
  --cmm-paper:   #FFFFFF;  /* lt1 */
  --cmm-gray:    #7A828A;  /* muted ink for eyebrow / footer */
  --cmm-rule:    #CCCCCC;  /* followed hyperlink / hairlines */

  /* Type (theme1.xml fontScheme): Georgia headings, Arial body */
  --cmm-font-head: Georgia, 'Times New Roman', serif;
  --cmm-font-body: Arial, Helvetica, sans-serif;

  --cmm-logo: url({logo});
  --cmm-rings: url({rings});
}}

/* ---- Base slide -------------------------------------------------------- */

section {{
  font-family: var(--cmm-font-body);
  color: var(--cmm-ink);
  background-color: var(--cmm-paper);
  font-size: 25px;
  line-height: 1.4;
  padding: 64px 80px 88px;   /* content inset ~6%, room for chrome at bottom */
}}

/* Wordmark, bottom-right of every content slide. No markup required.
   Hidden on title / section / invert below. */
section::before {{
  content: "";
  position: absolute;
  right: 68px;
  bottom: 30px;
  width: 156px;
  height: 24px;
  background: var(--cmm-logo) no-repeat right bottom;
  background-size: contain;
}}

/* Page number (default theme's section::after), centered so it clears the
   wordmark (right) and footer (left). */
section::after {{
  color: var(--cmm-navy);
  font-family: var(--cmm-font-body);
  font-size: 15px;
  left: 50%;
  right: auto;
  bottom: 30px;
  transform: translateX(-50%);
}}

/* ---- Eyebrow (header:) and confidentiality line (footer:) -------------- */

header {{
  color: var(--cmm-gray);
  font-family: var(--cmm-font-body);
  font-weight: 700;
  font-size: 15px;
  letter-spacing: .12em;
  text-transform: uppercase;
  top: 34px;
  left: 80px;
}}
footer {{
  color: var(--cmm-gray);
  font-family: var(--cmm-font-body);
  font-size: 13px;
  letter-spacing: .04em;
  text-transform: uppercase;
  left: 80px;
  bottom: 30px;
}}

/* ---- Headings ---------------------------------------------------------- */

h1, h2, h3, h4, h5, h6 {{
  font-family: var(--cmm-font-head);
  color: var(--cmm-navy);
  font-weight: 700;
  line-height: 1.15;
}}
h1 {{
  font-size: 44px;
  margin: 0 0 22px;
  padding-bottom: 12px;
  border-bottom: 4px solid var(--cmm-magenta);
}}
h2 {{ font-size: 32px; color: var(--cmm-navy); }}
h3 {{ font-size: 25px; color: var(--cmm-blue); }}

/* ---- Inline text ------------------------------------------------------- */

a {{ color: var(--cmm-magenta); text-decoration: none; border-bottom: 1px solid var(--cmm-magenta); }}
strong {{ color: var(--cmm-navy); }}
mark {{ background: var(--cmm-peach); color: var(--cmm-ink); padding: 0 .15em; }}
ul > li::marker {{ color: var(--cmm-orange); }}
ol > li::marker {{ color: var(--cmm-magenta); font-weight: 700; }}
li {{ margin: .28em 0; }}

/* ---- Blockquote -------------------------------------------------------- */

blockquote {{
  border-left: 6px solid var(--cmm-orange);
  background: var(--cmm-mist);
  margin: 0;
  padding: 16px 28px;
  font-style: normal;
  color: var(--cmm-ink);
}}
blockquote > *:first-child {{ margin-top: 0; }}
blockquote > *:last-child {{ margin-bottom: 0; }}

/* ---- Code -------------------------------------------------------------- */

code {{
  font-family: 'SF Mono', 'Consolas', monospace;
  background: var(--cmm-peach);
  color: var(--cmm-navy);
  border-radius: 4px;
  padding: 1px 6px;
  font-size: .9em;
}}
pre {{ background: var(--cmm-ink); border-radius: 8px; padding: 20px 24px; }}
pre code {{ background: transparent; color: var(--cmm-mist); padding: 0; }}

/* ---- Tables ------------------------------------------------------------ */

table {{ border-collapse: collapse; font-size: .82em; width: 100%; }}
th {{
  background: var(--cmm-navy);
  color: var(--cmm-paper);
  font-family: var(--cmm-font-body);
  font-weight: 700;
  text-align: left;
  padding: 10px 14px;
}}
td {{ padding: 10px 14px; border-bottom: 1px solid var(--cmm-rule); }}
tr:nth-child(even) td {{ background: var(--cmm-mist); }}

/* ---- Two columns: auto-flow  <!-- _class: columns --> ------------------ */

section.columns {{ column-count: 2; column-gap: 56px; }}
section.columns h1 {{ column-span: all; }}
section.columns > * {{ break-inside: avoid; }}

/* ---- Group panels: <div class="cols"><div class="card orange">...</div> */

.cols {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  align-items: start;
  margin-top: 6px;
}}
.cols.three {{ grid-template-columns: repeat(3, 1fr); }}

.card {{
  background: var(--cmm-mist);
  border-radius: 6px;
  overflow: hidden;
  padding-bottom: 14px;
  font-size: 20px;
  line-height: 1.35;
  min-width: 0;   /* let long content wrap instead of overflowing the grid cell */
}}
.card li {{ margin: .18em 0; }}

/* Plain (uncolored) column: <!-- col --> */
.cols > .col {{ min-width: 0; font-size: 20px; line-height: 1.35; }}
/* First heading in a card becomes the color header bar */
.card > h1:first-child,
.card > h2:first-child,
.card > h3:first-child {{
  margin: 0 0 12px;
  padding: 14px 24px;
  color: var(--cmm-paper);
  background: var(--cmm-navy);
  font-family: var(--cmm-font-body);
  font-weight: 700;
  font-size: 24px;
  border-bottom: none;
}}
/* Body content in a card gets side padding (the header bar is full-bleed) */
.card > *:not(h1):not(h2):not(h3) {{ margin-left: 24px; margin-right: 24px; }}

/* Authoritative color pairs */
.card.orange  {{ background: var(--cmm-peach); }}
.card.orange  > :first-child {{ background: var(--cmm-orange); }}
.card.magenta {{ background: var(--cmm-pink); }}
.card.magenta > :first-child {{ background: var(--cmm-magenta); }}
.card.blue    {{ background: var(--cmm-mist); }}
.card.blue    > :first-child {{ background: var(--cmm-blue); }}
.card.navy    {{ background: var(--cmm-mist); }}
.card.navy    > :first-child {{ background: var(--cmm-navy); }}

/* ---- Title slide:  <!-- _class: title --> ------------------------------ */

section.title {{
  background: var(--cmm-paper) var(--cmm-rings) no-repeat center / cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 80px 140px;
}}
section.title::before {{ position: static; width: 340px; height: 52px; margin-bottom: 36px; }}
section.title::after {{ content: none; }}
section.title header, section.title footer {{ color: var(--cmm-gray); }}
section.title h1 {{ border-bottom: none; color: var(--cmm-navy); font-size: 52px; padding: 0; margin: 0 0 12px; }}
section.title h2 {{ color: var(--cmm-magenta); font-family: var(--cmm-font-body); font-weight: 400; font-size: 25px; }}

/* ---- Section divider:  <!-- _class: section --> ------------------------ */

section.section {{
  background: var(--cmm-navy);
  color: var(--cmm-paper);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 96px;
}}
section.section::before {{ content: none; }}
section.section h1 {{ color: var(--cmm-paper); font-size: 50px; border-bottom: none; padding: 0 0 16px; }}
section.section h1::after {{ content: ""; display: block; width: 120px; height: 6px; margin-top: 20px; background: var(--cmm-orange); }}
section.section h2, section.section h3 {{ color: var(--cmm-peach); }}
section.section a {{ color: var(--cmm-orange); border-bottom-color: var(--cmm-orange); }}
section.section header, section.section footer {{ color: rgba(255,255,255,.6); }}

/* ---- Lead (centered):  <!-- _class: lead --> --------------------------- */

section.lead {{ display: flex; flex-direction: column; justify-content: center; text-align: center; }}
section.lead h1 {{ border-bottom: none; }}

/* ---- Invert (orange emphasis):  <!-- _class: invert --> ---------------- */

section.invert {{ background: var(--cmm-orange); color: var(--cmm-ink); }}
section.invert h1, section.invert h2, section.invert h3 {{ color: var(--cmm-navy); }}
section.invert h1 {{ border-bottom-color: var(--cmm-navy); }}
section.invert::before {{ content: none; }}
section.invert header, section.invert footer {{ color: var(--cmm-navy); }}
"""

out = f"{assets}/covermymeds.css"
with open(out, "w", encoding="utf-8") as fh:
    fh.write(css)
print(f"wrote {out} ({len(css):,} bytes)")
