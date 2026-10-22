"""
Government Agricultural Schemes & Subsidies Database (Kisan Kalyan Portal)
Provides eligibility criteria, benefit amounts, and application details for key Indian agricultural schemes.
"""

GOVT_SCHEMES = [
    {
        "id": "pm_kisan",
        "name": "PM-Kisan Samman Nidhi Yojana",
        "category": "Direct Income Support",
        "benefit": "₹6,000 / year (in 3 equal installments of ₹2,000 directly into bank account)",
        "eligibility": "All landholding farmer families with cultivable land in their name.",
        "documents": ["Aadhaar Card", "Land Ownership Papers (7/12 or Khatauni)", "Bank Account linked to Aadhaar"],
        "official_url": "https://pmkisan.gov.in/",
        "icon": "💰"
    },
    {
        "id": "pmfby",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "category": "Crop Insurance & Disaster Relief",
        "benefit": "Comprehensive insurance coverage against crop failure due to drought, floods, pests, or hailstorms. Premium: only 1.5% - 2% paid by farmer.",
        "eligibility": "All farmers growing notified crops in notified areas (both loanee and non-loanee farmers).",
        "documents": ["Crop Sowing Certificate", "Land Revenue Record", "Bank Passbook", "Aadhaar Card"],
        "official_url": "https://pmfby.gov.in/",
        "icon": "🛡️"
    },
    {
        "id": "pm_kusum",
        "name": "PM-KUSUM (Solar Agricultural Pump Subsidy)",
        "category": "Renewable Energy & Irrigation Subsidy",
        "benefit": "Up to 60% government subsidy (Central + State) on installing standalone solar water pumps.",
        "eligibility": "Individual farmers, groups of farmers, Water User Associations, and Cooperatives.",
        "documents": ["Aadhaar Card", "Land Record showing irrigation need", "Bank details", "Electricity bill (if grid-connected)"],
        "official_url": "https://pmkusum.mnre.gov.in/",
        "icon": "☀️"
    },
    {
        "id": "kcc",
        "name": "Kisan Credit Card (KCC) Scheme",
        "category": "Low-Interest Farm Credit",
        "benefit": "Short-term farm credit up to ₹3,00,000 at a subsidized interest rate of effectively 4% per annum (with prompt repayment).",
        "eligibility": "All farmers, sharecroppers, tenant farmers, and self-help groups.",
        "documents": ["Duly filled application form", "Identity & Address proof (Aadhaar/Voter ID)", "Land cultivation proof"],
        "official_url": "https://myscheme.gov.in/schemes/kcc",
        "icon": "💳"
    },
    {
        "id": "micro_irrigation",
        "name": "Per Drop More Crop (Micro Irrigation / Drip & Sprinkler)",
        "category": "Irrigation Equipment Subsidy",
        "benefit": "45% to 55% subsidy on installation of Drip and Sprinkler irrigation systems to save water.",
        "eligibility": "Small and marginal farmers get up to 55% subsidy; other farmers get 45% subsidy.",
        "documents": ["Land records", "Soil & Water test report", "Quotation from approved drip supplier"],
        "official_url": "https://pmksy.gov.in/",
        "icon": "💧"
    },
    {
        "id": "soil_health",
        "name": "Soil Health Card Scheme (SHC)",
        "category": "Soil Testing & Fertility",
        "benefit": "Free lab testing of soil every 2 years with crop-wise nutrient recommendations.",
        "eligibility": "Open to all farmers across India.",
        "documents": ["Soil sample from farm", "Farmer Aadhaar & contact number"],
        "official_url": "https://soilhealth.dac.gov.in/",
        "icon": "🧪"
    }
]
