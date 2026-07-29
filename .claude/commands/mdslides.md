<!-- Marp deck skill: author or validate a CoverMyMeds-branded slide deck as plain,
     diff-friendly markdown. The .md stays minimal (front-matter + headings + content +
     the occasional class directive or column marker); all brand styling lives in the
     theme CSS, and columns are HTML-comment markers expanded by the Marp config engine.
     Render with a live preview window; export to PPTX or HTML.
     Usage: /mdslides <new|validate|preview|export> [file|name] [args]
     Requires: node + npx (marp-cli is fetched on first run). Chrome/Chromium/Edge for
     the live preview window and PPTX/PNG export; HTML export needs no browser. -->

`$ARGUMENTS` begins with a verb: `new`, `validate`, `preview`, or `export`. If no verb
is given, infer from context (a `.md` path with Marp front-matter -> `validate`;
otherwise ask). Everything the skill renders uses the repo config; never inline brand
colors into a deck.

## Shared constants

- **Config:** `.claude/assets/marp/marp.config.js` (relative to the repo root). Pass it
  to every marp-cli call with `-c`. It registers the brand theme (`covermymeds.css`,
  self-contained with the logo and ring frame embedded), enables the column engine, and
  sets `html`/`allowLocalFiles`. Because the config carries everything, a deck reproduces
  identically outside the skill:
  ```bash
  npx @marp-team/marp-cli deck.md -c .claude/assets/marp/marp.config.js --no-stdin -o deck.html
  ```
- **marp-cli:** `npx -y @marp-team/marp-cli` (first run downloads it; later runs cached).
- **`--no-stdin` on every call.** marp-cli v4 blocks waiting on stdin when stdin is a
  pipe (as it is here); always pass `--no-stdin` or the command hangs.
- **Browser (preview / PPTX / PNG only):** detect once and export `CHROME_PATH`:
  ```bash
  for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium" \
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
    [ -x "$p" ] && export CHROME_PATH="$p" && break
  done
  ```
  If none is found: HTML export still works; `preview` and `export pptx` do not. Say so
  and fall back to `export html`.

## The markdown contract

Enforce this shape when authoring and when validating. The point is a clean source file
that diffs well, parses easily, and survives auto-formatters; the config does the
branding and the column layout.

**Front-matter** (YAML, first thing in the file):
```yaml
marp: true
theme: covermymeds
paginate: true
header: 'CoverMyMeds'      # optional eyebrow, top-left
footer: '(c) 2026 CoverMyMeds LLC.  |  Confidential and Proprietary'   # optional
```
No `html: true` and no `--theme-set` needed; the config supplies both.

**Render-instructions header.** Immediately after the front-matter, every deck carries a
one-line HTML comment pointing to the how-to page, so anyone who opens the raw `.md`
knows it renders to slides:
```markdown
<!-- Render this like PowerPoint slides!  ->  https://covermymeds.atlassian.net/wiki/x/DQAT9g -->
```
It renders to nothing on the slides and survives formatters. Keep it to this one line; the
linked page carries the full render + authoring instructions.

**Slides** are separated by a `---` line. Every slide is a heading plus content. The
wordmark, page number, fonts, and palette are applied automatically; author nothing for
them.

**Per-slide class** is the only styling an author writes, and only when a slide differs
from a standard content slide. Set it with a directive comment at the top of the slide:
```markdown
<!-- _class: title -->
```

| Class | Use | Notes |
|---|---|---|
| _(none)_ | Standard content | corner wordmark + page number |
| `title` | Cover slide | ring frame + centered wordmark; suppress header/footer with `<!-- _header: '' -->` and `<!-- _footer: '' -->` |
| `section` | Divider between parts | navy background, orange rule |
| `lead` | One centered idea / quote | |
| `invert` | Orange emphasis slide | |

**Columns and colored panels** use markdown-neutral HTML-comment markers. The config
engine expands them into the theme's `cols`/`card` layout at render time, inserting the
blank lines Marp needs; the source never contains `<div>` or `html: true`, and formatters
leave the comments alone.
```markdown
<!-- columns -->
<!-- col orange -->
### General Items
- point
- point
<!-- col magenta -->
### Needed Conversations
- point
<!-- /columns -->
```
- `<!-- columns -->` opens a row; `<!-- columns three -->` for three across.
- `<!-- col <color> -->` starts a column as a colored card. Authoritative colors:
  `orange` (peach body), `magenta` (pink body); `blue` and `navy` use a neutral body.
- `<!-- col -->` (no color) starts a plain column with no box.
- `<!-- /columns -->` closes the row.

**Images** use Marp resize syntax: `![w:480](path)` or `![h:300](path)`. Never a raw
`<img>` tag or inline sizing.

**Never** put `<style>` blocks, `style=` attributes, hardcoded hex colors, or raw layout
`<div>`s into a deck. Columns are the markers above; everything else is the theme.

## Verb: new

Author a new deck.

