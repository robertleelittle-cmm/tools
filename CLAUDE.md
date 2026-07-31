# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project purpose

Personal EM toolbox: Claude Code slash commands for daily team operations and compliance workflows.

## Architecture

Each slash command is a `.md` file in `.claude/commands/`. Commands that need data from external APIs use a backing Node.js script in `.claude/scripts/`; commands that drive Claude directly via MCP tools or the `gh` CLI need no script.

```
.claude/
  commands/       # one .md file per slash command
  scripts/        # one .js file per script-backed commands
  assets/         # static assets a command depends on (e.g. the Marp theme)
  standup-context.json   # gitignored; managed by Claude, not edited manually
```

## Jira integration

Scripts call the Jira REST API directly using Basic auth (email + API token). No MCP required.

**Required environment variables:**

| Variable | Example |
|---|---|
| `JIRA_BASE_URL` | `https://covermymeds.atlassian.net` |
| `JIRA_EMAIL` | `you@covermymeds.com` |
| `JIRA_API_TOKEN` | token from https://id.atlassian.com/manage/api-tokens |

Set these in a `.env` file at the repo root (gitignored) or in your shell profile.

## standup-context.json

Gitignored. Managed entirely by Claude -- never edit manually (except `holidays`, which the script itself computes and caches). Structure:

```json
{
  "defaultExclude": ["Name to always omit"],
  "pto": [
    { "name": "Full Name", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "note": "reason" },
    { "name": "Full Name", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "allDay": false, "startTime": "1:00 PM", "endTime": "5:00 PM" }
  ],
  "holidays": { "year": 2026, "dates": ["2026-01-01", "..."] }
}
```

Tell Claude in natural language to update it: "Rob is out next week", "remove Jeffrey from the ignore list", "Seyoung is back Thursday", "Dana's out this afternoon 1-5".

PTO entries default to full-day. `allDay: false` + `startTime`/`endTime` marks a partial-day absence -- the engineer is only shown as out during that clock window, not flagged out (or excluded from backlog suggestions) for the whole day.

`holidays` caches CMM's standard observed US holidays (New Year's, MLK Day, Memorial Day, Juneteenth, July 4th, Labor Day, Thanksgiving + the Friday after, Christmas), computed once when the year in the cache no longer matches the current year. Used to compute "next work day" (skips weekends and holidays) for PTO return dates and recommendation phrasing.

## /emreview

Performs an EM review of a GitHub pull request for SOX/ITGC compliance. Fetches PR metadata, commit history, review decisions, and the linked Jira ticket, then evaluates the 7 compliance criteria and produces a copyable PR comment.

**Usage:** `/emreview <PR number>` (default repo: `covermymeds/drugs-api`)

**Requires:** `gh` CLI authenticated + Atlassian Rovo MCP connected. No script -- runs entirely via `gh` and MCP tool calls.

**Output:** A markdown table with ✅/❌/⚠️ per criterion, a plain-English change summary, and a APPROVED/NOT APPROVED/PENDING verdict.

## /standup

Runs a PARCH kanban standup report (default project). Override with `--project KEY`.

**Output includes:**
- National day of the day (deterministic pick, same for everyone on a given date)
- Computed SLE (85th percentile of 28-day cycle time history)
- Team Status: every active engineer, cards ordered right-to-left by kanban stage then age descending; available engineers get a suggested next backlog card
- Aging WIP chart: ASCII visualization of card age vs. workflow stage with SLE threshold
- Multi-Ticket Owners and Collaborator Load sections (used by Claude for recommendations)
- Writes `standup.md` to the working directory on every run

**PTO handling:** active full-day PTO suppresses backlog suggestions; a partial-day absence (`allDay: false`) only suppresses them while the current time is inside its window. Upcoming PTO (within 7 days) is flagged on the engineer's line. "Returns" and "next work day" dates skip weekends and CMM holidays (see `holidays` in standup-context.json).

## /goalsetting

Guides any McKesson Platform employee through the annual Workday goal-setting process. Produces SMART goals aligned to the three Platform evaluation criteria.

**Usage:** `/goalsetting` (no arguments; starts an interactive interview)

**Requires:** No external tools. Pure Claude skill.

