"""
Eco Sync & Thermo AI - UI Components, Schematics, and Plotly Visualizations
Provides custom styles, interactive diagrams, and dynamic charts for Streamlit.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
from simulation import SimulationResult
from ai_scheduler import LogEntry

def get_custom_css() -> str:
    """Returns responsive CSS for modern eco-tech theme."""
    return """
    <style>
        /* Import clean font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

        /* Root styling variables */
        :root {
            --primary-eco: #10b981;
            --primary-glow: rgba(16, 185, 129, 0.25);
            --secondary-cyan: #06b6d4;
            --warning-amber: #f59e0b;
            --danger-red: #ef4444;
            --dark-card: #131d24;
            --dark-border: #1e2e38;
            --text-muted: #94a3b8;
        }

        /* Top header card */
        .main-hero-banner {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 182, 212, 0.08) 50%, rgba(19, 29, 36, 0.6) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 14px;
            padding: 22px 28px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
        }

        .hero-title {
            font-size: 2.1rem;
            font-weight: 700;
            background: linear-gradient(90deg, #10b981, #38bdf8, #a7f3d0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }

        .hero-subtitle {
            color: #94a3b8;
            font-size: 1.02rem;
            margin-bottom: 0px;
        }

        /* KPI Metric Card */
        .eco-metric-card {
            background: #131d24;
            border: 1px solid #1e2e38;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }

        .eco-metric-card:hover {
            border-color: rgba(16, 185, 129, 0.5);
            transform: translateY(-2px);
        }

        .eco-metric-title {
            color: #94a3b8;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
            margin-bottom: 6px;
        }

        .eco-metric-value {
            font-size: 1.85rem;
            font-weight: 700;
            color: #f8fafc;
            line-height: 1.2;
            font-family: 'Inter', sans-serif;
        }

        .eco-metric-sub {
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 6px;
        }

        /* Safety Override Alerts */
        .alert-box-critical {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.22) 0%, rgba(185, 28, 28, 0.15) 100%);
            border: 2px solid #ef4444;
            border-radius: 12px;
            padding: 18px 24px;
            margin-bottom: 22px;
            animation: pulse-danger 2.2s infinite;
        }

        @keyframes pulse-danger {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 14px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }

        .alert-box-caution {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(217, 119, 6, 0.12) 100%);
            border: 1.5px solid #f59e0b;
            border-radius: 12px;
            padding: 16px 22px;
            margin-bottom: 20px;
        }

        .alert-box-normal {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(5, 150, 105, 0.08) 100%);
            border: 1px solid rgba(16, 185, 129, 0.4);
            border-radius: 12px;
            padding: 14px 20px;
            margin-bottom: 20px;
        }

        /* AI Log Feed Styling */
        .log-container {
            background: #0b1115;
            border: 1px solid #1a2730;
            border-radius: 10px;
            padding: 12px;
            max-height: 420px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.83rem;
        }

        .log-entry-row {
            padding: 8px 10px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            line-height: 1.45;
        }

        .log-badge {
            display: inline-block;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-right: 8px;
        }

        .badge-CRITICAL { background: #ef4444; color: #fff; }
        .badge-WARNING  { background: #f59e0b; color: #000; }
        .badge-SUCCESS  { background: #10b981; color: #fff; }
        .badge-INFO     { background: #0284c7; color: #fff; }

        /* Consumer card */
        .consumer-card {
            background: #131d24;
            border: 1px solid #1e2e38;
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 12px;
        }
    </style>
    """

def render_safety_banner(sim: SimulationResult) -> str:
    """Generates the HTML markup for the safety alert banner."""
    if sim.safety_override_active:
        mitigations_html = "".join([f"<li><strong>{m}</strong></li>" for m in sim.mitigation_actions])
        return f"""
        <div class="alert-box-critical">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.8rem;">🚨</span>
                    <div>
                        <h3 style="color: #f87171; margin: 0; font-size: 1.3rem; font-weight: 700;">
                            CRITICAL SAFETY OVERRIDE ACTIVE
                        </h3>
                        <p style="color: #fca5a5; margin: 2px 0 0 0; font-size: 0.92rem;">
                            {sim.override_reason}
                        </p>
                    </div>
                </div>
                <div style="text-align: right; background: rgba(0,0,0,0.3); padding: 8px 14px; border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.4);">
                    <div style="color: #94a3b8; font-size: 0.75rem;">OUTLET WATER TEMP</div>
                    <div style="color: #ef4444; font-size: 1.5rem; font-weight: 800;">{sim.outlet_water_temp_c:.1f}°C</div>
                    <div style="color: #f87171; font-size: 0.72rem;">SAFE LIMIT: ≤49.0°C</div>
                </div>
            </div>
            <div style="background: rgba(0,0,0,0.25); border-radius: 8px; padding: 10px 14px; margin-top: 10px;">
                <div style="color: #fca5a5; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;">
                    ⚡ AUTONOMOUS THERMO-AI INTERVENTIONS ENGAGED:
                </div>
                <ul style="color: #f8fafc; font-size: 0.85rem; margin: 0 0 0 18px; padding: 0;">
                    {mitigations_html}
                </ul>
            </div>
        </div>
        """
    elif sim.safety_status == "CAUTION":
        return f"""
        <div class="alert-box-caution">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.6rem;">⚠️</span>
                    <div>
                        <h4 style="color: #fbbf24; margin: 0; font-size: 1.15rem; font-weight: 700;">
                            THERMAL CAUTION LEVEL ELEVATED
                        </h4>
                        <p style="color: #fde68a; margin: 2px 0 0 0; font-size: 0.9rem;">
                            {sim.override_reason}
                        </p>
                    </div>
                </div>
                <div style="text-align: right; background: rgba(0,0,0,0.25); padding: 6px 12px; border-radius: 8px;">
                    <span style="color: #f59e0b; font-weight: 700;">Outlet: {sim.outlet_water_temp_c:.1f}°C</span>
                </div>
            </div>
        </div>
        """
    else:
        return f"""
        <div class="alert-box-normal">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.3rem;">✅</span>
                    <div>
                        <span style="color: #34d399; font-weight: 700; font-size: 1.05rem;">
                            THERMAL LOOP OPERATING NOMINALLY
                        </span>
                        <span style="color: #94a3b8; font-size: 0.88rem; margin-left: 10px;">
                            Water Outlet: <strong style="color: #10b981;">{sim.outlet_water_temp_c:.1f}°C</strong> (Operating Band: 30°C to 50°C) | Flow: {sim.cooling_flow_rate_active:.1f} L/s
                        </span>
                    </div>
                </div>
                <div style="background: rgba(16,185,129,0.15); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(16,185,129,0.3);">
                    <span style="color: #6ee7b7; font-size: 0.8rem; font-weight: 600;">ECO SYNC: ACTIVE</span>
                </div>
            </div>
        </div>
        """

def render_interactive_schematic(sim: SimulationResult) -> str:
    """
    Renders an SVG and HTML schematic of the complete data center waste heat recovery system.
    Shows the server racks, liquid cooling loop, heat exchanger, and the distribution paths.
    """
    # Color logic for temperatures
    outlet_c = sim.outlet_water_temp_c
    if outlet_c >= 49.0:
        water_color = "#ef4444"
        pipe_glow = "rgba(239, 68, 68, 0.6)"
    elif outlet_c >= 44.0:
        water_color = "#f59e0b"
        pipe_glow = "rgba(245, 158, 11, 0.5)"
    elif outlet_c >= 38.0:
        water_color = "#10b981"
        pipe_glow = "rgba(16, 185, 129, 0.4)"
    else:
        water_color = "#38bdf8"
        pipe_glow = "rgba(56, 189, 248, 0.4)"

    gh_kwh = sim.distribution_kwh.get("Urban Eco-Greenhouse", 0)
    dhw_kwh = sim.distribution_kwh.get("District / Building Hot Water", 0)
    ind_kwh = sim.distribution_kwh.get("Industrial Low-Temp Drying", 0)
    tes_kwh = sim.distribution_kwh.get("Thermal Buffer Storage (TES)", 0)

    return f"""
    <div style="background: #0f171d; border: 1px solid #1e2e38; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div style="font-weight: 700; color: #f8fafc; font-size: 1.05rem; display: flex; align-items: center; gap: 8px;">
                <span>🔄</span> Live System Flow & Thermodynamic Circuit
            </div>
            <div style="display: flex; gap: 14px; font-size: 0.8rem; color: #94a3b8;">
                <span>Inlet Coolant: <strong style="color: #38bdf8;">{sim.inlet_water_temp_c:.1f}°C</strong></span>
                <span>Outlet Return: <strong style="color: {water_color};">{sim.outlet_water_temp_c:.1f}°C</strong></span>
                <span>Harvested: <strong style="color: #10b981;">{sim.heat_captured_kw:.0f} kW</strong></span>
            </div>
        </div>
        
        <svg viewBox="0 0 940 330" style="width: 100%; height: auto; font-family: Inter, sans-serif;">
            <defs>
                <linearGradient id="pipeHotGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#38bdf8" />
                    <stop offset="35%" stop-color="{water_color}" />
                    <stop offset="100%" stop-color="{water_color}" />
                </linearGradient>
                <linearGradient id="serverGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#1e293b" />
                    <stop offset="100%" stop-color="#0f172a" />
                </linearGradient>
                <filter id="glowEffect" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>

            <!-- 1. Data Center Block -->
            <rect x="20" y="55" width="200" height="210" rx="10" fill="url(#serverGrad)" stroke="#334155" stroke-width="2" />
            <rect x="35" y="70" width="170" height="24" rx="4" fill="#1e2e38" />
            <text x="120" y="86" fill="#38bdf8" font-size="11" font-weight="700" text-anchor="middle">DATA CENTRE CLUSTER</text>
            <text x="120" y="108" fill="#94a3b8" font-size="10" text-anchor="middle">1,200 High-Density GPU Nodes</text>

            <!-- Server Racks representation -->
            <rect x="40" y="120" width="35" height="120" rx="3" fill="#0b1115" stroke="#475569" stroke-width="1" />
            <rect x="85" y="120" width="35" height="120" rx="3" fill="#0b1115" stroke="#475569" stroke-width="1" />
            <rect x="130" y="120" width="35" height="120" rx="3" fill="#0b1115" stroke="#475569" stroke-width="1" />
            <rect x="175" y="120" width="35" height="120" rx="3" fill="#0b1115" stroke="#475569" stroke-width="1" />

            <!-- Blinking LED lights -->
            <circle cx="58" cy="132" r="2.5" fill="#10b981" />
            <circle cx="103" cy="132" r="2.5" fill="#10b981" />
            <circle cx="148" cy="132" r="2.5" fill="#10b981" />
            <circle cx="193" cy="132" r="2.5" fill="{water_color}" />

            <text x="120" y="258" fill="#e2e8f0" font-size="11" font-weight="600" text-anchor="middle">
                IT Load: {sim.effective_workload_pct:.0f}% ({sim.electrical_power_kw:.0f} kW)
            </text>

            <!-- 2. Coolant Loop Pipes -->
            <!-- Chilled Supply pipe (bottom) -->
            <path d="M 400 240 L 220 240" fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" />
            <polygon points="300,235 315,240 300,245" fill="#38bdf8" />
            <text x="310" y="260" fill="#38bdf8" font-size="10" font-weight="600" text-anchor="middle">
                Supply Return: {sim.inlet_water_temp_c:.1f}°C
            </text>

            <!-- Hot Return pipe (top) -->
            <path d="M 220 150 L 400 150" fill="none" stroke="{water_color}" stroke-width="7" stroke-linecap="round" filter="url(#glowEffect)" />
            <polygon points="320,144 335,150 320,156" fill="{water_color}" />
            <text x="310" y="138" fill="{water_color}" font-size="11" font-weight="700" text-anchor="middle">
                Hot Water: {sim.outlet_water_temp_c:.1f}°C ({sim.heat_captured_kw:.0f} kW)
            </text>

            <!-- 3. Thermo AI Heat Exchanger & Valving Unit -->
            <rect x="400" y="115" width="130" height="150" rx="10" fill="#1e293b" stroke="#06b6d4" stroke-width="2" />
            <rect x="415" y="128" width="100" height="22" rx="4" fill="#0f172a" />
            <text x="465" y="143" fill="#38bdf8" font-size="10" font-weight="700" text-anchor="middle">THERMO-AI UNIT</text>
            <text x="465" y="165" fill="#94a3b8" font-size="9" text-anchor="middle">Plate Heat Exchanger</text>
            <text x="465" y="180" fill="#10b981" font-size="10" font-weight="700" text-anchor="middle">
                η = 88% Capture
            </text>
            <!-- 3-Way Smart Valving icon -->
            <circle cx="465" cy="210" r="14" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5" />
            <text x="465" y="214" fill="#f59e0b" font-size="9" font-weight="700" text-anchor="middle">VALVE</text>
            <text x="465" y="246" fill="#94a3b8" font-size="9" text-anchor="middle">Flow: {sim.cooling_flow_rate_active:.1f} L/s</text>

            <!-- Distribution branch lines -->
            <!-- To Greenhouse -->
            <path d="M 530 140 L 670 70" fill="none" stroke="{water_color}" stroke-width="4" stroke-dasharray="6,3" />
            <!-- To District Hot Water -->
            <path d="M 530 160 L 670 140" fill="none" stroke="{water_color}" stroke-width="5" />
            <!-- To Industrial Drying -->
            <path d="M 530 200 L 670 210" fill="none" stroke="{water_color}" stroke-width="4" stroke-dasharray="6,3" />
            <!-- To Thermal Storage Buffer -->
            <path d="M 530 230 L 670 280" fill="none" stroke="{water_color}" stroke-width="4" stroke-dasharray="4,4" />

            <!-- 4. Consumers Blocks -->
            <!-- Urban Eco-Greenhouse -->
            <g transform="translate(670, 45)">
                <rect x="0" y="0" width="245" height="56" rx="8" fill="#131d24" stroke="#10b981" stroke-width="1.5" />
                <text x="12" y="22" font-size="12" fill="#10b981" font-weight="700">🌱 Urban Eco-Greenhouse</text>
                <text x="12" y="38" font-size="10" fill="#94a3b8">Hydronic Soil & Canopy Heating</text>
                <text x="235" y="30" font-size="13" fill="#f8fafc" font-weight="700" text-anchor="end">{gh_kwh:.0f} kWh ({sim.distribution_pct.get('Urban Eco-Greenhouse', 0)}%)</text>
            </g>

            <!-- District / Building Hot Water -->
            <g transform="translate(670, 115)">
                <rect x="0" y="0" width="245" height="56" rx="8" fill="#131d24" stroke="#06b6d4" stroke-width="1.5" />
                <text x="12" y="22" font-size="12" fill="#06b6d4" font-weight="700">🏢 District Hot Water (DHW)</text>
                <text x="12" y="38" font-size="10" fill="#94a3b8">1,800 Homes & Campus Heating</text>
                <text x="235" y="30" font-size="13" fill="#f8fafc" font-weight="700" text-anchor="end">{dhw_kwh:.0f} kWh ({sim.distribution_pct.get('District / Building Hot Water', 0)}%)</text>
            </g>

            <!-- Industrial Low-Temp Drying -->
            <g transform="translate(670, 185)">
                <rect x="0" y="0" width="245" height="56" rx="8" fill="#131d24" stroke="#f59e0b" stroke-width="1.5" />
                <text x="12" y="22" font-size="12" fill="#f59e0b" font-weight="700">🏭 Industrial Drying Tunnels</text>
                <text x="12" y="38" font-size="10" fill="#94a3b8">Biomass, Timber & Algae</text>
                <text x="235" y="30" font-size="13" fill="#f8fafc" font-weight="700" text-anchor="end">{ind_kwh:.0f} kWh ({sim.distribution_pct.get('Industrial Low-Temp Drying', 0)}%)</text>
            </g>

            <!-- Thermal Energy Storage Buffer -->
            <g transform="translate(670, 255)">
                <rect x="0" y="0" width="245" height="56" rx="8" fill="#131d24" stroke="#8b5cf6" stroke-width="1.5" />
                <text x="12" y="22" font-size="12" fill="#a78bfa" font-weight="700">🔋 Stratified Thermal Storage (TES)</text>
                <text x="12" y="38" font-size="10" fill="#94a3b8">15 MWh Thermocline Buffer</text>
                <text x="235" y="30" font-size="13" fill="#f8fafc" font-weight="700" text-anchor="end">{tes_kwh:.0f} kWh ({sim.distribution_pct.get('Thermal Buffer Storage (TES)', 0)}%)</text>
            </g>
        </svg>
    </div>
    """

def render_log_feed(logs: List[LogEntry]) -> str:
    """Renders the AI decision logs into an interactive stream format."""
    rows = []
    for entry in logs:
        badge_cls = f"badge-{entry.level}"
        meta = f"<div style='color: #64748b; font-size: 0.73rem; margin-top: 3px;'>📊 {entry.metrics_summary}</div>" if entry.metrics_summary else ""
        rows.append(f"""
        <div class="log-entry-row">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <div>
                    <span class="log-badge {badge_cls}">{entry.category}</span>
                    <span style="color: #38bdf8; font-weight: 600; margin-right: 6px;">[{entry.source}]</span>
                    <span style="color: #e2e8f0;">{entry.message}</span>
                </div>
                <span style="color: #64748b; font-size: 0.72rem; white-space: nowrap; margin-left: 10px;">{entry.timestamp}</span>
            </div>
            {meta}
        </div>
        """)
    return f"""
    <div class="log-container">
        {''.join(rows)}
    </div>
    """

def build_heat_distribution_chart(sim: SimulationResult) -> go.Figure:
    """Builds an interactive Donut chart showing thermal energy allocation."""
    labels = list(sim.distribution_kwh.keys())
    values = list(sim.distribution_kwh.values())

    color_map = {
        "Urban Eco-Greenhouse": "#10b981",
        "District / Building Hot Water": "#06b6d4",
        "Industrial Low-Temp Drying": "#f59e0b",
        "Thermal Buffer Storage (TES)": "#8b5cf6",
        "Emergency Dry Cooler / Dump": "#ef4444"
    }
    colors = [color_map.get(label, "#94a3b8") for label in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        textinfo="label+percent",
        marker=dict(colors=colors, line=dict(color="#0f171d", width=2)),
        hovertemplate="<b>%{label}</b><br>Thermal Power: %{value:.1f} kWh<br>Share: %{percent}<extra></extra>"
    )])

    fig.update_layout(
        title=dict(text="Real-Time Thermal Allocation Breakdown", font=dict(color="#f8fafc", size=14)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=280,
        showlegend=False,
        annotations=[dict(
            text=f"<b>{sim.heat_captured_kw:.0f}</b><br><span style='font-size:11px;color:#94a3b8;'>Total kWh</span>",
            x=0.5, y=0.5, font_size=16, font_color="#f8fafc", showarrow=False
        )]
    )
    return fig

def build_operating_curve_chart(current_workload: float, current_ambient: float, 
                                current_outlet: float) -> go.Figure:
    """
    Renders an operating envelope curve showing Outlet Water Temperature vs Server Workload
    under 3 ambient temperature regimes (-5°C, 20°C, 35°C), highlighting the safe 30-50°C band.
    """
    workloads = list(range(0, 105, 5))
    
    # Calculate temp curves for 3 ambient scenarios
    def temp_calc(w, amb):
        p_idle = 2000.0 * 0.22
        power = p_idle + (2000.0 - p_idle) * ((w / 100.0) ** 1.18)
        inlet = 22.0 + 0.22 * max(0.0, amb - 16.0) - 0.08 * max(0.0, 16.0 - amb)
        delta_t = (power * 0.88) / (22.0 * 4.184)
        return round(inlet + delta_t, 1)

    cold_curve = [temp_calc(w, -5.0) for w in workloads]
    mild_curve = [temp_calc(w, 20.0) for w in workloads]
    hot_curve  = [temp_calc(w, 35.0) for w in workloads]

    fig = go.Figure()

    # Safe operating zone (30°C to 50°C)
    fig.add_hrect(
        y0=30, y1=49, fillcolor="#10b981", opacity=0.08,
        line_width=0, annotation_text="Standard Recovery Operating Band (30°C - 50°C)",
        annotation_position="inside top left", annotation_font_color="#6ee7b7", annotation_font_size=10
    )

    # Danger zone (above 49°C)
    fig.add_hrect(
        y0=49, y1=56, fillcolor="#ef4444", opacity=0.12,
        line_width=1, line_dash="dash", line_color="#ef4444",
        annotation_text="Critical Thermal Override Threshold (≥49°C)",
        annotation_position="inside top right", annotation_font_color="#f87171", annotation_font_size=10
    )

    fig.add_trace(go.Scatter(
        x=workloads, y=cold_curve, mode="lines", name="Cold Ambient (-5°C)",
        line=dict(color="#38bdf8", width=2, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=workloads, y=mild_curve, mode="lines", name="Mild Ambient (20°C)",
        line=dict(color="#10b981", width=2)
    ))
    fig.add_trace(go.Scatter(
        x=workloads, y=hot_curve, mode="lines", name="Hot Ambient (35°C)",
        line=dict(color="#f59e0b", width=2, dash="dash")
    ))

    # Current Operating Point
    fig.add_trace(go.Scatter(
        x=[current_workload], y=[current_outlet],
        mode="markers+text",
        name="Current Operating Point",
        text=[f"Current: {current_outlet:.1f}°C"],
        textposition="top center",
        marker=dict(size=14, color="#ef4444" if current_outlet >= 49.0 else "#10b981",
                    line=dict(color="#ffffff", width=2))
    ))

    fig.update_layout(
        title=dict(text="Outlet Water Temperature Response vs Server Workload", font=dict(color="#f8fafc", size=14)),
        xaxis=dict(title="Server Workload / AI Traffic (%)", range=[0, 100], gridcolor="#1e2e38", zeroline=False),
        yaxis=dict(title="Water Temperature (°C)", range=[24, 56], gridcolor="#1e2e38", zeroline=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_24h_telemetry_chart(workload_base: float, ambient_base: float) -> go.Figure:
    """Generates a 24-hour simulation profile showing dynamic co-generation."""
    hours = [f"{h:02d}:00" for h in range(24)]
    
    # Simulate realistic diurnal curve
    workload_profile = []
    temp_profile = []
    captured_profile = []

    for h in range(24):
        # Workload peaks during afternoon inference & overnight AI training batch
        w_factor = 0.85 + 0.18 * ((1.0 if (2 <= h <= 6 or 13 <= h <= 17) else 0.7) - 0.7)
        w = max(15.0, min(100.0, workload_base * w_factor))
        workload_profile.append(round(w, 1))

        # Ambient follows solar cycle
        amb = ambient_base + 6.0 * (1.0 if (12 <= h <= 16) else (-1.0 if (1 <= h <= 5) else 0.0))
        temp_profile.append(round(amb, 1))

        # Heat captured in kWh
        heat_kwh = (2000.0 * 0.22 + (2000.0 - 440.0) * ((w / 100.0) ** 1.18)) * 0.88
        captured_profile.append(round(heat_kwh, 1))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=hours, y=captured_profile, name="Waste Heat Harvested (kWh)",
        marker_color="#10b981", opacity=0.75
    ))
    fig.add_trace(go.Scatter(
        x=hours, y=workload_profile, name="AI Workload Traffic (%)",
        yaxis="y2", line=dict(color="#38bdf8", width=2.5)
    ))

    fig.update_layout(
        title=dict(text="24-Hour Predictive Heat Harvesting & Workload Forecast", font=dict(color="#f8fafc", size=14)),
        xaxis=dict(gridcolor="#1e2e38"),
        yaxis=dict(title="Thermal Energy (kWh)", gridcolor="#1e2e38"),
        yaxis2=dict(title="AI Traffic (%)", overlaying="y", side="right", range=[0, 110], showgrid=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=280,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig
