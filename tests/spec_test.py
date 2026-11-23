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

    check("R-02", ev("()=>document.querySelectorAll('#tabs button').length") == 4)
    check("R-06", ev("()=>{const d=defaults();return d.font==='TH SarabunIT๙'&&d.thai===true}"))
    check("R-10", ev("()=>{const {F}=build();const g=F.find(f=>f.kind==='img');return Math.abs(GARUDA_RATIO-167/177)<0.001&&g&&g.h===30&&Math.abs(g.x+g.w/2-105)<0.1}"))
    check("R-14", ev("()=>/^\\s+\\S+ (พ\\.ศ\\. )?\\d{4}$/.test(thaiDate('2026-11-06'))&&!/\\d\\s+พฤศ/.test(thaiDate('2026-11-06'))"))
    check("R-33", ev("""()=>{const w=t=>segWords(t).map(x=>x.t);const has=(t,k)=>w(t).includes(k);
       return has('เวลา 09.30 น. ณ','09.30 น.')&&has('ปี พ.ศ. 2569 นี้','พ.ศ. 2569')&&w('อัยการ กอ.รมน.จังหวัด').some(x=>x.startsWith('กอ.รมน.'))&&has('มาตรา 56 (ข) และ','(ข)')&&w('ผู้อำนวยการกอง').some(x=>x.startsWith('ผู้อำนวยการ'))}"""))
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
    check("R-41", ev("()=>{const {P,F}=build();const b=F.find(f=>f.kind==='block'&&f.mode==='side');return b&&!b.lines.some(l=>/สำเนาส่ง/.test(l))&&P.some(p=>p.runs.some(r=>r.t==='สำเนาส่ง'))}"))
    check("R-50", ev("()=>document.querySelectorAll('#page .sheet').length===2&&/๒/.test(document.querySelector('#page .pgno').textContent)"))
    check("R-51", ev("()=>{const {P}=build();const i=P.findIndex(p=>p.runs.length===1&&p.runs[0].t==='ขอแสดงความนับถือ');let n=0;for(let j=i-1;j>=0&&P[j].keep;j--)n+=Math.ceil((measure(P[j].runs.map(r=>r.t||'').join(''))+(P[j].first||0))/(CW-P[j].indL-P[j].indR));return n>=2}"))
    check("R-52", ev("()=>{const {P}=build();return P.filter(p=>p.runs.some(r=>/ดังนี้\\s*$/.test(r.t||''))).every(p=>p.kn)}"))
    check("R-61", ev("()=>{const b=document.querySelector('#form .pbox');return Math.abs(parseFloat(getComputedStyle(b).fontSize)-16*96/72*(b.clientWidth-16)/(160*96/25.4))<1.5}"))
    tab(0, "copy")
    check("R-11", ev("()=>{const {F}=build();const t=F.find(f=>f.kind==='text'&&f.text==='สำเนาคู่ฉบับ');return t&&t.pt>=32&&!F.some(f=>f.kind==='img')&&F.some(f=>f.kind==='initials')}"))
    with pg.expect_download() as dl: pg.click("#bDocx")
    data = open(dl.value.path(), "rb").read()
    z = zipfile.ZipFile(io.BytesIO(data)); x = z.read("word/document.xml").decode(); h = z.read("word/header1.xml").decode()
    check("R-03", data[:2] == b"PK" and "w:body" in x)
    check("R-80", all(k in x for k in ["thaiDistribute", "keepNext", 'w:val="right"', " "]) and "ThaiArabic" in h)

    # ---- ประเภทอื่น ----
    for i, name in [(1, "memo"), (2, "stamp"), (3, "order")]:
        tab(i)
        check("R-63", ev("()=>document.querySelectorAll('#page .sheet').length===2"), f"{name} ยาว 2 หน้า")
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
    ev("()=>{document.querySelectorAll('#tabs button')[0].click();document.getElementById('bTypo').click();}"); pg.wait_for_timeout(400)
    sc = ev("()=>spellScan().map(r=>r.w)")
    check("R-70", len(sc) >= 5 and any("พุธ" in w for w in sc), f"พบ {len(sc)} จุด")
    pg.wait_for_timeout(400)
    check("R-71", ev("()=>!!(CSS.highlights&&CSS.highlights.get('sp-err')&&CSS.highlights.get('sp-err').size>0)&&/\\(\\d+\\)/.test(document.getElementById('bSpell').textContent)"), "ขีดเส้นใต้แดงทันที")
    check("R-72", ev("()=>/ชฎา/.test(spDiff('ปรากฎ','ปรากฏ'))&&/ปฏัก/.test(spDiff('ปรากฎ','ปรากฏ'))"), "บอกตัวอักษรที่ต่าง")
    check("ERR", not errs, "; ".join(errs[:3]))
    b.close()

bad = [r for r in results if not r[1]]
print(f"\nรวม {len(results)} รายการ · ผ่าน {len(results)-len(bad)} · ไม่ผ่าน {len(bad)}")
sys.exit(1 if bad else 0)
