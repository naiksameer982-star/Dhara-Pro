"""
Kisan AI Agronomist Module (AgriGPT)
Specialized agricultural advisory assistant capable of answering questions on
organic farming (Zero Budget Natural Farming), pest lifecycles, and agronomy.
"""

# Curated Agronomic Knowledge Base
AGRI_KNOWLEDGE_BASE = {
    "jeevamrit": {
        "title": "🌿 How to Prepare Jeevamrit (Organic Bio-Fertilizer)",
        "ingredients": [
            "Fresh Desi Cow Dung: 10 kg",
            "Desi Cow Urine: 5 to 10 Liters",
            "Jaggery (Gud / Organic Sugar): 2 kg",
            "Pulse Flour (Besan / Gram flour): 2 kg",
            "Virgin Soil from field border or banyan tree root: 1 handful (100g)",
            "Water: 200 Liters"
        ],
        "procedure": "Mix all ingredients thoroughly in a 200L plastic drum using a wooden stick. Keep under shade covered with a wet gunny bag. Stir clockwise 2-3 times daily for 4-7 days.",
        "application": "Apply 200 liters per acre with irrigation water or spray 10% filtered solution as a foliar growth promoter."
    },
    "neemastra": {
        "title": "🛡️ How to Prepare Neemastra (Organic Insecticide)",
        "ingredients": [
            "Desi Cow Urine: 5 Liters",
            "Fresh Cow Dung: 2 kg",
            "Crushed Neem Leaves / Pulp: 5 kg",
            "Water: 100 Liters"
        ],
        "procedure": "Mix dung, urine, and crushed neem leaves in water. Ferment for 48 hours under shade. Stir twice daily.",
        "application": "Filter through muslin cloth and spray directly without dilution to control sucking pests (aphids, jassids, whiteflies)."
    },
    "intercropping": {
        "title": "🌾 High-Yield Intercropping Combinations",
        "combinations": [
            "Sugarcane + Mungbean / Soybean (Fixes atmospheric nitrogen in early sugarcane phase)",
            "Cotton + Pigeonpea (Arhar) (Border trap crop for bollworm management)",
            "Maize + Cowpea (Lobia) (Reduces weed growth and enhances fodder value)",
            "Wheat + Mustard (Row ratio 9:1 - optimizes spatial sunlight and root zones)"
        ]
    },
    "fall_armyworm": {
        "title": "🐛 Integrated Management for Fall Armyworm (Maize)",
        "steps": [
            "Pheromone Traps: Install 5 funnel traps per acre for early moth monitoring.",
            "Bio-Pesticide: Spray Metarhizium anisopliae or Beauveria bassiana @ 5g/liter at early instars.",
            "Whorl Application: Apply a mixture of dry sand and neem cake powder (9:1) directly into central plant whorls.",
            "Targeted Chemical: If infestation exceeds 10%, spray Chlorantraniliprole 18.5 SC @ 0.4 ml/L into central whorls."
        ]
    },
    "soil_salinity": {
        "title": "🧂 Reclamation of Saline and Alkaline Soils",
        "steps": [
            "Gypsum Application: For alkali (sodic) soils, apply agricultural gypsum (CaSO4) based on soil test report.",
            "Leaching: Flood the field with good quality irrigation water and provide deep drainage channels to wash down salts.",
            "Green Manuring: Grow and incorporate Dhaincha (Sesbania aculeata) at 45 days stage before the main crop.",
            "Organic Matter: Generously apply farmyard manure or vermicompost to improve soil structure and water percolation."
        ]
    }
}


def ask_agronomist(user_query: str) -> str:
    """
    Evaluates farmer query and returns verified agronomic solutions.
    """
    q = user_query.lower()

    if any(w in q for w in ["jeevamrit", "organic fertilizer", "cow dung", "bio fertilizer", "natural farming"]):
        data = AGRI_KNOWLEDGE_BASE["jeevamrit"]
        res = f"### {data['title']}\n\n**Ingredients for 1 Acre (200L):**\n"
        for ing in data["ingredients"]:
            res += f"- {ing}\n"
        res += f"\n**Method:**\n{data['procedure']}\n\n**Application:**\n{data['application']}"
        return res

    elif any(w in q for w in ["neem", "neemastra", "organic pesticide", "sucking pest", "aphid", "whitefly"]):
        data = AGRI_KNOWLEDGE_BASE["neemastra"]
        res = f"### {data['title']}\n\n**Ingredients (for 100L):**\n"
        for ing in data["ingredients"]:
            res += f"- {ing}\n"
        res += f"\n**Procedure:**\n{data['procedure']}\n\n**How to Spray:**\n{data['application']}"
        return res

    elif any(w in q for w in ["intercrop", "companion", "mixed crop", "two crops"]):
        data = AGRI_KNOWLEDGE_BASE["intercropping"]
        res = f"### {data['title']}\n\n**Scientifically Proven Crop Pairings:**\n"
        for comb in data["combinations"]:
            res += f"- **{comb}**\n"
        res += "\n_Tip: Legumes (pulses) should always be included in intercropping to fix soil nitrogen naturally._"
        return res

    elif any(w in q for w in ["armyworm", "fall army", "corn pest", "maize insect", "whorl"]):
        data = AGRI_KNOWLEDGE_BASE["fall_armyworm"]
        res = f"### {data['title']}\n\n"
        for step in data["steps"]:
            res += f"- {step}\n"
        return res

    elif any(w in q for w in ["saline", "salt", "alkaline", "white soil", "gypsum", "kallar"]):
        data = AGRI_KNOWLEDGE_BASE["soil_salinity"]
        res = f"### {data['title']}\n\n"
        for step in data["steps"]:
            res += f"- {step}\n"
        return res

    elif any(w in q for w in ["drip", "irrigation schedule", "water"]):
        return (
            "### 💧 Precision Irrigation Guidelines\n\n"
            "- **Critical Watering Stages:** Flowering and grain-filling/pod development stages are most sensitive to water deficit.\n"
            "- **Drip Efficiency:** Drip systems deliver water with 90-95% efficiency directly at the root zone compared to 40% in flood irrigation.\n"
            "- **Evaporation Control:** Irrigate during early morning (5:00 AM - 8:00 AM) or late evening to minimize atmospheric evaporation loss."
        )

    else:
        return (
            f"### 🌾 Agronomist Advisory for: *'{user_query}'*\n\n"
            "**Key Scientific Recommendations:**\n"
            "1. **Soil & Root Health:** Always maintain at least 0.5% - 0.75% Organic Carbon in the root zone by adding compost or green manure.\n"
            "2. **Integrated Pest Management (IPM):** Combine cultural practices, pheromone monitoring traps, biological agents (Trichoderma / Pseudomonas), and use chemical pesticides only as a final resort.\n"
            "3. **Crop Rotation:** Never sow the same botanical family crop consecutively on the same plot to break insect and pathogen breeding cycles.\n"
            "4. **Need Specific Advice?** Try asking about: *'How to prepare Jeevamrit'*, *'Neemastra recipe'*, *'Control fall armyworm'*, or *'Reclaiming saline soils'*."
        )
