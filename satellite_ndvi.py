"""
Satellite & NDVI Crop Health Intelligence Module
Simulates multispectral satellite telemetry (Sentinel-2 / Landsat) to compute
Normalized Difference Vegetation Index (NDVI) and partition farm plots into precision zones.
"""

import numpy as np
import pandas as pd

def generate_ndvi_field_scan(crop_name: str = "Wheat", field_id: str = "Plot-A (North Field)", grid_size: int = 6):
    """
    Simulates a multispectral satellite scan over a farm plot.
    Returns:
    - NDVI grid (2D array of values 0.2 to 0.88)
    - Health zone percentages
    - Target precision actions
    """
    np.random.seed(sum(ord(c) for c in crop_name + field_id))
    
    # Generate realistic spatial NDVI values
    base_ndvi = 0.68
    grid = np.random.normal(base_ndvi, 0.12, (grid_size, grid_size))
    grid = np.clip(grid, 0.20, 0.88)
    
    # Calculate zone statistics
    total_pixels = grid_size * grid_size
    healthy_count = np.sum(grid >= 0.60)
    moderate_count = np.sum((grid >= 0.40) & (grid < 0.60))
    stressed_count = np.sum(grid < 0.40)

    healthy_pct = round((healthy_count / total_pixels) * 100, 1)
    moderate_pct = round((moderate_count / total_pixels) * 100, 1)
    stressed_pct = round((stressed_count / total_pixels) * 100, 1)

    avg_ndvi = round(float(np.mean(grid)), 2)

    # Precision Farming Recommendations based on satellite scan
    prescriptions = []
    if stressed_pct > 15:
        prescriptions.append({
            "zone": "Red Zone (Critical Stress)",
            "area_pct": f"{stressed_pct}%",
            "diagnosis": "Severe canopy thinning or moisture drought detected.",
            "action": "Inspect irrigation nozzles in the eastern sector. Check for localized termite or root-knot nematode attack."
        })
    if moderate_pct > 25:
        prescriptions.append({
            "zone": "Yellow Zone (Moderate Vegetative Vigor)",
            "area_pct": f"{moderate_pct}%",
            "diagnosis": "Mild nitrogen deficiency causing pale leaf yellowing.",
            "action": "Variable-rate top-dressing: apply 15 kg Urea per acre specifically to this patch."
        })
    prescriptions.append({
        "zone": "Green Zone (High Vigor)",
        "area_pct": f"{healthy_pct}%",
        "diagnosis": "Optimal photosynthetic activity and robust biomass accumulation.",
        "action": "Maintain current nutrient and watering schedule."
    })

    # Prepare DataFrame for heatmap visualization
    df_grid = pd.DataFrame(
        np.round(grid, 2),
        columns=[f"Sector {j+1}" for j in range(grid_size)],
        index=[f"Row {i+1}" for i in range(grid_size)]
    )

    return {
        "field_id": field_id,
        "crop": crop_name,
        "avg_ndvi": avg_ndvi,
        "healthy_pct": healthy_pct,
        "moderate_pct": moderate_pct,
        "stressed_pct": stressed_pct,
        "grid_df": df_grid,
        "prescriptions": prescriptions
    }
