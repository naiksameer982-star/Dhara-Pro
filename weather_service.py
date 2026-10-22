"""
Weather & Agricultural Climate Advisory Module
Integrates with the free Open-Meteo Geocoding & Weather APIs (No API key required)
to deliver real-time meteorological metrics and practical farming advisories.
"""

import requests

WEATHER_CODE_MAP = {
    0: "Clear Sky ☀️",
    1: "Mainly Clear 🌤️",
    2: "Partly Cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Depositing Rime Fog 🌫️",
    51: "Light Drizzle 🌦️",
    53: "Moderate Drizzle 🌦️",
    55: "Dense Drizzle 🌧️",
    61: "Slight Rain 🌧️",
    63: "Moderate Rain 🌧️",
    65: "Heavy Rain ⛈️",
    71: "Slight Snow ❄️",
    73: "Moderate Snow ❄️",
    75: "Heavy Snow ❄️",
    80: "Slight Rain Showers 🌦️",
    81: "Moderate Rain Showers 🌧️",
    82: "Violent Rain Showers ⛈️",
    95: "Thunderstorm 🌩️",
    96: "Thunderstorm with Slight Hail ⛈️",
    99: "Thunderstorm with Heavy Hail ⛈️"
}


def get_coordinates_for_city(city_name: str):
    """
    Looks up latitude and longitude using Open-Meteo geocoding.
    """
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if "results" in data and len(data["results"]) > 0:
                item = data["results"][0]
                return {
                    "name": item.get("name"),
                    "country": item.get("country", ""),
                    "admin1": item.get("admin1", ""), # state/province
                    "lat": item.get("latitude"),
                    "lon": item.get("longitude")
                }
    except Exception:
        pass
    return None


def fetch_farm_weather(city_name: str = "New Delhi"):
    """
    Fetches real-time and 5-day weather data for the specified location,
    plus generates intelligent agricultural warnings (spraying conditions, irrigation need).
    """
    geo = get_coordinates_for_city(city_name)
    if not geo:
        # Fallback default location if offline or city not found
        geo = {"name": city_name, "country": "India", "admin1": "Region", "lat": 28.6139, "lon": 77.2090}

    lat, lon = geo["lat"], geo["lon"]

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max"
            f"&timezone=auto"
        )
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            data = res.json()
            curr = data.get("current", {})
            daily = data.get("daily", {})

            temp = curr.get("temperature_2m", 26.0)
            humidity = curr.get("relative_humidity_2m", 60)
            wind = curr.get("wind_speed_10m", 8.0)
            precip = curr.get("precipitation", 0.0)
            code = curr.get("weather_code", 0)
            condition = WEATHER_CODE_MAP.get(code, "Clear / Mild")

            # Compute Farming Advisories
            advisories = []
            
            # 1. Spraying Advisory
            if wind > 15:
                advisories.append({
                    "title": "💨 Spraying Warning",
                    "status": "Unfavorable",
                    "color": "red",
                    "message": f"High wind speed ({wind} km/h). Avoid pesticide or herbicide spray due to heavy drift risk."
                })
            elif precip > 1.0 or (daily.get("precipitation_probability_max") and daily["precipitation_probability_max"][0] > 60):
                advisories.append({
                    "title": "🌧️ Spraying Warning",
                    "status": "Unfavorable",
                    "color": "red",
                    "message": "Rain is likely today. Chemical sprays will wash off. Postpone application by 24-48 hours."
                })
            else:
                advisories.append({
                    "title": "✅ Spraying Condition",
                    "status": "Favorable",
                    "color": "green",
                    "message": "Calm winds and low rain probability. Ideal window for foliar fertilizer or pest spraying."
                })

            # 2. Irrigation Advisory
            next_24h_rain = (daily.get("precipitation_sum") or [0])[0]
            if next_24h_rain > 10.0:
                advisories.append({
                    "title": "💧 Irrigation Recommendation",
                    "status": "Skip Irrigation",
                    "color": "blue",
                    "message": f"Forecast shows substantial rainfall (~{next_24h_rain:.1f} mm). Hold back irrigation to conserve water and avoid root suffocation."
                })
            elif temp > 34:
                advisories.append({
                    "title": "💧 Irrigation Recommendation",
                    "status": "Urgent Watering",
                    "color": "orange",
                    "message": f"High daytime temperature ({temp}°C). Provide light evening irrigation or mulch to protect root zone moisture."
                })
            else:
                advisories.append({
                    "title": "💧 Irrigation Recommendation",
                    "status": "Normal Cycle",
                    "color": "green",
                    "message": "Normal soil moisture consumption. Follow standard irrigation rotation for your current crop stage."
                })

            forecast_days = []
            dates = daily.get("time", [])[:5]
            max_temps = daily.get("temperature_2m_max", [])[:5]
            min_temps = daily.get("temperature_2m_min", [])[:5]
            rain_sums = daily.get("precipitation_sum", [])[:5]
            codes = daily.get("weather_code", [])[:5]

            for i in range(len(dates)):
                forecast_days.append({
                    "date": dates[i],
                    "max_temp": max_temps[i] if i < len(max_temps) else 30,
                    "min_temp": min_temps[i] if i < len(min_temps) else 20,
                    "rain_mm": rain_sums[i] if i < len(rain_sums) else 0.0,
                    "condition": WEATHER_CODE_MAP.get(codes[i] if i < len(codes) else 0, "Clear")
                })

            return {
                "city": geo["name"],
                "region": geo["admin1"] + (f", {geo['country']}" if geo['country'] else ""),
                "temperature": temp,
                "humidity": humidity,
                "wind_speed": wind,
                "condition": condition,
                "advisories": advisories,
                "forecast": forecast_days,
                "success": True
            }
    except Exception as e:
        pass

    # Safe fallback if network error
    return {
        "city": city_name,
        "region": "Station Offline (Demo Mode)",
        "temperature": 27.5,
        "humidity": 65,
        "wind_speed": 9.2,
        "condition": "Partly Cloudy ⛅",
        "advisories": [
            {
                "title": "✅ Spraying Condition",
                "status": "Favorable",
                "color": "green",
                "message": "Mild weather conditions. Suitable for agricultural operations."
            },
            {
                "title": "💧 Irrigation Recommendation",
                "status": "Normal Cycle",
                "color": "green",
                "message": "Maintain standard scheduled irrigation intervals."
            }
        ],
        "forecast": [
            {"date": "Day 1", "max_temp": 31, "min_temp": 21, "rain_mm": 0.0, "condition": "Sunny ☀️"},
            {"date": "Day 2", "max_temp": 32, "min_temp": 22, "rain_mm": 2.0, "condition": "Partly Cloudy ⛅"},
            {"date": "Day 3", "max_temp": 29, "min_temp": 20, "rain_mm": 8.0, "condition": "Showers 🌦️"},
            {"date": "Day 4", "max_temp": 28, "min_temp": 19, "rain_mm": 0.5, "condition": "Overcast ☁️"},
            {"date": "Day 5", "max_temp": 30, "min_temp": 20, "rain_mm": 0.0, "condition": "Sunny ☀️"}
        ],
        "success": False
    }
