"""
Crop Recommendation Module
Matches soil (N, P, K, pH) and climate (temperature, humidity, rainfall)
against standard agronomic profiles for 22 major agricultural crops.
"""

# Optimal agronomic requirements based on ICAR & FAO agricultural datasets
CROP_DATABASE = {
    "Rice": {
        "N": (60, 100), "P": (35, 60), "K": (35, 45),
        "temp": (20, 35), "humidity": (70, 95), "ph": (5.0, 7.5), "rainfall": (150, 300),
        "season": "Kharif (Monsoon)",
        "duration": "100 - 150 days",
        "soil_type": "Clayey, Loamy with high water retention",
        "description": "Thrives in warm, humid climates with abundant water supply."
    },
    "Wheat": {
        "N": (80, 120), "P": (40, 60), "K": (30, 45),
        "temp": (12, 25), "humidity": (40, 70), "ph": (6.0, 7.5), "rainfall": (50, 100),
        "season": "Rabi (Winter)",
        "duration": "110 - 140 days",
        "soil_type": "Well-drained fertile loamy / clay loam",
        "description": "Requires cool winter growing season followed by warm weather at harvest."
    },
    "Maize (Corn)": {
        "N": (60, 100), "P": (40, 65), "K": (15, 30),
        "temp": (18, 30), "humidity": (55, 75), "ph": (5.5, 7.5), "rainfall": (60, 120),
        "season": "Kharif / Spring",
        "duration": "85 - 110 days",
        "soil_type": "Deep, well-drained fertile loamy soil",
        "description": "Adaptable grain crop with moderate water and high nitrogen requirement."
    },
    "Cotton": {
        "N": (100, 140), "P": (40, 60), "K": (15, 30),
        "temp": (22, 35), "humidity": (50, 75), "ph": (6.0, 8.0), "rainfall": (50, 110),
        "season": "Kharif (Cash crop)",
        "duration": "150 - 180 days",
        "soil_type": "Deep black soils (Regur) or alluvial soils",
        "description": "Needs warm climate and long frost-free period."
    },
    "Chickpea (Gram)": {
        "N": (20, 45), "P": (50, 75), "K": (65, 85),
        "temp": (15, 28), "humidity": (30, 60), "ph": (6.0, 8.0), "rainfall": (40, 80),
        "season": "Rabi (Winter pulse)",
        "duration": "90 - 120 days",
        "soil_type": "Sandy loam to clay loam with good drainage",
        "description": "Nitrogen-fixing legume; requires low rainfall and cool climate."
    },
    "Kidney Beans (Rajma)": {
        "N": (15, 35), "P": (55, 75), "K": (15, 30),
        "temp": (15, 25), "humidity": (50, 65), "ph": (5.5, 6.5), "rainfall": (60, 120),
        "season": "Rabi / Kharif (Hills)",
        "duration": "90 - 110 days",
        "soil_type": "Light, loose, well-drained organic rich soil",
        "description": "Sensitive to waterlogging, requires moderate temperatures."
    },
    "Pigeonpeas (Arhar / Tur)": {
        "N": (15, 35), "P": (50, 70), "K": (15, 30),
        "temp": (20, 35), "humidity": (45, 70), "ph": (5.5, 7.5), "rainfall": (60, 110),
        "season": "Kharif",
        "duration": "150 - 200 days",
        "soil_type": "Well-drained deep loamy soil",
        "description": "Drought-tolerant leguminous crop with deep root system."
    },
    "Mothbeans": {
        "N": (15, 30), "P": (35, 55), "K": (15, 30),
        "temp": (24, 35), "humidity": (40, 60), "ph": (6.5, 8.5), "rainfall": (30, 70),
        "season": "Kharif (Arid / Semi-arid)",
        "duration": "75 - 90 days",
        "soil_type": "Sandy or light loam",
        "description": "Highly drought-resistant legume ideal for low-rainfall areas."
    },
    "Mungbean (Green Gram)": {
        "N": (15, 35), "P": (35, 55), "K": (15, 30),
        "temp": (22, 34), "humidity": (60, 85), "ph": (6.2, 7.5), "rainfall": (40, 90),
        "season": "Kharif / Zaid (Summer)",
        "duration": "60 - 75 days",
        "soil_type": "Loam to sandy loam",
        "description": "Short duration catch crop suitable for multiple cropping systems."
    },
    "Blackgram (Urad)": {
        "N": (35, 55), "P": (55, 75), "K": (15, 30),
        "temp": (25, 35), "humidity": (60, 75), "ph": (6.5, 7.5), "rainfall": (60, 100),
        "season": "Kharif / Summer",
        "duration": "70 - 90 days",
        "soil_type": "Loamy to heavy clay soils",
        "description": "Demands warm and humid climate; improves soil nitrogen."
    },
    "Lentil (Masoor)": {
        "N": (15, 35), "P": (55, 80), "K": (15, 30),
        "temp": (15, 26), "humidity": (50, 70), "ph": (5.8, 7.5), "rainfall": (40, 70),
        "season": "Rabi",
        "duration": "110 - 130 days",
        "soil_type": "Light loamy to alluvial soils",
        "description": "Cool-season legume with excellent protein profile and low water need."
    },
    "Pomegranate": {
        "N": (15, 35), "P": (10, 25), "K": (35, 50),
        "temp": (20, 35), "humidity": (30, 50), "ph": (6.0, 7.5), "rainfall": (50, 110),
        "season": "Perennial (Ambe / Mrig / Hasta Bahar)",
        "duration": "Perennial (Fruit in 6 months)",
        "soil_type": "Deep well-drained sandy loam to clay loam",
        "description": "Subtropical fruit tolerant to drought; likes hot dry summers."
    },
    "Banana": {
        "N": (90, 120), "P": (70, 95), "K": (45, 60),
        "temp": (24, 32), "humidity": (75, 90), "ph": (6.0, 7.5), "rainfall": (100, 200),
        "season": "Year-round planting",
        "duration": "11 - 13 months",
        "soil_type": "Rich, well-drained loamy soil with organic matter",
        "description": "High nutrient and water feeder with fast biomass accumulation."
    },
    "Mango": {
        "N": (15, 40), "P": (15, 35), "K": (25, 40),
        "temp": (24, 35), "humidity": (45, 65), "ph": (5.5, 7.5), "rainfall": (80, 150),
        "season": "Flowering in Winter, Harvest in Summer",
        "duration": "Perennial tree",
        "soil_type": "Deep alluvial, well-drained loamy soil",
        "description": "Requires distinct dry period to stimulate flowering."
    },
    "Grapes": {
        "N": (15, 35), "P": (110, 140), "K": (190, 210),
        "temp": (15, 35), "humidity": (45, 65), "ph": (6.5, 8.0), "rainfall": (50, 90),
        "season": "Perennial (Vineyard)",
        "duration": "Harvest in Feb - April",
        "soil_type": "Well-drained sandy loam or gravelly soil",
        "description": "High potassium demand; prone to fungus in high humidity."
    },
    "Watermelon": {
        "N": (80, 120), "P": (15, 30), "K": (45, 60),
        "temp": (24, 35), "humidity": (50, 65), "ph": (6.0, 7.0), "rainfall": (40, 70),
        "season": "Zaid (Summer crop)",
        "duration": "80 - 100 days",
        "soil_type": "Sandy or sandy loam with good drainage",
        "description": "Requires sunny, hot dry conditions for sweetness accumulation."
    },
    "Apple": {
        "N": (15, 35), "P": (120, 145), "K": (190, 210),
        "temp": (10, 24), "humidity": (55, 75), "ph": (5.5, 6.8), "rainfall": (100, 150),
        "season": "Temperate perennial",
        "duration": "Harvest Aug - Oct",
        "soil_type": "Loam to sandy loam rich in organic matter",
        "description": "Requires winter chilling hours (< 7°C) for dormancy breaking."
    },
    "Orange / Citrus": {
        "N": (10, 30), "P": (10, 25), "K": (10, 20),
        "temp": (15, 35), "humidity": (50, 70), "ph": (6.0, 7.5), "rainfall": (80, 140),
        "season": "Perennial",
        "duration": "Maturity 8-9 months",
        "soil_type": "Light, well-aerated sandy loam",
        "description": "Sensitive to waterlogging, needs moderate humidity and sunshine."
    },
    "Papaya": {
        "N": (40, 65), "P": (50, 70), "K": (45, 60),
        "temp": (22, 35), "humidity": (60, 80), "ph": (6.0, 7.0), "rainfall": (100, 180),
        "season": "Year-round in tropics",
        "duration": "9 - 11 months",
        "soil_type": "Rich sandy loam with excellent drainage",
        "description": "Fast-growing fruit crop susceptible to frost and standing water."
    },
    "Coconut": {
        "N": (15, 35), "P": (10, 25), "K": (25, 40),
        "temp": (25, 35), "humidity": (70, 90), "ph": (5.2, 8.0), "rainfall": (150, 250),
        "season": "Perennial coastal crop",
        "duration": "Perennial (yields for decades)",
        "soil_type": "Coastal sandy, alluvial or red sandy loam",
        "description": "Requires humid tropical weather and generous moisture."
    },
    "Jute": {
        "N": (65, 95), "P": (40, 60), "K": (35, 50),
        "temp": (24, 36), "humidity": (75, 90), "ph": (6.0, 7.5), "rainfall": (140, 200),
        "season": "Kharif (Monsoon)",
        "duration": "120 - 150 days",
        "soil_type": "Alluvial, clayey or loamy soil",
        "description": "Golden fiber crop needing high rainfall and muggy monsoon heat."
    },
    "Coffee": {
        "N": (80, 120), "P": (20, 40), "K": (25, 40),
        "temp": (18, 28), "humidity": (65, 85), "ph": (5.5, 6.5), "rainfall": (150, 220),
        "season": "Hill plantation",
        "duration": "Perennial (annual picking Nov - Feb)",
        "soil_type": "Rich volcanic loam with deep leaf mold",
        "description": "Grown under shade trees in high-altitude tropical hill slopes."
    }
}


