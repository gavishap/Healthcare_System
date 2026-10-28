# Healthcare System vault

## Graphify

When the user types `/graphify`, read the installed Graphify skill before
doing anything else, as requested by the vault owner.

## Omnia ingestion workspace

The Obsidian vault is this folder. Its Omnia project repository is
`omnia-vault/`. For ingestion, knowledge queries, and vault maintenance,
first read `omnia-vault/AGENTS.md` and `omnia-vault/_relay/STATE.md`.
Run Omnia's scripts with the working directory set to `omnia-vault/` so
the source paths, catalog, relay, and Git history stay together.

Capture sources under `omnia-vault/Raw/Sources/` and compile knowledge under
`omnia-vault/Wiki/`. Original binary attachments belong in
`omnia-vault/Raw/Files/`. Follow the applicable bundled ingestion skill.
The starter guide is `omnia-vault/Wiki/Concepts/source-ingestion-workflow.md`.
