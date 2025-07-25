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

Defined in [`mkdocs.yml`](./mkdocs.yml). Controls navigation layout in the rendered docs.

### Docs Content

Defined in [`docs/`](docs/).

#### Blog, News, and Notes

Please give a date-based name with a title like `yyyy-mm-dd-title.md` and put in
[`docs/blog/posts/`](docs/blog/posts/).

## Archival Scripts

See the [Archive README](archive/README.md).
