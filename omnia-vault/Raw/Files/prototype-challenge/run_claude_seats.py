import concurrent.futures
from run_council import run, pack
seats=[('rebuilder','Rebuilder: discard assumptions; rebuild from first principles.'),('maximalist','Maximalist: find the bigger product opportunity and upside; argue strongly for it.')]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    fs=[pool.submit(run,n,'claude',r+'\n\n'+pack) for n,r in seats]
    for f in concurrent.futures.as_completed(fs):
        f.result()
