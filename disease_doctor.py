"""
Plant Doctor & Crop Disease Diagnostician Module
Contains diagnostic profiles for top commercial crops, symptom matching algorithms,
and treatment protocols (Organic, Chemical, and Cultural Prevention).
"""

DISEASE_DB = {
    "Tomato": [
        {
            "disease": "Early Blight (Alternaria solani)",
            "symptoms": ["Dark concentric rings / target spots on older leaves", "Yellow halo around spots", "Premature defoliation"],
            "severity": "Medium",
            "organic_cure": "Spray Neem oil (5ml/L) or Copper oxychloride (2g/L); prune lower leaves touching soil.",
            "chemical_cure": "Mancozeb 75 WP @ 2.5 g/L or Azoxystrobin 23 SC @ 1 ml/L water.",
            "prevention": "Ensure good air circulation, practice crop rotation, and avoid overhead sprinkler watering."
        },
        {
            "disease": "Late Blight (Phytophthora infestans)",
            "symptoms": ["Water-soaked dark lesions on leaf tips", "White fuzzy fungal growth on underside", "Rapid rotting of fruit"],
            "severity": "Critical",
            "organic_cure": "Bordeaux mixture (1%) spray; remove and burn infected plant debris immediately.",
            "chemical_cure": "Metalaxyl + Mancozeb (Ridomil MZ) @ 2.5 g/L or Cymoxanil @ 2 g/L.",
            "prevention": "Plant resistant cultivars and avoid waterlogged soil conditions."
        },
        {
            "disease": "Tomato Leaf Curl Virus (ToLCV)",
            "symptoms": ["Upward leaf curling and puckering", "Stunted bushy plant growth", "Thickened veins and poor flowering"],
            "severity": "High",
            "organic_cure": "Install yellow sticky traps (15/acre) to control Whitefly vectors; spray 2% castor oil emulsion.",
            "chemical_cure": "Dimethoate 30 EC @ 1.7 ml/L or Imidacloprid 17.8 SL @ 0.5 ml/L to suppress insect vectors.",
            "prevention": "Use 40-mesh insect-proof nylon nets in nursery beds."
        }
    ],
    "Potato": [
        {
            "disease": "Late Blight of Potato",
            "symptoms": ["Dark irregular patches on leaves", "White mold beneath leaves in moist morning", "Tuber rot"],
            "severity": "Critical",
            "organic_cure": "Trichoderma viride seed tuber treatment; spray fermented buttermilk diluted 1:10 with water.",
            "chemical_cure": "Fenamidone + Mancozeb (Sectin) @ 1.5 g/L or Chlorothalonil 75 WP @ 2 g/L.",
            "prevention": "Earthing up properly to protect tubers; use certified disease-free seed tubers."
        },
        {
            "disease": "Common Scab (Streptomyces scabies)",
            "symptoms": ["Rough, corky lesions on tuber skin", "Crater-like pits on potato surface"],
            "severity": "Medium",
            "organic_cure": "Apply green manuring with Sesbania (Dhaincha) before planting to lower soil pH.",
            "chemical_cure": "Dip seed tubers in Emisan-6 (0.25%) solution for 30 minutes before planting.",
            "prevention": "Maintain adequate soil moisture during tuber initiation (tuberization stage)."
        }
    ],
    "Wheat": [
        {
            "disease": "Yellow / Stripe Rust (Puccinia striiformis)",
            "symptoms": ["Yellow powdery pustules in parallel stripes along leaf veins", "Chlorotic stripes on leaves"],
            "severity": "High",
            "organic_cure": "Spray extract of Garlic and Neem seed kernel extract (NSKE 5%).",
            "chemical_cure": "Propiconazole 25 EC (Tilt) @ 1 ml/L or Tebuconazole @ 1 ml/L water.",
            "prevention": "Sow rust-resistant varieties (e.g., HD-2967, PBW-550); avoid excessive nitrogen fertilizer."
        },
        {
            "disease": "Loose Smut (Ustilago tritici)",
            "symptoms": ["Entire ear head turned into black powdery fungal mass", "Grains replaced by dark spores"],
            "severity": "High",
            "organic_cure": "Solar heat treatment of seed during bright summer days for 4 hours.",
            "chemical_cure": "Seed treatment with Carboxin 75 WP (Vitavax) @ 2.5 g/kg seed before sowing.",
            "prevention": "Rogue out smutted heads early in morning in polythene bags and destroy by burning."
        }
    ],
    "Rice": [
        {
            "disease": "Rice Blast (Magnaporthe oryzae)",
            "symptoms": ["Spindle / eye-shaped lesions with grey center and brown border on leaves", "Blackening of panicle neck (Neck Blast)"],
            "severity": "Critical",
            "organic_cure": "Spray Pseudomonas fluorescens @ 10 g/L or 2% Neem oil formulation.",
            "chemical_cure": "Tricyclazole 75 WP @ 0.6 g/L or Isoprothiolane 40 EC @ 1.5 ml/L.",
            "prevention": "Avoid split heavy doses of nitrogen; maintain proper spacing and drainage."
        },
        {
            "disease": "Bacterial Leaf Blight (BLB - Xanthomonas oryzae)",
            "symptoms": ["Water-soaked translucent stripes on leaf margins", "Milky bacterial ooze droplets in morning", "Leaves dry and turn bleached white"],
            "severity": "High",
            "organic_cure": "Spray fresh cow dung extract (20%) supernatant twice at 15-day interval.",
            "chemical_cure": "Streptocycline (antibiotic) @ 0.1 g/L combined with Copper Oxychloride @ 1.25 g/L.",
            "prevention": "Avoid clipping seedling tips during transplanting; drain excess water from field."
        }
    ],
    "Cotton": [
        {
            "disease": "Cotton Bollworm / Pink Bollworm",
            "symptoms": ["Bored holes in flower buds and bolls", "Rosetted flowers that fail to open", "Stained lint and premature boll drop"],
            "severity": "Critical",
            "organic_cure": "Install Pheromone traps @ 5/acre for monitoring; release Trichogramma egg parasitoids @ 60,000/acre.",
            "chemical_cure": "Chlorantraniliprole 18.5 SC @ 0.3 ml/L or Emamectin Benzoate 5 SG @ 0.5 g/L.",
            "prevention": "Avoid extending the cotton season beyond 160-180 days to break pest lifecycle."
        },
        {
            "disease": "Cotton Leaf Curl Virus (CLCuD)",
            "symptoms": ["Upward or downward cupping of leaves", "Thickened leaf veins with enations (leafy outgrowths on underside)"],
            "severity": "High",
            "organic_cure": "Neem seed kernel extract (NSKE 5%) spray every 10 days to deter Whitefly vectors.",
            "chemical_cure": "Flonicamid 50 WG @ 0.3 g/L or Spiromesifen 22.9 SC @ 1 ml/L.",
            "prevention": "Eradicate weed hosts (such as Parthenium and Xanthium) around field borders."
        }
    ],
    "Maize (Corn)": [
        {
            "disease": "Fall Armyworm (Spodoptera frugiperda)",
            "symptoms": ["Ragged feeding holes on whorl leaves", "Abundant sawdust-like frass inside the plant whorl", "Damaged growing tip"],
            "severity": "Critical",
            "organic_cure": "Apply neem cake in the whorl; release egg parasitoid Telenomus remus; spray Metarhizium anisopliae @ 5 g/L.",
            "chemical_cure": "Chlorantraniliprole 18.5 SC @ 0.4 ml/L or Spinetoram 11.7 SC @ 0.5 ml/L directed into the central whorl.",
            "prevention": "Intercrop with pulses (Cowpea/Mungbean) to encourage natural predators."
        }
    ]
}


def diagnose_by_crop_and_symptom(crop: str, symptom_keyword: str):
    """
    Matches user-observed symptoms to the disease database.
    """
    diseases = DISEASE_DB.get(crop, [])
    matches = []
    
    keyword_clean = symptom_keyword.strip().lower()

    for item in diseases:
        score = 0
        all_symptom_text = " ".join(item["symptoms"]).lower()
        if keyword_clean in all_symptom_text or keyword_clean in item["disease"].lower():
            score += 2
        for word in keyword_clean.split():
            if len(word) > 2 and word in all_symptom_text:
                score += 1
        
        # Even if low score, present the relevant entry
        matches.append({
            "disease": item["disease"],
            "match_confidence": min(95, 60 + score * 15) if score > 0 else 50,
            "severity": item["severity"],
            "symptoms": item["symptoms"],
            "organic_cure": item["organic_cure"],
            "chemical_cure": item["chemical_cure"],
            "prevention": item["prevention"]
        })

    matches.sort(key=lambda x: x["match_confidence"], reverse=True)
    return matches
