# 爵士101 Reels 照片抓取：Wikimedia Commons（自由授權）＋ Library of Congress（Gottlieb 公有領域）
import json, urllib.request, urllib.parse, time, os, sys, re, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photoplan import P
from PIL import Image
D = 'photos'; os.makedirs(D, exist_ok=True)
UA = {'User-Agent': 'Jazz101Reels/1.0 (educational jazz history account; github jazz101tw)'}
meta = {}; used = set()
def get(u):
    for i in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
        except Exception as e:
            code = getattr(e, 'code', None)
            if code in (400, 403, 404): return None
            ra = 0
            try: ra = int(e.headers.get('retry-after', 0))
            except Exception: pass
            w = min(90, max(ra + 1, 5 + 10 * i)); print('retry', i, code or e, w, u[:80], flush=True); time.sleep(w)
    return None
API = 'https://commons.wikimedia.org/w/api.php?'
IIP = dict(action='query', format='json', prop='imageinfo', iiprop='url|extmetadata|size|mime', iiurlwidth='1600')
def clean(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s or '')).strip()
def from_pages(pages):
    out = []
    for pg in pages:
        ii = (pg.get('imageinfo') or [None])[0]
        if not ii or ii.get('mime') not in ('image/jpeg', 'image/png'): continue
        if ii.get('width', 0) < 600 or ii.get('height', 0) < 450: continue
        em = ii.get('extmetadata', {}); lic = em.get('LicenseShortName', {}).get('value', '')
        if not lic or re.search(r'fair|non-free', lic, re.I): continue
        art = clean(em.get('Artist', {}).get('value', '')) or '作者不詳'
        if re.search(r'unknown|anonymous', art, re.I): art = '作者不詳'
        out.append(dict(src=pg['title'], url=ii.get('thumburl') or ii['url'], artist=art[:70], license=lic, page=ii.get('descriptionurl'), title=pg['title']))
    return out
def commons(q):
    p = dict(IIP); p.update(generator='search', gsrnamespace='6', gsrsearch=q + ' filetype:bitmap', gsrlimit='12')
    r = get(API + urllib.parse.urlencode(p)); time.sleep(1)
    if not r: return []
    pages = sorted(json.loads(r).get('query', {}).get('pages', {}).values(), key=lambda x: x.get('index', 99))
    return from_pages(pages)
def wiki(t):
    r = get('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(dict(action='query', format='json', prop='pageimages', piprop='name', pilicense='free', titles=t, redirects='1'))); time.sleep(1)
    if not r: return []
    f = list(json.loads(r)['query']['pages'].values())[0].get('pageimage')
    if not f: return []
    p = dict(IIP); p.update(titles='File:' + f)
    r = get(API + urllib.parse.urlencode(p)); time.sleep(1)
    return from_pages(json.loads(r).get('query', {}).get('pages', {}).values()) if r else []
def loc(name):
    r = get('https://www.loc.gov/photos/?' + urllib.parse.urlencode(dict(q=name + ' gottlieb', fo='json', c='10'))); time.sleep(3)
    out = []
    if not r: return out
    last = name.split()[-1].lower()
    for it in json.loads(r).get('results', []):
        iu = [u for u in it.get('image_url', []) if 'iiif' in u]
        t = it.get('title') or ''
        if not iu or 'gottlieb' not in json.dumps(it).lower() or last not in t.lower(): continue
        out.append(dict(src=it.get('id') or iu[-1], url=re.sub(r'/full/[^/]+/', '/full/!1600,1600/', iu[-1]), artist='William P. Gottlieb', license='Public domain', page=it.get('id'), title=t))
    return out
PERSON = re.compile(r"^[A-Z][a-zé']+( [A-Z][a-z'.]+)? [A-Z][a-zé']+$")
NOTPERSON = {'Massey Hall', 'Cotton Club', 'Hammond organ', 'Foster Auditorium', 'English Channel', 'Lima, Ohio', 'Jazz kissa', 'Weather Report', 'Little Rock Nine'}
for ep in sorted(P):
    for key, mode, q in P[ep]:
        k = f'{ep}_{key}'; cs = []
        base = re.sub(r' \(.*\)', '', q)
        if mode == 'w' and PERSON.match(base) and base not in NOTPERSON: cs += loc(base)
        if mode == 'w': cs += wiki(q)
        cs += commons(q)
        pick = None
        for c in cs:
            if c['src'] in used: continue
            b = get(c['url'])
            if not b: continue
            try: im = Image.open(io.BytesIO(b)).convert('RGB')
            except Exception: continue
            im.thumbnail((1600, 1600)); fn = k + '.jpg'; im.save(os.path.join(D, fn), quality=90)
            pick = c; time.sleep(1); break
        if pick:
            used.add(pick['src']); pick.update(file=fn, q=q, alts=[dict(url=c['url'], title=c['title'], artist=c['artist'], license=c['license'], page=c['page']) for c in cs if c is not pick and c['src'] not in used][:6])
        meta[k] = pick
        print('ok' if pick else 'NONE', k, (pick or {}).get('license', ''), (pick or {}).get('title', q)[:60], flush=True)
        json.dump(meta, open(os.path.join(D, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
print('DONE', sum(1 for v in meta.values() if v), '/', len(meta))
