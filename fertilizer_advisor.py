"""
Fertilizer & Soil Health Advisory Module
Calculates nutrient deficits (N-P-K) and converts them into exact commercial
fertilizer quantities (Urea, DAP, MOP) and application schedules.
"""

from crop_advisor import CROP_DATABASE

FERTILIZERS = {
    "Urea": {"N": 0.46, "P": 0.0, "K": 0.0, "name": "Urea (46% Nitrogen)"},
    "DAP": {"N": 0.18, "P": 0.46, "K": 0.0, "name": "Di-Ammonium Phosphate (DAP: 18% N, 46% P)"},
    "MOP": {"N": 0.0, "P": 0.0, "K": 0.60, "name": "Muriate of Potash (MOP: 60% K2O)"},
    "SSP": {"N": 0.0, "P": 0.16, "K": 0.0, "name": "Single Super Phosphate (SSP: 16% P)"}
}

def analyze_soil_and_fertilizer(crop_name: str, current_n: float, current_p: float, current_k: float, farm_size_acres: float = 1.0):
    """
    Computes fertilizer recommendation for target crop based on current soil test.
    farm_size_acres: area of land in acres (1 hectare ≈ 2.47 acres)
    """
    if crop_name not in CROP_DATABASE:
        crop_data = CROP_DATABASE["Wheat"]
    else:
        crop_data = CROP_DATABASE[crop_name]

    # Target values (midpoint of optimal range in kg/hectare)
    target_n = (crop_data["N"][0] + crop_data["N"][1]) / 2.0
    target_p = (crop_data["P"][0] + crop_data["P"][1]) / 2.0
    target_k = (crop_data["K"][0] + crop_data["K"][1]) / 2.0

    # Deficit per hectare (if current is less than target)
    def_n = max(0.0, target_n - current_n)
    def_p = max(0.0, target_p - current_p)
    def_k = max(0.0, target_k - current_k)

    # Convert to user farm area (1 acre = 0.4047 hectare)
    hectares = farm_size_acres * 0.4047
    needed_n = def_n * hectares
    needed_p = def_p * hectares
    needed_k = def_k * hectares

    # Calculation logic for standard fertilizers:
    # 1. P is fulfilled first by DAP (which also provides 18% N)
    dap_kg = needed_p / 0.46 if needed_p > 0 else 0.0
    n_from_dap = dap_kg * 0.18

    # 2. Remaining N fulfilled by Urea
    remaining_n = max(0.0, needed_n - n_from_dap)
    urea_kg = remaining_n / 0.46 if remaining_n > 0 else 0.0

    # 3. K fulfilled by MOP (Muriate of Potash 60%)
    mop_kg = needed_k / 0.60 if needed_k > 0 else 0.0

    status = {
        "N": "Deficient" if def_n > 15 else ("Sufficient" if current_n <= crop_data["N"][1] else "Excess"),
        "P": "Deficient" if def_p > 10 else ("Sufficient" if current_p <= crop_data["P"][1] else "Excess"),
        "K": "Deficient" if def_k > 10 else ("Sufficient" if current_k <= crop_data["K"][1] else "Excess")
    }

    # Agronomic schedule & management practices
    schedule = [
        {
            "stage": "Basal Dose (During Soil Preparation & Sowing)",
            "action": f"Apply 100% of DAP ({dap_kg:.1f} kg), 100% of MOP ({mop_kg:.1f} kg), and 33% of Urea ({urea_kg * 0.33:.1f} kg). Incorporate well into the top 10-15 cm of soil."
        },
        {
            "stage": "First Top Dressing (Vegetative / Tillering Stage - 20-30 days)",
            "action": f"Broadcast 33% of Urea ({urea_kg * 0.33:.1f} kg) right after first irrigation/weeding."
        },
        {
            "stage": "Second Top Dressing (Panicle / Flowering Initiation - 45-60 days)",
            "action": f"Broadcast remaining 34% of Urea ({urea_kg * 0.34:.1f} kg) during active growth phase."
        }
    ]

    organic_alternatives = [
        "Well-rotted Farmyard Manure (FYM) or Compost: Apply 4 - 5 tons per acre 3 weeks prior to sowing.",
        "Vermicompost: Apply 1 - 1.5 tons per acre for enhancing microbial activity and soil water retention.",
        "Biofertilizers: Seed treatment with Azotobacter / Rhizobium (for pulses) and Phosphobacteria (PSB) @ 250g per 10kg seed."
    ]

    return {
        "crop": crop_name,
        "farm_size_acres": farm_size_acres,
        "current": {"N": current_n, "P": current_p, "K": current_k},
        "target": {"N": round(target_n, 1), "P": round(target_p, 1), "K": round(target_k, 1)},
        "status": status,
        "commercial_fertilizers": {
            "Urea": round(urea_kg, 1),
            "DAP": round(dap_kg, 1),
            "MOP": round(mop_kg, 1),
            "total_bags_urea": round(urea_kg / 45.0, 1),  # standard 45kg bag
            "total_bags_dap": round(dap_kg / 50.0, 1),   # standard 50kg bag
            "total_bags_mop": round(mop_kg / 50.0, 1)    # standard 50kg bag
        },
        "schedule": schedule,
        "organic": organic_alternatives
    }
