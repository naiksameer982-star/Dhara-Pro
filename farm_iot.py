"""
Smart Farm IoT Telemetry & Precision Irrigation Actuator Module
Simulates live sensor streams (soil moisture probes, temperature, electrical conductivity)
and automated water pump relay actuation.
"""

import pandas as pd
import numpy as np

def get_live_sensor_telemetry(soil_moisture_override: float = None):
    """
    Generates telemetry readings representing multi-depth farm probes.
    """
    # 15 cm depth represents active root zone
    moisture_15cm = soil_moisture_override if soil_moisture_override is not None else 38.5
    moisture_30cm = min(80.0, moisture_15cm + 6.2)
    soil_temp = 24.8
    ec_salinity = 1.15 # dS/m (Decisiemens per meter, <2 is ideal)
    solar_radiation = 680 # W/m2

    # Automatic Pump Actuation Logic
    if moisture_15cm < 35.0:
        pump_state = "ON 🟢 (Automated Irrigation Active)"
        pump_color = "green"
        recommendation = "Soil moisture is below root wilting point (35%). Drip irrigation relay engaged."
    elif moisture_15cm > 65.0:
        pump_state = "OFF 🔴 (Field at Field Capacity)"
        pump_color = "red"
        recommendation = "Soil is well-saturated. Water pump cut off automatically to avoid root suffocation and save power."
    else:
        pump_state = "STANDBY 🟡 (Optimal Moisture Window)"
        pump_color = "orange"
        recommendation = "Soil moisture is in the ideal 40% - 65% agronomic range. Pump in standby mode."

    # Historical 24-hour sensor trends
    hours = [f"{h:02d}:00" for h in range(0, 24, 2)]
    moist_trend = [
        48, 46, 44, 42, 40, 37, 34, 32, 58, 62, 59, 54
    ]
    df_history = pd.DataFrame({
        "Hour": hours,
        "Soil Moisture (%)": moist_trend
    })

    return {
        "moisture_15cm": moisture_15cm,
        "moisture_30cm": moisture_30cm,
        "soil_temp": soil_temp,
        "ec_salinity": ec_salinity,
        "solar_radiation": solar_radiation,
        "pump_state": pump_state,
        "pump_color": pump_color,
        "recommendation": recommendation,
        "history_df": df_history,
        "water_saved_liters": 12400,
        "electricity_saved_kwh": 18.5
    }
