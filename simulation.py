"""
Eco Sync & Thermo AI - Core Simulation Engine
Models data center thermodynamics, direct-to-chip liquid cooling,
waste-heat recovery, and thermal distribution networks.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple
import math

@dataclass
class FacilityConfig:
    """Configurable specifications for the data centre facility."""
    nominal_it_power_kw: float = 2000.0  # 2.0 MW IT load at 100% capacity
    server_count: int = 1200             # High-density GPU/CPU server nodes
    idle_power_ratio: float = 0.22       # Baseline power draw at 0% workload
    heat_capture_efficiency: float = 0.88 # 88% recovered directly into liquid coolant loop
    coolant_flow_rate_lps: float = 22.0  # Coolant mass flow rate in Liters/second (kg/s)
    base_coolant_inlet_c: float = 22.0   # Baseline chilled/return coolant temperature
    specific_heat_water: float = 4.184   # kJ / (kg * K)
    co2_kg_per_kwh_thermal: float = 0.202 # kg CO2 saved per kWh heat replacing gas boilers
    heating_cost_per_kwh: float = 0.085  # USD savings per recovered thermal kWh


@dataclass
class SimulationResult:
    """Encapsulates all computed physical, operational, and ecological metrics."""
    # Inputs
    workload_pct: float
    ambient_temp_c: float
    effective_workload_pct: float
    
    # Power & Thermal generation
    electrical_power_kw: float
    heat_generated_kw: float
    heat_captured_kw: float
    heat_captured_kwh_hourly: float
    heat_captured_daily_proj_kwh: float
    
    # Temperatures
    inlet_water_temp_c: float
    outlet_water_temp_c: float
    delta_t_c: float
    estimated_junction_temp_c: float
    
    # Safety assessment
    safety_status: str  # "NORMAL", "CAUTION", "CRITICAL_OVERRIDE"
    safety_override_active: bool
    override_reason: str
    mitigation_actions: List[str]
    
    # Heat distribution (kWh and percentages)
    distribution_pct: Dict[str, float]
    distribution_kwh: Dict[str, float]
    consumer_status: Dict[str, Dict[str, Any]]
    
    # Ecological & Economic impacts
    co2_saved_hourly_kg: float
    co2_saved_annual_tons: float
    financial_savings_hourly: float
    baseline_pue: float
    effective_pue: float
    energy_reuse_effectiveness: float
    cooling_flow_rate_active: float


class ThermoSimulationEngine:
    """Thermodynamic simulation engine for data centre waste heat harvesting."""

    def __init__(self, config: FacilityConfig = None):
        self.config = config or FacilityConfig()
        # Storage buffer state (0 - 100% full, capacity in kWh)
        self.buffer_capacity_kwh = 15000.0  # 15 MWh thermal energy storage (TES)
        self.buffer_state_of_charge_pct = 42.0

    def compute(self, workload_pct: float, ambient_temp_c: float, 
                manual_safety_override: bool = False,
                user_flow_multiplier: float = 1.0) -> SimulationResult:
        """
        Executes a real-time thermodynamic cycle calculation.
        """
        # Clamp bounds
        workload_pct = max(0.0, min(100.0, float(workload_pct)))
        ambient_temp_c = max(-20.0, min(50.0, float(ambient_temp_c)))

        cfg = self.config

        # 1. First-pass temperature estimate to check safety triggers
        # Non-linear workload to power model: P = P_idle + (P_max - P_idle) * (W/100)^1.18
        p_idle = cfg.nominal_it_power_kw * cfg.idle_power_ratio
        raw_power_kw = p_idle + (cfg.nominal_it_power_kw - p_idle) * math.pow(workload_pct / 100.0, 1.18)

        # Baseline Inlet water temperature: affected slightly by outdoor temperature
        # Cool ambient allows sub-cooling, hot ambient increases inlet minimum
        ambient_inlet_influence = 0.22 * max(0.0, ambient_temp_c - 16.0) - 0.08 * max(0.0, 16.0 - ambient_temp_c)
        inlet_temp = cfg.base_coolant_inlet_c + ambient_inlet_influence
        inlet_temp = max(18.0, min(33.0, inlet_temp))

        # Direct-to-Chip heat capture
        pre_override_heat_captured_kw = raw_power_kw * cfg.heat_capture_efficiency
        
        # Base flow rate
        base_flow = cfg.coolant_flow_rate_lps * user_flow_multiplier
        
        # Delta T = Q / (m_dot * Cp)
        raw_delta_t = pre_override_heat_captured_kw / (base_flow * cfg.specific_heat_water)
        raw_outlet_temp = inlet_temp + raw_delta_t
        raw_junction_temp = raw_outlet_temp + 14.0 + (workload_pct / 100.0) * 16.0

        # 2. Safety Override Logic Assessment
        # Thresholds:
        # - Warning: Outlet >= 44.0°C or Junction >= 76.0°C
        # - Critical: Outlet >= 49.0°C or Junction >= 86.0°C or (Workload >= 90% and Ambient >= 37°C)
        safety_status = "NORMAL"
        safety_override_active = False
        override_reason = ""
        mitigations = []
        effective_workload = workload_pct
        active_flow_rate = base_flow

        is_critical = (
            raw_outlet_temp >= 49.0 or 
            raw_junction_temp >= 86.0 or 
            (workload_pct >= 90.0 and ambient_temp_c >= 37.0) or
            manual_safety_override
        )
        is_caution = (
            raw_outlet_temp >= 44.0 or 
            raw_junction_temp >= 76.0 or 
            (workload_pct >= 82.0 and ambient_temp_c >= 32.0)
        )

        if is_critical:
            safety_status = "CRITICAL_OVERRIDE"
            safety_override_active = True
            
            reasons = []
            if raw_outlet_temp >= 49.0:
                reasons.append(f"Coolant outlet temp ({raw_outlet_temp:.1f}°C) exceeded critical limit (49.0°C)")
            if raw_junction_temp >= 86.0:
                reasons.append(f"Estimated server chip junction temp ({raw_junction_temp:.1f}°C) reached thermal ceiling (86.0°C)")
            if workload_pct >= 90.0 and ambient_temp_c >= 37.0:
                reasons.append(f"Hostile ambient conditions ({ambient_temp_c:.1f}°C) coupled with critical AI traffic ({workload_pct:.0f}%)")
            if manual_safety_override:
                reasons.append("Manual operator emergency safety override activated")
                
            override_reason = " | ".join(reasons) if reasons else "Critical thermal protection protocol engaged"

            # Autonomous AI Mitigations:
            # a) Flow boost (+40%)
            active_flow_rate = base_flow * 1.40
            mitigations.append("Activated Secondary Emergency Boost Pump (+40% coolant circulation flow)")
            
            # b) Workload throttle (-25% batch shedding to protect hardware)
            effective_workload = max(40.0, workload_pct * 0.75)
            mitigations.append(f"Thermo AI auto-throttled low-priority batch training from {workload_pct:.0f}% to {effective_workload:.0f}%")
            
            # c) Auxiliary dry cooler bypass
            mitigations.append("Opened Auxiliary Adiabatic Dry-Cooler bypass loop for rapid thermal dissipation")

        elif is_caution:
            safety_status = "CAUTION"
            override_reason = f"Thermal load elevated (Outlet: {raw_outlet_temp:.1f}°C, Server Tj: {raw_junction_temp:.1f}°C). Smart predictive mitigation active."
            # Minor flow boost
            active_flow_rate = base_flow * 1.15
            mitigations.append("Thermo AI pre-emptively ramped variable frequency pump (+15% flow)")
            mitigations.append("Prioritizing thermal dump to district buffer and sub-cooling manifolds")

        # 3. Final Physical Calculations with Mitigations Applied
        p_idle = cfg.nominal_it_power_kw * cfg.idle_power_ratio
        actual_power_kw = p_idle + (cfg.nominal_it_power_kw - p_idle) * math.pow(effective_workload / 100.0, 1.18)
        heat_gen_kw = actual_power_kw * 0.985  # 98.5% of electricity becomes heat
        heat_cap_kw = heat_gen_kw * cfg.heat_capture_efficiency

        # Final water temperature
        delta_t = heat_cap_kw / (active_flow_rate * cfg.specific_heat_water)
        outlet_temp = inlet_temp + delta_t
        junction_temp = outlet_temp + 13.0 + (effective_workload / 100.0) * 15.0

        # Calibrate outlet water temp within realistic 30°C to 50°C standard window
        outlet_temp = max(30.0, min(54.0, outlet_temp))

        # Hourly & Daily kWh
        heat_kwh_hourly = heat_cap_kw * 1.0  # 1 hour at this power
        heat_daily_proj = heat_kwh_hourly * 24.0

        # 4. Eco Sync Dynamic Heat Distribution Algorithm
        dist_pct, dist_kwh, consumer_details = self._calculate_heat_distribution(
            heat_cap_kw, outlet_temp, ambient_temp_c, safety_override_active
        )

        # 5. Ecological & Financial Impact
        co2_saved_hourly = heat_kwh_hourly * cfg.co2_kg_per_kwh_thermal
        co2_saved_annual = (co2_saved_hourly * 24.0 * 365.0) / 1000.0  # metric tons
        fin_savings_hourly = heat_kwh_hourly * cfg.heating_cost_per_kwh

        # PUE calculation: Baseline ~ 1.35. Heat reuse reduces effective PUE towards 1.05 - 1.10
        # Energy Reuse Effectiveness (ERE) = (Total Energy - Reuse Energy) / IT Energy
        reused_kw = heat_cap_kw * (1.0 - dist_pct.get("Dry Cooler / Safety Dump", 0.0) / 100.0)
        baseline_pue = 1.35 + 0.005 * max(0.0, ambient_temp_c - 20.0)
        facility_total_kw = actual_power_kw * baseline_pue
        effective_pue = max(1.02, (facility_total_kw - reused_kw * 0.65) / actual_power_kw)
        ere = max(0.35, (facility_total_kw - reused_kw) / actual_power_kw)

        return SimulationResult(
            workload_pct=workload_pct,
            ambient_temp_c=ambient_temp_c,
            effective_workload_pct=effective_workload,
            electrical_power_kw=round(actual_power_kw, 1),
            heat_generated_kw=round(heat_gen_kw, 1),
            heat_captured_kw=round(heat_cap_kw, 1),
            heat_captured_kwh_hourly=round(heat_kwh_hourly, 1),
            heat_captured_daily_proj_kwh=round(heat_daily_proj, 1),
            inlet_water_temp_c=round(inlet_temp, 1),
            outlet_water_temp_c=round(outlet_temp, 1),
            delta_t_c=round(delta_t, 1),
            estimated_junction_temp_c=round(junction_temp, 1),
            safety_status=safety_status,
            safety_override_active=safety_override_active,
            override_reason=override_reason,
            mitigation_actions=mitigations,
            distribution_pct=dist_pct,
            distribution_kwh=dist_kwh,
            consumer_status=consumer_details,
            co2_saved_hourly_kg=round(co2_saved_hourly, 1),
            co2_saved_annual_tons=round(co2_saved_annual, 1),
            financial_savings_hourly=round(fin_savings_hourly, 2),
            baseline_pue=round(baseline_pue, 2),
            effective_pue=round(effective_pue, 2),
            energy_reuse_effectiveness=round(ere, 2),
            cooling_flow_rate_active=round(active_flow_rate, 1)
        )

    def _calculate_heat_distribution(self, total_heat_kw: float, water_temp_c: float,
                                     ambient_temp_c: float, 
                                     is_override: bool) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, Dict[str, Any]]]:
        """
        Dynamically distributes harvested heat among real-world consumers
        based on temperature quality, ambient climate requirements, and safety state.
        """
        # If in critical safety override, prioritize emergency heat dump / dry coolers
        if is_override:
            pct_dump = 45.0
            pct_district = 25.0
            pct_greenhouse = 15.0
            pct_buffer = 15.0
            pct_industrial = 0.0
        else:
            # Normal smart distribution
            # 1. Greenhouse demand: High when cold, low when ambient > 24°C
            # Water temp ideal: 32°C - 42°C
            if ambient_temp_c < 5.0:
                gh_weight = 45.0  # Cold snap heating
            elif ambient_temp_c < 18.0:
                gh_weight = 32.0  # Spring / Autumn baseline
            elif ambient_temp_c < 28.0:
                gh_weight = 18.0  # Mild / Warm
            else:
                gh_weight = 8.0   # Summer night / minimal heating

            # 2. District / Building Hot Water: Requires hotter water (> 40°C is best)
            # Higher weight when water temp is hot
            temp_bonus = max(0.0, (water_temp_c - 36.0) * 1.5)
            if ambient_temp_c < 12.0:
                dhw_weight = 38.0 + temp_bonus
            else:
                dhw_weight = 28.0 + temp_bonus

            # 3. Industrial Low-Temp Drying / Agri-Processing: Steady 15-25%
            ind_weight = 18.0

            # 4. Thermal Energy Storage (TES Buffer): Absorbs surplus or off-peak heat
            buf_weight = max(10.0, 100.0 - (gh_weight + dhw_weight + ind_weight))

            # Normalize to 100%
            total_weight = gh_weight + dhw_weight + ind_weight + buf_weight
            pct_greenhouse = (gh_weight / total_weight) * 100.0
            pct_district = (dhw_weight / total_weight) * 100.0
            pct_industrial = (ind_weight / total_weight) * 100.0
            pct_buffer = (buf_weight / total_weight) * 100.0
            pct_dump = 0.0

        # Form distribution dictionaries
        dist_pct = {
            "Urban Eco-Greenhouse": round(pct_greenhouse, 1),
            "District / Building Hot Water": round(pct_district, 1),
            "Industrial Low-Temp Drying": round(pct_industrial, 1),
            "Thermal Buffer Storage (TES)": round(pct_buffer, 1),
        }
        if pct_dump > 0.0:
            dist_pct["Emergency Dry Cooler / Dump"] = round(pct_dump, 1)

        dist_kwh = {
            k: round(total_heat_kw * (v / 100.0), 1)
            for k, v in dist_pct.items()
        }

        # Consumer telemetry details
        consumer_status = {
            "Urban Eco-Greenhouse": {
                "description": "Supplies hydronic root-zone heating to a 4.5-hectare commercial greenhouse complex (tomatoes, herbs, strawberries).",
                "ideal_temp_range": "32°C - 42°C",
                "current_delivery_temp": f"{water_temp_c:.1f}°C",
                "status": "Optimal" if 32.0 <= water_temp_c <= 46.0 else "Sub-optimal",
                "cop_gain": "5.2x compared to electric heating",
                "offset_fuel": "Natural Gas Boilers"
            },
            "District / Building Hot Water": {
                "description": "Preheats domestic hot water (DHW) and space heating loop for 1,800 adjacent residential units & corporate campus.",
                "ideal_temp_range": "42°C - 55°C",
                "current_delivery_temp": f"{water_temp_c:.1f}°C",
                "status": "High Efficiency" if water_temp_c >= 40.0 else "Heat-Pump Boosted",
                "cop_gain": "4.8x COP heat pump lift",
                "offset_fuel": "Municipal Steam Grid"
            },
            "Industrial Low-Temp Drying": {
                "description": "Continuous biomass, wood chip, and spirulina algae dehydration drying tunnels.",
                "ideal_temp_range": "35°C - 48°C",
                "current_delivery_temp": f"{water_temp_c:.1f}°C",
                "status": "Continuous Run",
                "cop_gain": "Replaces 280kW resistive dryers",
                "offset_fuel": "Fuel Oil / LPG"
            },
            "Thermal Buffer Storage (TES)": {
                "description": "Stratified pressurized hot-water thermocline storage tank (15 MWh capacity) for peak thermal shaving.",
                "ideal_temp_range": "30°C - 55°C",
                "current_delivery_temp": f"{water_temp_c:.1f}°C",
                "status": "Charging" if not is_override else "Emergency Bypass",
                "cop_gain": "94% thermal round-trip efficiency",
                "offset_fuel": "Peak grid electrical peakers"
            }
        }

        return dist_pct, dist_kwh, consumer_status
