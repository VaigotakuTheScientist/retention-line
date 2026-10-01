#!/usr/bin/env python3
"""Build the reader using only Python's standard library."""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
book = json.loads((ROOT / 'book.json').read_text())
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
(OUT / '.nojekyll').touch()

def esc(value):
    return html.escape(str(value), quote=True)

def inline(text):
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)

def prose(text):
    paragraphs = re.split(r'\n\s*\n', text.strip())
    return '\n'.join(f'<p>{inline(p.strip())}</p>' for p in paragraphs)

chapters = [(v, c) for v in book['volumes'] for c in v['chapters']]
assert chapters, 'Add at least one chapter to book.json.'
assert len({c['slug'] for _, c in chapters}) == len(chapters), 'Chapter slugs must be unique.'
for _, c in chapters:
    assert re.fullmatch(r'[a-z0-9-]+', c['slug']), 'Use lowercase letters, digits and hyphens in slugs.'

def shell(title, body, description):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{esc(description)}">
<title>{esc(title)} · {esc(book['title'])}</title>
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<script src="assets/preferences.js"></script>
<link rel="stylesheet" href="assets/style.css">
<script src="assets/reader.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to reading</a>
<header class="site-header">
<a class="wordmark" href="index.html">{esc(book['title'])}</a>
<nav class="tools" aria-label="Reader controls">
<a href="contents.html">Contents</a>
<details class="settings">
<summary aria-label="Reading settings">Aa</summary>
<div class="settings-panel">
<p class="settings-title">Reading settings</p>
<label for="theme">Page colour</label>
<select id="theme"><option value="system">System</option><option value="light">Paper</option><option value="dark">Night</option></select>
<label for="size">Text size <output id="size-label" for="size">21 px</output></label>
<input type="range" id="size" min="17" max="28" step="1" value="21">
</div>
</details>
</nav>
</header>
{body}
<footer class="site-footer">{esc(book['title'])}</footer>
</body>
</html>'''

for i, (volume, chapter) in enumerate(chapters):
    text = (ROOT / chapter['file']).read_text()
    minutes = max(1, round(len(text.split()) / 220))
    prev = (f'<a href="{esc(chapters[i-1][1]["slug"])}.html" rel="prev">← Previous chapter</a>' if i else '<span>First chapter</span>')
    nxt = (f'<a href="{esc(chapters[i+1][1]["slug"])}.html" rel="next">Next chapter →</a>' if i + 1 < len(chapters) else '<span>You’re all caught up.</span>')
    body = f'''<main id="main" class="reading" tabindex="-1">
<header class="chapter-heading">
<p class="eyebrow">Volume {esc(volume['number'])}</p>
<p class="volume-title">{esc(volume['title'])}</p>
<p class="chapter-number">Chapter {esc(chapter['number'])}</p>
<h1>{esc(chapter['title'])}</h1>
<p class="reading-time">{minutes} minute read</p>
</header>
<article aria-label="Chapter {esc(chapter['number'])}: {esc(chapter['title'])}" class="prose">
{prose(text)}
</article>
<div class="end-mark" aria-hidden="true">◇</div>
<nav class="chapter-nav" aria-label="Chapter navigation">{prev}{nxt}</nav>
<a class="back-contents" href="contents.html">Back to contents</a>
</main>'''
    page = shell(chapter['title'], body, f"{book['title']} — Volume {volume['number']}: {volume['title']}. Chapter {chapter['number']}: {chapter['title']}.")
    (OUT / f"{chapter['slug']}.html").write_text(page)
    if i == 0:
        (OUT / 'index.html').write_text(page)

sections = []
for v in book['volumes']:
    links = ''.join(f'<li><a href="{esc(c["slug"])}.html"><span class="toc-number">{esc(str(c["number"]).zfill(2))}</span><span>{esc(c["title"])}</span><span aria-hidden="true">→</span></a></li>' for c in v['chapters'])
    sections.append(f'<section class="volume"><p class="eyebrow">Volume {esc(v["number"])}</p><h2>{esc(v["title"])}</h2><ol class="chapter-list">{links}</ol></section>')
(OUT / 'contents.html').write_text(shell('Contents', f'<main id="main" class="reading contents" tabindex="-1"><p class="eyebrow">The Retention Line</p><h1>Contents</h1>{"".join(sections)}</main>', 'Volumes and chapters of The Retention Line.'))
print(f'Built {len(chapters)} chapter(s) in {OUT}')
