import json, math, sys
g=json.load(open(sys.argv[1]))['features']
by={f['properties']['dname'].replace('เขต',''):f['geometry']['coordinates'][0] for f in g}
E=['บางซื่อ','ดุสิต','พระนคร','สัมพันธวงศ์','บางรัก','สาทร','ยานนาวา','บางคอแหลม','คลองเตย']
W=['บางพลัด','บางกอกน้อย','บางกอกใหญ่','ธนบุรี','คลองสาน','ราษฏร์บูรณะ','ทุ่งครุ','บางกอกใหญ่']
TOL=2.5e-4
pts=[]
for e in E:
  for w in W:
    if e not in by or w not in by: continue
    wv=by[w]
    for p in by[e]:
      if any(abs(p[0]-q[0])<TOL and abs(p[1]-q[1])<TOL for q in wv): pts.append((p[0],p[1]))
pts=list(dict.fromkeys(pts))
# chain by nearest neighbour from the northernmost point
cur=max(pts,key=lambda p:p[1]); line=[cur]; rest=set(pts); rest.discard(cur)
while rest:
  nxt=min(rest,key=lambda q:(q[0]-cur[0])**2+(q[1]-cur[1])**2)
  if math.hypot(nxt[0]-cur[0],nxt[1]-cur[1])>0.01: break
  line.append(nxt); rest.discard(nxt); cur=nxt
print(len(pts),len(line),'start',line[0],'end',line[-1],'left',len(rest))
json.dump([[round(y,5),round(x,5)] for x,y in line],open(sys.argv[2],'w'))
