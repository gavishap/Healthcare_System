from pathlib import Path
import re
root=Path.cwd()
missing=set()
for p in (root/'Wiki').rglob('*.md'):
    for link in re.findall(r'\[\[([^]|#]+)',p.read_text(encoding='utf-8')):
        if link.startswith('Wiki/') and not (root/(link+'.md')).exists():
            missing.add(link)
print('Missing linked notes:',sorted(missing))
