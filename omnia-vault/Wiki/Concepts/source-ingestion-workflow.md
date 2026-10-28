---
tags:
  - "concept"
topics:
  - "healthcare-system"
status: growing
created: 2026-10-27
updated: 2026-10-27
sources:
  - Raw/Sources/2026-10-27-starter-tool-verification.md
  - Raw/Sources/omnia-vault-system-demo.md
source_count: 2
aliases:
  - "Ingestion guide"
---

# Source ingestion workflow

To add knowledge, give the agent a URL, document, recording, or pasted notes and
say **"Ingest this into the Healthcare System vault."** The agent captures the
source, compiles linked notes, and validates their provenance.

## Where things go

Paths below are relative to `omnia-vault/`, inside the parent Obsidian vault.

| Content | Location |
| --- | --- |
| Original documents and recordings | `Raw/Files/` (local, gitignored) |
| Captured text and transcripts with provenance | `Raw/Sources/` |
| Compiled knowledge | `Wiki/` |
| Selected screenshots | `assets/` |
| Source note template | `_templates/source-note.md` |

Obsidian's **Templates: Insert template** command exposes the six Omnia
templates. For a manual source note, create it in `Raw/Sources/`, insert
`source-note`, and fill in Title, Reference, Created, and the original content.
Leave `Processed: false`; the coverage scanner updates it after compilation.

## Starter tools

- **Web pages:** Defuddle extracts readable Markdown. Capture its output in a
  source note with the original URL; the clip alone is not compiled knowledge.
- **Documents and notes:** preserve extracted text and the original filename
  or reference, then compile focused Wiki notes.
- **Recordings:** CRV and FFmpeg produce a transcript, frames, and a viewer.
  Review both speech and visuals before compiling; correct uncertainties in
  the compiled notes without rewriting the captured source.
- **Code repositories:** Graphify is installed. Add a specific repository
  before generating a graph; no project code graph exists yet.

## Agent workflow

Run vault commands from the `omnia-vault/` repository, not its parent folder.
In Windows PowerShell, set `$env:PYTHONUTF8='1'` before running Graphify or CRV.

1. Capture the source under `Raw/Sources/` with the required source metadata.
2. Search `python scripts/wiki_tool.py search-catalog --query '<topic>'`.
3. Create or update focused Wiki notes. Each note's `sources` must name real
   captured files, and `source_count` must equal the number of sources.
4. Run the gate below, update the relay baton, and commit the scoped changes.

```powershell
python scripts/wiki_tool.py doctor
python scripts/wiki_tool.py build
python scripts/wiki_tool.py lint
python scripts/wiki_tool.py source-scan --update --accept-covered
python scripts/wiki_tool.py source-lint
python scripts/audit_public.py
```

The pre-commit hook checks vault health, note schemas, source provenance, and
the existing audit rules. The setup session verified clipping and synthetic
recording extraction; the first actual project source is still to come.

## Related

- [[Wiki/Projects/healthcare-system|Healthcare System project]]
- [[Wiki/Topics/healthcare-system|Healthcare System topic]]
- [[Wiki/Concepts/raw-vs-compiled-knowledge|Raw versus compiled knowledge]]
