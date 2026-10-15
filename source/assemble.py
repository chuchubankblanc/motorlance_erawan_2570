import sys
d=sys.argv[1]
app=open(d+'/app.html').read()
css=open(d+'/vendor/leaflet.css').read()
data=open(d+'/data.js').read()
body=app.replace('/*__LEAFLET_CSS__*/',css).replace('/*__DATA__*/',data)
import base64
# preview page cannot load font files, so embed them
art=body
for w in ('Regular','Bold'):
    art=art.replace('url("fonts/SaoChingcha-'+w+'.otf")','url("data:font/otf;base64,'+base64.b64encode(open(d+'/fonts/SaoChingcha-'+w+'.otf','rb').read()).decode()+'")')
art=art.replace('<!--__LEAFLET_JS__-->','<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>')
open(d+'/artifact.html','w').write(art)
gh=body.replace('<!--__LEAFLET_JS__-->','<script src="vendor/leaflet.js"></script>')
head,rest=gh.split('\n',1)  # first line is <title>
open(d+'/index.html','w').write('<!doctype html>\n<html lang="th">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+head+'\n'+rest.replace('<div class="wrap">','</head>\n<body>\n<div class="wrap">',1)+'\n</body>\n</html>\n')
