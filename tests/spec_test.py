"""ชุดทดสอบตามทะเบียนข้อกำหนด (REQUIREMENTS.md)
รัน:  python3 tests/spec_test.py            (ต้องมี: pip install playwright && playwright install chromium)
ผลลัพธ์: แต่ละบรรทัด = รหัสข้อกำหนด ผ่าน/ไม่ผ่าน · ออกด้วยรหัส 1 ถ้ามีข้อไม่ผ่าน
ทุกครั้งที่เพิ่มข้อกำหนดใหม่ใน REQUIREMENTS.md ให้เพิ่มการตรวจที่นี่ด้วย"""
import os, sys, zipfile, io, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "index.html").as_uri()
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
results = []
def check(rid, ok, note=""):
    results.append((rid, bool(ok), note)); print(("ผ่าน  " if ok else "ไม่ผ่าน ") + rid + ("  " + note if note else ""))

with sync_playwright() as p:
    kw = {"executable_path": CHROME} if os.path.exists(CHROME) else {}
    b = p.chromium.launch(**kw)
    pg = b.new_page(viewport={"width": 1500, "height": 1100}, accept_downloads=True)
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(900)
    ev = lambda js: pg.evaluate(js)
    def tab(i, view="real"):
        ev(f"()=>{{document.querySelectorAll('#tabs button')[{i}].click();document.getElementById('bSample').click();setView('{view}')}}"); pg.wait_for_timeout(450)

    check("R-02", ev("()=>document.querySelectorAll('#tabs button').length") == 5)
    check("R-06", ev("()=>{const d=defaults();return d.font==='TH SarabunIT๙'&&d.thai===true}"))
    check("R-10", ev("()=>{const {F}=build();const g=F.find(f=>f.kind==='img');return Math.abs(GARUDA_RATIO-167/177)<0.001&&g&&g.h===30&&Math.abs(g.x+g.w/2-105)<0.1}"))
    check("R-14", ev("()=>/^\\s+\\S+ (พ\\.ศ\\. )?\\d{4}$/.test(thaiDate('2026-11-06'))&&!/\\d\\s+พฤศ/.test(thaiDate('2026-11-06'))"))
    check("R-33", ev("""()=>{const w=t=>segWords(t).map(x=>x.t);const has=(t,k)=>w(t).includes(k);
       return has('เวลา 09.30 น. ณ','09.30 น.')&&has('ปี พ.ศ. 2569 นี้','พ.ศ. 2569')&&w('อัยการ กอ.รมน.จังหวัด').some(x=>x.startsWith('กอ.รมน.'))&&has('มาตรา 56 (ข) และ','(ข)')&&w('ผู้อำนวยการกอง').some(x=>x.startsWith('ผู้อำนวยการ'))}"""))
    check("R-68", ev("()=>[['073-211-586','0 7321 1586'],['0869608696','086 960 8696'],['+66 86 960 8696','086 960 8696'],['๐๗๓๒๑๑๕๘๖','0 7321 1586'],['0 7321 1586 ต่อ 12','0 7321 1586 ต่อ 12'],['073211586/073211587','0 7321 1586/0 7321 1587'],['ที่ ยล 0017.1/1872','ที่ ยล 0017.1/1872'],['0 7321 1586 - 7','0 7321 1586 - 7']].every(([a,b])=>normTel(a)===b)"), "เบอร์โทรทุกรูปแบบ")
    check("R-65", ev("()=>normNo('ยล0017.2/ว123')==='ยล 0017.2/ว 123'&&normNo('มท 0211.5/ว 8876')==='มท 0211.5/ว 8876'&&normNo('123/2569')==='123/2569'"), "เว้นวรรคเลขที่หนังสืออัตโนมัติ")
    check("R-36", ev("()=>{D.body='ก\\n>ข';const {P}=build();const a=P.find(p=>p.runs.some(r=>r.t==='ข'));return a&&a.first===30}"))

    # ---- หนังสือภายนอก (ข้อมูลตัวอย่างเต็ม 2 หน้า) ----
    tab(0)
    check("R-01", ev("()=>document.querySelectorAll('#form input[type=date],#form input[type=month]').length===0"), "ไม่มีช่องวันที่ของเบราว์เซอร์")
    check("R-13", ev("()=>{const {P}=build();const i=P.findIndex(p=>p.runs.length===1&&/^\\s+\\S+ [0-9๐-๙]{4}$/.test(p.runs[0].t));return i>0&&P[i].before===12}"))
    check("R-15", ev("()=>!document.getElementById('page').textContent.includes('(ชื่อเต็ม)')"))
    check("R-20", ev("()=>{const {P}=build();return P.some(p=>p.runs.some(r=>/^[2๒]\\.$/.test(r.t)))}"))
    check("R-21", ev("()=>{const {P}=build();return P.filter(p=>p.rtab).every(p=>p.runs.some(r=>/^จำนวน/.test(r.t)))&&P.filter(p=>p.rtab).length>=2}"))
    check("R-22", ev("()=>{const {P}=build();return P.some(p=>p.runs.length===1&&/^ครั้งที่ [1๑][1๑]\\/[2๒][5๕][6๖][9๙]/.test(p.runs[0].t))}"))
    check("R-23", ev("()=>{const L=[...document.querySelectorAll('#page .jt')].filter(j=>/^หนังสือกระทรวงมหาดไทย/.test(j.textContent));return L.length&&L.every(j=>j.dataset.last==='1')}"))
    lines = ev("""()=>[...document.querySelectorAll('#page .jt')].map(sp=>{const m=[...sp.querySelectorAll('span')].map(s=>parseFloat(s.style.marginRight)).filter(x=>!isNaN(x));
        const pr=sp.parentElement.getBoundingClientRect(),q=sp.getBoundingClientRect();return {ls:m[0]||0,last:sp.dataset.last,over:q.right-pr.right}})""")
    check("R-30", any(l["last"] == "0" and l["ls"] > 0 for l in lines) and all(l["ls"] <= 0.05 for l in lines if l["last"] == "1" and l["over"] < 0))
    check("R-31", max(l["ls"] for l in lines) <= 1.5 and max(l["over"] for l in lines) <= 1.0, f"ยืดสูงสุด {max(l['ls'] for l in lines):.2f}px ล้นสูงสุด {max(l['over'] for l in lines):.1f}px")
    check("R-32", ev("()=>{const {P}=build();const p=P.find(p=>p.runs.some(r=>r.br));return !!p}"))
    check("R-35", ev("()=>document.querySelectorAll('#form .pbox').length>0&&!document.querySelector('#form textarea.big')&&!/\\*\\*/.test(document.querySelector('#form .pbed').textContent)"), "ไม่แสดง ** ในช่องข้อความ")
    check("R-37", ev("()=>!!document.querySelector('#form .combo')&&!document.querySelector('[data-k=endpX]')"))
    check("R-40", ev("()=>{const {P}=build();const c=P.find(p=>p.runs.length===1&&p.runs[0].t==='ขอแสดงความนับถือ');return c&&c.before>=12}"))
    check("R-41", ev("()=>{const {P,F}=build();const b=F.find(f=>f.kind==='block'&&f.mode==='side');const iPos=b?b.at:-1,iOwn=P.findIndex(p=>p.runs.some(r=>r.t==='สำนักงานจังหวัด'));return b&&b.qr&&b.lines.join()==='สิ่งที่ส่งมาด้วย'&&iOwn>iPos&&P.some(p=>p.runs.some(r=>r.t==='สำเนาส่ง'))}"), "QR ข้างลายมือชื่อ ส่วนราชการเจ้าของเรื่องอยู่ใต้ตำแหน่ง")
    check("R-50", ev("()=>document.querySelectorAll('#page .sheet').length===2&&/๒/.test(document.querySelector('#page .pgno').textContent)"))
    check("R-51", ev("()=>{const {P}=build();const i=P.findIndex(p=>p.runs.length===1&&p.runs[0].t==='ขอแสดงความนับถือ');let n=0;for(let j=i-1;j>=0&&P[j].keep;j--)n+=Math.ceil((measure(P[j].runs.map(r=>r.t||'').join(''))+(P[j].first||0))/(CW-P[j].indL-P[j].indR));return n>=2}"))
    check("R-52", ev("()=>{const {P}=build();return P.filter(p=>p.runs.some(r=>/ดังนี้\\s*$/.test(r.t||''))).every(p=>p.kn)}"))
    check("R-61", ev("()=>{const b=document.querySelector('#form .pbox');return Math.abs(parseFloat(getComputedStyle(b).fontSize)-16*96/72*(b.clientWidth-16)/(160*96/25.4))<1.5}"))
    check("R-54", ev("()=>{const op=window.print;window.print=()=>{};doPrint();window.print=op;const n=document.querySelectorAll('#print .psheet').length,k=document.querySelectorAll('#page .sheet').length;const ok=n===k&&/margin:0/.test(document.getElementById('pagecss').textContent)&&!document.querySelector('#print .guide');document.getElementById('print').innerHTML='';return ok}"), "หน้า PDF = หน้าพรีวิว ขอบ 0")
    tab(0, "copy")
    check("R-11", ev("()=>{const {F}=build();const t=F.find(f=>f.kind==='text'&&f.text==='สำเนาคู่ฉบับ');return t&&t.pt>=32&&!F.some(f=>f.kind==='img')&&F.some(f=>f.kind==='initials')}"))
    with pg.expect_download() as dl: pg.click("#bDocx")
    data = open(dl.value.path(), "rb").read()
    z = zipfile.ZipFile(io.BytesIO(data)); x = z.read("word/document.xml").decode(); h = z.read("word/header1.xml").decode()
    check("R-03", data[:2] == b"PK" and "w:body" in x)
    check("R-80", all(k in x for k in ["keepNext", 'w:val="right"', "\u00a0", 'w:pgNumType w:fmt="thaiNumbers"']) and "PAGE" in h)
    nl = ev("()=>[...document.querySelectorAll('#page .jt')].filter(j=>j.dataset.last==='0').length")
    check("R-81", x.count("<w:br/>") >= nl and 'w:lineRule="exact"' in x and "<w:widowControl/>" in x and 'w:jc w:val="both"' in x, f"br {x.count('<w:br/>')} / บรรทัดพรีวิว {nl}")
    import re as _re
    check("R-81", bool(_re.search(r'<w:spacing w:val="-?\d+"/><w:sz ', x)) and not _re.search(r'<w:u [^>]*/>(<w:color|<w:spacing|<w:sz )', x), "ลำดับ rPr ตาม schema (Word ไม่ทิ้งระยะตัวอักษร)")

    # ---- ประเภทอื่น ----
    for i, name in [(1, "memo"), (2, "stamp"), (3, "order")]:
        tab(i)
        check("R-63", ev("()=>document.querySelectorAll('#page .sheet').length===2"), f"{name} ยาว 2 หน้า")
    for i in (0, 2):
        tab(i)
        check("R-39", ev("()=>!document.querySelector('#form [data-k=secs] select')&&D.secs.length===1&&document.querySelectorAll('#form .pbox').length>3&&document.querySelectorAll('#form .pbox.single:not(.grp)').length===0"), ["ภายนอก","","ประทับตรา"][i]+" ไม่มีหัวข้อ หลายกล่อง")
        if i == 0: check("R-64", ev("()=>{const b=[...document.querySelectorAll('#form .pbox.grp')].find(b=>/^4\\./.test(b.textContent));return b&&b.children.length===5&&[...b.children].map(d=>+d.dataset.lvl).join()==='0,1,1,2,2'}"), "ข้อ 4 กับข้อย่อยอยู่กล่องเดียว ทุกบรรทัดมีระดับของตัวเอง")
    ev("()=>{D.secs=[{h:'เรื่องเดิม',text:'ก'},{h:MSEC[0],text:'ข'}];save();renderForm();}"); pg.wait_for_timeout(200)
    check("R-39", ev("()=>D.secs.length===1&&/\\*\\*เรื่องเดิม\\*\\*/.test(D.secs[0].text)"), "ข้อความเก่าที่มีหัวข้อรวมเป็นช่องเดียว")
    check("R-66", ev("()=>!document.querySelector('.pbg')&&[...document.querySelectorAll('#form .fmtbar button')].some(b=>b.textContent==='⇥')"))
    tab(0)
    bx = pg.locator('#form .pbox').nth(1); bx.click(); pg.keyboard.press("Tab"); pg.wait_for_timeout(150)
    check("R-66", ev("()=>pbParse(D.secs[0].text)[1].lvl===1"), "Tab = เลื่อนเข้า")
    tab(1)
    check("R-64", ev("()=>[...document.querySelectorAll('#form [data-k=secs] .pbox')].every(b=>b.classList.contains('single'))&&document.querySelectorAll('#form .pbox.single').length===D.secs.length"), "บันทึก: กล่องเดียวต่อหัวข้อ")
    sb = pg.locator('#form .pbox.single').first; sb.click(); pg.keyboard.press("Control+End"); pg.keyboard.press("Enter"); pg.keyboard.type("ทดสอบ"); pg.keyboard.press("Shift+Enter"); pg.keyboard.type("ต่อ"); pg.wait_for_timeout(200)
    check("R-64", ev("()=>/\\nทดสอบ↵\\nต่อ$/.test(D.secs[0].text)&&document.querySelectorAll('#form .pbox.single').length===D.secs.length"), "Enter = ย่อหน้าใหม่ในกล่องเดิม, Shift+Enter = ↵")
    tab(1)
    check("R-39", ev("()=>!document.querySelector('#form [data-k=body]')&&document.querySelector('#form [data-k=secs] select')&&document.querySelectorAll('#form .fmtbar').length===1"), "การ์ดมีรายการเลือกหัวข้อ")
    ev("()=>{D.secs=[{h:MSEC[0],text:'x'}];save();renderForm();}"); pg.wait_for_timeout(200)
    check("R-38b", ev("""()=>{const a=[{h:MSEC[0],text:'x'},{h:'ข้อพิจารณา',text:'y'},{h:'เรื่องเดิม',text:'z'}];secOrder(a);
      const o=[...document.querySelector('#form [data-k=secs] select').options].map(o=>o.value);
      return a[1].h==='เรื่องเดิม'&&o[0]==='ต้นเรื่อง/ข้อเท็จจริง'&&o.includes('ข้อเสนอ')&&o[1]==='เรื่องเดิม'&&o.at(-1)===MSEC[0]}"""), "ต้นเรื่อง/เรื่องเดิม มาก่อน")
    ev("()=>{D.secs=[{h:'ต้นเรื่อง/ข้อเท็จจริง',text:'ก'},{h:MSEC[0],text:'ข'}];save();renderForm();}"); pg.wait_for_timeout(200)
    check("R-38c", ev("()=>{const s=[...document.querySelectorAll('#form [data-k=secs] select')][1];return ![...s.options].some(o=>o.value==='ข้อเท็จจริง')}"), "เลือกต้นเรื่องแล้วไม่มีข้อเท็จจริง")
    tab(1)
    check("R-38e", ev("""()=>{const {P}=build();const i=P.findIndex(p=>p.runs.some(r=>/^[2๒]\\. ข้อเท็จจริง$/.test(r.t)));const h=P[i],c=P[i+1];return Math.abs(c.first-(h.first+measure(h.runs[0].t.split(' ')[0]+' ',16,true)))<0.01}"""), "ข้อความใต้หัวข้อตรงแนวชื่อหัวข้อ")
    check("R-04", ev("()=>document.getElementById('vCopy').disabled===true"), "บันทึกข้อความไม่มีสำเนาคู่ฉบับ")
    tab(1)
    check("R-38", ev("()=>MSEC[0].includes('ไม่มีหัวข้อ')&&(()=>{const {P}=build();return P.some(p=>p.runs.some(r=>/^[1๑]\\. เรื่องเดิม$/.test(r.t)&&r.b))})()"))
    tab(2)
    check("R-42", ev("()=>{const {P}=build();const i=P.findIndex(p=>p.runs.some(r=>/^สำนักงานจังหวัด$/.test(r.t)));return i>0&&P[i].keep}"))
    # ตรวจคำผิด
    ev("()=>{document.querySelectorAll('#tabs button')[0].click();typoSample();}"); pg.wait_for_timeout(400)
    sc = ev("()=>spellScan().map(r=>r.w)")
    check("R-70", len(sc) >= 5 and any("พุธ" in w for w in sc), f"พบ {len(sc)} จุด")
    pg.wait_for_timeout(400)
    check("R-71", ev("()=>!!(CSS.highlights&&CSS.highlights.get('sp-err')&&CSS.highlights.get('sp-err').size>0)&&+document.getElementById('bSpell').dataset.n>0"), "ขีดเส้นใต้แดงทันที")
    check("R-72", ev("()=>/ชฎา/.test(spDiff('ปรากฎ','ปรากฏ'))&&/ปฏัก/.test(spDiff('ปรากฎ','ปรากฏ'))"), "บอกตัวอักษรที่ต่าง")
    ev("()=>{localStorage.removeItem('thdoc_drafts');document.querySelectorAll('#tabs button')[1].click();document.getElementById('bSample').click();document.getElementById('bDrafts').click();document.getElementById('drSave').click();document.getElementById('drSave').click();document.getElementById('drClose').click();document.querySelectorAll('#tabs button')[0].click();document.getElementById('bClear').click();}"); pg.wait_for_timeout(300)
    check("R-73", ev("()=>{const a=drGet();if(a.length!==1||a[0].type!=='memo')return false;document.getElementById('bDrafts').click();document.querySelector('#drList .it button.pri').click();const ok=TYPE==='memo'&&/ขออนุมัติ/.test(D.subject)&&document.getElementById('drafts').style.display==='none';localStorage.removeItem('thdoc_drafts');return ok}"), "บันทึก (ชื่อซ้ำ = ทับ) แล้วเปิดต่อในประเภทเดิม")
    tab(1)
    nm0 = ev("()=>D.name")
    ev("()=>{localStorage.removeItem('thdoc_signers');const s=document.querySelector('#form [data-k=sigMode] select');s.value='blank';s.onchange();}"); pg.wait_for_timeout(300)
    check("R-43", ev("()=>{const n=build().P.length;return !document.getElementById('page').textContent.includes(D.name)&&document.querySelector('#form [data-k=name]').style.display==='none'}"), "เว้นว่าง: ไม่มีชื่อในหนังสือ ซ่อนช่องชื่อ")
    ev("()=>{const s=document.querySelector('#form [data-k=sigMode] select');s.value='name';s.onchange();[...document.querySelectorAll('#form [data-k=sigMode] button')][0].click();D.name='ก ข';D.pos='ค';save();renderForm();[...document.querySelectorAll('#form [data-k=sigMode] button')][0].click();}"); pg.wait_for_timeout(200)
    check("R-43", ev("()=>{const ps=document.querySelectorAll('#form [data-k=sigMode] select')[1];const i=[...ps.options].findIndex(o=>o.textContent.startsWith('"+nm0+"'));ps.value=ps.options[i].value;ps.onchange();const ok=D.name==='"+nm0+"'&&document.getElementById('page').textContent.includes('"+nm0+"')&&store.get('thdoc_signers').length===2;localStorage.removeItem('thdoc_signers');return ok}"), "รายชื่อผู้ลงนาม dropdown")
    tab(0)
    ev("()=>{localStorage.removeItem('thdoc_hist');document.getElementById('bClear').click();}"); pg.wait_for_timeout(200)
    t = pg.locator('#form [data-k=to] input'); t.fill('ทดสอบผู้รับซ้ำ'); t.blur(); pg.wait_for_timeout(100)
    ev("()=>document.getElementById('bClear').click()"); pg.wait_for_timeout(200)
    check("R-67", ev("()=>{const s=document.querySelector('#form [data-k=to] select.hist');const ok=!!s&&!!document.querySelector('#form [data-k=to] datalist');if(!ok)return false;s.value='0';s.onchange();const r=D.to==='ทดสอบผู้รับซ้ำ';localStorage.removeItem('thdoc_hist');return r}"), "เลือกค่าที่เคยกรอกได้")
    check("R-74", ev("()=>{window._u=[];const o=window.open;window.open=u=>{window._u.push(u)};document.getElementById('bFb').click();document.getElementById('fbTitle').value='t';document.getElementById('fbBody').value='x';document.getElementById('fbSend').click();window.open=o;const u=window._u[0]||'';return u.startsWith('https://github.com/xarif09/thai-official-letter/issues/new?labels=bug')&&decodeURIComponent(u).includes(APP_VERSION)&&document.getElementById('fb').style.display==='none'}"), "ส่งเป็น GitHub Issue พร้อมรุ่น")
    ev("()=>{document.getElementById('spell').style.display='none';document.getElementById('drafts').style.display='none'}")
    tab(4)
    check("R-100", ev("()=>TYPE==='brief'&&!!document.querySelector('#page .btab')&&document.querySelectorAll('#page .sheet').length===0&&document.getElementById('vCopy').disabled&&/✓/.test(document.querySelector('#page .btab').textContent)&&document.getElementById('page').textContent.includes('ผู้มีอำนาจสั่งการ')&&document.getElementById('page').textContent.includes('(นางสาวณัฏฐณิชา แซ่โก)')"), "พรีวิวบันทึกย่อ 1 หน้า ตาราง + ช่องเลือก + ผู้จัดทำ")
    check("R-101", ev("()=>{const P=build().P.filter(p=>p.cell);return P.length>0&&P.every(p=>p.first===20||p.first===0)&&P.some(p=>p.first===20)&&+document.querySelector('#form [data-k=body] .pbox').dataset.base===20}"), "ย่อหน้า 2.0 ซม. ทั้งหนังสือและฟอร์ม")
    check("R-102", ev("()=>{const pg=document.getElementById('page'),z=pg.getBoundingClientRect().height/pg.offsetHeight||1,mm=e=>(e.getBoundingClientRect().top-pg.getBoundingClientRect().top)/z*25.4/96;const t=mm(document.querySelector('#page .btab'));return Math.abs(t-56.1)<1.5&&Math.abs(t+parseFloat(document.querySelector('#page .btab').style.height)-BT.bottom)<0.5}"), "ตารางเริ่ม ~56 มม. จบ 290 มม. ตามต้นฉบับ")
    with pg.expect_download() as dl: pg.click("#bDocx")
    xb = zipfile.ZipFile(io.BytesIO(open(dl.value.path(),"rb").read())).read("word/document.xml").decode()
    check("R-82", "NaN" not in xb and "undefined" not in xb and "NaN" not in x and "undefined" not in x, "Word ไม่มีค่าเสีย (NaN/undefined) ที่ทำให้ MS Word เปิดไม่ได้")
    check("R-100", xb.count("<w:tbl>")==1 and xb.count("<w:tr>")==2 and xb.count('w:char="F0FE"')==1 and xb.count('w:char="F0A8"')==9 and "ผู้มีอำนาจสั่งการ" in xb and 'w:val="nil"' not in xb, "Word: ตารางจริง 2 แถว กรอบครบ ช่องเลือก 10 ช่อง (เลือก 1)")
    ev("()=>{document.getElementById('fb').style.display='none';document.querySelectorAll('#tabs button')[1].click();document.getElementById('bClear').click();window._p=0;window.print=()=>{window._p++};}"); pg.wait_for_timeout(300)
    ev("()=>document.getElementById('bPrint').click()"); pg.wait_for_timeout(300)
    check("R-75", ev("()=>window._p===0&&document.getElementById('reqbox').style.display==='block'&&document.querySelectorAll('#form .f.req-miss').length>=5&&!!document.querySelector('#form .reqm')"), "ข้อมูลไม่ครบ พิมพ์ไม่ได้ + บอกช่องที่ขาด")
    ev("()=>{document.getElementById('bSample').click()}"); pg.wait_for_timeout(300)
    check("R-75", ev("()=>reqMissing().length===0&&document.getElementById('reqbox').style.display==='none'"), "กรอกครบแล้วกล่องเตือนหาย")
    tab(0)
    check("R-70b", ev("""()=>{const ok=["ด้วยจังหวัดได้ปรากฏเหตุการณ์ ขอให้ปฏิบัติตามกฎหมาย","สัญญานี้ทำขึ้น สัญญาน่าจะลงนาม สัญญานายหน้า","ทำนุบำรุง ทะนุบำรุง เผอิญ","ศาสตราจารย์ วิทยาศาสตร์ กระทรวง ครุภัณฑ์ ผลลัพธ์","ต่าง ๆ ได้แก่"];
      const bad=[["ครุภัณท์","ครุภัณฑ์"],["ยุทธศาสตร ","ยุทธศาสตร์"],["ทรัพยากรณ์","ทรัพยากร"],["ผู้บังคับบันชา","บัญชา"],["มาตราฐาน","มาตรฐาน"],["เอกสารแนป","แนบ"],["สัมนา","สัมมนา"],["ลิขสิทธ์","สิทธิ์"]];
      return ok.every(t=>!findIssues(t).some(r=>r.lv==='err'))&&bad.every(([w,f])=>findIssues(w).some(r=>r.lv==='err'&&(w.slice(0,r.i)+r.fix+w.slice(r.i+r.w.length)).includes(f.trim())))}"""), "ไม่ทักคำถูก (สัญญานี้ ทะนุบำรุง เผอิญ ศาสตราจารย์) และจับคำผิดที่เพิ่ม")
    check("R-71b", ev("""()=>{document.querySelectorAll('#tabs button')[1].click();D.secs=[{h:MSEC[0],text:'ต่าง ๆ'+String.fromCharCode(10)+'กรณี'}];save();renderForm();update();liveSpell();const H=CSS.highlights.get('sp-sug');return !H||H.size===0}"""), "ไม่ทักไม้ยมกตรงรอยต่อย่อหน้า และไม่ทักช่องว่างจัดหน้าในพรีวิว")
    pg.evaluate("t=>dictLoad(t)", open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","dict-th.txt"),encoding="utf-8").read())
    r76 = pg.evaluate("""()=>{const lv=t=>findIssues(t).map(r=>r.lv+':'+r.w+(r.fix?'>'+r.fix:''));
      const samples=Object.keys(SAMPLE).every(k=>{const d=SAMPLE[k];return [...Object.entries(d).filter(([kk,v])=>typeof v==='string'&&kk!=='qr'&&!NAMEK.includes(kk)).map(([kk,v])=>v),...(d.secs||[]).map(s=>s.text||'')].every(t=>!findIssues(t).some(r=>r.lv==='err'||r.lv==='unk'))});
      const typo=lv('ขอให้ทรมาณ และกบฎ').some(x=>x.startsWith('err:กบฎ>กบฏ'))&&findIssues('ทรมาณ').some(r=>r.fix==='ทรมาน'||(r.lv==='unk'&&unkSuggest(r).some(g=>g.x==='ทรมาน')));
      const names=!findIssues('(นายวีรพัฒน์ บุณฑริก) สนจ.ยล. ว 123').some(r=>r.lv==='unk');
      const w='ซอเรมาลอ';const before=findIssues(w).some(r=>r.lv==='unk');dictAddUser(w);const after=!findIssues(w).some(r=>r.lv==='unk');localStorage.removeItem('thdoc_userdict');DICT.W.delete(w);
      return {samples,typo,names,user:before&&after,size:DICT.W.size}}""")
    r76c = pg.evaluate("""()=>{const t='ขอให้ปฎิบัติตามกฏหมาย สังเกตุว่าครุภัณท์ชำรุด เข้าร่วมสัมนา งบประมาน คอมพิวเตอ ปรากฎว่า เเต่งตั้ง อนุญาติ';
      const r=findIssues(t).filter(x=>x.lv==='err').map(x=>x.w);const need=['ปฎิ','กฏ','สังเกตุ','ภัณท์','สัมนา','งบประมาน','คอมพิวเตอ','ปรากฎ','เเ','อนุญาติ'];
      return need.filter(w=>!r.includes(w)).concat(r.length!==new Set(r).size?['ซ้ำ']:[])}""")
    check("R-76", not r76c, "มีพจนานุกรมแล้วต้องยังจับคำผิดในตัวครบ ไม่ซ้ำ: ขาด "+",".join(r76c))
    r76d = pg.evaluate("""()=>{const t='ส่วนราชการ/หน่วยงาสนใดได้รับ ขอให้นำแจ้งล่nวงหน้า **พร้อมไฟล์ข้อมูลฟ** วันที่ 20 พฤศจิกายน 2569hfwofhgกธฯ หัวหน้ฟาส่วงนราชการ ตามแบ้บฟรอร์ม QR Cัode สิ่งที่ส่งมไาด้วย';
      const r=findIssues(t).map(x=>x.w);return ['หน่วยงาสน','ข้อมูลฟ','กธ','บฟร','Cั','่n','ไา','9hfwofhg'].filter(w=>!r.includes(w)).concat(r.length<10?['พบ '+r.length]:[])}""")
    check("R-76", not r76d, "จับคำพิมพ์พลาดแบบที่ผู้ใช้ทดสอบ (พิมพ์เกิน/อักษรอังกฤษปน/สระลอย): ขาด "+",".join(r76d))
    r76e = pg.evaluate("""()=>['(สวทช.) โดยสถาบัน','จนท.....','ถนนสุขยางค์ ตำบลสะเตง อำเภอเมืองยะลา','อำเภอธารโต อำเภอเบตง','ขนาด A4 จำนวน 2 TB','ห้องประชุมศรียะลา'].flatMap(t=>findIssues(t).filter(x=>x.lv!=='sug').map(x=>x.w))""")
    check("R-76", not r76e, "ไม่ทักคำย่อ/ชื่อพื้นที่ยะลา: "+",".join(r76e))
    check("R-76", all([r76["samples"],r76["typo"],r76["names"],r76["user"]]) and r76["size"]>50000, str(r76))
    # R-76b: เปิดผ่านเว็บแล้วพจนานุกรมต้องโหลดเองทันที (ไม่ต้องคลิกอะไร)
    import http.server, threading, functools
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
    srv.RequestHandlerClass.log_message = lambda *a, **k: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    pg2 = b.new_page(); pg2.goto(f"http://127.0.0.1:{srv.server_address[1]}/index.html"); pg2.wait_for_timeout(2500)
    check("R-76", pg2.evaluate("()=>DICT?DICT.W.size:0") > 50000 and pg2.evaluate("()=>findIssues('กฏหมาย').some(r=>r.lv==='err')"), "เปิดหน้าเว็บแล้วโหลดพจนานุกรมเอง ไม่ต้องคลิกแท็บ")
    pg2.close(); srv.shutdown()
    r79 = pg.evaluate("""()=>{const t='1. ไมโครโฟน เป็นเงิน 45,000 บาท'+String.fromCharCode(10)+'2. สาย เป็นเงิน 7,800 บาท'+String.fromCharCode(10)+'รวมเป็นเงินทั้งสิ้น 92,800 บาท (แปดหมื่นสองพันแปดร้อยบาทถ้วน)';
      const r=findIssues(t);return [bahtText(117800)==='หนึ่งแสนหนึ่งหมื่นเจ็ดพันแปดร้อยบาทถ้วน', bahtText(21)==='ยี่สิบเอ็ดบาทถ้วน', r.some(x=>/ผลรวม 2 รายการ/.test(x.note)), r.some(x=>x.fix==='เก้าหมื่นสองพันแปดร้อยบาทถ้วน'),
        findIssues('ขอเชิญเข้ารวมประชุม ลงวันที 15 ใด้รับ').length===3, findIssues('รวมทั้งสิ้น รวมกลุ่ม เข้าร่วมประชุม').length===0]}""")
    check("R-79", all(r79), "จำนวนเงิน/ตัวหนังสือ/ยอดรวม และคำที่ใช้สลับกัน "+str(r79))
    r84 = pg.evaluate("""()=>{const bad=['มากาา','ก่่อน','ก้่อน','กิีน','กุิ','ก่ิน','นำ้','เก็่บ','กัาร','เแก','ขอบคุณๆๆ','ทำำงาน','กิา','ประชุมฯฯ'];const ok=['น้ำท่วม','ทั่ว','สิทธิ์','พันธุ์','ศักดิ์','ใหญ่ๆ','เก็บ','ก่อน'];
      return bad.filter(w=>!orthoIssues(w).length).concat(ok.filter(w=>orthoIssues(w).length).map(w=>'ทักผิด:'+w))}""")
    check("R-84", not r84, "ผิดหลักการเขียนภาษาไทย: "+",".join(r84))
    r83 = pg.evaluate("""()=>{const i=document.querySelector('#form input');i.value='ครุภัณท์ หน่วยงาสน ทรมาณ';i.dispatchEvent(new Event('input'));hlPaint(i.closest('.f')||i.parentNode,findIssues(i.value));
      const b=i.closest('.hlw')&&i.closest('.hlw').querySelector('.hlb');const css=[...document.styleSheets].flatMap(s=>{try{return [...s.cssRules].map(r=>r.cssText)}catch(e){return []}}).join(' ');
      return [!!b&&b.querySelectorAll('mark.err').length>0, /fdd5d5|253, 213, 213/.test(css), /fde1c2|253, 225, 194/.test(css), /fff3b0|255, 243, 176/.test(css)]}""")
    check("R-83", all(r83), "ไฮไลต์แดง/ส้ม/เหลืองอ่อนในช่องพิมพ์ "+str(r83))
    r85 = pg.evaluate("""()=>{const o=D.no;D.no='ยลกขค 0017.3/ว 13301';renderForm();update();liveSpell();
      const f=document.querySelector('#form [data-k="no"] input');const b=f.closest('.hlw')&&f.closest('.hlw').querySelector('mark');
      const inList=spellScan().some(r=>r.f.label==='ที่');const hl=[...CSS.highlights.get('sp-unk')||[],...CSS.highlights.get('sp-err')||[]].some(rg=>/ยล|กขค/.test(rg.toString()));
      D.no=o;renderForm();update();return [!b,!inList,!hl]}""")
    check("R-85", all(r85), "ไม่ตรวจเลขที่หนังสือ (ช่อง/รายการ/พรีวิว) "+str(r85))
    r86 = pg.evaluate("""()=>{typoSample();const bt=document.getElementById('bSpell');const noBtn=!document.getElementById('bTypo')&&bt.textContent.startsWith('รายการคำผิด')&&+bt.querySelector('.spn-b').textContent>0;bt.click();
      const L=document.getElementById('spList');const gh=[...L.querySelectorAll('.gh')].map(g=>g.className);const it=L.querySelector('.it.err');
      const ctx=it&&it.querySelector('.ctx').textContent.length>it.querySelector('.ctx mark').textContent.length+6;
      const n0=spellScan().filter(r=>r.lv==='err').length;it.querySelector('.ch button.pri').click();const n1=spellScan().filter(r=>r.lv==='err').length;
      const it2=document.querySelector('#spList .it.err');const inp=it2.querySelector('.ed input');const r=spellScan().find(x=>x.lv==='err');const seg=inp.value;
      inp.value=seg.replace(r.w,r.fix||'');it2.querySelector('.ed button').click();const n2=spellScan().filter(r=>r.lv==='err').length;
      document.getElementById('spClose').click();return [noBtn,gh.length>=1&&gh[0].includes('err'),ctx,n1===n0-1,n2===n1-1]}""")
    check("R-86", all(r86), "ปุ่มรายการคำผิด แยกกลุ่ม แสดงข้อความก่อน-หลัง เลือกคำถูก/แก้เอง "+str(r86))
    r87 = pg.evaluate("""()=>{typoSample();document.getElementById('bSpell').click();const ok=[...document.querySelectorAll('#spList .it')].every(it=>{const v=it.querySelector('.ed input').value;return [...v].length<=40});
      const r=spellScan()[0];const v=document.querySelector('#spList .it .ed input').value;document.getElementById('spClose').click();
      return [ok, v.length<=r.w.length+24, !!document.querySelector('#side h1 #bFb'), !document.querySelector('.btns #bFb')]}""")
    check("R-87", all(r87), "แก้เองแสดงคำ ±1 คำ · ปุ่มแจ้งปัญหาอยู่หัวระบบ "+str(r87))
    check("R-87", pg.evaluate("()=>{const t='ช่วยเหลือทางกฏหมายและบังคับคดี';const [a,b]=spWord1(t,12,14);return t.slice(a,b)}")=="ทางกฏหมาย", "แก้เอง: คำผิด + คำถูกหน้า/หลัง 1 คำ")
    r88 = pg.evaluate("""()=>{const c=[['ได้กำพหนดประชุม','กำหนด'],['ดำเนินกาารตาม','า'],['ผู้ว่าราขการจังหวัด','ราชการ']];
      const bad=c.filter(([t,f])=>{const r=findIssues(t);return !(r.length===1&&r[0].fix===f)}).map(x=>x[0]);
      return bad.concat(['คราวละสามปี โดย','(นายชารีฟ เจ๊ะแอ)'].filter(t=>findIssues(t).some(x=>x.lv==='sug')).map(t=>'ทักผิด:'+t))}""")
    check("R-89", pg.evaluate("()=>{const o=D;D=defaults();renderForm();update();liveSpell();const ok=!document.querySelector('#bSpell .spn-b');D=o;renderForm();update();liveSpell();return ok&&!!document.querySelector('#bSpell .spn-b')}"), "ไม่มีคำผิดไม่แสดงตัวเลข / มีแสดง")
    check("R-88", not r88, "คำพิมพ์พลาดที่แตกเป็นหลายท่อน: "+",".join(r88))
    check("ERR", not errs, "; ".join(errs[:3]))
    b.close()

bad = [r for r in results if not r[1]]
print(f"\nรวม {len(results)} รายการ · ผ่าน {len(results)-len(bad)} · ไม่ผ่าน {len(bad)}")
sys.exit(1 if bad else 0)