**What it produces:**
- 3–4 performance goals (What You Deliver) and 1–2 development goals (How You Grow), reviewed individually with SMART scoring before finalization
- A single markdown artifact per goal with GOAL, DESCRIPTION, and MILESTONES sections
- Optional post-delivery advice on executing each goal for elevated or exceptional performance

**Flow:** Interview (job context or prewritten goals) → per-goal SMART review → artifact → optional performance execution review.

## /metadoc

Produces canonical meta-documents: reference documents that define what must be true or what must exist within a documentation hierarchy. Does **not** produce the project documents that fulfill those requirements -- those live in project folios and reference back to the meta-document.

**Usage:** `/metadoc [optional topic hint]`

**Requires:** Atlassian Rovo MCP connected (for optional Confluence publishing). No script -- runs entirely via interactive interview and MCP.

**What it produces:**
- **Meta-documents**: canonical references stating requirements by phase, with a "what must exist" table naming subordinate meta-docs and project templates. Short by design -- if requirements exceed ~15 items, the skill splits off a subordinate rather than expanding.
- **Subordinate meta-documents**: child documents that expand one complex requirement area from a parent meta-doc into its own structure. Published as Confluence children of their parent.
- **Project templates** (optional): project-facing starters teams clone into their folio. Pre-populated with required sections and guidance notes; back-reference the meta-doc as the compliance standard.

**Workflow:** Interactive interview → markdown draft for review → optional subordinate/template drafts → optional Confluence publish.

## /mdslides

Authors or validates a CoverMyMeds-branded slide deck as plain, diff-friendly markdown. The `.md` stays minimal (front-matter + headings + content + the occasional per-slide class); all brand styling lives in the theme CSS, so the source parses cleanly for AI and diffs like any code file.

**Usage:** `/mdslides <new|validate|preview|export> [file|name] [args]`

**Requires:** `node` + `npx` (marp-cli is fetched on first run, no global install). A Chrome/Chromium/Edge browser for the live `--preview` window and PPTX/PNG export; HTML export needs no browser.

**Verbs:**
- `new [name]` — interview or ingest content, then write a branded `<name>.md` that follows the markdown contract; validates before handing back
- `validate <file>` — lint for valid + minimal Marp and brand-theme compliance; reports a ✅/⚠️/❌ table + verdict, does not silently rewrite
- `preview <file>` — open the live-reloading preview window (`--preview --watch`); falls back to HTML export if no browser
- `export <file> [pptx|html]` — write a shareable file next to the source and open it

**Config:** `.claude/assets/marp/marp.config.js` -- passed to marp-cli with `-c`. Registers the brand theme, enables the column engine, and sets `html`/`allowLocalFiles`, so a deck reproduces identically outside the skill (`npx @marp-team/marp-cli deck.md -c .claude/assets/marp/marp.config.js --no-stdin -o deck.html`) with no repo dependencies to install. Always pass `--no-stdin` (marp-cli v4 hangs on a piped stdin otherwise).

**Theme:** `.claude/assets/marp/covermymeds.css` -- self-contained, built from the authoritative `CoverMyMeds_PowerPointTemplate_2026.potx` ("CMM Master"): Georgia headings / Arial body, the CMM palette, corner wordmark and ring frame embedded as data URIs. Regenerate with `.claude/assets/marp/gen_theme.py` if the brand marks change.

**Devices:** per-slide classes `title` / `section` / `lead` / `invert`; native `header:`/`footer:` directives for the eyebrow and confidentiality line; and columns via markdown-neutral HTML-comment markers (`<!-- columns -->`, `<!-- col orange|magenta|blue|navy -->`, `<!-- /columns -->`) that the config engine expands into the theme's colored card panels at render time -- no `<div>` or `html: true` in the source, so decks stay formatter-safe. `.claude/assets/marp/example.md` exercises every device.

**Render-instructions header:** every deck carries a one-line HTML comment right after the front-matter -- `<!-- Render this like PowerPoint slides!  ->  https://covermymeds.atlassian.net/wiki/x/DQAT9g -->` -- pointing to the Confluence how-to page ("Rendering CoverMyMeds Marp Slide Decks") that carries the full render + authoring instructions. It renders to nothing on the slides. Update the page, not each deck.
