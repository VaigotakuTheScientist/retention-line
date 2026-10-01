#!/usr/bin/env python3
"""Build both reader languages using only Python's standard library."""
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

UI = {
    'en': dict(contents='Contents', skip='Skip to reading', controls='Reader controls', settings='Reading settings', colour='Page colour', system='System', paper='Paper', night='Night', size='Text size', width='Text width', full='Full width', language='Language', volume='Volume', chapter='Chapter', minutes='minute read', previous='← Previous chapter', next='Next chapter →', first='First chapter', caught='You’re all caught up.', navigation='Chapter navigation', back='Back to contents'),
    'ru': dict(contents='Оглавление', skip='Перейти к чтению', controls='Настройки чтения', settings='Настройки чтения', colour='Цвет страницы', system='Как в системе', paper='Бумага', night='Ночь', size='Размер текста', width='Ширина текста', full='Во всю ширину', language='Язык', volume='Том', chapter='Глава', minutes='мин. чтения', previous='← Предыдущая глава', next='Следующая глава →', first='Первая глава', caught='Вы прочитали всё, что опубликовано.', navigation='Навигация по главам', back='К оглавлению'),
}

def esc(value):
    return html.escape(str(value), quote=True)

def inline(text):
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)

def prose(text, lang):
    # The Russian source is verbatim text, not Markdown; preserve literal symbols.
    render = esc if lang == 'ru' else inline
    return '\n'.join(f'<p>{render(p)}</p>' for p in re.split(r'\n\s*\n', text.strip()))

def localized(record, key, lang):
    return record[key + ('_ru' if lang == 'ru' else '')]

def url(slug, lang):
    return f'{slug}{".ru" if lang == "ru" else ""}.html'

chapters = [(v, c) for v in book['volumes'] for c in v['chapters']]
assert chapters, 'Add at least one chapter to book.json.'
assert len({c['slug'] for _, c in chapters}) == len(chapters), 'Chapter slugs must be unique.'
for _, c in chapters:
    assert re.fullmatch(r'[a-z0-9-]+', c['slug']), 'Use lowercase letters, digits and hyphens in slugs.'

def shell(title, body, description, lang, slug):
    u = UI[lang]
    book_title = localized(book, 'title', lang)
    languages = ''.join(f'<a href="{url(slug, code)}" lang="{code}" hreflang="{code}"{chr(32) + "aria-current=\"true\"" if code == lang else ""}>{label}</a>' for code, label in [('en', 'EN'), ('ru', 'Русский')])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{esc(description)}">
<title>{esc(title)} · {esc(book_title)}</title>
<link rel="alternate" hreflang="en" href="{url(slug, 'en')}">
<link rel="alternate" hreflang="ru" href="{url(slug, 'ru')}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<script src="assets/preferences.js"></script>
<link rel="stylesheet" href="assets/style.css">
<script src="assets/reader.js" defer></script>
</head>
<body>
<a class="skip" href="#main">{u['skip']}</a>
<header class="site-header">
<a class="wordmark" href="{url('index', lang)}">{esc(book_title)}</a>
<nav class="tools" aria-label="{u['controls']}">
<a href="{url('contents', lang)}">{u['contents']}</a>
<span class="language-switch" role="group" aria-label="{u['language']}">{languages}</span>
<details class="settings">
<summary aria-label="{u['settings']}">Aa</summary>
<div class="settings-panel">
<p class="settings-title">{u['settings']}</p>
<label for="theme">{u['colour']}</label>
<select id="theme"><option value="system">{u['system']}</option><option value="light">{u['paper']}</option><option value="dark">{u['night']}</option></select>
<label for="size">{u['size']} <output id="size-label" for="size">21 px</output></label>
<input type="range" id="size" min="17" max="28" step="1" value="21">
<label for="width">{u['width']} <output id="width-label" for="width">660 px</output></label>
<input type="range" id="width" min="660" max="1500" step="60" value="660" data-full-label="{u['full']}">
</div>
</details>
</nav>
</header>
{body}
<footer class="site-footer">{esc(book_title)}</footer>
</body>
</html>'''

for lang, u in UI.items():
    book_title = localized(book, 'title', lang)
    for i, (volume, chapter) in enumerate(chapters):
        text = (ROOT / localized(chapter, 'file', lang)).read_text()
        title = localized(chapter, 'title', lang)
        volume_title = localized(volume, 'title', lang)
        minutes = max(1, round(len(text.split()) / 220))
        prev = (f'<a href="{url(chapters[i-1][1]["slug"], lang)}" rel="prev">{u["previous"]}</a>' if i else f'<span>{u["first"]}</span>')
        nxt = (f'<a href="{url(chapters[i+1][1]["slug"], lang)}" rel="next">{u["next"]}</a>' if i + 1 < len(chapters) else f'<span>{u["caught"]}</span>')
        body = f'''<main id="main" class="reading" tabindex="-1">
<header class="chapter-heading">
<p class="eyebrow">{u['volume']} {esc(volume['number'])}</p>
<p class="volume-title">{esc(volume_title)}</p>
<p class="chapter-number">{u['chapter']} {esc(chapter['number'])}</p>
<h1>{esc(title)}</h1>
<p class="reading-time">{minutes} {u['minutes']}</p>
</header>
<article aria-label="{u['chapter']} {esc(chapter['number'])}: {esc(title)}" class="prose">
{prose(text, lang)}
</article>
<div class="end-mark" aria-hidden="true">◇</div>
<nav class="chapter-nav" aria-label="{u['navigation']}">{prev}{nxt}</nav>
<a class="back-contents" href="{url('contents', lang)}">{u['back']}</a>
</main>'''
        description = f"{book_title} — {u['volume']} {volume['number']}: {volume_title}. {u['chapter']} {chapter['number']}: {title}."
        (OUT / url(chapter['slug'], lang)).write_text(shell(title, body, description, lang, chapter['slug']))
        if i == 0:
            (OUT / url('index', lang)).write_text(shell(title, body, description, lang, 'index'))
    sections = []
    for v in book['volumes']:
        links = ''.join(f'<li><a href="{url(c["slug"], lang)}"><span class="toc-number">{esc(str(c["number"]).zfill(2))}</span><span>{esc(localized(c, "title", lang))}</span><span aria-hidden="true">→</span></a></li>' for c in v['chapters'])
        sections.append(f'<section class="volume"><p class="eyebrow">{u["volume"]} {esc(v["number"])}</p><h2>{esc(localized(v, "title", lang))}</h2><ol class="chapter-list">{links}</ol></section>')
    (OUT / url('contents', lang)).write_text(shell(u['contents'], f'<main id="main" class="reading contents" tabindex="-1"><p class="eyebrow">{esc(book_title)}</p><h1>{u["contents"]}</h1>{"".join(sections)}</main>', f'{u["contents"]} — {book_title}', lang, 'contents'))
print(f'Built {len(chapters)} chapter(s) in English and Russian in {OUT}')
