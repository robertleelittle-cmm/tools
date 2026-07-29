// Marp config for CoverMyMeds decks. Carries the brand theme and the column
// engine, so any marp-cli invocation reproduces the same HTML with no repo
// dependencies to install:
//
//   npx @marp-team/marp-cli deck.md -c .claude/assets/marp/marp.config.js --no-stdin -o deck.html
//
// marp-cli constructs the Marp instance and hands it to `engine` below; we only
// add a small markdown-it rule. Portable to CI and the VS Code Marp extension.
const path = require('path');

// Expand markdown-neutral HTML-comment markers into the theme's column/card
// divs, inserting the blank lines Marp needs. Authors write only comments, so a
// deck stays formatter-safe (Prettier leaves comments alone) and free of layout
// HTML and `html: true`.
//
//   <!-- columns -->        open a row   (<!-- columns three --> for 3 across)
//   <!-- col orange -->     start a column with a card style
//                           (orange | magenta | blue | navy)
//   <!-- col -->            start a plain (uncolored) column
//   <!-- /columns -->       close the row
function expandColumns(src) {
  const out = [];
  let inCol = false;
  const closeCol = () => { if (inCol) { out.push('', '</div>'); inCol = false; } };
  for (const line of src.split('\n')) {
    const m = line.match(/^\s*<!--\s*(columns|col|\/columns)\b\s*([^>]*?)\s*-->\s*$/);
    if (!m) { out.push(line); continue; }
    const [, kind, rest] = m;
    const args = rest.trim();
    if (kind === 'columns') {
      out.push(`<div class="${args ? `cols ${args}` : 'cols'}">`);
    } else if (kind === 'col') {
      closeCol();
      out.push(`<div class="${args ? `card ${args}` : 'col'}">`, '');
      inCol = true;
    } else { // /columns
      closeCol();
      out.push('</div>');
    }
  }
  return out.join('\n');
}

// Rewrite the source before markdown-it parses it, so Marp reads the real file
// (live --preview --watch keeps working) and the divs are generated at render.
const columnsPlugin = (md) => {
  md.core.ruler.before('normalize', 'expand_columns', (state) => {
    state.src = expandColumns(state.src);
  });
};

module.exports = {
  html: true,                                            // render the generated divs
  allowLocalFiles: true,                                 // decks may reference local images
  themeSet: [path.join(__dirname, 'covermymeds.css')],   // register the brand theme
  engine: ({ marp }) => marp.use(columnsPlugin),
};
