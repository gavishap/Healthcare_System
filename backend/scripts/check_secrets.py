"""Fail on actual configured key values in prospective tracked code or the frontend build."""

from pathlib import Path
import subprocess
from app.config import get_settings

root = Path(__file__).resolve().parent.parent
settings = get_settings()
secrets = [
    s
    for s in [
        settings.openai_api_key.get_secret_value(),
        settings.ncbi_api_key.get_secret_value(),
        settings.app_access_token.get_secret_value(),
    ]
    if len(s) > 8
]
findings = []
for repo in [root, root.parent / "frontend"]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=repo,
        capture_output=True,
        check=True,
    )
    files = [repo / p.decode("utf-8") for p in result.stdout.split(b"\0") if p]
    if repo.name == "frontend":
        files += list((repo / "dist").rglob("*"))
    for file in files:
        if not file.is_file():
            continue
        data = file.read_bytes()
        if any(secret.encode() in data for secret in secrets):
            findings.append(str(file.relative_to(root.parent)))
    tracked = subprocess.run(
        ["git", "ls-files", ".env", ".env.*"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    if any(p != ".env.example" for p in tracked):
        findings.append(repo.name + " has a tracked secret environment file")
print(
    "Secret checks: "
    + (
        "FAILED: " + ", ".join(findings)
        if findings
        else "passed; configured keys absent from candidate code/builds and environment files untracked."
    )
)
raise SystemExit(bool(findings))
