# The Retention Line

A quiet, mobile-friendly webnovel reader. Includes Volume I, *The Present That Never Was*, and Chapter 1, *What Had Already Ended*, using the English translation supplied in the conversation.

Features: comfortable serif typography, paper and night themes, adjustable text size, volume/chapter contents and previous/next chapter navigation. Preferences stay on the reader's device. No analytics, external fonts or runtime dependencies. The complete chapter remains readable without JavaScript.

## Add a chapter

1. Create a UTF-8 Markdown file in `chapters/`, for example `volume-1-chapter-2.md`.
2. Separate paragraphs with a blank line. Use `*italics*` and `**bold**`. The simple renderer supports these inline styles and paragraphs; do not include a title in the chapter file.
3. Add its entry to the relevant `chapters` array in `book.json`:

```json
{
  "number": 2,
  "title": "Your chapter title",
  "slug": "volume-1-chapter-2",
  "file": "chapters/volume-1-chapter-2.md"
}
```

Commit the changes to `main`. The included GitHub Actions workflow builds and publishes automatically once Pages is enabled. Contents and chapter navigation update automatically. The home page opens on the first chapter.

For another volume, add an object to `volumes` with `number`, `title`, and a `chapters` array.

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