def calculate_suitability(crop_name: str, n: float, p: float, k: float, temp: float, humidity: float, ph: float, rainfall: float) -> float:
    """
    Computes a 0-100% suitability match score using normalized penalty logic.
    """
    crop = CROP_DATABASE[crop_name]
    penalties = []

    def param_penalty(val, min_val, max_val, tolerance_ratio=0.5):
        if min_val <= val <= max_val:
            return 0.0
        dist = min_val - val if val < min_val else val - max_val
        span = max_val - min_val if max_val > min_val else 1.0
        penalty = dist / (span * (1 + tolerance_ratio))
        return min(penalty, 1.0)

    # Calculate penalties for each agricultural factor
    penalties.append(param_penalty(n, crop["N"][0], crop["N"][1]) * 1.0)
    penalties.append(param_penalty(p, crop["P"][0], crop["P"][1]) * 1.0)
    penalties.append(param_penalty(k, crop["K"][0], crop["K"][1]) * 1.0)
    penalties.append(param_penalty(temp, crop["temp"][0], crop["temp"][1]) * 1.5)
    penalties.append(param_penalty(humidity, crop["humidity"][0], crop["humidity"][1]) * 1.2)
    penalties.append(param_penalty(ph, crop["ph"][0], crop["ph"][1]) * 1.3)
    penalties.append(param_penalty(rainfall, crop["rainfall"][0], crop["rainfall"][1]) * 1.4)

    total_weight = 1.0 + 1.0 + 1.0 + 1.5 + 1.2 + 1.3 + 1.4
    avg_penalty = sum(penalties) / total_weight
    score = max(0.0, 100.0 * (1.0 - avg_penalty))
    return round(score, 1)


def recommend_crops(n: float, p: float, k: float, temp: float, humidity: float, ph: float, rainfall: float, top_n: int = 5):
    """
    Evaluates all crops and returns sorted recommendations.
    """
    results = []
    for name, data in CROP_DATABASE.items():
        score = calculate_suitability(name, n, p, k, temp, humidity, ph, rainfall)
        results.append({
            "crop": name,
            "score": score,
            "season": data["season"],
            "duration": data["duration"],
            "soil_type": data["soil_type"],
            "description": data["description"],
            "ideal_n": f"{data['N'][0]} - {data['N'][1]} kg/ha",
            "ideal_p": f"{data['P'][0]} - {data['P'][1]} kg/ha",
            "ideal_k": f"{data['K'][0]} - {data['K'][1]} kg/ha",
            "ideal_temp": f"{data['temp'][0]} - {data['temp'][1]} °C",
            "ideal_ph": f"{data['ph'][0]} - {data['ph'][1]}",
            "ideal_rain": f"{data['rainfall'][0]} - {data['rainfall'][1]} mm"
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
