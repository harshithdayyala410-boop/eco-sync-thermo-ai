"""
Eco Sync & Thermo AI - AI Scheduler & Decision Engine
Simulates intelligent thermal dispatching, predictive AI scheduling,
and automatic safety override interventions.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random
from simulation import SimulationResult

@dataclass
class LogEntry:
    timestamp: str
    category: str       # "OPTIMIZATION", "DISPATCH", "SAFETY_OVERRIDE", "PREDICTIVE", "PUE_METRIC"
    level: str          # "INFO", "SUCCESS", "WARNING", "CRITICAL"
    source: str         # "Thermo-AI Core", "Eco-Sync Grid", "Safety Watchdog", "Thermal-Cast"
    message: str
    metrics_summary: str = ""


class ThermoAIScheduler:
    """Intelligent scheduling and safety decision engine."""

    def __init__(self):
        self.history: List[LogEntry] = []
        self._initialize_baseline_logs()

    def _initialize_baseline_logs(self):
        """Seeds realistic historical decision logs."""
        base_time = datetime.now() - timedelta(minutes=45)
        seed_events = [
            (
                "OPTIMIZATION", "INFO", "Thermo-AI Core",
                "Initialized Direct-to-Chip closed loop liquid cooling telemetry. Model checkpoint: ThermoCast-v4.2.",
                "Loop flow: 22.0 L/s | Return baseline: 22.5°C"
            ),
            (
                "DISPATCH", "SUCCESS", "Eco-Sync Grid",
                "Connected to Urban Eco-Greenhouse primary heat exchanger. Commenced baseload hot water circulation.",
                "Target root temp: 21.0°C | Valve: 35% open"
            ),
            (
                "PREDICTIVE", "INFO", "Thermal-Cast",
                "Ingested 6-hour meteorological forecast. Projected night ambient drop to 8.4°C. Preparing buffer pre-charge.",
                "Anticipated DHW spike: 06:30 - 08:30"
            ),
            (
                "PUE_METRIC", "SUCCESS", "Thermo-AI Core",
                "Facility PUE reduced from 1.38 to 1.12 via direct waste-heat repurposing across 3 municipal consumers.",
                "Avoided natural gas: 340 m³/day equivalent"
            ),
            (
                "DISPATCH", "INFO", "Eco-Sync Grid",
                "District heating demand surge detected (+18%). Diverted secondary manifold output to Municipal DHW preheaters.",
                "Heat delivery: 42.4°C @ 480 kWh"
            )
        ]

        for i, (cat, lvl, src, msg, met) in enumerate(seed_events):
            t_str = (base_time + timedelta(minutes=i * 9)).strftime("%H:%M:%S")
            self.history.append(LogEntry(
                timestamp=t_str,
                category=cat,
                level=lvl,
                source=src,
                message=msg,
                metrics_summary=met
            ))

    def evaluate_and_log(self, sim: SimulationResult, user_mode: str = "Eco-Max") -> List[LogEntry]:
        """
        Analyzes current real-time state and generates smart AI decisions.
        Returns the updated log history (most recent first).
        """
        now_str = datetime.now().strftime("%H:%M:%S")
        new_entries = []

        # 1. Critical Safety Override Check
        if sim.safety_override_active:
            override_msg = (
                f"CRITICAL SAFETY OVERRIDE TRIGGERED: {sim.override_reason}. "
                f"Autonomous failsafe mitigation activated: Boosted coolant flow to {sim.cooling_flow_rate_active:.1f} L/s, "
                f"throttled compute cluster to {sim.effective_workload_pct:.0f}%, opened emergency dry-cooler dump."
            )
            new_entries.append(LogEntry(
                timestamp=now_str,
                category="SAFETY_OVERRIDE",
                level="CRITICAL",
                source="Safety Watchdog",
                message=override_msg,
                metrics_summary=f"Outlet: {sim.outlet_water_temp_c:.1f}°C | Server Tj: {sim.estimated_junction_temp_c:.1f}°C | Emergency Dump: {sim.distribution_kwh.get('Emergency Dry Cooler / Dump', 0):.0f} kWh"
            ))
            
            # Additional emergency dispatch log
            new_entries.append(LogEntry(
                timestamp=now_str,
                category="DISPATCH",
                level="WARNING",
                source="Eco-Sync Grid",
                message="Diverted 45% thermal flux to Auxiliary Adiabatic Dry-Cooler bypass to protect GPU silicon integrity.",
                metrics_summary=f"Dump Active: {sim.distribution_kwh.get('Emergency Dry Cooler / Dump', 0):.0f} kWh"
            ))

        elif sim.safety_status == "CAUTION":
            caution_msg = (
                f"Thermal caution advisory: High thermal density detected. "
                f"Thermo AI initiated proactive flow adjustment (+15%) and prioritizing stratified buffer charging."
            )
            new_entries.append(LogEntry(
                timestamp=now_str,
                category="SAFETY_OVERRIDE",
                level="WARNING",
                source="Safety Watchdog",
                message=caution_msg,
                metrics_summary=f"Outlet: {sim.outlet_water_temp_c:.1f}°C | Flow: {sim.cooling_flow_rate_active:.1f} L/s"
            ))

        # 2. Smart Scheduling Decision based on Workload & Ambient Temp (Only when not in full override)
        if not sim.safety_override_active:
            if sim.ambient_temp_c < 5.0:
                decision_msg = (
                    f"Cold ambient condition ({sim.ambient_temp_c:.1f}°C). "
                    f"Thermo AI redirected {sim.distribution_pct.get('Urban Eco-Greenhouse', 0)}% of harvested heat ({sim.distribution_kwh.get('Urban Eco-Greenhouse', 0):.0f} kWh) "
                    f"to Urban Eco-Greenhouse frost-protection circuits, preventing auxiliary boiler firing."
                )
                new_entries.append(LogEntry(
                    timestamp=now_str,
                    category="DISPATCH",
                    level="SUCCESS",
                    source="Eco-Sync Grid",
                    message=decision_msg,
                    metrics_summary=f"Delivered Temp: {sim.outlet_water_temp_c:.1f}°C | Greenhouse Target: 21°C"
                ))
            elif sim.ambient_temp_c > 30.0:
                decision_msg = (
                    f"Warm climate regime ({sim.ambient_temp_c:.1f}°C). Greenhouse thermal load low. "
                    f"Diverting {sim.distribution_pct.get('District / Building Hot Water', 0)}% to District DHW pre-heaters "
                    f"and {sim.distribution_pct.get('Thermal Buffer Storage (TES)', 0)}% to stratified storage."
                )
                new_entries.append(LogEntry(
                    timestamp=now_str,
                    category="OPTIMIZATION",
                    level="INFO",
                    source="Thermo-AI Core",
                    message=decision_msg,
                    metrics_summary=f"Buffer Input: {sim.distribution_kwh.get('Thermal Buffer Storage (TES)', 0):.0f} kWh"
                ))
            else:
                # Balanced condition
                decision_msg = (
                    f"Optimal balanced co-generation mode ({user_mode}). "
                    f"Captured {sim.heat_captured_kwh_hourly:.0f} kWh/h of waste heat. "
                    f"Evenly distributed across municipal hot water ({sim.distribution_pct.get('District / Building Hot Water', 0)}%) "
                    f"and eco-greenhouses ({sim.distribution_pct.get('Urban Eco-Greenhouse', 0)}%)."
                )
                new_entries.append(LogEntry(
                    timestamp=now_str,
                    category="DISPATCH",
                    level="INFO",
                    source="Eco-Sync Grid",
                    message=decision_msg,
                    metrics_summary=f"PUE: {sim.effective_pue:.2f} (from baseline {sim.baseline_pue:.2f})"
                ))

            # 3. Workload Optimization / AI Batch Scheduling
            if sim.workload_pct > 80.0:
                opt_msg = (
                    f"High AI compute density ({sim.workload_pct:.0f}% load). "
                    f"Coordinating distributed LLM training jobs with thermal recovery buffer capacity. "
                    f"Carbon avoidance running at {sim.co2_saved_hourly_kg:.1f} kg CO₂/hr."
                )
                new_entries.append(LogEntry(
                    timestamp=now_str,
                    category="OPTIMIZATION",
                    level="SUCCESS",
                    source="Thermo-AI Core",
                    message=opt_msg,
                    metrics_summary=f"Thermal Power: {sim.heat_captured_kw:.0f} kW | Avoided Gas: {sim.co2_saved_hourly_kg/0.2:.1f} kWh-eq"
                ))
            elif sim.workload_pct < 30.0:
                low_msg = (
                    f"Low compute load ({sim.workload_pct:.0f}%). Thermo AI maintaining minimal circulation "
                    f"flow to sustain 30°C return water threshold. Drawing supplementary heat from TES buffer if required."
                )
                new_entries.append(LogEntry(
                    timestamp=now_str,
                    category="PREDICTIVE",
                    level="INFO",
                    source="Thermal-Cast",
                    message=low_msg,
                    metrics_summary=f"Outlet Water: {sim.outlet_water_temp_c:.1f}°C (Threshold >= 30.0°C)"
                ))

        # Add new entries to head of history, avoiding duplicate spam
        for entry in reversed(new_entries):
            # Check if identical to last entry message
            if not self.history or self.history[0].message != entry.message:
                self.history.insert(0, entry)

        # Cap history to 60 items
        if len(self.history) > 60:
            self.history = self.history[:60]

        return self.history
