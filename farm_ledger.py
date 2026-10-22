"""
Kisan Bahi-Khata (Farm Financial Accounting & P&L Statement)
Enables farmers to track itemized input expenditures and evaluate commercial profitability.
"""

import pandas as pd

def calculate_farm_pnl(seed_cost: float, fert_cost: float, pest_cost: float, machinery_cost: float, labor_cost: float, other_cost: float, yield_quintals: float, selling_price: float):
    """
    Computes total input cost, gross revenue, net profit, break-even price, and expense distribution.
    """
    total_cost = seed_cost + fert_cost + pest_cost + machinery_cost + labor_cost + other_cost
    gross_revenue = yield_quintals * selling_price
    net_profit = gross_revenue - total_cost
    
    profit_margin = (net_profit / gross_revenue * 100) if gross_revenue > 0 else 0.0
    cost_per_quintal = (total_cost / yield_quintals) if yield_quintals > 0 else 0.0
    break_even_price = cost_per_quintal # Price at which profit is exactly 0

    expense_breakdown = pd.DataFrame({
        "Category": ["Seeds", "Fertilizers & Manure", "Pesticides & Bio-agents", "Tractor & Machinery", "Labor Wages", "Irrigation & Misc"],
        "Amount (₹)": [seed_cost, fert_cost, pest_cost, machinery_cost, labor_cost, other_cost]
    })
    
    # Calculate percentages
    if total_cost > 0:
        expense_breakdown["Percentage (%)"] = (expense_breakdown["Amount (₹)"] / total_cost * 100).round(1)
    else:
        expense_breakdown["Percentage (%)"] = 0.0

    return {
        "total_cost": round(total_cost),
        "gross_revenue": round(gross_revenue),
        "net_profit": round(net_profit),
        "profit_margin_pct": round(profit_margin, 1),
        "break_even_price": round(break_even_price, 1),
        "cost_per_quintal": round(cost_per_quintal, 1),
        "expense_breakdown": expense_breakdown
    }
