from flask import Flask, render_template_string
import random

app = Flask(__name__)

@app.route("/")
def dashboard():
    worker_count = random.randint(15, 35)
    ppe_compliance = random.uniform(85, 98)
    temperature = random.uniform(28, 42)
    dust_level = random.uniform(20, 80)
    crane_load = random.uniform(60, 110)
    zone_intrusion = random.choice([False, False, False, True])

    alerts = []
    if ppe_compliance < 92:
        alerts.append("PPE compliance below threshold — risk of injury")
    if temperature > 38:
        alerts.append("High ambient temperature — heat stress risk active")
    if dust_level > 60:
        alerts.append("Dust levels critical — respiratory hazard")
    if crane_load > 100:
        alerts.append("Crane overload detected — halt all lift operations")
    if zone_intrusion:
        alerts.append("Restricted zone breach — intruder detected")

    html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Construction Site OS</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@200;300;400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    :root{
      --amber:#ff9500;--amber2:#ffcc00;--red:#ff2d2d;--green:#00ff88;
      --blue:#00cfff;--bg:#030508;--bg2:#070b11;--bg3:#0d1117;
      --border:rgba(255,149,0,0.15);--border2:rgba(255,149,0,0.35);
      --mono:'Share Tech Mono',monospace;
      --head:'Orbitron',sans-serif;
      --body:'Exo 2',sans-serif;
    }
    body{background:var(--bg);overflow-x:hidden;min-height:100vh}
    .bg-scanlines{position:fixed;inset:0;pointer-events:none;z-index:0;
      background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.18) 2px,rgba(0,0,0,0.18) 4px);}
    .bg-grid{position:fixed;inset:0;pointer-events:none;z-index:0;
      background-image:linear-gradient(rgba(255,149,0,0.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,149,0,0.05) 1px,transparent 1px);
      background-size:60px 60px;}
    .bg-tl{position:fixed;top:-200px;left:-200px;width:600px;height:600px;border-radius:50%;
      filter:blur(120px);opacity:0.07;background:var(--amber);pointer-events:none;z-index:0;}
    .bg-br{position:fixed;bottom:-200px;right:-200px;width:600px;height:600px;border-radius:50%;
      filter:blur(120px);opacity:0.07;background:var(--blue);pointer-events:none;z-index:0;}
    .bg-radar{position:fixed;right:-180px;bottom:-180px;width:500px;height:500px;
      pointer-events:none;z-index:0;border-radius:50%;
      border:1px solid rgba(255,149,0,0.06);overflow:hidden;}
    .radar-sweep{position:absolute;top:50%;left:50%;width:50%;height:1px;
      background:linear-gradient(90deg,transparent,rgba(255,149,0,0.3));
      transform-origin:left center;animation:radar-spin 5s linear infinite;}
    @keyframes radar-spin{to{transform:rotate(360deg)}}

    .content{position:relative;z-index:2;padding:22px;max-width:1120px;margin:0 auto;
      font-family:var(--body);color:#fff;}

    /* HEADER */
    .header{display:grid;grid-template-columns:1fr auto 1fr;align-items:start;
      margin-bottom:24px;gap:16px;}
    .sys-tag{font-family:var(--mono);font-size:9px;color:var(--amber);
      letter-spacing:0.22em;text-transform:uppercase;margin-bottom:6px;
      display:flex;align-items:center;gap:6px;}
    .sys-tag::before{content:'';width:16px;height:1px;background:var(--amber);opacity:0.6;}
    .site-title{font-family:var(--head);font-size:30px;font-weight:900;letter-spacing:0.06em;
      background:linear-gradient(135deg,#fff 30%,var(--amber) 100%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1;}
    .site-sub{font-size:11px;font-weight:200;color:rgba(255,255,255,0.35);
      letter-spacing:0.12em;text-transform:uppercase;margin-top:6px;}

    .holo-badge{display:inline-block;position:relative;padding:14px 20px;
      border:1px solid var(--border2);border-radius:6px;
      background:rgba(255,149,0,0.04);min-width:160px;text-align:center;}
    .holo-badge::before,.holo-badge::after{content:'';position:absolute;
      width:8px;height:8px;border-color:var(--amber);border-style:solid;}
    .holo-badge::before{top:-1px;left:-1px;border-width:1px 0 0 1px;border-radius:1px 0 0 0;}
    .holo-badge::after{bottom:-1px;right:-1px;border-width:0 1px 1px 0;border-radius:0 0 1px 1px;}
    .holo-label{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.35);
      letter-spacing:0.18em;text-transform:uppercase;margin-bottom:6px;}
    .holo-val{font-family:var(--head);font-size:16px;font-weight:700;letter-spacing:0.1em;}
    .holo-sub{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.3);
      margin-top:4px;letter-spacing:0.1em;}

    .header-right{text-align:right;}
    .clock-block{font-family:var(--mono);font-size:26px;color:var(--amber);
      letter-spacing:0.08em;text-shadow:0 0 20px rgba(255,149,0,0.4);}
    .date-block{font-family:var(--mono);font-size:10px;color:rgba(255,255,255,0.28);
      letter-spacing:0.1em;margin-top:4px;text-transform:uppercase;}
    .rc-wrap{margin-top:8px;display:flex;align-items:center;gap:8px;justify-content:flex-end;}
    .rc-label{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.25);letter-spacing:0.08em;}
    .rc-bar{width:90px;height:2px;background:rgba(255,149,0,0.12);border-radius:1px;overflow:hidden;}
    .rc-fill{height:100%;background:linear-gradient(90deg,var(--amber2),var(--amber));border-radius:1px;
      animation:refill 5s linear forwards;}
    @keyframes refill{from{width:100%}to{width:0%}}

    .divider{height:1px;background:linear-gradient(90deg,transparent,var(--amber),transparent);
      opacity:0.25;margin-bottom:22px;position:relative;}
    .divider::after{content:'';position:absolute;top:-2px;left:50%;transform:translateX(-50%);
      width:6px;height:6px;background:var(--amber);border-radius:50%;box-shadow:0 0 12px var(--amber);}

    /* STATUS BAR */
    .status-bar{display:flex;align-items:center;justify-content:space-between;
      background:var(--bg2);border:1px solid var(--border);border-radius:6px;
      padding:10px 18px;margin-bottom:16px;}
    .status-left{display:flex;align-items:center;gap:12px;}
    .status-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
    .status-txt{font-family:var(--head);font-size:13px;font-weight:700;letter-spacing:0.1em;}
    .status-right{display:flex;align-items:center;gap:20px;}
    .sensor-pill{display:flex;align-items:center;gap:5px;font-family:var(--mono);
      font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:0.08em;}
    .sensor-pip{width:4px;height:4px;border-radius:50%;background:var(--green);
      animation:pulse-dot 2.5s ease-in-out infinite;}
    @keyframes pulse-dot{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.3;transform:scale(0.6)}}

    /* METRICS GRID */
    .metrics-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:16px;}
    .metric-card{position:relative;background:var(--bg2);border:1px solid var(--border);
      border-radius:6px;padding:20px;overflow:hidden;
      transition:border-color 0.5s,box-shadow 0.5s;}
    .metric-card:hover{border-color:var(--border2);
      box-shadow:0 8px 40px rgba(0,0,0,0.6),0 0 0 1px rgba(255,149,0,0.1);}
    .metric-card.alerted{border-color:rgba(255,45,45,0.4)!important;background:#0d0505;
      box-shadow:0 0 30px rgba(255,45,45,0.08);}
    .card-accent{position:absolute;top:0;left:0;right:0;height:2px;opacity:0.5;}
    .metric-card::before,.metric-card::after{content:'';position:absolute;
      width:10px;height:10px;border-color:rgba(255,149,0,0.25);border-style:solid;}
    .metric-card::before{top:6px;left:6px;border-width:1px 0 0 1px;}
    .metric-card::after{bottom:6px;right:6px;border-width:0 1px 1px 0;}
    .metric-card.alerted::before,.metric-card.alerted::after{border-color:rgba(255,45,45,0.4);}
    .card-id{font-family:var(--mono);font-size:8px;color:rgba(255,255,255,0.18);
      letter-spacing:0.2em;text-transform:uppercase;position:absolute;top:14px;right:16px;}
    .card-label{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.38);
      letter-spacing:0.15em;text-transform:uppercase;margin-bottom:12px;
      display:flex;align-items:center;gap:6px;}
    .label-dot{width:4px;height:4px;border-radius:50%;box-shadow:0 0 6px currentColor;
      animation:pulse-dot 2s ease-in-out infinite;}
    .card-value{font-family:var(--head);font-size:40px;font-weight:900;line-height:1;
      letter-spacing:0.02em;}
    .card-unit{font-family:var(--mono);font-size:12px;color:rgba(255,255,255,0.35);margin-left:4px;}
    .bar-track{height:2px;background:rgba(255,255,255,0.05);border-radius:1px;margin-top:14px;overflow:hidden;}
    .bar-fill{height:100%;border-radius:1px;position:relative;}
    .bar-fill::after{content:'';position:absolute;right:0;top:-1px;bottom:-1px;width:3px;
      background:inherit;filter:brightness(1.5);border-radius:1px;}
    .card-sub{margin-top:8px;font-size:10px;color:rgba(255,255,255,0.28);
      font-weight:300;letter-spacing:0.04em;}
    .card-sub.warn{color:rgba(255,149,0,0.7);}
    .card-sub.danger{color:rgba(255,100,100,0.8);}
    .intrusion-row{display:flex;align-items:center;gap:10px;margin-top:12px;}
    .intrusion-ring{width:36px;height:36px;border-radius:50%;border:2px solid;
      display:flex;align-items:center;justify-content:center;
      font-family:var(--mono);font-size:9px;font-weight:700;flex-shrink:0;}
    .intrusion-ring.secure{border-color:var(--green);color:var(--green);box-shadow:0 0 14px rgba(0,255,136,0.2);}
    .intrusion-ring.breach{border-color:var(--red);color:var(--red);
      box-shadow:0 0 20px rgba(255,45,45,0.4);animation:ring-pulse 0.7s ease-in-out infinite;}
    @keyframes ring-pulse{0%,100%{box-shadow:0 0 20px rgba(255,45,45,0.4)}
      50%{box-shadow:0 0 40px rgba(255,45,45,0.7),0 0 0 4px rgba(255,45,45,0.1)}}

    /* ALERTS PANEL */
    .alerts-panel{border-radius:6px;border:1px solid rgba(255,45,45,0.25);
      background:#0c0606;overflow:hidden;margin-bottom:16px;}
    .alerts-top{padding:12px 18px;background:rgba(255,45,45,0.07);
      border-bottom:1px solid rgba(255,45,45,0.15);display:flex;align-items:center;gap:10px;}
    .alerts-heading{font-family:var(--head);font-size:11px;font-weight:700;
      letter-spacing:0.14em;text-transform:uppercase;color:var(--red);flex:1;}
    .alerts-badge{background:var(--red);color:#fff;font-family:var(--mono);
      font-size:9px;padding:3px 7px;border-radius:2px;letter-spacing:0.05em;}
    .alert-row{display:flex;align-items:center;gap:12px;padding:11px 18px;
      border-bottom:1px solid rgba(255,255,255,0.03);}
    .alert-row:last-child{border-bottom:none;}
    .alert-pip{width:5px;height:5px;border-radius:50%;background:var(--red);
      flex-shrink:0;animation:pulse-dot 0.8s ease-in-out infinite;}
    .alert-msg{font-size:12px;font-weight:300;color:rgba(255,180,180,0.8);letter-spacing:0.03em;}

    /* FOOTER */
    .footer{display:flex;align-items:center;justify-content:space-between;
      padding-top:14px;border-top:1px solid rgba(255,255,255,0.05);}
    .footer-sys{font-family:var(--mono);font-size:9px;color:rgba(255,255,255,0.18);letter-spacing:0.1em;}
    .footer-sync{font-family:var(--mono);font-size:9px;color:rgba(255,149,0,0.4);letter-spacing:0.08em;}

    @media(max-width:700px){
      .metrics-grid{grid-template-columns:repeat(2,1fr)}
      .site-title{font-size:20px}.clock-block{font-size:20px}
      .header{grid-template-columns:1fr}
      .header-center,.header-right{display:none}
    }
    @media(max-width:480px){.metrics-grid{grid-template-columns:1fr}}
  </style>
</head>
<body>
  <div class="bg-scanlines"></div>
  <div class="bg-grid"></div>
  <div class="bg-tl"></div>
  <div class="bg-br"></div>
  <div class="bg-radar"><div class="radar-sweep"></div></div>

  <div class="content">
    <div class="header">
      <div class="header-left">
        <div class="sys-tag">SYS:MONITOR · BUILD 4.1.2</div>
        <div class="site-title">CONSTRUCTION<br>SITE OS</div>
        <div class="site-sub">Sector 7 · Block C · Live Intelligence Feed</div>
      </div>
      <div class="header-center">
        <div class="holo-badge">
          <div class="holo-label">SITE STATUS</div>
          <div class="holo-val" style="color:{{ 'var(--red)' if alerts else 'var(--green)' }}">
            {{ 'ALERT' if alerts else 'ALL CLEAR' }}
          </div>
          <div class="holo-sub">{{ alerts|length }} active alert{{ 's' if alerts|length != 1 else '' }}</div>
        </div>
      </div>
      <div class="header-right">
        <div class="clock-block" id="clock">--:--:--</div>
        <div class="date-block" id="dateline">— — —</div>
        <div class="rc-wrap">
          <span class="rc-label">NEXT REFRESH</span>
          <div class="rc-bar"><div class="rc-fill"></div></div>
        </div>
      </div>
    </div>

    <div class="divider"></div>

    <div class="status-bar">
      <div class="status-left">
        <div class="status-dot" style="
          background:{{ 'var(--red)' if alerts else 'var(--green)' }};
          box-shadow:0 0 14px {{ '#ff2d2d' if alerts else '#00ff88' }};
          animation:pulse-dot {{ '0.8s' if alerts else '3s' }} ease-in-out infinite;
        "></div>
        <span class="status-txt" style="color:{{ 'var(--red)' if alerts else 'var(--green)' }}">
          {{ (alerts|length)|string + ' ALERT' + ('S' if alerts|length != 1 else '') + ' ACTIVE' if alerts else 'SYSTEMS NOMINAL' }}
        </span>
      </div>
      <div class="status-right">
        <div class="sensor-pill"><span class="sensor-pip"></span>PPE CAM</div>
        <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:0.4s"></span>DUST SENSOR</div>
        <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:0.8s"></span>CRANE LOAD</div>
        <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:1.2s"></span>THERMAL</div>
        <div class="sensor-pill"><span class="sensor-pip" style="animation-delay:1.6s"></span>ZONE DETECT</div>
      </div>
    </div>

    {% macro value_color(alert, warn, ok, is_alert, is_warn) %}
      {{ '#ff5050' if is_alert else ('#ff9500' if is_warn else ok) }}
    {% endmacro %}

    <div class="metrics-grid">
      <!-- Workers -->
      {% set wc = worker_count %}
      <div class="metric-card">
        <div class="card-accent" style="background:linear-gradient(90deg,transparent,var(--amber),transparent);opacity:0.5"></div>
        <div class="card-id">WRK-01</div>
        <div class="card-label"><span class="label-dot" style="background:var(--amber);color:var(--amber)"></span>Workers On Site</div>
        <div style="display:flex;align-items:baseline;gap:6px">
          <div class="card-value" style="color:#fff">{{ wc }}</div>
        </div>
        <div class="bar-track"><div class="bar-fill" style="width:{{ (wc/40*100)|round }}%;background:var(--amber)"></div></div>
        <div class="card-sub">{{ wc }} personnel tracked on radar</div>
      </div>

      <!-- PPE -->
      {% set pa = ppe_compliance < 92 %}
      {% set pw = ppe_compliance < 95 and not pa %}
      {% set pc = '#ff5050' if pa else ('#ff9500' if pw else '#00ff88') %}
      <div class="metric-card {{ 'alerted' if pa else '' }}">
        <div class="card-accent" style="background:linear-gradient(90deg,transparent,{{ '#ff2d2d' if pa else 'var(--amber)' }},transparent);opacity:{{ '0.9' if pa else '0.5' }}"></div>
        <div class="card-id">PPE-02</div>
        <div class="card-label"><span class="label-dot" style="background:{{ pc }};color:{{ pc }};animation-duration:{{ '0.8s' if pa else '2s' }}"></span>PPE Compliance</div>
        <div style="display:flex;align-items:baseline;gap:6px">
          <div class="card-value" style="color:{{ pc }};text-shadow:0 0 30px {{ pc }}40">{{ "%.1f"|format(ppe_compliance) }}</div>
          <span class="card-unit">%</span>
        </div>
        <div class="bar-track"><div class="bar-fill" style="width:{{ ppe_compliance|round }}%;background:{{ pc }}"></div></div>
        <div class="card-sub {{ 'danger' if pa else ('warn' if pw else '') }}">
          {{ 'CRITICAL — Below safety threshold' if pa else ('Low — monitor closely' if pw else 'All personnel equipped') }}
        </div>
      </div>

      <!-- Temperature -->
      {% set ta = temperature > 38 %}
      {% set tw = temperature > 34 and not ta %}
      {% set tc = '#ff5050' if ta else ('#ff9500' if tw else '#00cfff') %}
      <div class="metric-card {{ 'alerted' if ta else '' }}">
        <div class="card-accent" style="background:linear-gradient(90deg,transparent,{{ '#ff2d2d' if ta else 'var(--amber)' }},transparent);opacity:{{ '0.9' if ta else '0.5' }}"></div>
        <div class="card-id">TMP-03</div>
        <div class="card-label"><span class="label-dot" style="background:{{ tc }};color:{{ tc }};animation-duration:{{ '0.8s' if ta else '2s' }}"></span>Ambient Temperature</div>
        <div style="display:flex;align-items:baseline;gap:6px">
          <div class="card-value" style="color:{{ tc }};text-shadow:0 0 30px {{ tc }}40">{{ "%.1f"|format(temperature) }}</div>
          <span class="card-unit">°C</span>
        </div>
        <div class="bar-track"><div class="bar-fill" style="width:{{ ((temperature-20)/30*100)|round }}%;background:{{ tc }}"></div></div>
        <div class="card-sub {{ 'danger' if ta else ('warn' if tw else '') }}">
          {{ 'HEAT STRESS RISK — Hydration mandatory' if ta else ('Elevated — monitor workers' if tw else 'Temperature nominal') }}
        </div>
      </div>

      <!-- Dust -->
      {% set da = dust_level > 60 %}
      {% set dw = dust_level > 45 and not da %}
      {% set dc = '#ff5050' if da else ('#ff9500' if dw else '#00ff88') %}
      <div class="metric-card {{ 'alerted' if da else '' }}">
        <div class="card-accent" style="background:linear-gradient(90deg,transparent,{{ '#ff2d2d' if da else 'var(--amber)' }},transparent);opacity:{{ '0.9' if da else '0.5' }}"></div>
        <div class="card-id">DST-04</div>
        <div class="card-label"><span class="label-dot" style="background:{{ dc }};color:{{ dc }};animation-duration:{{ '0.8s' if da else '2s' }}"></span>Dust Particulate</div>
        <div style="display:flex;align-items:baseline;gap:6px">
          <div class="card-value" style="color:{{ dc }};text-shadow:0 0 30px {{ dc }}40">{{ "%.0f"|format(dust_level) }}</div>
          <span class="card-unit">mg/m³</span>
        </div>
        <div class="bar-track"><div class="bar-fill" style="width:{{ (dust_level/80*100)|round }}%;background:{{ dc }}"></div></div>
        <div class="card-sub {{ 'danger' if da else ('warn' if dw else '') }}">
          {{ 'CRITICAL — Respirators required' if da else ('Elevated — use precaution' if dw else 'Air quality nominal') }}
        </div>
      </div>

      <!-- Crane -->
      {% set ca = crane_load > 100 %}
      {% set cw = crane_load > 85 and not ca %}
      {% set cc = '#ff5050' if ca else ('#ff9500' if cw else '#00ff88') %}
      <div class="metric-card {{ 'alerted' if ca else '' }}">
        <div class="card-accent" style="background:linear-gradient(90deg,transparent,{{ '#ff2d2d' if ca else 'var(--amber)' }},transparent);opacity:{{ '0.9' if ca else '0.5' }}"></div>
        <div class="card-id">CRN-05</div>
        <div class="card-label"><span class="label-dot" style="background:{{ cc }};color:{{ cc }};animation-duration:{{ '0.8s' if ca else '2s' }}"></span>Crane Load</div>
        <div style="display:flex;align-items:baseline;gap:6px">
          <div class="card-value" style="color:{{ cc }};text-shadow:0 0 30px {{ cc }}40">{{ "%.0f"|format(crane_load) }}</div>
          <span class="card-unit">%</span>
        </div>
        <div class="bar-track"><div class="bar-fill" style="width:{{ [crane_load, 100]|min|round }}%;background:{{ cc }}"></div></div>
        <div class="card-sub {{ 'danger' if ca else ('warn' if cw else '') }}">
          {{ 'OVERLOAD — Halt operations immediately' if ca else ('High load — proceed with caution' if cw else '%.0f'|format(crane_load) + '% capacity utilized') }}
        </div>
      </div>

      <!-- Zone Intrusion -->
      {% set zc = '#ff5050' if zone_intrusion else '#00ff88' %}
      <div class="metric-card {{ 'alerted' if zone_intrusion else '' }}">
        <div class="card-accent" style="background:linear-gradient(90deg,transparent,{{ '#ff2d2d' if zone_intrusion else 'var(--amber)' }},transparent);opacity:{{ '0.9' if zone_intrusion else '0.5' }}"></div>
        <div class="card-id">ZON-06</div>
        <div class="card-label"><span class="label-dot" style="background:{{ zc }};color:{{ zc }};animation-duration:{{ '0.8s' if zone_intrusion else '2s' }}"></span>Zone Intrusion</div>
        <div class="card-value" style="color:{{ zc }};text-shadow:0 0 30px {{ zc }}40;font-family:var(--head);font-size:34px;font-weight:900;letter-spacing:0.04em">
          {{ 'BREACH' if zone_intrusion else 'SECURE' }}
        </div>
        <div class="intrusion-row">
          <div class="intrusion-ring {{ 'breach' if zone_intrusion else 'secure' }}">{{ 'ERR' if zone_intrusion else 'OK' }}</div>
          <div class="card-sub {{ 'danger' if zone_intrusion else '' }}" style="margin-top:0">
            {{ 'INTRUDER DETECTED — Evacuate restricted zone' if zone_intrusion else 'All zones secure' }}
          </div>
        </div>
      </div>
    </div>

    {% if alerts %}
    <div class="alerts-panel">
      <div class="alerts-top">
        <span class="alerts-heading">⬡ Active Safety Alerts</span>
        <span class="alerts-badge">{{ alerts|length }}</span>
      </div>
      {% for alert in alerts %}
      <div class="alert-row">
        <span class="alert-pip"></span>
        <span class="alert-msg">{{ alert }}</span>
      </div>
      {% endfor %}
    </div>
    {% endif %}

    <div class="footer">
      <div class="footer-sys">SMART-SITE™ · SAFETY INTELLIGENCE PLATFORM · v4.1</div>
      <div class="footer-sync" id="footer-sync">LAST SYNC: —</div>
    </div>
  </div>

  <script>
    function tick(){
      const now=new Date();
      const t=now.toLocaleTimeString('en-GB',{hour12:false});
      const d=now.toLocaleDateString('en-GB',{weekday:'short',day:'2-digit',month:'short',year:'numeric'}).toUpperCase();
      document.getElementById('clock').textContent=t;
      document.getElementById('dateline').textContent=d;
      document.getElementById('footer-sync').textContent='LAST SYNC: '+t;
    }
    tick();
    setInterval(tick,1000);
    setTimeout(()=>location.reload(),5000);
  </script>
</body>
</html>
    """
    return render_template_string(html,
        worker_count=worker_count, ppe_compliance=ppe_compliance,
        temperature=temperature, dust_level=dust_level,
        crane_load=crane_load, zone_intrusion=zone_intrusion,
        alerts=alerts)

if __name__ == "__main__":
    app.run(debug=True)