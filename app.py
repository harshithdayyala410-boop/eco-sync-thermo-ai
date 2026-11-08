"""
Eco Sync & Thermo AI - Data Centre Waste-Heat Recovery System
Main Streamlit Application
"""

import streamlit as st
import time
from datetime import datetime
import pandas as pd

from simulation import ThermoSimulationEngine, FacilityConfig
from ai_scheduler import ThermoAIScheduler
import components as ui

# Page configuration
st.set_page_config(
    page_title="Eco Sync & Thermo AI | Data Centre Waste-Heat Recovery",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom modern styling
st.markdown(ui.get_custom_css(), unsafe_allow_html=True)

# Initialize session state objects
if "sim_engine" not in st.session_state:
    st.session_state.sim_engine = ThermoSimulationEngine()

if "ai_scheduler" not in st.session_state:
    st.session_state.ai_scheduler = ThermoAIScheduler()

if "preset_applied" not in st.session_state:
    st.session_state.preset_applied = False


# ==========================================
# SIDEBAR CONTROLS & CONFIGURATION
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
            <span style="font-size: 2rem;">🌐</span>
            <div>
                <h3 style="margin: 0; color: #10b981; font-size: 1.25rem;">Eco Sync & Thermo AI</h3>
                <span style="font-size: 0.75rem; color: #94a3b8;">Waste-Heat Recovery Simulator</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚙️ Scenario Presets")
    preset_choice = st.selectbox(
        "Load Quick Demonstration Scenario:",
        [
            "Custom User Control",
            "🌱 Balanced Eco-Harvesting (Spring)",
            "❄️ Winter Peak AI Training & Greenhouse Boost",
            "🔥 Summer Heatwave (High Ambient Stress)",
            "🚨 Extreme Overload (Trigger Safety Override)",
            "🌙 Overnight Low Compute (Buffer Standby)"
        ],
        index=0
    )

    # Preset value overrides
    default_workload = 68.0
    default_ambient = 18.0

    if preset_choice == "🌱 Balanced Eco-Harvesting (Spring)":
        default_workload = 65.0
        default_ambient = 16.0
    elif preset_choice == "❄️ Winter Peak AI Training & Greenhouse Boost":
        default_workload = 88.0
        default_ambient = -4.0
    elif preset_choice == "🔥 Summer Heatwave (High Ambient Stress)":
        default_workload = 82.0
        default_ambient = 36.0
    elif preset_choice == "🚨 Extreme Overload (Trigger Safety Override)":
        default_workload = 96.0
        default_ambient = 39.0
    elif preset_choice == "🌙 Overnight Low Compute (Buffer Standby)":
        default_workload = 22.0
        default_ambient = 10.0

    st.markdown("---")
    st.subheader("🎛️ Primary Simulation Controls")
    
    # 1. Interactive slider: Server Workload / AI Traffic (%)
    st.markdown("**1️⃣ Server Workload / AI Traffic**")
    workload = st.slider(
        "Compute Load & Active GPU Clusters (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(default_workload),
        step=1.0,
        help="Simulates active AI training jobs, LLM inference volume, and data processing throughput.",
        key="slider_workload"
    )

    # 2. Interactive slider: Outdoor Ambient Temperature (°C)
    st.markdown("**2️⃣ Outdoor Ambient Temperature**")
    ambient_temp = st.slider(
        "External Weather Climate (°C)",
        min_value=-15.0,
        max_value=45.0,
        value=float(default_ambient),
        step=0.5,
        help="Ambient temperature outside the facility. Influences cooling tower performance and greenhouse/building heating demand.",
        key="slider_ambient"
    )

    st.markdown("---")
    st.subheader("🛡️ Safety & Facility Parameters")
    
    # Manual emergency safety toggle
    manual_override = st.toggle("Simulate Manual Safety Override", value=False,
                                help="Forces emergency bypass loop engagement, coolant flow surge, and batch compute throttle.")

    # Flow rate multiplier
    flow_multiplier = st.slider(
        "Coolant Flow Rate Adjuster",
        min_value=0.7,
        max_value=1.5,
        value=1.0,
        step=0.05,
        help="Adjusts primary liquid circulation pump baseline speed."
    )

    # AI Scheduling Strategy
    ai_strategy = st.selectbox(
        "Thermo AI Optimization Strategy:",
        ["Eco-Max (Carbon Minimization)", "Cost-Optimal (Utility Arbitrage)", "Buffer-Priority (Grid Peak Shaving)"]
    )

    st.markdown("---")
    st.caption("Developed for Eco-Innovation Research | Data Centre Thermodynamics v4.2")


# ==========================================
# EXECUTE THERMODYNAMIC SIMULATION
# ==========================================
sim_result = st.session_state.sim_engine.compute(
    workload_pct=workload,
    ambient_temp_c=ambient_temp,
    manual_safety_override=manual_override,
    user_flow_multiplier=flow_multiplier
)

# Update AI Scheduler logs
log_history = st.session_state.ai_scheduler.evaluate_and_log(
    sim=sim_result,
    user_mode=ai_strategy
)


# ==========================================
# MAIN PAGE HEADER & BRANDING
# ==========================================
st.markdown("""
    <div class="main-hero-banner">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <div class="hero-title">🌱 Eco Sync & Thermo AI</div>
                <div class="hero-subtitle">
                    Autonomous Data Centre Waste-Heat Recovery, Co-Generation & Intelligent Thermal Dispatch
                </div>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 8px;">
                <span style="background: rgba(16,185,129,0.2); color: #10b981; border: 1px solid rgba(16,185,129,0.4); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 600;">
                    LIVE CO-GEN ACTIVE
                </span>
                <span style="background: rgba(56,189,248,0.2); color: #38bdf8; border: 1px solid rgba(56,189,248,0.4); padding: 4px 10px; border-radius: 6px; font-size: 0.78rem; font-weight: 600;">
                    AI DISPATCH v4.2
                </span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# SAFETY OVERRIDE ALERT BANNER
# ==========================================
st.markdown(ui.render_safety_banner(sim_result), unsafe_allow_html=True)


# ==========================================
# PRIMARY REAL-TIME KPI METRICS
# ==========================================
mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)

with mcol1:
    # Outlet Water Temp (30°C to 50°C band)
    temp_val = sim_result.outlet_water_temp_c
    status_label = "Nominal" if temp_val < 44.0 else ("Caution" if temp_val < 49.0 else "Critical Override")
    temp_color = "#10b981" if temp_val < 44.0 else ("#f59e0b" if temp_val < 49.0 else "#ef4444")
    
    st.markdown(f"""
        <div class="eco-metric-card">
            <div class="eco-metric-title">WATER OUTLET TEMP</div>
            <div class="eco-metric-value" style="color: {temp_color};">
                {temp_val:.1f}°C
            </div>
            <div class="eco-metric-sub">
                Target: <strong>30°C to 50°C</strong> ({status_label})
            </div>
        </div>
    """, unsafe_allow_html=True)

with mcol2:
    # Heat Captured in kWh
    st.markdown(f"""
        <div class="eco-metric-card">
            <div class="eco-metric-title">HEAT CAPTURED (kWh)</div>
            <div class="eco-metric-value" style="color: #38bdf8;">
                {sim_result.heat_captured_kwh_hourly:,.0f} <span style="font-size: 1.1rem; color: #94a3b8;">kWh/h</span>
            </div>
            <div class="eco-metric-sub">
                Thermal Power: <strong>{sim_result.heat_captured_kw:,.0f} kW</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

with mcol3:
    # Server IT Power Consumption
    st.markdown(f"""
        <div class="eco-metric-card">
            <div class="eco-metric-title">ACTIVE IT COMPUTE LOAD</div>
            <div class="eco-metric-value" style="color: #f8fafc;">
                {sim_result.effective_workload_pct:.0f}%
            </div>
            <div class="eco-metric-sub">
                Power Draw: <strong>{sim_result.electrical_power_kw:,.0f} kW</strong> (1,200 Nodes)
            </div>
        </div>
    """, unsafe_allow_html=True)

with mcol4:
    # Carbon emissions avoided
    st.markdown(f"""
        <div class="eco-metric-card">
            <div class="eco-metric-title">CO₂ EMISSIONS AVOIDED</div>
            <div class="eco-metric-value" style="color: #34d399;">
                {sim_result.co2_saved_hourly_kg:,.1f} <span style="font-size: 1.1rem; color: #94a3b8;">kg/h</span>
            </div>
            <div class="eco-metric-sub">
                Annual: <strong>~{sim_result.co2_saved_annual_tons:,.0f} Tons CO₂/yr</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

with mcol5:
    # Effective PUE with Heat Reuse Credit
    st.markdown(f"""
        <div class="eco-metric-card">
            <div class="eco-metric-title">ENERGY REUSE PUE</div>
            <div class="eco-metric-value" style="color: #a78bfa;">
                {sim_result.effective_pue:.2f}
            </div>
            <div class="eco-metric-sub">
                Baseline: <strong>{sim_result.baseline_pue:.2f}</strong> | ERE: <strong>{sim_result.energy_reuse_effectiveness:.2f}</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)


# ==========================================
# SYSTEM SCHEMATIC & THERMODYNAMIC CIRCUIT
# ==========================================
st.markdown(ui.render_interactive_schematic(sim_result), unsafe_allow_html=True)


# ==========================================
# HEAT DISTRIBUTION & APPLICATION DESTINATIONS
# ==========================================
st.subheader("🔥 Dynamic Heat Distribution to Applications")
st.markdown("""
Harvested liquid cooling thermal energy is routed via intelligent 3-way mixing valves to commercial greenhouses,
district hot water networks, low-temperature industrial drying, and stratified thermal storage tanks.
""")

dist_col1, dist_col2 = st.columns([1.1, 1.0])

with dist_col1:
    st.plotly_chart(ui.build_heat_distribution_chart(sim_result), use_container_width=True)

with dist_col2:
    # Individual consumer breakdown cards
    for consumer_name, kwh_val in sim_result.distribution_kwh.items():
        pct_val = sim_result.distribution_pct.get(consumer_name, 0.0)
        details = sim_result.consumer_status.get(consumer_name, {})
        
        icon = "🌱" if "Greenhouse" in consumer_name else ("🏢" if "District" in consumer_name else ("🏭" if "Industrial" in consumer_name else ("🔋" if "Buffer" in consumer_name else "🚨")))
        color = "#10b981" if "Greenhouse" in consumer_name else ("#06b6d4" if "District" in consumer_name else ("#f59e0b" if "Industrial" in consumer_name else ("#8b5cf6" if "Buffer" in consumer_name else "#ef4444")))

        st.markdown(f"""
            <div class="consumer-card" style="border-left: 4px solid {color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: {color}; font-size: 0.95rem;">{icon} {consumer_name}</strong>
                    <span style="font-weight: 700; color: #f8fafc; font-size: 1.05rem;">
                        {kwh_val:,.1f} kWh <span style="font-size: 0.8rem; color: #94a3b8;">({pct_val:.1f}%)</span>
                    </span>
                </div>
                <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">
                    {details.get('description', '')}
                </div>
                <div style="display: flex; gap: 14px; font-size: 0.75rem; color: #64748b; margin-top: 6px;">
                    <span>Delivery Temp: <strong style="color: #cbd5e1;">{details.get('current_delivery_temp', f'{sim_result.outlet_water_temp_c:.1f}°C')}</strong></span>
                    <span>Target Band: <strong style="color: #cbd5e1;">{details.get('ideal_temp_range', '30-45°C')}</strong></span>
                    <span>Offset: <strong style="color: #cbd5e1;">{details.get('offset_fuel', 'Natural Gas')}</strong></span>
                </div>
            </div>
        """, unsafe_allow_html=True)


# ==========================================
# AI STATUS LOG & SCHEDULING DECISION FEED
# ==========================================
st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
st.subheader("🧠 Thermo AI - Real-Time Smart Scheduling Status Log")
st.markdown("""
The Thermo AI dispatch engine autonomously evaluates temperature differentials, weather forecasts,
server chip thermal headroom, and consumer heating demand to orchestrate energy flow and prevent thermal runaway.
""")

log_filter_col1, log_filter_col2, log_filter_col3 = st.columns([1.5, 1.0, 1.0])

with log_filter_col1:
    log_category_filter = st.selectbox(
        "Filter Decision Stream:",
        ["All Events", "OPTIMIZATION", "DISPATCH", "SAFETY_OVERRIDE", "PREDICTIVE", "PUE_METRIC"]
    )

with log_filter_col2:
    if st.button("🔄 Step AI Scheduling Cycle", use_container_width=True):
        st.session_state.ai_scheduler.evaluate_and_log(sim_result, ai_strategy)
        st.rerun()

with log_filter_col3:
    if st.button("🗑️ Clear Log History", use_container_width=True):
        st.session_state.ai_scheduler.history = []
        st.rerun()

# Apply category filtering
filtered_logs = log_history
if log_category_filter != "All Events":
    filtered_logs = [entry for entry in log_history if entry.category == log_category_filter]

st.markdown(ui.render_log_feed(filtered_logs), unsafe_allow_html=True)


# ==========================================
# ANALYTICS & THERMODYNAMIC OPERATING ENVELOPE
# ==========================================
st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
st.subheader("📊 Engineering Analytics & Predictive Horizons")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.plotly_chart(
        ui.build_operating_curve_chart(
            current_workload=sim_result.effective_workload_pct,
            current_ambient=sim_result.ambient_temp_c,
            current_outlet=sim_result.outlet_water_temp_c
        ),
        use_container_width=True
    )

with chart_col2:
    st.plotly_chart(
        ui.build_24h_telemetry_chart(
            workload_base=sim_result.effective_workload_pct,
            ambient_base=sim_result.ambient_temp_c
        ),
        use_container_width=True
    )


# ==========================================
# MATHEMATICAL & THERMODYNAMIC MODELS FOOTER
# ==========================================
with st.expander("🔬 View Thermodynamic Equations & Computational Physics Model"):
    st.markdown(r"""
    ### Governing Thermodynamic Model:
    
    1. **Server Power Consumption Non-Linearity**:
       $$P_{IT}(W) = P_{idle} + (P_{max} - P_{idle}) \cdot \left(\frac{W}{100}\right)^{1.18}$$
       Where $P_{max} = 2,000 \text{ kW}$, $P_{idle} = 440 \text{ kW}$ (22% idle baseline).

    2. **Direct-to-Chip Thermal Heat Capture**:
       $$Q_{captured} = P_{IT} \cdot \eta_{capture}$$
       With direct-to-chip microchannel cold plates achieving $\eta_{capture} = 88\%$.

    3. **Cooling Water Outlet Temperature**:
       $$T_{water, out} = T_{water, in}(T_{ambient}) + \frac{Q_{captured}}{\dot{m} \cdot C_p}$$
       Where $\dot{m} = 22.0 \text{ kg/s}$ (active coolant circulation), and $C_p = 4.184 \text{ kJ/(kg}\cdot\text{K)}$.
       Target standard co-generation delivery band operates between **30°C and 50°C**.

    4. **Safety Override Failsafe Envelope**:
       $$\text{Trigger Condition: } T_{water, out} \ge 49.0^\circ\text{C} \quad \lor \quad T_{junction} \ge 86.0^\circ\text{C} \quad \lor \quad (W \ge 90\% \ \land \ T_{ambient} \ge 37^\circ\text{C})$$
       When triggered, Thermo AI engages:
       - Failsafe flow boost: $\dot{m}' = \dot{m} \times 1.40$
       - Workload throttling: $W' = W \times 0.75$
       - Auxiliary adiabatic dry-cooler bypass activation to safeguard server silicon.
    """)

st.caption("Eco Sync & Thermo AI © 2026 | Next-Generation Green Computing Infrastructure")
