from pathlib import Path
import subprocess, concurrent.futures, tempfile, json, time, os, sys

root = Path.cwd()
local = root / 'Raw/Files/prototype-challenge'
codex = '[USER_HOME]/AppData/Local/OpenAI/Codex/bin/a96ca4c1eee0cf35/codex.exe'
claude = 'C:/nvm4w/nodejs/node_modules/@anthropic-ai/claude-code/bin/claude.exe'
pack = (local / 'context.md').read_text(encoding='utf-8')
outsider = '''Decision only: Choose an architecture for a two-hour prototype and later full-stack product that turns a medical condition into a cited research briefing for a health system strategy team: current care landscape, emerging therapies, and involved organizations. Options: typed Python API plus React, one TypeScript full-stack service, Streamlit/n8n, or an autonomous multi-agent workflow. How should deterministic evidence controls and LLM reasoning/tool calls divide responsibilities? The tool compares evidence/development stages rather than advising individual patients. Argue as an OUTSIDER who has no project history, in 150-300 words. No tools, file access, writes, or delegation. End POSITION: <one-sentence stance>.'''

def run(name, bench, prompt, outside=False):
    out = local / f'{name}.txt'
    (local / f'{name}-prompt.md').write_text(prompt, encoding='utf-8')
    wd = tempfile.mkdtemp(prefix='health-council-outsider-') if outside else str(root)
    for attempt in range(2):
        started = time.monotonic()
        if bench == 'codex':
            args = [codex, 'exec', '-s', 'read-only', '--skip-git-repo-check', '--json', '-o', str(out), '-']
        else:
            args = [claude, '-p', '--permission-mode', 'plan', '--output-format', 'json', '--tools', '', '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}', '--disable-slash-commands']
        try:
            # Regular files prevent inherited child stdout handles from delaying EOF.
            stdout_path=local/f'{name}-stdout-{attempt+1}.jsonl'
            stderr_path=local/f'{name}-stderr-{attempt+1}.txt'
            with stdout_path.open('w',encoding='utf-8') as so, stderr_path.open('w',encoding='utf-8') as se:
                p = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=so,stderr=se,text=True,encoding='utf-8',errors='replace',cwd=wd)
                try:
                    p.communicate(input=prompt,timeout=600)
                except subprocess.TimeoutExpired:
                    p.kill()
                    p.wait()
                    raise
            stdout=stdout_path.read_text(encoding='utf-8',errors='replace')
            stderr=stderr_path.read_text(encoding='utf-8',errors='replace')
            (local / f'{name}-execution-{attempt+1}.json').write_text(json.dumps({'returncode':p.returncode,'stdout':stdout,'stderr':stderr,'elapsed':round(time.monotonic()-started,1)}, ensure_ascii=False), encoding='utf-8')
            if bench == 'claude':
                try:
                    obj = json.loads(stdout)
                    if not obj.get('is_error'):
                        out.write_text(obj.get('result',''), encoding='utf-8')
                except (ValueError, TypeError):
                    pass
            if p.returncode == 0 and out.exists() and out.stat().st_size:
                print(f'{name}: complete ({round(time.monotonic()-started)}s)', flush=True)
                return name
            print(f'{name}: failed attempt {attempt+1}; exit {p.returncode}', flush=True)
        except subprocess.TimeoutExpired:
            print(f'{name}: 600s timeout; no blind retry', flush=True)
            break
    print(f'{name}: DEAD SEAT', flush=True)
    return name

if __name__ == '__main__':
    seats = [('rebuilder','claude','Rebuilder: discard assumptions; rebuild from first principles.'),('maximalist','claude','Maximalist: find the bigger product opportunity and upside; argue strongly for it.'),('skeptic','codex','Skeptic: hunt the fatal flaw and try to kill the wrong approach.'),('operator','codex','Operator: ground the decision in what can actually ship within the prototype budget.'),('outsider','codex','')]
    # Three independent seats at a time respects the available concurrency budget.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        fs = [pool.submit(run,n,b,outsider if n=='outsider' else role+'\n\n'+pack,n=='outsider') for n,b,role in seats]
        for f in concurrent.futures.as_completed(fs):
            f.result()
    print('Round 1 finished. Read outputs before cross-review.', flush=True)
