# Contributing to the Documentation

Welcome! We use `mkdocs`, a documentation build system that renders markdown source files as html to be served as a set of static web pages on the internet. We use `mkdocs-material` as the base for our theming and plugins.

The production documentation can be viewed at <https://gs-us.github.io/strikecard-backend/>.

## Installation

- Obtain the repository from <https://github.com/GS-US/strikecard-backend>.
    - If you are a Quality Assurance Tester or Developer, then you may have already have the repository from when you ran `install.sh`. If so, you can find the documentation source in your local repository at `$INSTALL_DIR/docs`.
    - Otherwise, clone the repository from <https://github.com/GS-US/strikecard-backend.git>.
        - How to: [Cloning a repository (GitHub.com)](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
- Install the Python requirements.

## Working With the Docs

### Installing the Docs

TBD

### Building the Docs

To check for errors, use the following command.

```shell
mkdocs build --strict
```

To engage with a local dynamic server, use the following command.

```shell
mkdocs serve
```

## Documentation

### Docs Configuration

Defined in [`mkdocs.yml`](https://github.com/GS-US/strikecard-backend/blob/main/mkdocs.yml). Controls navigation layout in the rendered docs.

### Docs Content

Defined in [`docs/`](https://github.com/GS-US/strikecard-backend/tree/main/docs).

#### Blogs for Meeting Notes

Each blog has a directory named like `blog-new-strike-card`. The part after `blog-` is the blog title. When adding a new file, put it under `blog-title/posts/` with a date-prefixed name using ISO dates, i.e., `yyyy-mm-dd`.

For meeting notes, use the pattern `yyyy-mm-dd-meeting-notes.md`.

All blog files must start with front matter including the creation date, like the following. Use a full ISO datetime with your timezone offset.

```yaml
---
date:
    created: 2025-12-31T12:34:56-05:00
---
```

After the front matter comes a level 1 heading like `# <blog-title> - Meeting yyyy-mm-dd`. A new Strikecard meeting note would be placed in `/docs/blog-new-strike-card/posts/2025-12-31-meeting-notes.md`.

Include a text-based or unordered list summary of the meeting and agenda. After the summary, all blog posts require `<!-- more -->` to indicate the summary cutoff.

Here is a full example, putting it all together.

```markdown
---
date:
    created: 2025-12-31T12:34:56-05:00
---

# New Strike Card - Meeting 2025-12-31

Today we talked about some strike card related things.

- Thing 1
- Thing 2

<!-- more -->

## A Subheading

And the rest...
```

## Archival Script

See the [Archive README](https://github.com/GS-US/strikecard-backend/blob/main/archive/README.md).
