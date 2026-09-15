# RISC-V Specification Manuals

This repository contains RISC-V instruction set manuals and specifications for
several ratified extensions. Because many of the original specifications are
distributed only as HTML or PDF files, Markdown versions are also provided so
that the documents can be searched and used efficiently by the included Codex
skill.

## Repository Layout

| Path | Description |
| --- | --- |
| `PDFs/` | Original RISC-V specification documents in PDF format |
| `markdown/` | Specification documents converted to Markdown |
| `riscv-spec-skill/` | Codex skill for consulting the local specifications |
| `scripts/convert_pdfs2md.py` | Batch PDF-to-Markdown conversion script |
| `scripts/install-riscv-skill.sh` | Installation script for the Codex skill |

## Convert PDFs to Markdown

The conversion script uses
[MarkItDown](https://github.com/microsoft/markitdown) to convert PDF files into
Markdown.

### Requirements

- Python 3.8 or later
- The `markitdown` command installed and available on `PATH`

Install MarkItDown:

```sh
pip install "markitdown[pdf]"
```

Convert all PDF files in a directory:

```sh
python3 scripts/convert_pdfs2md.py PDFs
```

The generated files are written to a `markdown/` subdirectory inside the input
directory. For example, the command above writes files to `PDFs/markdown/`.

Useful options:

```sh
# Search subdirectories recursively
python3 scripts/convert_pdfs2md.py PDFs --recursive

# Overwrite existing Markdown files
python3 scripts/convert_pdfs2md.py PDFs --overwrite

# Preview the files that would be converted
python3 scripts/convert_pdfs2md.py PDFs --dry-run

# Set the number of parallel workers
python3 scripts/convert_pdfs2md.py PDFs --workers 8
```

## Install the Codex Skill

Run the installation script from the repository root:

```sh
sh scripts/install-riscv-skill.sh
```

The script installs the skill under `~/.codex/skills/riscv-spec` and adds the
`SPEC_SKILL_ROOT` environment variable to `~/.profile`. Reload the profile after
installation:

```sh
. ~/.profile
```

The skill uses the Markdown files in `$SPEC_SKILL_ROOT/markdown` as its primary
source when answering questions about the RISC-V architecture, extensions,
profiles, privilege levels, debugging, tracing, and related subsystems.
