#!/usr/bin/env node
'use strict';
// Merges a fresh standup draft into the live HTML file after a board change.
// Diffs recommendations by <h3> section, preserves the monitor-log history.
// Usage: node update-live-standup.js --live <path> --draft <path> --time HH:MM --changes '[...]'
// Output: JSON { success, changes, recsAdded, recsRemoved }

const fs = require('fs');

function arg(flag) {
  const i = process.argv.indexOf(flag);
  return i !== -1 ? process.argv[i + 1] : null;
}

const livePath = arg('--live');
const draftPath = arg('--draft');
const timeStr = arg('--time') || new Date().toTimeString().slice(0, 5);
const changesRaw = arg('--changes');
const noChanges = process.argv.includes('--no-changes');

if (!livePath) {
  console.error('Usage: update-live-standup.js --live <path> [--draft <path>] [--time HH:MM] [--changes \'[...]\'] [--no-changes]');
  process.exit(1);
}
if (!noChanges && !draftPath) {
  console.error('--draft is required unless --no-changes is set');
  process.exit(1);
}

// ── Section extraction using <!-- SEC:X --> / <!-- /SEC:X --> markers ──────

function extractSection(html, name) {
  const start = html.indexOf(`<!-- SEC:${name} -->`);
  const end = html.indexOf(`<!-- /SEC:${name} -->`);
  if (start === -1 || end === -1) return null;
  return html.substring(start + `<!-- SEC:${name} -->`.length, end);
}

function replaceSection(html, name, newContent) {
  const start = html.indexOf(`<!-- SEC:${name} -->`);
  const end = html.indexOf(`<!-- /SEC:${name} -->`);
  if (start === -1 || end === -1) return html;
  const before = html.substring(0, start + `<!-- SEC:${name} -->`.length);
  const after = html.substring(end);
  return before + newContent + after;
}

// ── recs-content extraction (single-line div by id) ─────────────────────────

function extractRecsInner(html) {
  const m = html.match(/id="recs-content">([\s\S]*?)<\/div>\s*<\/div>/);
  return m ? m[1] : null;
}

function replaceRecsInner(html, newInner) {
  return html.replace(
    /(id="recs-content">)([\s\S]*?)(<\/div>\s*<\/div>)/,
    (_, open, _old, close) => open + newInner + close,
  );
}

// ── monitor-log extraction / replacement ────────────────────────────────────

function extractMonitorEntries(html) {
  const m = html.match(/id="monitor-log">([\s\S]*?)<\/div>\s*<\/div>/);
  if (!m) return '';
  return m[1].replace('<!-- MONITORING_LOG_PLACEHOLDER -->', '').trim();
}

function replaceMonitorCard(html, newEntries, time) {
  const checkedSpan = `<span id="monitor-last-checked" style="font-size:.8rem;font-weight:400;color:#6b7280">— checked ${time}</span>`;
  return html.replace(
    /(<div class="card" id="monitoring")[^>]*>([\s\S]*?id="monitor-log">)([\s\S]*?)(<\/div>\s*<\/div>)/,
    (_, cardOpen, _logOpen, _old, closeTag) =>
      `${cardOpen}><h2>Live Updates ${checkedSpan}</h2><div id="monitor-log">${newEntries}${closeTag}`,
  );
}

// ── Recommendations diff ─────────────────────────────────────────────────────

function parseRecSections(html) {
  if (!html) return [];
  const sections = [];
  const parts = html.split(/<h3>/);
  for (let i = 1; i < parts.length; i++) {
    const closeIdx = parts[i].indexOf('</h3>');
    if (closeIdx === -1) continue;
    const heading = parts[i].substring(0, closeIdx).replace(/<[^>]+>/g, '').trim();
    // Grab everything up to the next <h3> or end of string
    const body = parts[i].substring(closeIdx + 5);
    sections.push({ heading, html: '<h3>' + parts[i].split('<h3>')[0] });
  }
  return sections;
}

