---
marp: true
theme: covermymeds
paginate: true
header: 'CoverMyMeds'
footer: '(c) 2026 CoverMyMeds LLC.  |  Confidential and Proprietary'
---

<!-- Render this like PowerPoint slides!  ->  https://covermymeds.atlassian.net/wiki/x/DQAT9g -->

<!-- _class: title -->
<!-- _header: '' -->
<!-- _footer: '' -->

# CoverMyMeds Marp Deck

## The minimal-markup slide format

---

<!-- _class: section -->

# How this deck is built

---

# The whole format in one slide

A deck is **plain markdown** with a short front-matter block:

```yaml
marp: true
theme: covermymeds
paginate: true
```

- Slides are separated by `---`
- A slide is a heading plus content; wordmark, page number, fonts, and colors are automatic
- The eyebrow and footer are the `header:` and `footer:` directives, not custom syntax
- The only styling you write is a per-slide class, and only when a slide differs

---

# Standard content reads like a document

The source stays **diff-friendly** and easy for people and tools to parse: no
`<style>` blocks, no inline colors, no layout HTML.

1. Write the content
2. Let the theme brand it
3. Commit the `.md` like any other source file

> Blockquotes get the orange rule. Use them for callouts.

Links like [the Marp docs](https://marpit.marp.app/) pick up brand magenta.

---

## Layout classes

| Class | When to use it | Markup |
|---|---|---|
| _(none)_ | Standard content | just a heading |
| `title` | Cover slide | `<!-- _class: title -->` |
| `section` | Divider between parts | `<!-- _class: section -->` |
| `lead` | Centered quote / key point | `<!-- _class: lead -->` |
| `invert` | Orange emphasis slide | `<!-- _class: invert -->` |
| `columns` | Auto-flow content into two columns | `<!-- _class: columns -->` |

---

# Colored group panels

Side-by-side panels use HTML-comment markers. The color word picks the brand
pair; **color never appears in the content**. No `<div>`, no `html: true`.

<!-- columns -->
<!-- col orange -->
### Do

- Keep bullets short
- Let the theme color the header and body
- Use `orange` and `magenta` (the authoritative tint pairs)
<!-- col magenta -->
### Avoid

- Inline `style=` attributes
- Hardcoded hex colors
- `<style>` blocks that fight the theme
<!-- /columns -->

---

<!-- _class: lead -->

# "Center a single idea with the lead class."

Good for one quote or one number.

---

<!-- _class: invert -->

# Key takeaway

Keep the markdown minimal. Let the theme carry the brand.

---

# Images use Marp's resize syntax

Size with `![w:480](path)` or `![h:300](path)`, never a raw `<img>` tag:

![w:280](covermymeds-logo.png)
