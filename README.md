# 🌱 Eco Sync & Thermo AI

> **Next-Generation Data Centre Waste-Heat Recovery & Intelligent Thermal Dispatch Simulator**

An interactive Python Streamlit web application that simulates a liquid-cooled data centre co-generation system. The system harvests low-to-medium grade waste heat (30°C to 50°C) from high-density AI/compute clusters and dynamically dispatches it to municipal and industrial consumers such as urban greenhouses, district hot water networks, and thermal storage tanks.

---

## 🌟 Key Features

1. **Interactive Controls**:
   - **Server Workload / AI Traffic Slider (0% - 100%)**: Models server compute power draw, GPU training jobs, and dynamic heat generation.
   - **Outdoor Ambient Temperature Slider (-15°C to 45°C)**: Simulates local climate conditions, seasonal heating demands, and cooling tower efficiency.
   - **Quick Scenario Presets**: 1-click loading for scenarios like Winter AI Peak, Summer Heatwave, Balanced Eco-Operation, and Extreme Overload.

2. **Real-Time Physics & Thermodynamic Calculations**:
   - **Water Temperature (30°C to 50°C Band)**: Models inlet coolant temperature, fluid flow rate ($\dot{m}$), and outlet return temperature using $Q = \dot{m} \cdot C_p \cdot \Delta T$.
   - **Heat Captured in kWh**: Live thermal power ($kW_{th}$) and equivalent energy harvested ($kWh/h$ and daily cumulative projections).
   - **Carbon & Cost Avoidance**: Calculates avoided fossil fuel emissions ($kg\ CO_2/hr$) and heating utility savings.
   - **PUE & ERE Optimization**: Demonstrates reduction in effective Power Usage Effectiveness from baseline 1.38 down towards 1.08 with waste-heat credits.

3. **Dynamic Heat Distribution**:
   - **Urban Eco-Greenhouse**: Hydronic soil root-zone and canopy heating for commercial greenhouses (spikes in freezing ambient conditions).
   - **District / Building Hot Water**: Domestic hot water pre-heating and space heating for municipal apartments & campus facilities.
   - **Industrial Low-Temp Drying**: Steady heat for biomass, timber, and spirulina algae dehydration.
   - **Stratified Thermal Energy Storage (TES Buffer)**: 15 MWh thermocline storage buffer for grid peak shaving and surplus absorption.

4. **AI Status Log & Smart Scheduling (Thermo AI)**:
   - Intelligent decision log feed tracking valve movements, dispatch decisions, meteorological forecast integration, and PUE optimizations.
   - Filterable by event categories (`OPTIMIZATION`, `DISPATCH`, `SAFETY_OVERRIDE`, `PREDICTIVE`, `PUE_METRIC`).

5. **Autonomous Safety Override Alert System**:
   - Multi-tier safety watchdog:
     - **Normal Operating Envelope**: Water outlet $< 44^\circ\text{C}$.
     - **Caution State**: Water outlet $44^\circ\text{C} - 49^\circ\text{C}$ (automatic pump ramp +15%).
     - **Critical Safety Override**: Triggered if water outlet $\ge 49^\circ\text{C}$, junction temp $\ge 86^\circ\text{C}$, or critical ambient stress ($W \ge 90\%$ and Ambient $\ge 37^\circ\text{C}$).
   - **Autonomous Interventions**:
     - Emergency coolant flow boost (+40%)
     - Automated batch workload throttling (-25%)
     - Auxiliary adiabatic dry-cooler bypass activation to safeguard server silicon.

6. **Interactive Visualizations**:
   - Live SVG/HTML Thermodynamic Schematic showing server racks, coolant flow, heat exchanger unit, and consumer branches.
   - Plotly Real-Time Thermal Allocation Donut Chart.
   - Thermodynamic Operating Envelope Curve with operating band and danger thresholds.
   - 24-Hour Predictive Heat Harvesting & Workload Profile.

---

## 🚀 How to Run the Application

### Option 1: Double-click launcher (Windows)
Double-click `run_app.bat` inside this folder.

### Option 2: PowerShell
Run the following command in PowerShell:
```powershell
.\run_app.ps1
```

### Option 3: Terminal command
Run using Python with Streamlit:
```bash
python -m streamlit run app.py
```
*(If on Windows with WindowsApps Python, run: `C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe -m streamlit run app.py`)*

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
eco-sync-thermo-ai/
├── app.py              # Main Streamlit web application
├── simulation.py       # Physics, thermodynamics & heat distribution engine
├── ai_scheduler.py     # Thermo AI smart decision logger & safety watchdog
├── components.py       # Modern styling, interactive SVG schematic & Plotly charts
├── run_app.bat         # 1-click batch launcher for Windows
├── run_app.ps1         # PowerShell launcher script
└── README.md           # Documentation & engineering model
```

---

## 🔬 Computational Model

The thermodynamics are grounded in standard mechanical engineering principles:

$$\Delta T = \frac{Q_{captured}}{\dot{m} \cdot C_p}$$

Where:
- $Q_{captured} = P_{IT} \times \eta_{capture}$ (with $\eta_{capture} = 88\%$ for Direct-to-Chip cold plates)
- $P_{IT} = P_{idle} + (P_{max} - P_{idle}) \times (W/100)^{1.18}$
- $\dot{m} = 22.0 \text{ kg/s}$ (active coolant circulation)
- $C_p = 4.184 \text{ kJ/(kg}\cdot\text{K)}$
