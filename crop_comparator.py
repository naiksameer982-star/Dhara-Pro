"""
Crop Duel & Multi-Factor Risk Comparator Module
Enables side-by-side risk, investment, and return evaluation between competing crops.
"""

from crop_advisor import CROP_DATABASE

CROP_PROFILES = {
    "Wheat": {
        "water_need": "Medium (450 - 650 mm)",
        "capital_per_acre": "₹16,000",
        "labor_demand": "Low (Mechanized combine harvesting)",
        "market_risk": "Low (Guaranteed Govt. MSP procurement)",
        "duration": "120 - 135 days",
        "net_profit_est": "₹28,000 - ₹34,000 / acre",
        "msp_safety": "High ✅",
        "verdict_tag": "Safe & Stable Food Security"
    },
    "Cotton": {
        "water_need": "High (700 - 1000 mm)",
        "capital_per_acre": "₹26,000",
        "labor_demand": "High (Multiple manual picking cycles)",
        "market_risk": "High (Global commodity and pest volatility)",
        "duration": "160 - 180 days",
        "net_profit_est": "₹38,000 - ₹52,000 / acre",
        "msp_safety": "Medium ⚖️",
        "verdict_tag": "High Risk, High Reward Cash Crop"
    },
    "Soybean (Yellow)": {
        "water_need": "Medium (500 - 650 mm)",
        "capital_per_acre": "₹14,000",
        "labor_demand": "Low (Fast canopy coverage suppresses weeds)",
        "market_risk": "Low to Medium (Strong oilseed demand)",
        "duration": "90 - 105 days",
        "net_profit_est": "₹22,000 - ₹28,000 / acre",
        "msp_safety": "High ✅",
        "verdict_tag": "Fast Cash Rotation & Nitrogen Fixer"
    },
    "Maize (Corn)": {
        "water_need": "Medium (500 - 800 mm)",
        "capital_per_acre": "₹18,000",
        "labor_demand": "Medium (Cob harvesting & shelling)",
        "market_risk": "Medium (High demand in poultry & ethanol)",
        "duration": "90 - 110 days",
        "net_profit_est": "₹25,000 - ₹35,000 / acre",
        "msp_safety": "Medium ⚖️",
        "verdict_tag": "Industrial Feed & Biofuel Demand"
    },
    "Chickpea (Gram)": {
        "water_need": "Low (250 - 350 mm)",
        "capital_per_acre": "₹12,000",
        "labor_demand": "Low",
        "market_risk": "Low (Pulse deficit in country)",
        "duration": "100 - 120 days",
        "net_profit_est": "₹24,000 - ₹32,000 / acre",
        "msp_safety": "High ✅",
        "verdict_tag": "Drought Resilient Pulse"
    },
    "Rice (Basmati / Paddy)": {
        "water_need": "Very High (1200 - 1500 mm)",
        "capital_per_acre": "₹22,000",
        "labor_demand": "High (Nursery transplanting)",
        "market_risk": "Low to Medium",
        "duration": "120 - 140 days",
        "net_profit_est": "₹30,000 - ₹42,000 / acre",
        "msp_safety": "High ✅",
        "verdict_tag": "Water Abundant Staple"
    },
    "Mustard (Rapeseed)": {
        "water_need": "Low (250 - 400 mm)",
        "capital_per_acre": "₹13,000",
        "labor_demand": "Low",
        "market_risk": "Medium",
        "duration": "105 - 125 days",
        "net_profit_est": "₹26,000 - ₹35,000 / acre",
        "msp_safety": "High ✅",
        "verdict_tag": "Low Cost, High Edible Oil Value"
    }
}


def compare_two_crops(crop_a: str, crop_b: str):
    """
    Returns side by side comparison table and strategic decision verdict.
    """
    data_a = CROP_PROFILES.get(crop_a, CROP_PROFILES["Wheat"])
    data_b = CROP_PROFILES.get(crop_b, CROP_PROFILES["Soybean (Yellow)"])

    metrics = [
        {"Parameter": "⏳ Crop Duration", crop_a: data_a["duration"], crop_b: data_b["duration"]},
        {"Parameter": "💧 Water Footprint", crop_a: data_a["water_need"], crop_b: data_b["water_need"]},
        {"Parameter": "💰 Capital Needed (per acre)", crop_a: data_a["capital_per_acre"], crop_b: data_b["capital_per_acre"]},
        {"Parameter": "👷 Labor Intensity", crop_a: data_a["labor_demand"], crop_b: data_b["labor_demand"]},
        {"Parameter": "📉 Price Volatility Risk", crop_a: data_a["market_risk"], crop_b: data_b["market_risk"]},
        {"Parameter": "🏛️ Govt MSP Safety", crop_a: data_a["msp_safety"], crop_b: data_b["msp_safety"]},
        {"Parameter": "📈 Expected Net Profit", crop_a: data_a["net_profit_est"], crop_b: data_b["net_profit_est"]},
        {"Parameter": "🏷️ Strategic Category", crop_a: data_a["verdict_tag"], crop_b: data_b["verdict_tag"]}
    ]

    return metrics
