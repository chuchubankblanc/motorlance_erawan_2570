import json, sys, re, math, subprocess
geo_path, docx_path, out_path, sub_path = sys.argv[1:5]
txt = subprocess.run(['pandoc', docx_path, '-t', 'plain', '--wrap=none'], capture_output=True, text=True).stdout
teams = []; cur = None
for line in txt.splitlines():
    line = line.strip()
    if not line: continue
    if line.startswith('MTL'):
        m = re.match(r'MTL\s+(.+?)\s*(?:\((.+)\))?$', line)
        cur = {'name': m.group(1).strip(), 'hospital': (m.group(2) or ('รพ.' + m.group(1).strip())).strip(), 'points': []}
        teams.append(cur); continue
    m = re.match(r'(.+?)\s+(\d+\.\d+),\s*(\d+\.\d+)$', line)
    if m: cur['points'].append({'name': m.group(1).strip(), 'lat': float(m.group(2)), 'lng': float(m.group(3))})

def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dmax, idx = 0, 0
    for i in range(1, len(pts)-1):
        p = pts[i]
        dx, dy = b[0]-a[0], b[1]-a[1]
        if dx == dy == 0: d = math.hypot(p[0]-a[0], p[1]-a[1])
        else: d = abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/math.hypot(dx, dy)
        if d > dmax: dmax, idx = d, i
    if dmax > eps: return rdp(pts[:idx+1], eps)[:-1] + rdp(pts[idx:], eps)
    return [a, b]
def pip(x, y, ring):
    ins = False; j = len(ring)-1
    for i in range(len(ring)):
        xi, yi = ring[i]; xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj-xi)*(y-yi)/(yj-yi)+xi: ins = not ins
        j = i
    return ins
g = json.load(open(geo_path)); feats = []
for f in g['features']:
    geom = f['geometry']
    polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
    raw = polys
    simp = [[[[round(x, 4), round(y, 4)] for x, y in rdp(r, 0.0006)] for r in poly[:1]] for poly in polys]
    feats.append({'type': 'Feature', 'properties': {'name': f['properties']['dname'].replace('เขต', ''), 'en': f['properties']['dname_e']},
                  'geometry': {'type': 'MultiPolygon', 'coordinates': simp}, '_raw': raw})
for t in teams:
    for p in t['points']:
        p['district'] = None
        for f in feats:
            if any(pip(p['lng'], p['lat'], poly[0]) for poly in f['_raw']): p['district'] = f['properties']['name']; break
subs = json.load(open(sub_path))['features']
for t in teams:
    for p in t['points']:
        p['subdistrict'] = None
        for f in subs:
            if pip(p['lng'], p['lat'], f['geometry']['coordinates'][0]):
                p['subdistrict'] = f['properties']['SNAME'].replace('แขวง', ''); sd = f['properties']['DNAME'].replace('เขต', '')
                if sd != p['district']: print('MISMATCH', p['name'], sd, p['district'])
                break
for f in feats: del f['_raw']
data = {'teams': teams, 'districts': {'type': 'FeatureCollection', 'features': feats}}
open(out_path, 'w').write('window.MTL_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
for t in teams: print(t['name'], '|', t['hospital'], len(t['points']), [(p['subdistrict'], p['district']) for p in t['points']])
print(sum(len(t['points']) for t in teams), 'points', len({p['district'] for t in teams for p in t['points']}), 'districts')