1. Gather the content. Either the user supplies an outline / doc / bullets, or run a
   short interview: title + subtitle, audience and purpose, the section breakdown, and
   any comparison/agenda content that wants columns.
2. Draft `<name>.md` (in the working directory; default name from the title, kebab-case)
   following the contract above. Decisions:
   - One idea per slide. **Split dense slides** rather than shrinking type; a column that
     overflows the slide is the signal to split. Aim for content that fits at the theme's
     default sizes.
   - Open with a `title` slide; use `section` dividers between parts.
   - Use `<!-- col -->` (plain) for simple two-up content and colored `<!-- col orange -->`
     cards when each column needs its own labeled header.
   - Set `header:`/`footer:` once in front-matter if the deck wants the eyebrow and
     confidentiality line.
3. Run `validate` on the result (below) and fix anything it flags before showing the user.
4. Show the path and offer to `preview`.

## Verb: validate

Lint an existing `.md`. Read the file, check each item, and report a table with
✅ pass / ⚠️ warn / ❌ fail and the line number, then a verdict
(VALID / VALID WITH WARNINGS / INVALID). Report findings; do not silently rewrite the
user's deck. Offer to fix afterward.

Checks:
1. **Front-matter** present and includes `marp: true` and `theme: covermymeds`. (fail)
2. **Slide separators**: at least one `---` between slides where multiple were intended;
   front-matter fence not miscounted. (fail)
3. **Column markers balanced**: every `<!-- columns -->` has a matching `<!-- /columns -->`;
   each contains at least one `<!-- col ... -->`; `col` markers appear only inside a
   `columns` block. (fail)
4. **Card color is authoritative**: each `<!-- col <color> -->` color is one of
   orange/magenta/blue/navy (or empty for a plain column). Unknown color -> warn. (warn)
5. **No off-theme styling**: no `<style>` blocks, no `style=` attributes, no hardcoded
   hex colors (`#RRGGBB`) in the body. (fail)
6. **Prefer markers over raw HTML**: raw `<div class="cols|card ...">` or `html: true` in
   front-matter still renders but should be the comment markers instead. (warn)
7. **Known classes only**: every `_class:` value is one of title/section/lead/invert.
   Unknown class -> warn (won't be themed). (warn)
8. **Images** use `![w:/h:](...)` sizing, not raw `<img>`. (warn)
9. **Density**: flag slides with more than ~6 top-level bullets or a very long column as a
   likely overflow; suggest splitting. (warn)
10. **Render-instructions header**: the one-line "Render this like PowerPoint slides!"
    comment is present right after the front-matter; warn if missing (a recipient who
    opens the raw file won't know how to render it). (warn)
11. **Renders clean**: do a real render to a temp file and report any marp-cli
    warnings/errors:
    ```bash
    npx -y @marp-team/marp-cli <file> -c .claude/assets/marp/marp.config.js \
      --no-stdin -o "$(mktemp -d)/lint.html"
    ```
    A non-zero exit or emitted error is a fail.

## Verb: preview

Open the live preview window that reloads as the file is edited. Requires a browser
(detect as above).
```bash
npx -y @marp-team/marp-cli <file> -c .claude/assets/marp/marp.config.js \
  --no-stdin --preview --watch
```
Run it in the background so the watch process does not block. If no browser is found,
tell the user and offer `export html` instead.

## Verb: export

Write a shareable file. Format from the second arg (`pptx` or `html`); default `html`.
Output next to the source (`<name>.pptx` / `<name>.html`). marp-cli picks the format from
the `-o` extension.
```bash
# PPTX (needs a browser)
npx -y @marp-team/marp-cli <file> -c .claude/assets/marp/marp.config.js \
  --no-stdin --pptx -o <name>.pptx

# HTML (self-contained, no browser needed)
npx -y @marp-team/marp-cli <file> -c .claude/assets/marp/marp.config.js \
  --no-stdin -o <name>.html
```
For PPTX without a browser, stop and say so; do not silently produce HTML instead.
After a successful export, `open` the file and report the path.

## Deck header

Prepend this one line verbatim to every deck, immediately after the front-matter. It is
an HTML comment, so it never renders on a slide; it points recipients to the how-to page
(render steps, output formats, and how to author their own with this skill):

```markdown
<!-- Render this like PowerPoint slides!  ->  https://covermymeds.atlassian.net/wiki/x/DQAT9g -->
```

The linked page ("Rendering CoverMyMeds Marp Slide Decks", in the toolkit owner's
Confluence space) is the single source of setup instructions; update it there, not in
every deck. If the page moves, change the URL here.

## Reference

`.claude/assets/marp/example.md` is a complete deck exercising every class and the column
markers; render it to see the theme, or use it as the validator fixture. The config's
column engine lives in `.claude/assets/marp/marp.config.js`; the theme is regenerated from
the source `.potx` by `.claude/assets/marp/gen_theme.py` if the brand marks ever change.
