import json, urllib.request, concurrent.futures
from urllib.parse import urlencode
from pathlib import Path

base = Path('Raw/Files/prototype-challenge')
endpoints = {
    'clinicaltrials': 'https://clinicaltrials.gov/api/v2/studies?' + urlencode({'query.cond':'type 2 diabetes','pageSize':1,'format':'json'}),
    'pubmed': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?' + urlencode({'db':'pubmed','term':'type 2 diabetes','retmax':1,'retmode':'json'})
}
def probe(name,url):
    try:
        req = urllib.request.Request(url,headers={'User-Agent':'HealthcareArchitectureReview/0.1'})
        with urllib.request.urlopen(req,timeout=25) as resp:
            data = json.load(resp)
        (base / (name+'-sample.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        return {'source':name,'status':'ok','top_level_fields':list(data),'meaning':'One public GET succeeded; this is not clinical validation or an application integration test.'}
    except Exception as e:
        return {'source':name,'status':'failed','error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(lambda p:probe(*p), endpoints.items()))
(base/'probe-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
