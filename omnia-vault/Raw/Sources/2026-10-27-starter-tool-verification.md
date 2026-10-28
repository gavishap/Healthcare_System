---
Title: "Starter ingestion tool verification"
Author: "Codex"
Reference: "Local setup verification, 2026-10-27; scripts/setup_vault.py; ingestion skill instructions"
ContentType:
  - "markdown"
Created: 2026-10-27
Processed: true
tags:
  - "source"
---

# Starter ingestion tool verification

## Tool availability

`python scripts/setup_vault.py --check` and `--install` found all starter tools
already present. No package installation was necessary.

- Python 3.12.3 and Git: available.
- Graphify 0.9.63: CLI help runs. It reports older global skill copies;
  no graph was generated because no project code repository was supplied.
- CRV (`claude-real-video`) 0.7.0: CLI help and a recording extraction run.
- FFmpeg 8.0.1: available, including the media tools needed by CRV.
- Node v22.13.1 and npm 10.9.2: available.
- Defuddle: CLI help and local HTML-to-Markdown conversion run.
- Codex CLI: detected by the vault's setup checker.
- Whisper: available; tiny, base, small, and medium models are already cached.

## Local web clipping check

Defuddle parsed a synthetic HTML article using `defuddle parse <file> --md -o <output>`.
The resulting Markdown retained the two article paragraphs:

> This local article checks that the starter web clipper converts HTML to readable Markdown.
>
> Captured sources retain provenance and compiled notes link back to their source files.

This checks local HTML parsing. It does not test every website or login flow.

## Local recording check

Windows speech synthesis produced a short WAV recording. FFmpeg combined it
with a synthetic video, then CRV processed it with `--lang en --whisper-model tiny
--max-frames 3 --viewer` in temporary storage outside the vault.

CRV produced three retained frames, a manifest, a viewer, and this transcript:

> This is the Injection Setup check.
> The vault is ready for documents and recordings.

The spoken word "ingestion" was transcribed as "Injection". This demonstrates
why transcripts need review. External video URLs, authentication, and larger
recordings were not exercised. No actual project recording was ingested.

## Obsidian and workflow configuration

The active vault is the parent `Healthcare_System` folder, with Omnia in its
`omnia-vault/` subfolder. Obsidian's Templates plugin now lists all six Omnia
templates from `omnia-vault/_templates`. New attachments go to
`omnia-vault/Raw/Files`, whose binary contents are gitignored by Omnia.

The maintenance hook is enabled with `core.hooksPath = .githooks`.

The bundled `llm-wiki-ingest` and `video-ingest` instructions define the workflow:
capture the full source with its reference, search the catalog, compile focused
Wiki notes citing that source, rebuild, scan coverage, lint, and audit. CRV
outputs belong in scratch storage; only reviewed source captures and selected
screenshots belong in committed knowledge.
