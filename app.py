import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Construction Site OS", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #030508;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
.main {
    background: linear-gradient(180deg, #030508 0%, #070b11 100%);
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}
.title {
    font-size: 38px;
    font-weight: 800;
    color: #ff9500;
    letter-spacing: 2px;
}
.subtitle {
    color: #bbbbbb;
    font-size: 14px;
    margin-bottom: 20px;
}
.card {
    background: #0d1117;
    border: 1px solid rgba(255,149,0,0.2);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 0 12px rgba(255,149,0,0.08);
}
.alert-card {
    background: #140909;
    border: 1px solid rgba(255,45,45,0.35);
    border-radius: 12px;
    padding: 16px;
    margin-top: 10px;
}
.metric-label {
    color: #bcbcbc;
    font-size: 13px;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 34px;
    font-weight: 800;
}
.safe {
    color: #00ff88;
}
.warn {
    color: #ff9500;
}
.danger {
    color: #ff5050;
}
.small {
    color: #8f8f8f;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

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

status = "ALERT" if alerts else "ALL CLEAR"
status_class = "danger" if alerts else "safe"

st.markdown('<div class="title">CONSTRUCTION SITE OS</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Sector 7 · Block C · Live Intelligence Feed</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f'<div class="card"><div class="metric-label">SITE STATUS</div><div class="metric-value {status_class}">{status}</div><div class="small">{len(alerts)} active alert(s)</div></div>', unsafe_allow_html=True)
with col2:
    now = datetime.now()
    st.markdown(f'<div class="card"><div class="metric-label">TIME</div><div class="metric-value warn">{now.strftime("%H:%M:%S")}</div><div class="small">{now.strftime("%d %b %Y")}</div></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f'<div class="card"><div class="metric-label">Workers On Site</div><div class="metric-value">{worker_count}</div><div class="small">Personnel tracked on radar</div></div>', unsafe_allow_html=True)
    ppe_class = "danger" if ppe_compliance < 92 else "warn" if ppe_compliance < 95 else "safe"
    st.markdown(f'<div class="card"><div class="metric-label">PPE Compliance</div><div class="metric-value {ppe_class}">{ppe_compliance:.1f}%</div><div class="small">Helmet and gear compliance</div></div>', unsafe_allow_html=True)

with c2:
    temp_class = "danger" if temperature > 38 else "warn" if temperature > 34 else "safe"
    st.markdown(f'<div class="card"><div class="metric-label">Ambient Temperature</div><div class="metric-value {temp_class}">{temperature:.1f}°C</div><div class="small">Heat stress monitoring</div></div>', unsafe_allow_html=True)
    dust_class = "danger" if dust_level > 60 else "warn" if dust_level > 45 else "safe"
    st.markdown(f'<div class="card"><div class="metric-label">Dust Particulate</div><div class="metric-value {dust_class}">{dust_level:.0f} mg/m³</div><div class="small">Air quality status</div></div>', unsafe_allow_html=True)

with c3:
    crane_class = "danger" if crane_load > 100 else "warn" if crane_load > 85 else "safe"
    st.markdown(f'<div class="card"><div class="metric-label">Crane Load</div><div class="metric-value {crane_class}">{crane_load:.0f}%</div><div class="small">Lift utilization</div></div>', unsafe_allow_html=True)
    zone_text = "BREACH" if zone_intrusion else "SECURE"
    zone_class = "danger" if zone_intrusion else "safe"
    st.markdown(f'<div class="card"><div class="metric-label">Zone Intrusion</div><div class="metric-value {zone_class}">{zone_text}</div><div class="small">Restricted area monitoring</div></div>', unsafe_allow_html=True)

st.markdown("### Active Safety Alerts")
if alerts:
    for alert in alerts:
        st.markdown(f'<div class="alert-card">⚠️ {alert}</div>', unsafe_allow_html=True)
else:
    st.success("No active alerts. Systems nominal.")

st.caption("SMART-SITE™ · SAFETY INTELLIGENCE PLATFORM · v4.1")