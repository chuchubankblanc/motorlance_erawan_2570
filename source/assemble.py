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

# หน้าแชร์งานลอยกระทง: สำเนาเต็มของหน้า (ไม่ redirect) เพื่อให้ LINE/Facebook อ่านหัวข้อและภาพตัวอย่างของหน้านี้
import os
LOY_TITLE='การปฏิบัติการการแพทย์ฉุกเฉินของ กทม. ในวันลอยกระทง 2569'
LOY_DESC='ศูนย์เอราวัณ สำนักการแพทย์ กรุงเทพมหานคร · แผนที่จุด standby รถพยาบาล รถ ALS โรงพยาบาล Motorlance และ HYDROLANCE ในวันลอยกระทง 24 พ.ย. 2569'
BASE='https://chuchubankblanc.github.io/motorlance_erawan_2570/'
def og(title,desc,url,img):
    t=[('og:type','website'),('og:site_name','ศูนย์เอราวัณ สำนักการแพทย์ กรุงเทพมหานคร'),('og:title',title),('og:description',desc),('og:url',url),('og:locale','th_TH')]
    if img: t+=[('og:image',img),('og:image:width','1200'),('og:image:height','630')]
    out='<meta name="description" content="%s">\n' % desc
    out+=''.join('<meta property="%s" content="%s">\n' % kv for kv in t)
    out+='<meta name="twitter:card" content="%s">\n' % ('summary_large_image' if img else 'summary')
    return out
main=open(d+'/index.html').read()
main=main.replace(head+'\n', head+'\n'+og('Motorlance กทม.','แผนที่มอเตอร์ไซค์พยาบาลฉุกเฉิน (Motorlance) ของโรงพยาบาลในสังกัดสำนักการแพทย์ กรุงเทพมหานคร · ศูนย์เอราวัณ',BASE,None),1)
open(d+'/index.html','w').write(main)
# loy2569/ คือลิงก์หลักสำหรับแชร์ (ใหม่ LINE ยังไม่เคยจำ); loykrathong/ เก็บไว้ให้ลิงก์ที่แชร์ไปแล้วยังใช้ได้
for slug in ('loy2569','loykrathong'):
    loy=main.replace('<meta charset="utf-8">','<meta charset="utf-8">\n<base href="../">',1)
    loy=loy.replace(head,'<title>'+LOY_TITLE+'</title>',1)
    i=loy.index('<meta name="description"'); j=loy.index('<meta name="twitter:card"'); j=loy.index('\n',j)+1
    loy=loy[:i]+og(LOY_TITLE,LOY_DESC,BASE+slug+'/',BASE+'loykrathong/og.jpg?v=2')+loy[j:]
    loy=loy.replace('</head>','<script>window.START_VIEW="loy"</script>\n</head>',1)
    os.makedirs(d+'/'+slug,exist_ok=True)
    open(d+'/'+slug+'/index.html','w').write(loy)
