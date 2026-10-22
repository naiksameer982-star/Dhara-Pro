"""
Agricultural Market & Mandi Price Intelligence Module
Tracks benchmark commodity rates, market trends, and calculates estimated farm revenues.
"""

import pandas as pd
import numpy as np

MARKET_COMMODITIES = {
    "Wheat": {
        "modal_price": 2425, # INR per quintal (100 kg)
        "min_price": 2275,
        "max_price": 2580,
        "msp": 2275, # Minimum Support Price
        "change_pct": +2.4,
        "trend": "Bullish 📈",
        "avg_yield_per_acre": 18, # Quintals
        "cost_per_acre": 16000 # INR estimated cost of cultivation
    },
    "Paddy (Basmati)": {
        "modal_price": 3650,
        "min_price": 3200,
        "max_price": 4100,
        "msp": 2300,
        "change_pct": +3.1,
        "trend": "Bullish 📈",
        "avg_yield_per_acre": 22,
        "cost_per_acre": 22000
    },
    "Cotton (Medium Staple)": {
        "modal_price": 7120,
        "min_price": 6800,
        "max_price": 7500,
        "msp": 7121,
        "change_pct": -0.8,
        "trend": "Neutral ⚖️",
        "avg_yield_per_acre": 10,
        "cost_per_acre": 26000
    },
    "Soybean (Yellow)": {
        "modal_price": 4650,
        "min_price": 4350,
        "max_price": 4850,
        "msp": 4600,
        "change_pct": +1.5,
        "trend": "Bullish 📈",
        "avg_yield_per_acre": 9,
        "cost_per_acre": 14000
    },
    "Maize (Corn)": {
        "modal_price": 2150,
        "min_price": 1950,
        "max_price": 2300,
        "msp": 2090,
        "change_pct": +1.8,
        "trend": "Bullish 📈",
        "avg_yield_per_acre": 25,
        "cost_per_acre": 18000
    },
    "Mustard (Rapeseed)": {
        "modal_price": 5450,
        "min_price": 5100,
        "max_price": 5700,
        "msp": 5650,
        "change_pct": -1.2,
        "trend": "Bearish 📉",
        "avg_yield_per_acre": 8,
        "cost_per_acre": 13000
    },
    "Potato (Jyoti)": {
        "modal_price": 1450,
        "min_price": 1150,
        "max_price": 1750,
        "msp": None,
        "change_pct": +4.6,
        "trend": "Bullish 📈",
        "avg_yield_per_acre": 95,
        "cost_per_acre": 45000
    },
    "Onion (Red Nashik)": {
        "modal_price": 2100,
        "min_price": 1600,
        "max_price": 2600,
        "msp": None,
        "change_pct": -3.5,
        "trend": "Bearish 📉",
        "avg_yield_per_acre": 80,
        "cost_per_acre": 48000
    }
}


def get_market_summary():
    """
    Returns a dataframe of live market rates across key agricultural commodities.
    """
    rows = []
    for crop, data in MARKET_COMMODITIES.items():
        rows.append({
            "Commodity": crop,
            "Modal Price (₹/Qtl)": f"₹{data['modal_price']:,}",
            "Min Price (₹)": f"₹{data['min_price']:,}",
            "Max Price (₹)": f"₹{data['max_price']:,}",
            "Govt. MSP (₹)": f"₹{data['msp']:,}" if data['msp'] else "Market Driven",
            "24h Change": f"{'+' if data['change_pct'] > 0 else ''}{data['change_pct']}%",
            "Market Trend": data["trend"]
        })
    return pd.DataFrame(rows)


def generate_price_history(crop_name: str, days: int = 14):
    """
    Generates synthetic historical daily prices simulating mandi auction volatility.
    """
    base = MARKET_COMMODITIES.get(crop_name, {}).get("modal_price", 2500)
    np.random.seed(sum(ord(c) for c in crop_name))
    
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days).strftime("%d %b")
    # Random walk around the base price
    noise = np.random.normal(0, base * 0.015, days).cumsum()
    prices = np.round(base + noise).astype(int)
    
    df = pd.DataFrame({
        "Date": dates,
        "Price (₹/Quintal)": prices
    })
    return df


def calculate_estimated_profit(crop_name: str, acres: float, expected_yield_per_acre: float = None):
    """
    Computes estimated gross revenue, costs, and net farm profit.
    """
    data = MARKET_COMMODITIES.get(crop_name, MARKET_COMMODITIES["Wheat"])
    yield_qtl = expected_yield_per_acre if expected_yield_per_acre else data["avg_yield_per_acre"]
    total_yield = yield_qtl * acres
    
    gross_revenue = total_yield * data["modal_price"]
    total_cost = data["cost_per_acre"] * acres
    net_profit = gross_revenue - total_cost
    roi = (net_profit / total_cost * 100) if total_cost > 0 else 0

    return {
        "crop": crop_name,
        "acres": acres,
        "total_yield_qtl": round(total_yield, 1),
        "price_per_qtl": data["modal_price"],
        "gross_revenue": round(gross_revenue),
        "estimated_costs": round(total_cost),
        "net_profit": round(net_profit),
        "roi_pct": round(roi, 1)
    }
