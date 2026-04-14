import streamlit as st
import streamlit.components.v1 as components
import random
import json

st.set_page_config(
    page_title="Construction Site OS",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu,footer,header,.stDeployButton,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"]{display:none!important}
.block-container{padding:0!important;margin:0!important;max-width:100%!important}
section[data-testid="stSidebar"]{display:none!important}
html,body,[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"]{padding:0!important;margin:0!important;background:#030508!important;}
iframe{width:100vw!important;height:100vh!important;border:none!important;
  display:block!important;position:fixed!important;top:0!important;left:0!important;z-index:9999!important;}
</style>
""", unsafe_allow_html=True)

def generate_data():
    wc  = random.randint(15, 35)
    ppe = round(random.uniform(85, 98), 1)
    tmp = round(random.uniform(28, 42), 1)
    dst = round(random.uniform(20, 80))
    crn = round(random.uniform(60, 110))
    zon = random.random() < 0.25

    alerts = []
    if ppe < 92:  alerts.append("PPE compliance below threshold — risk of injury")
    if tmp > 38:  alerts.append("High ambient temperature — heat stress risk active")
    if dst > 60:  alerts.append("Dust levels critical — respiratory hazard")
    if crn > 100: alerts.append("Crane overload detected — halt all lift operations")
    if zon:       alerts.append("Restricted zone breach — intruder detected")

    def vc(a, w): return "#ff5050" if a else ("#ff9500" if w else "#00ff88")

    ppe_a = ppe < 92;  ppe_w = ppe < 95 and not ppe_a
    tmp_a = tmp > 38;  tmp_w = tmp > 34 and not tmp_a
    dst_a = dst > 60;  dst_w = dst > 45 and not dst_a
    crn_a = crn > 100; crn_w = crn > 85 and not crn_a

    return {
        "wc": wc, "ppe": ppe, "tmp": tmp, "dst": dst, "crn": crn, "zon": zon,
        "ppe_c": vc(ppe_a, ppe_w), "tmp_c": vc(tmp_a, tmp_w),
        "dst_c": vc(dst_a, dst_w), "crn_c": vc(crn_a, crn_w),
        "zon_c": "#ff5050" if zon else "#00ff88",
        "ppe_alert": ppe_a, "ppe_warn": ppe_w,
        "tmp_alert": tmp_a, "tmp_warn": tmp_w,
        "dst_alert": dst_a, "dst_warn": dst_w,
        "crn_alert": crn_a, "crn_warn": crn_w,
        "alerts": alerts,
        "status_color": "#ff2d2d" if alerts else "#00ff88",
        "status_text": f"{len(alerts)} ALERT{'S' if len(alerts)!=1 else ''} ACTIVE" if alerts else "SYSTEMS NOMINAL",
        "holo_text": "ALERT" if alerts else "ALL CLEAR",
        "alert_count": len(alerts),
    }

# Generate initial data
d = generate_data()
initial_json = json.dumps(d)

components.html(f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@200;300;400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --amber:#ff9500;--amber2:#ffcc00;--red:#ff2d2d;--green:#00ff88;
  --blue:#00cfff;--bg:#030508;--bg2:#070b11;
  --border:rgba(255,149,0,0.15);--border2:rgba(255,149,0,0.35);
  --mono:'Share Tech Mono',monospace;--head:'Orbitron',sans-serif;--body:'Exo 2',sans-serif;
}}
html,body{{background:var(--bg);color:#fff;font-family:var(--body);width:100%;height:100%;min-height:100vh;overflow-x:hidden;}}

/* fade transition on value changes */
.fade-val{{transition:opacity 0.4s ease, color 0.6s ease, text-shadow 0.6s ease;}}
.fading{{opacity:0;}}

.bg-scanlines{{position:fixed;inset:0;pointer-events:none;z-index:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.18) 2px,rgba(0,0,0,0.18) 4px);}}
.bg-grid{{position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:linear-gradient(rgba(255,149,0,0.05) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,149,0,0.05) 1px,transparent 1px);background-size:60px 60px;}}
.bg-tl{{position:fixed;top:-200px;left:-200px;width:600px;height:600px;border-radius:50%;
  filter:blur(120px);opacity:0.07;background:var(--amber);pointer-events:none;z-index:0;}}
.bg-br{{position:fixed;bottom:-200px;right:-200px;width:600px;height:600px;border-radius:50%;
  filter:blur(120px);opacity:0.07;background:var(--blue);pointer-events:none;z-index:0;}}
.bg-radar{{position:fixed;right:-180px;bottom:-180px;width:500px;height:500px;
  pointer-events:none;z-index:0;border-radius:50%;border:1px solid rgba(255,149,0,0.06);overflow:hidden;}}
.radar-sweep{{position:absolute;top:50%;left:50%;width:50%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,149,0,0.3));
  transform-origin:left center;animation:radar-spin 5s linear infinite;}}
@keyframes radar-spin{{to{{transform:rotate(360deg)}}}}

.dashboard{{position:relative;z-index:2;padding:24px 32px;min-height:100vh;display:flex;flex-direction:column;}}
.header{{display:grid;grid-template-columns:1fr auto 1fr;align-items:start;margin-bottom:20px;gap:16px;}}
.sys-tag{{font-family:var(--mono);font-size:9px;color:var(--amber);letter-spacing:0.22em;
  text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;gap:6px;}}
.sys-tag::before{{content:'';width:16px;height:1px;background:var(--amber);opacity:0.6;}}
.site-title{{font-family:var(--head);font-size:clamp(22px,3vw,36px);font-weight:900;letter-spacing:0.06em;
  background:linear-gradient(135deg,#fff 30%,var(--amber) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1;}}
.site-sub{{font-size:11px;font-weight:200;color:rgba(255,255,255,0.35);letter-spacing:0.12em;text-transform:uppercase;margin-top:6px;}}
.header-center{{text-align:center;display:flex;align-items:center;justify-content:center;}}
.holo-badge{{display:inline-block;position:relative;padding:14px 20px;border:1px solid var(--border2);
  border-radius:6px;background:rgba(255,149,0,0.04);min-width:160px;text-align:center;}}
.holo-badge::before,.holo-badge::after{{content:'';position:absolute;width:8px;height:8px;border-color:var(--amber);border-style:solid;}}
.holo-badge::before{{top:-1px;left:-1px;border-width:1px 0 0 1px;border-radius:1px 0 0 0;}}
.holo-badge::after{{bottom:-1px;right:-1px;border-width:0 1px 1px 0;border-radius:0 0 1px 1px;}}
.holo-label{{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.35);letter-spacing:0.18em;text-transform:uppercase;margin-bottom:6px;}}
.holo-val{{font-family:var(--head);font-size:16px;font-weight:700;letter-spacing:0.1em;transition:color 0.6s ease;}}
.holo-sub{{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.3);margin-top:4px;letter-spacing:0.1em;}}
.header-right{{text-align:right;}}
.clock-block{{font-family:var(--mono);font-size:clamp(20px,2.5vw,30px);color:var(--amber);
  letter-spacing:0.08em;text-shadow:0 0 20px rgba(255,149,0,0.4);}}
.date-block{{font-family:var(--mono);font-size:10px;color:rgba(255,255,255,0.28);letter-spacing:0.1em;margin-top:4px;text-transform:uppercase;}}
.rc-wrap{{margin-top:8px;display:flex;align-items:center;gap:8px;justify-content:flex-end;}}
.rc-label{{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.25);letter-spacing:0.08em;}}
.rc-bar{{width:90px;height:2px;background:rgba(255,149,0,0.12);border-radius:1px;overflow:hidden;}}
.rc-fill{{height:100%;background:linear-gradient(90deg,var(--amber2),var(--amber));border-radius:1px;width:100%;transition:width 0.1s linear;}}

.divider{{height:1px;background:linear-gradient(90deg,transparent,var(--amber),transparent);
  opacity:0.25;margin-bottom:18px;position:relative;}}
.divider::after{{content:'';position:absolute;top:-2px;left:50%;transform:translateX(-50%);
  width:6px;height:6px;background:var(--amber);border-radius:50%;box-shadow:0 0 12px var(--amber);}}

.status-bar{{display:flex;align-items:center;justify-content:space-between;
  background:var(--bg2);border:1px solid var(--border);border-radius:6px;
  padding:10px 18px;margin-bottom:14px;}}
.status-left{{display:flex;align-items:center;gap:12px;}}
.status-dot{{width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0;transition:background 0.6s,box-shadow 0.6s;}}
.status-txt{{font-family:var(--head);font-size:13px;font-weight:700;letter-spacing:0.1em;transition:color 0.6s;}}
.status-right{{display:flex;align-items:center;gap:16px;flex-wrap:wrap;}}
.sensor-pill{{display:flex;align-items:center;gap:5px;font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:0.08em;}}
.sensor-pip{{width:4px;height:4px;border-radius:50%;background:var(--green);display:inline-block;animation:pulse-dot 2.5s ease-in-out infinite;}}
@keyframes pulse-dot{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:0.3;transform:scale(0.6)}}}}

.metrics-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:14px;flex:1;}}
.metric-card{{position:relative;background:var(--bg2);border:1px solid var(--border);
  border-radius:6px;padding:20px;overflow:hidden;
  transition:border-color 0.6s ease,box-shadow 0.6s ease,background 0.6s ease;}}
.metric-card:hover{{border-color:var(--border2);box-shadow:0 8px 40px rgba(0,0,0,0.6),0 0 0 1px rgba(255,149,0,0.1);}}
.metric-card.alerted{{border-color:rgba(255,45,45,0.4)!important;background:#0d0505;box-shadow:0 0 30px rgba(255,45,45,0.08);}}
.card-accent{{position:absolute;top:0;left:0;right:0;height:2px;transition:background 0.6s,opacity 0.6s;}}
.metric-card::before,.metric-card::after{{content:'';position:absolute;width:10px;height:10px;border-color:rgba(255,149,0,0.25);border-style:solid;transition:border-color 0.6s;}}
.metric-card::before{{top:6px;left:6px;border-width:1px 0 0 1px;}}
.metric-card::after{{bottom:6px;right:6px;border-width:0 1px 1px 0;}}
.metric-card.alerted::before,.metric-card.alerted::after{{border-color:rgba(255,45,45,0.4);}}
.card-id{{font-family:var(--mono);font-size:8px;color:rgba(255,255,255,0.18);letter-spacing:0.2em;text-transform:uppercase;position:absolute;top:14px;right:16px;}}
.card-label{{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.38);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:12px;display:flex;align-items:center;gap:6px;}}
.label-dot{{width:4px;height:4px;border-radius:50%;box-shadow:0 0 6px currentColor;display:inline-block;animation:pulse-dot 2s ease-in-out infinite;transition:background 0.6s,color 0.6s;}}
.card-value{{font-family:var(--head);font-size:clamp(28px,3.5vw,44px);font-weight:900;line-height:1;letter-spacing:0.02em;transition:color 0.6s ease,text-shadow 0.6s ease;}}
.card-unit{{font-family:var(--mono);font-size:12px;color:rgba(255,255,255,0.35);margin-left:4px;}}
.bar-track{{height:2px;background:rgba(255,255,255,0.05);border-radius:1px;margin-top:14px;overflow:hidden;}}
.bar-fill{{height:100%;border-radius:1px;position:relative;transition:width 0.8s cubic-bezier(0.25,0.46,0.45,0.94),background 0.6s ease;}}
.bar-fill::after{{content:'';position:absolute;right:0;top:-1px;bottom:-1px;width:3px;background:inherit;filter:brightness(1.5);border-radius:1px;}}
.card-sub{{margin-top:8px;font-size:10px;color:rgba(255,255,255,0.28);font-weight:300;letter-spacing:0.04em;transition:color 0.6s;}}
.card-sub.warn{{color:rgba(255,149,0,0.7);}}
.card-sub.danger{{color:rgba(255,100,100,0.8);}}
.intrusion-row{{display:flex;align-items:center;gap:10px;margin-top:12px;}}
.intrusion-ring{{width:36px;height:36px;border-radius:50%;border:2px solid;display:inline-flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:9px;font-weight:700;flex-shrink:0;transition:border-color 0.6s,color 0.6s,box-shadow 0.6s;}}
.intrusion-ring.secure{{border-color:var(--green);color:var(--green);box-shadow:0 0 14px rgba(0,255,136,0.2);}}
.intrusion-ring.breach{{border-color:var(--red);color:var(--red);box-shadow:0 0 20px rgba(255,45,45,0.4);animation:ring-pulse 0.7s ease-in-out infinite;}}
@keyframes ring-pulse{{0%,100%{{box-shadow:0 0 20px rgba(255,45,45,0.4)}}50%{{box-shadow:0 0 40px rgba(255,45,45,0.7),0 0 0 4px rgba(255,45,45,0.1)}}}}

.alerts-panel{{border-radius:6px;border:1px solid rgba(255,45,45,0.25);background:#0c0606;overflow:hidden;margin-bottom:14px;
  transition:opacity 0.5s ease,max-height 0.5s ease;}}
.alerts-panel.hidden{{opacity:0;max-height:0;margin-bottom:0;overflow:hidden;}}
.alerts-top{{padding:12px 18px;background:rgba(255,45,45,0.07);border-bottom:1px solid rgba(255,45,45,0.15);display:flex;align-items:center;gap:10px;}}
.alerts-heading{{font-family:var(--head);font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:var(--red);flex:1;}}
.alerts-badge{{background:var(--red);color:#fff;font-family:var(--mono);font-size:9px;padding:3px 7px;border-radius:2px;letter-spacing:0.05em;}}
.alert-row{{display:flex;align-items:center;gap:12px;padding:10px 18px;border-bottom:1px solid rgba(255,255,255,0.03);}}
.alert-row:last-child{{border-bottom:none;}}
.alert-pip{{width:5px;height:5px;border-radius:50%;background:var(--red);display:inline-block;flex-shrink:0;animation:pulse-dot 0.8s ease-in-out infinite;}}
.alert-msg{{font-size:12px;font-weight:300;color:rgba(255,180,180,0.8);letter-spacing:0.03em;}}

.footer{{display:flex;align-items:center;justify-content:space-between;padding-top:12px;border-top:1px solid rgba(255,255,255,0.05);margin-top:auto;}}
.footer-sys{{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.18);letter-spacing:0.1em;}}
.footer-sync{{font-family:var(--mono);font-size:9px;color:rgba(255,149,0,0.4);letter-spacing:0.08em;}}
</style>
</head>
<body>
<div class="bg-scanlines"></div>
<div class="bg-grid"></div>
<div class="bg-tl"></div>
<div class="bg-br"></div>
<div class="bg-radar"><div class="radar-sweep"></div></div>

<div class="dashboard">
  <div class="header">
    <div class="header-left">
      <div class="sys-tag">SYS:MONITOR · BUILD 4.1.2</div>
      <div class="site-title">CONSTRUCTION<br>SITE OS</div>
      <div class="site-sub">Sector 7 · Block C · Live Intelligence Feed</div>
    </div>
    <div class="header-center">
      <div class="holo-badge">
        <div class="holo-label">SITE STATUS</div>
        <div class="holo-val" id="holo-val">ALL CLEAR</div>
        <div class="holo-sub" id="holo-sub">0 active alerts</div>
      </div>
    </div>
    <div class="header-right">
      <div class="clock-block" id="clk">00:00:00</div>
      <div class="date-block"  id="dt">--- -- --- ----</div>
      <div class="rc-wrap">
        <span class="rc-label">NEXT REFRESH</span>
        <div class="rc-bar"><div class="rc-fill" id="bar"></div></div>
      </div>
    </div>
  </div>

  <div class="divider"></div>

  <div class="status-bar">
    <div class="status-left">
      <span class="status-dot" id="status-dot"></span>
      <span class="status-txt" id="status-txt">SYSTEMS NOMINAL</span>
    </div>
    <div class="status-right">
      <div class="sensor-pill"><span class="sensor-pip"></span>PPE CAM</div>
      <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:0.4s"></span>DUST SENSOR</div>
      <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:0.8s"></span>CRANE LOAD</div>
      <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:1.2s"></span>THERMAL</div>
      <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:1.6s"></span>ZONE DETECT</div>
    </div>
  </div>

  <div class="metrics-grid">
    <!-- Workers -->
    <div class="metric-card" id="card-wc">
      <div class="card-accent" id="acc-wc" style="background:linear-gradient(90deg,transparent,var(--amber),transparent);opacity:0.5"></div>
      <div class="card-id">WRK-01</div>
      <div class="card-label"><span class="label-dot" style="background:var(--amber);color:var(--amber)"></span>Workers On Site</div>
      <div style="display:flex;align-items:baseline;gap:6px">
        <div class="card-value fade-val" id="val-wc" style="color:#fff">--</div>
      </div>
      <div class="bar-track"><div class="bar-fill" id="bar-wc" style="background:var(--amber)"></div></div>
      <div class="card-sub" id="sub-wc">--</div>
    </div>
    <!-- PPE -->
    <div class="metric-card" id="card-ppe">
      <div class="card-accent" id="acc-ppe"></div>
      <div class="card-id">PPE-02</div>
      <div class="card-label"><span class="label-dot" id="dot-ppe"></span>PPE Compliance</div>
      <div style="display:flex;align-items:baseline;gap:6px">
        <div class="card-value fade-val" id="val-ppe">--</div><span class="card-unit">%</span>
      </div>
      <div class="bar-track"><div class="bar-fill" id="bar-ppe"></div></div>
      <div class="card-sub" id="sub-ppe">--</div>
    </div>
    <!-- Temp -->
    <div class="metric-card" id="card-tmp">
      <div class="card-accent" id="acc-tmp"></div>
      <div class="card-id">TMP-03</div>
      <div class="card-label"><span class="label-dot" id="dot-tmp"></span>Ambient Temperature</div>
      <div style="display:flex;align-items:baseline;gap:6px">
        <div class="card-value fade-val" id="val-tmp">--</div><span class="card-unit">°C</span>
      </div>
      <div class="bar-track"><div class="bar-fill" id="bar-tmp"></div></div>
      <div class="card-sub" id="sub-tmp">--</div>
    </div>
    <!-- Dust -->
    <div class="metric-card" id="card-dst">
      <div class="card-accent" id="acc-dst"></div>
      <div class="card-id">DST-04</div>
      <div class="card-label"><span class="label-dot" id="dot-dst"></span>Dust Particulate</div>
      <div style="display:flex;align-items:baseline;gap:6px">
        <div class="card-value fade-val" id="val-dst">--</div><span class="card-unit">mg/m³</span>
      </div>
      <div class="bar-track"><div class="bar-fill" id="bar-dst"></div></div>
      <div class="card-sub" id="sub-dst">--</div>
    </div>
    <!-- Crane -->
    <div class="metric-card" id="card-crn">
      <div class="card-accent" id="acc-crn"></div>
      <div class="card-id">CRN-05</div>
      <div class="card-label"><span class="label-dot" id="dot-crn"></span>Crane Load</div>
      <div style="display:flex;align-items:baseline;gap:6px">
        <div class="card-value fade-val" id="val-crn">--</div><span class="card-unit">%</span>
      </div>
      <div class="bar-track"><div class="bar-fill" id="bar-crn"></div></div>
      <div class="card-sub" id="sub-crn">--</div>
    </div>
    <!-- Zone -->
    <div class="metric-card" id="card-zon">
      <div class="card-accent" id="acc-zon"></div>
      <div class="card-id">ZON-06</div>
      <div class="card-label"><span class="label-dot" id="dot-zon"></span>Zone Intrusion</div>
      <div class="card-value fade-val" id="val-zon" style="font-size:34px">--</div>
      <div class="intrusion-row">
        <span class="intrusion-ring secure" id="ring-zon">OK</span>
        <div class="card-sub" id="sub-zon" style="margin-top:0">--</div>
      </div>
    </div>
  </div>

  <!-- Alerts Panel -->
  <div class="alerts-panel hidden" id="alerts-panel">
    <div class="alerts-top">
      <span class="alerts-heading" id="alerts-heading">&#x2B21; 0 Active Safety Alerts</span>
      <span class="alerts-badge" id="alerts-badge">0</span>
    </div>
    <div id="alerts-list"></div>
  </div>

  <div class="footer">
    <div class="footer-sys">SMART-SITE&#x2122; · SAFETY INTELLIGENCE PLATFORM · v4.1</div>
    <div class="footer-sync" id="sync">LAST SYNC: --:--:--</div>
  </div>
</div>

<script>
var REFRESH_MS = 5000;
var startTs    = Date.now();

// ── initial data from Python ─────────────────────────────────
var pending = {initial_json};

function pad(n) {{ return String(n).padStart(2,'0'); }}

// ── smooth update: fade out → update → fade in ───────────────
function fadeUpdate(fn) {{
  var vals = document.querySelectorAll('.fade-val');
  vals.forEach(function(el) {{ el.classList.add('fading'); }});
  setTimeout(function() {{
    fn();
    vals.forEach(function(el) {{ el.classList.remove('fading'); }});
  }}, 350);
}}

function applyData(d) {{
  fadeUpdate(function() {{
    // Workers
    document.getElementById('val-wc').textContent  = d.wc;
    document.getElementById('bar-wc').style.width  = Math.min(d.wc/40*100,100)+'%';
    document.getElementById('sub-wc').textContent  = d.wc+' personnel tracked on radar';

    // PPE
    var ppeEl = document.getElementById('val-ppe');
    ppeEl.textContent = d.ppe.toFixed(1);
    ppeEl.style.color = d.ppe_c;
    ppeEl.style.textShadow = '0 0 30px '+d.ppe_c+'40';
    document.getElementById('bar-ppe').style.width      = Math.min(d.ppe,100)+'%';
    document.getElementById('bar-ppe').style.background = d.ppe_c;
    document.getElementById('dot-ppe').style.background = d.ppe_c;
    document.getElementById('dot-ppe').style.color      = d.ppe_c;
    document.getElementById('acc-ppe').style.background = 'linear-gradient(90deg,transparent,'+(d.ppe_alert?'#ff2d2d':'var(--amber)')+',transparent)';
    document.getElementById('acc-ppe').style.opacity    = d.ppe_alert?'0.9':'0.5';
    document.getElementById('card-ppe').classList.toggle('alerted', d.ppe_alert);
    var ppeSub = d.ppe_alert?'CRITICAL — Below safety threshold':(d.ppe_warn?'Low — monitor closely':'All personnel equipped');
    var ppeSubEl = document.getElementById('sub-ppe');
    ppeSubEl.textContent  = ppeSub;
    ppeSubEl.className    = 'card-sub'+(d.ppe_alert?' danger':d.ppe_warn?' warn':'');

    // Temp
    var tmpEl = document.getElementById('val-tmp');
    tmpEl.textContent = d.tmp.toFixed(1);
    tmpEl.style.color = d.tmp_c;
    tmpEl.style.textShadow = '0 0 30px '+d.tmp_c+'40';
    document.getElementById('bar-tmp').style.width      = Math.min((d.tmp-20)/30*100,100)+'%';
    document.getElementById('bar-tmp').style.background = d.tmp_c;
    document.getElementById('dot-tmp').style.background = d.tmp_c;
    document.getElementById('dot-tmp').style.color      = d.tmp_c;
    document.getElementById('acc-tmp').style.background = 'linear-gradient(90deg,transparent,'+(d.tmp_alert?'#ff2d2d':'var(--amber)')+',transparent)';
    document.getElementById('acc-tmp').style.opacity    = d.tmp_alert?'0.9':'0.5';
    document.getElementById('card-tmp').classList.toggle('alerted', d.tmp_alert);
    var tmpSub = d.tmp_alert?'HEAT STRESS RISK — Hydration mandatory':(d.tmp_warn?'Elevated — monitor workers':'Temperature nominal');
    var tmpSubEl = document.getElementById('sub-tmp');
    tmpSubEl.textContent = tmpSub;
    tmpSubEl.className   = 'card-sub'+(d.tmp_alert?' danger':d.tmp_warn?' warn':'');

    // Dust
    var dstEl = document.getElementById('val-dst');
    dstEl.textContent = d.dst;
    dstEl.style.color = d.dst_c;
    dstEl.style.textShadow = '0 0 30px '+d.dst_c+'40';
    document.getElementById('bar-dst').style.width      = Math.min(d.dst/80*100,100)+'%';
    document.getElementById('bar-dst').style.background = d.dst_c;
    document.getElementById('dot-dst').style.background = d.dst_c;
    document.getElementById('dot-dst').style.color      = d.dst_c;
    document.getElementById('acc-dst').style.background = 'linear-gradient(90deg,transparent,'+(d.dst_alert?'#ff2d2d':'var(--amber)')+',transparent)';
    document.getElementById('acc-dst').style.opacity    = d.dst_alert?'0.9':'0.5';
    document.getElementById('card-dst').classList.toggle('alerted', d.dst_alert);
    var dstSub = d.dst_alert?'CRITICAL — Respirators required':(d.dst_warn?'Elevated — use precaution':'Air quality nominal');
    var dstSubEl = document.getElementById('sub-dst');
    dstSubEl.textContent = dstSub;
    dstSubEl.className   = 'card-sub'+(d.dst_alert?' danger':d.dst_warn?' warn':'');

    // Crane
    var crnEl = document.getElementById('val-crn');
    crnEl.textContent = d.crn;
    crnEl.style.color = d.crn_c;
    crnEl.style.textShadow = '0 0 30px '+d.crn_c+'40';
    document.getElementById('bar-crn').style.width      = Math.min(d.crn,100)+'%';
    document.getElementById('bar-crn').style.background = d.crn_c;
    document.getElementById('dot-crn').style.background = d.crn_c;
    document.getElementById('dot-crn').style.color      = d.crn_c;
    document.getElementById('acc-crn').style.background = 'linear-gradient(90deg,transparent,'+(d.crn_alert?'#ff2d2d':'var(--amber)')+',transparent)';
    document.getElementById('acc-crn').style.opacity    = d.crn_alert?'0.9':'0.5';
    document.getElementById('card-crn').classList.toggle('alerted', d.crn_alert);
    var crnSub = d.crn_alert?'OVERLOAD — Halt operations immediately':(d.crn_warn?'High load — proceed with caution':d.crn+'% capacity utilized');
    var crnSubEl = document.getElementById('sub-crn');
    crnSubEl.textContent = crnSub;
    crnSubEl.className   = 'card-sub'+(d.crn_alert?' danger':d.crn_warn?' warn':'');

    // Zone
    var zonEl   = document.getElementById('val-zon');
    var ringEl  = document.getElementById('ring-zon');
    var dotZon  = document.getElementById('dot-zon');
    zonEl.textContent = d.zon ? 'BREACH' : 'SECURE';
    zonEl.style.color = d.zon_c;
    zonEl.style.textShadow = '0 0 30px '+d.zon_c+'40';
    ringEl.textContent = d.zon ? 'ERR' : 'OK';
    ringEl.className   = 'intrusion-ring '+(d.zon?'breach':'secure');
    dotZon.style.background = d.zon_c;
    dotZon.style.color      = d.zon_c;
    document.getElementById('acc-zon').style.background = 'linear-gradient(90deg,transparent,'+(d.zon?'#ff2d2d':'var(--amber)')+',transparent)';
    document.getElementById('acc-zon').style.opacity    = d.zon?'0.9':'0.5';
    document.getElementById('card-zon').classList.toggle('alerted', d.zon);
    var zonSubEl = document.getElementById('sub-zon');
    zonSubEl.textContent = d.zon?'INTRUDER DETECTED — Evacuate restricted zone':'All zones secure';
    zonSubEl.className   = 'card-sub'+(d.zon?' danger':'');

    // Status bar
    var dot = document.getElementById('status-dot');
    var txt = document.getElementById('status-txt');
    dot.style.background  = d.status_color;
    dot.style.boxShadow   = '0 0 14px '+d.status_color;
    txt.style.color       = d.status_color;
    txt.textContent       = d.status_text;

    // Holo badge
    var hv = document.getElementById('holo-val');
    hv.textContent  = d.holo_text;
    hv.style.color  = d.status_color;
    document.getElementById('holo-sub').textContent = d.alert_count+' active alert'+(d.alert_count!==1?'s':'');

    // Alerts panel
    var panel   = document.getElementById('alerts-panel');
    var list    = document.getElementById('alerts-list');
    var badge   = document.getElementById('alerts-badge');
    var heading = document.getElementById('alerts-heading');
    if (d.alerts.length > 0) {{
      panel.classList.remove('hidden');
      badge.textContent   = d.alerts.length;
      heading.textContent = '\u2B21 '+d.alerts.length+' Active Safety Alert'+(d.alerts.length!==1?'s':'');
      list.innerHTML = d.alerts.map(function(a) {{
        return '<div class="alert-row"><span class="alert-pip"></span><span class="alert-msg">'+a+'</span></div>';
      }}).join('');
    }} else {{
      panel.classList.add('hidden');
    }}
  }});
}}

// ── clock & countdown ────────────────────────────────────────
function tick() {{
  var now    = new Date();
  var time   = pad(now.getHours())+':'+pad(now.getMinutes())+':'+pad(now.getSeconds());
  var days   = ['SUN','MON','TUE','WED','THU','FRI','SAT'];
  var months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];
  var date   = days[now.getDay()]+' '+pad(now.getDate())+' '+months[now.getMonth()]+' '+now.getFullYear();
  document.getElementById('clk').textContent  = time;
  document.getElementById('dt').textContent   = date;
  document.getElementById('sync').textContent = 'LAST SYNC: '+time;

  var elapsed   = (Date.now() - startTs) % REFRESH_MS;
  var remaining = 1 - elapsed/REFRESH_MS;
  document.getElementById('bar').style.width = (remaining*100).toFixed(2)+'%';
}}

// ── pure JS data generator (mirrors Python logic) ─────────────
function rand(a,b) {{ return Math.random()*(b-a)+a; }}

function generateData() {{
  var wc  = Math.round(rand(15,35));
  var ppe = Math.round(rand(85,98)*10)/10;
  var tmp = Math.round(rand(28,42)*10)/10;
  var dst = Math.round(rand(20,80));
  var crn = Math.round(rand(60,110));
  var zon = Math.random() < 0.25;

  var ppe_a = ppe < 92; var ppe_w = ppe < 95 && !ppe_a;
  var tmp_a = tmp > 38; var tmp_w = tmp > 34 && !tmp_a;
  var dst_a = dst > 60; var dst_w = dst > 45 && !dst_a;
  var crn_a = crn > 100; var crn_w = crn > 85 && !crn_a;

  function vc(a,w) {{ return a?'#ff5050':(w?'#ff9500':'#00ff88'); }}

  var alerts = [];
  if (ppe_a) alerts.push('PPE compliance below threshold — risk of injury');
  if (tmp_a) alerts.push('High ambient temperature — heat stress risk active');
  if (dst_a) alerts.push('Dust levels critical — respiratory hazard');
  if (crn_a) alerts.push('Crane overload detected — halt all lift operations');
  if (zon)   alerts.push('Restricted zone breach — intruder detected');

  return {{
    wc:wc, ppe:ppe, tmp:tmp, dst:dst, crn:crn, zon:zon,
    ppe_c:vc(ppe_a,ppe_w), tmp_c:vc(tmp_a,tmp_w),
    dst_c:vc(dst_a,dst_w), crn_c:vc(crn_a,crn_w),
    zon_c: zon?'#ff5050':'#00ff88',
    ppe_alert:ppe_a, ppe_warn:ppe_w,
    tmp_alert:tmp_a, tmp_warn:tmp_w,
    dst_alert:dst_a, dst_warn:dst_w,
    crn_alert:crn_a, crn_warn:crn_w,
    alerts:alerts,
    alert_count:alerts.length,
    status_color: alerts.length?'#ff2d2d':'#00ff88',
    status_text: alerts.length?(alerts.length+' ALERT'+(alerts.length!==1?'S':'')+' ACTIVE'):'SYSTEMS NOMINAL',
    holo_text: alerts.length?'ALERT':'ALL CLEAR',
  }};
}}

// ── boot ─────────────────────────────────────────────────────
applyData(pending);   // render initial data immediately
tick();
setInterval(tick, 100);

// refresh smoothly with JS — no page reload
setInterval(function() {{
  startTs = Date.now();
  applyData(generateData());
}}, REFRESH_MS);
</script>
</body>
</html>""", height=0, scrolling=False)