function buildDiffedRecs(oldSections, newSections) {
  const oldMap = new Map(oldSections.map(s => [s.heading, s.html]));
  const newMap = new Map(newSections.map(s => [s.heading, s.html]));
  const added = [], removed = [];
  const parts = [];

  for (const s of newSections) {
    if (oldMap.has(s.heading)) {
      parts.push(s.html);
    } else {
      parts.push(`<div class="rec-added"><span class="rec-badge"></span>${s.html}</div>`);
      added.push(s.heading);
    }
  }
  for (const s of oldSections) {
    if (!newMap.has(s.heading)) {
      parts.push(`<div class="rec-removed"><span class="rec-badge"></span>${s.html}</div>`);
      removed.push(s.heading);
    }
  }
  return { html: parts.join(''), added, removed };
}

// ── --no-changes: just update last-checked timestamp and show card ───────────

if (noChanges) {
  const liveHtml = fs.readFileSync(livePath, 'utf8');
  const checkedSpan = `<span id="monitor-last-checked" style="font-size:.8rem;font-weight:400;color:#6b7280">— checked ${timeStr}</span>`;
  let updated = liveHtml
    .replace(/<span id="monitor-last-checked"[^>]*>[^<]*<\/span>/, checkedSpan)
    .replace(/(<div class="card" id="monitoring")[^>]*>/, '$1>');
  fs.writeFileSync(livePath, updated, 'utf8');
  console.log(JSON.stringify({ success: true, time: timeStr, noChanges: true }));
  process.exit(0);
}

// ── Build new monitor-log entry ──────────────────────────────────────────────

const liveHtml = fs.readFileSync(livePath, 'utf8');
const draftHtml = fs.readFileSync(draftPath, 'utf8');

const changes = changesRaw ? JSON.parse(changesRaw) : [];
const changeHtml = changes.length > 0
  ? `<ul>${changes.map(c => `<li>${c}</li>`).join('')}</ul>`
  : '<span>Board updated</span>';
const newEntry = `<div class="monitor-entry"><span class="monitor-time">${timeStr}</span> — ${changeHtml}</div>`;

const existingEntries = extractMonitorEntries(liveHtml);
let allEntries = newEntry + (existingEntries || '');

// Trim to 10 entries max
let count = 0, cutIdx = -1;
for (let i = 0; i < allEntries.length; i++) {
  if (allEntries.startsWith('<div class="monitor-entry">', i)) {
    count++;
    if (count === 11) { cutIdx = i; break; }
  }
}
if (cutIdx !== -1) allEntries = allEntries.substring(0, cutIdx);

// ── Diff recs ────────────────────────────────────────────────────────────────

const oldRecsInner = extractRecsInner(liveHtml);
const newRecsInner = extractRecsInner(draftHtml);
// Draft may contain only a placeholder — treat as "no real recs" if no <h3> present
const newHasRealRecs = newRecsInner && newRecsInner.includes('<h3>');
const oldSecs = parseRecSections(oldRecsInner);
const newSecs = newHasRealRecs ? parseRecSections(newRecsInner) : [];

// Preserve live recs when draft only has a placeholder
let mergedRecsInner = newHasRealRecs ? newRecsInner : (oldRecsInner || '');
let recsAdded = [], recsRemoved = [];
if (oldSecs.length > 0 && newSecs.length > 0) {
  const diff = buildDiffedRecs(oldSecs, newSecs);
  mergedRecsInner = diff.html;
  recsAdded = diff.added;
  recsRemoved = diff.removed;
}

// ── Build merged HTML: draft as base, swap in merged recs + monitor-log ─────

let merged = draftHtml;

// Replace recs-content with diffed version (preserves live recs when draft has placeholder)
if (mergedRecsInner) {
  merged = replaceRecsInner(merged, mergedRecsInner);
}

// Replace monitoring card with preserved + new entries, visible, last-checked updated
merged = replaceMonitorCard(merged, allEntries, timeStr);

fs.writeFileSync(livePath, merged, 'utf8');

console.log(JSON.stringify({ success: true, time: timeStr, changes, recsAdded, recsRemoved }));
