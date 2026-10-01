# The Retention Line

A quiet, mobile-friendly webnovel reader. Includes Volume I, *The Present That Never Was*, and Chapter 1, *What Had Already Ended*, using the English translation supplied in the conversation.

Features: comfortable serif typography, paper and night themes, adjustable text size and reading width, volume/chapter contents and previous/next chapter navigation. English/Russian links switch between the original Russian text and the English translation of that source. Display preferences stay on the reader's device. No analytics, external fonts or runtime dependencies. The complete chapter remains readable without JavaScript.

## Add a chapter

1. Create a UTF-8 Markdown file in `chapters/`, for example `volume-1-chapter-2.md`.
2. Add the original Russian text as `chapters/volume-1-chapter-2.ru.md`, preserving its wording and paragraph breaks. Translate it into English for the `.md` file above.
3. Separate paragraphs with a blank line. Use `*italics*` and `**bold**`. The simple renderer supports these inline styles and paragraphs; do not include a title in the chapter file.
4. Add its entry to the relevant `chapters` array in `book.json`:

```json
{
  "number": 2,
  "title": "Your chapter title",
  "title_ru": "Название главы",
  "slug": "volume-1-chapter-2",
  "file": "chapters/volume-1-chapter-2.md",
  "file_ru": "chapters/volume-1-chapter-2.ru.md"
}
```

Commit the changes to `main`. The included GitHub Actions workflow builds and publishes automatically once Pages is enabled. Contents and chapter navigation update automatically. The home page opens on the first chapter.

For another volume, add an object to `volumes` with `number`, `title`, `title_ru`, and a `chapters` array. Both language versions are required; the build stops if one is missing rather than silently showing the wrong language.

## Run locally

```sh
python3 build.py
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. Python 3 is the only build dependency.

## Publish on GitHub Pages

1. Create a GitHub repository and upload this project, including `.github/workflows/pages.yml`.
2. In **Settings → Pages → Build and deployment → Source**, choose **GitHub Actions**.
3. Push to `main` or run **Actions → Publish reader → Run workflow**.

Alternatively, select **Deploy from a branch**, branch `main`, folder `/docs`. With that option, run `python3 build.py` and commit the generated `docs/` after every content edit; disable the Actions workflow to avoid competing deployments.

The site uses relative URLs and works under a repository subpath.

## Files

- `book.json`: volume and chapter titles, order and source file locations.
- `chapters/`: chapter prose.
- `assets/`: reader appearance and preferences.
- `build.py`: static HTML generator.
- `docs/`: generated website, also usable directly without a build server.

No license is granted for the novel text by this repository.

The Russian chapter text is copied verbatim from the original Google Doc, including its paragraph structure. The English version is a literary translation checked against that original. Russian files are rendered as plain text; only English files use the minimal Markdown formatting.
