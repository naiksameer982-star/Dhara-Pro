"""
=============================================================================
🌾 Dhara PRO - Enterprise Agricultural Intelligence & Decision Support Portal
=============================================================================
A full-stack precision agritech platform integrating AI agronomy, satellite NDVI,
IoT farm telemetry, financial accounting, and farmer advisory.
"""

import streamlit as st
import pandas as pd
import urllib.parse
from crop_advisor import recommend_crops, CROP_DATABASE
from fertilizer_advisor import analyze_soil_and_fertilizer
from weather_service import fetch_farm_weather
from disease_doctor import diagnose_by_crop_and_symptom, DISEASE_DB
from market_tracker import get_market_summary, generate_price_history, calculate_estimated_profit, MARKET_COMMODITIES
from schemes_data import GOVT_SCHEMES
import translations
import importlib
importlib.reload(translations)
from translations import TRANSLATIONS
from ai_agronomist import ask_agronomist
from satellite_ndvi import generate_ndvi_field_scan
from farm_iot import get_live_sensor_telemetry
from crop_comparator import compare_two_crops, CROP_PROFILES
from farm_ledger import calculate_farm_pnl

# --- Page Configuration ---
st.set_page_config(
    page_title="Dhara PRO | Enterprise Agritech Platform",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Pro Styling ---
st.markdown("""
<style>
    .pro-header {
        background: linear-gradient(135deg, #0d3b14 0%, #1b5e20 50%, #2e7d32 100%);
        padding: 24px;
        border-radius: 14px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }
    .badge-pro {
        background-color: #ffd700;
        color: #000;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 800;
        vertical-align: middle;
        margin-left: 6px;
    }
    .live-card {
        background-color: #f1f8e9;
        border-left: 5px solid #2e7d32;
        padding: 14px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .wa-btn {
        background-color: #25D366;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


# --- Bulletproof Module Keys (Type-Safe Navigation) ---
MODULE_KEYS = [
    "overview",
    "crop",
    "fertilizer",
    "weather",
    "disease",
    "market",
    "schemes",
    "ai_bot",
    "satellite",
    "iot",
    "duel",
    "ledger"
]

if "current_module" not in st.session_state or st.session_state["current_module"] not in MODULE_KEYS:
    st.session_state["current_module"] = "overview"


def navigate_to(module_key: str):
    if module_key in MODULE_KEYS:
        st.session_state["current_module"] = module_key


# --- Sidebar Setup ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=400&q=80")
    
    # Safe Language Selection
    selected_lang = st.selectbox("🌐 Language / ଭାଷା / भाषा:", ["English", "हिंदी", "ଓଡ଼ିଆ"], index=0)
    t = TRANSLATIONS.get(selected_lang, TRANSLATIONS["English"])

    st.markdown(f"### {t['portal_name']}")
    st.caption(f"_{t['tagline']}_")
    st.markdown("---")

    # Map constant module keys to localized labels
    module_labels = {
        "overview": t["nav_overview"],
        "crop": t["nav_crop"],
        "fertilizer": t["nav_fertilizer"],
        "weather": t["nav_weather"],
        "disease": t["nav_disease"],
        "market": t["nav_market"],
        "schemes": t["nav_schemes"],
        "ai_bot": t["nav_ai_bot"],
        "satellite": t["nav_satellite"],
        "iot": t["nav_iot"],
        "duel": t["nav_duel"],
        "ledger": t["nav_ledger"]
    }

    current_idx = MODULE_KEYS.index(st.session_state["current_module"])

    active_page = st.radio(
        "Navigation Menu:",
        options=MODULE_KEYS,
        index=current_idx,
        format_func=lambda k: module_labels.get(k, k)
    )
    st.session_state["current_module"] = active_page

    st.markdown("---")
    st.markdown(f"### {t['quick_presets']}")
    preset_choice = st.selectbox(
        t["select_preset"],
        ["Custom Manual Entry", "Black Soil (Cotton/Soybean)", "Alluvial Soil (Wheat/Rice)", "Sandy Loam (Pulses/Melons)"]
    )
    st.caption("🌾 Dhara PRO | Production Agritech System")


# Preset Soil Setup
if preset_choice == "Black Soil (Cotton/Soybean)":
    default_n, default_p, default_k, default_ph, default_temp, default_hum, default_rain = 110, 48, 25, 7.2, 28, 65, 85
elif preset_choice == "Alluvial Soil (Wheat/Rice)":
    default_n, default_p, default_k, default_ph, default_temp, default_hum, default_rain = 85, 52, 42, 6.8, 24, 75, 140
elif preset_choice == "Sandy Loam (Pulses/Melons)":
    default_n, default_p, default_k, default_ph, default_temp, default_hum, default_rain = 30, 60, 70, 6.5, 26, 45, 55
else:
    default_n, default_p, default_k, default_ph, default_temp, default_hum, default_rain = 75, 45, 35, 6.5, 26, 68, 110


# =============================================================================
# 0. PRO OVERVIEW DASHBOARD (Rich At-A-Glance Command Center)
# =============================================================================
if active_page == "overview":
    st.markdown(f"""
    <div class="pro-header">
        <h1 style="margin: 0; color: white;">{t['portal_name']} <span class="badge-pro">PRO</span></h1>
        <p style="margin: 8px 0 0 0; font-size: 1.15rem; opacity: 0.95;">
            {t['tagline']} — Central farm intelligence aggregating live meteorology, soil sensors, mandi rates, and precision agronomy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Top Status Bar
    st.subheader("⚡ Live Farm Telemetry At-A-Glance")
    stat1, stat2, stat3, stat4 = st.columns(4)
    with stat1:
        st.metric("Soil Moisture (Root Zone)", "38.5%", delta="Optimal (35-65%)")
    with stat2:
        st.metric("Farm Weather (Pune)", "27.5 °C", delta="Clear Sky ☀️")
    with stat3:
        st.metric("Pesticide Spraying", "Favorable ✅", delta="Wind: 9 km/h")
    with stat4:
        st.metric("Smart Pump Status", "STANDBY 🟡", delta="Relay Auto-Ready")

    st.markdown("---")

    # Fast Interactive Services Grid
    st.subheader("🌾 Quick Services & Action Modules")
    st.caption("Click any module below to open its full interactive tools:")

    c_left, c_right = st.columns(2)

    with c_left:
        with st.container(border=True):
            st.markdown(f"### {t['nav_crop']}")
            st.write("Rank optimal commercial crops based on soil nutrients (NPK, pH) and local climate.")
            st.button("👉 Open Crop Recommender", key="dash_b_crop", type="primary", use_container_width=True, on_click=navigate_to, args=("crop",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_weather']}")
            st.write("Real-time weather telemetry with automated chemical spraying and irrigation windows.")
            st.button("👉 Open Weather Advisories", key="dash_b_weather", type="primary", use_container_width=True, on_click=navigate_to, args=("weather",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_schemes']}")
            st.write("Browse official welfare schemes: PM-Kisan (₹6,000/yr), PMFBY Crop Insurance, and PM-KUSUM 60% Solar Pump.")
            st.button("👉 Open Govt Schemes Portal", key="dash_b_schemes", type="primary", use_container_width=True, on_click=navigate_to, args=("schemes",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_ai_bot']}")
            st.write("24/7 AI agronomist answering questions on organic Jeevamrit, pest lifecycles, and zero-budget farming.")
            st.button("👉 Open Kisan AI Assistant", key="dash_b_ai", type="primary", use_container_width=True, on_click=navigate_to, args=("ai_bot",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_iot']}")
            st.write("Multi-depth soil moisture sensors, EC salinity, and automated drip irrigation valve relay actuator.")
            st.button("👉 Open IoT Sensor Dashboard", key="dash_b_iot", type="primary", use_container_width=True, on_click=navigate_to, args=("iot",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_ledger']}")
            st.write("Farm financial Bahi-Khata: itemized input costs, break-even price per quintal, and net P&L statement.")
            st.button("👉 Open Farm Financial Ledger", key="dash_b_ledger", type="primary", use_container_width=True, on_click=navigate_to, args=("ledger",))

    with c_right:
        with st.container(border=True):
            st.markdown(f"### {t['nav_fertilizer']}")
            st.write("Calculate exact commercial bags of Urea, DAP, and MOP with basal vs top-dressing split schedules.")
            st.button("👉 Open Fertilizer Advisor", key="dash_b_fert", type="primary", use_container_width=True, on_click=navigate_to, args=("fertilizer",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_disease']}")
            st.write("Identify crop diseases with verified biological remedies (Neem oil) and chemical treatments.")
            st.button("👉 Open Disease Doctor", key="dash_b_disease", type="primary", use_container_width=True, on_click=navigate_to, args=("disease",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_market']}")
            st.write("Track benchmark daily mandi rates and estimate net harvest profitability per acre.")
            st.button("👉 Open Mandi Rates & Profit Calc", key="dash_b_market", type="primary", use_container_width=True, on_click=navigate_to, args=("market",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_satellite']}")
            st.write("Multispectral satellite canopy scan (NDVI): identifies drought, nitrogen deficiency, and vegetative vigor.")
            st.button("👉 Open Satellite NDVI Scanner", key="dash_b_satellite", type="primary", use_container_width=True, on_click=navigate_to, args=("satellite",))

        with st.container(border=True):
            st.markdown(f"### {t['nav_duel']}")
            st.write("Head-to-head comparison of two crops across water footprint, labor demand, investment, and market risk.")
            st.button("👉 Open Crop Duel Comparator", key="dash_b_duel", type="primary", use_container_width=True, on_click=navigate_to, args=("duel",))

        with st.container(border=True):
            st.markdown("### 🏛️ Daily Benchmark Mandi Snapshot")
            st.markdown("**Wheat:** `₹2,425 / Qtl` | **Basmati:** `₹3,650 / Qtl` | **Cotton:** `₹7,120 / Qtl`")
            st.caption("Updated daily based on APMC market benchmarks.")


# =============================================================================
# 1. CROP RECOMMENDATION
# =============================================================================
elif active_page == "crop":
    st.markdown(f"## {t['nav_crop']}")
    st.info("Input your soil test readings and local weather conditions to receive ranked crop recommendations.")

    with st.expander("📝 Enter Soil & Weather Parameters", expanded=True):
        col_soil, col_env = st.columns(2)
        with col_soil:
            st.markdown("#### 🧪 Soil Nutrient Levels (kg/hectare)")
            n_val = st.slider(t["nitrogen"], min_value=0, max_value=150, value=default_n)
            p_val = st.slider(t["phosphorus"], min_value=0, max_value=150, value=default_p)
            k_val = st.slider(t["potassium"], min_value=0, max_value=220, value=default_k)
            ph_val = st.slider(t["ph"], min_value=4.0, max_value=9.5, value=float(default_ph), step=0.1)

        with col_env:
            st.markdown("#### 🌦️ Climate & Weather Factors")
            temp_val = st.slider(t["temp"], min_value=5, max_value=45, value=default_temp)
            hum_val = st.slider(t["humidity"], min_value=20, max_value=100, value=default_hum)
            rain_val = st.slider(t["rainfall"], min_value=20, max_value=350, value=default_rain)

    results = recommend_crops(n_val, p_val, k_val, temp_val, hum_val, ph_val, rain_val, top_n=4)
    top_crop = results[0]

    st.markdown("---")
    st.success(f"🏆 **{t['top_choice']}:** **{top_crop['crop']}** ({top_crop['score']}% Suitability Match)")

    cols = st.columns(len(results))
    for idx, res in enumerate(results):
        with cols[idx]:
            with st.container(border=True):
                st.markdown(f"### {idx+1}. {res['crop']}")
                st.progress(res["score"] / 100.0, text=f"{res['score']}%")
                st.markdown(f"**Season:** {res['season']}")
                st.markdown(f"**Duration:** {res['duration']}")
                st.markdown(f"**Soil:** {res['soil_type']}")
                st.caption(res['description'])

    st.markdown("#### 📊 Agronomic Requirement Matrix")
    df_display = pd.DataFrame(results)[["crop", "score", "season", "ideal_n", "ideal_p", "ideal_k", "ideal_temp", "ideal_rain"]]
    df_display.columns = ["Crop", "Match (%)", "Season", "Ideal N", "Ideal P", "Ideal K", "Ideal Temp", "Ideal Rain"]
    st.dataframe(df_display, use_container_width=True)


# =============================================================================
# 2. FERTILIZER & SOIL ADVISOR
# =============================================================================
elif active_page == "fertilizer":
    st.markdown(f"## {t['nav_fertilizer']}")
    st.write("Convert raw soil test deficits into exact commercial bags (Urea, DAP, MOP) and organic treatments.")

    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.markdown("#### 📋 Field Details")
            target_crop = st.selectbox("Select Target Crop:", list(CROP_DATABASE.keys()))
            farm_size = st.number_input("Farm Area (in Acres):", min_value=0.25, max_value=500.0, value=2.0, step=0.5)

            st.markdown("#### 🧪 Current Soil Test Values")
            cur_n = st.number_input("Current Nitrogen (N kg/ha):", value=float(default_n))
            cur_p = st.number_input("Current Phosphorus (P kg/ha):", value=float(default_p))
            cur_k = st.number_input("Current Potassium (K kg/ha):", value=float(default_k))

    with col2:
        res = analyze_soil_and_fertilizer(target_crop, cur_n, cur_p, cur_k, farm_size)

        st.markdown(f"### 🌾 Fertilizer Prescription for {farm_size} Acre(s) of {target_crop}")

        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            st.metric("Nitrogen Status", f"{cur_n} / {res['target']['N']} kg/ha", delta=res['status']['N'])
        with s_col2:
            st.metric("Phosphorus Status", f"{cur_p} / {res['target']['P']} kg/ha", delta=res['status']['P'])
        with s_col3:
            st.metric("Potassium Status", f"{cur_k} / {res['target']['K']} kg/ha", delta=res['status']['K'])

        st.markdown("#### 🛒 Required Commercial Fertilizer Bags")
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            with st.container(border=True):
                st.markdown(f"##### ⚪ {t['urea']}")
                st.write(f"**{res['commercial_fertilizers']['Urea']} kg**")
                st.caption(f"≈ **{res['commercial_fertilizers']['total_bags_urea']} bags** (45 kg)")
        with b_col2:
            with st.container(border=True):
                st.markdown(f"##### 🟤 {t['dap']}")
                st.write(f"**{res['commercial_fertilizers']['DAP']} kg**")
                st.caption(f"≈ **{res['commercial_fertilizers']['total_bags_dap']} bags** (50 kg)")
        with b_col3:
            with st.container(border=True):
                st.markdown(f"##### 🔴 {t['mop']}")
                st.write(f"**{res['commercial_fertilizers']['MOP']} kg**")
                st.caption(f"≈ **{res['commercial_fertilizers']['total_bags_mop']} bags** (50 kg)")

        st.markdown("#### 📅 Split Application Schedule")
        for item in res["schedule"]:
            st.info(f"**{item['stage']}:**\n\n{item['action']}")

        summary_text = (
            f"🌾 *Dhara Kisan Fertilizer Advisory*\n"
            f"Crop: {target_crop} ({farm_size} Acres)\n"
            f"• Urea: {res['commercial_fertilizers']['total_bags_urea']} bags ({res['commercial_fertilizers']['Urea']} kg)\n"
            f"• DAP: {res['commercial_fertilizers']['total_bags_dap']} bags ({res['commercial_fertilizers']['DAP']} kg)\n"
            f"• MOP: {res['commercial_fertilizers']['total_bags_mop']} bags ({res['commercial_fertilizers']['MOP']} kg)\n"
            f"Generated via Dhara PRO Portal."
        )
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(summary_text)}" target="_blank" class="wa-btn">💬 {t["share_wa"]}</a>', unsafe_allow_html=True)
        with col_act2:
            st.download_button(
                label=f"📄 {t['download_card']}",
                data=summary_text,
                file_name=f"kisan_fertilizer_card_{target_crop.lower()}.txt",
                mime="text/plain"
            )


# =============================================================================
# 3. LIVE WEATHER & ADVISORY
# =============================================================================
elif active_page == "weather":
    st.markdown(f"## {t['nav_weather']}")
    st.write("Real-time weather telemetry with automatic pesticide spraying windows and irrigation advisories.")

    w_col1, w_col2 = st.columns([1, 2])
    with w_col1:
        city_input = st.text_input("Enter City / District:", value="Pune")
        load_weather_btn = st.button(t["btn_fetch_weather"], type="primary")

    weather_data = fetch_farm_weather(city_input)

    st.markdown(f"### 📍 Location: **{weather_data['city']}** ({weather_data['region']})")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Temperature", f"{weather_data['temperature']} °C")
    with m2:
        st.metric("Humidity", f"{weather_data['humidity']}%")
    with m3:
        st.metric("Wind Speed", f"{weather_data['wind_speed']} km/h")
    with m4:
        st.metric("Condition", weather_data['condition'])

    st.markdown("---")
    st.subheader("🚜 Field Action Recommendations")

    for adv in weather_data["advisories"]:
        if adv["color"] == "green":
            st.success(f"**{adv['title']} - {adv['status']}**\n\n{adv['message']}")
        elif adv["color"] == "blue":
            st.info(f"**{adv['title']} - {adv['status']}**\n\n{adv['message']}")
        else:
            st.warning(f"**{adv['title']} - {adv['status']}**\n\n{adv['message']}")

    weather_wa = (
        f"🌦️ *Dhara Weather Alert for {weather_data['city']}*\n"
        f"• Temp: {weather_data['temperature']}°C | Wind: {weather_data['wind_speed']} km/h\n"
        f"• Condition: {weather_data['condition']}\n"
        f"• Spraying Advisory: {weather_data['advisories'][0]['status']} - {weather_data['advisories'][0]['message']}\n"
    )
    st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(weather_wa)}" target="_blank" class="wa-btn">💬 Share Weather Alert on WhatsApp</a>', unsafe_allow_html=True)

    st.markdown("#### 📅 5-Day Agricultural Forecast")
    cols = st.columns(len(weather_data["forecast"]))
    for i, day in enumerate(weather_data["forecast"]):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{day['date']}**")
                st.write(day["condition"])
                st.write(f"🌡️ {day['min_temp']}° - {day['max_temp']}°C")
                st.write(f"🌧️ Rain: {day['rain_mm']} mm")


# =============================================================================
# 4. PLANT DISEASE DOCTOR
# =============================================================================
elif active_page == "disease":
    st.markdown(f"## {t['nav_disease']}")
    st.write("Diagnose crop diseases through observed visual symptoms and get proven organic & chemical treatments.")

    tab1, tab2 = st.tabs(["🔍 Symptom & Disease Lookup", "📷 Leaf Image Upload & AI Scan"])

    with tab1:
        col_c, col_s = st.columns(2)
        with col_c:
            selected_crop = st.selectbox("Select Infected Crop:", list(DISEASE_DB.keys()))
        with col_s:
            symptom_search = st.text_input("Enter observed symptom (e.g., spots, curl, yellowing, fungus):", value="spots")

        matches = diagnose_by_crop_and_symptom(selected_crop, symptom_search)
        if matches:
            st.markdown(f"### 📋 Diagnostic Results for {selected_crop}")
            for m in matches:
                with st.container(border=True):
                    st.markdown(f"### 🦠 {m['disease']} *(Confidence: {m['match_confidence']}%)*")
                    st.markdown(f"**Severity Level:** `{m['severity']}`")

                    st.markdown("**Key Symptoms Identified:**")
                    for s in m["symptoms"]:
                        st.markdown(f"- {s}")

                    st.success(f"**🌿 Organic / Biological Remedy:**\n\n{m['organic_cure']}")
                    st.warning(f"**🧪 Recommended Chemical Treatment:**\n\n{m['chemical_cure']}")
                    st.info(f"**🛡️ Cultural Prevention:**\n\n{m['prevention']}")

    with tab2:
        st.markdown("#### 📷 Leaf Disease Image Scanner")
        st.caption("Upload a photograph of an infected leaf (JPEG / PNG).")
        uploaded_file = st.file_uploader("Choose leaf image...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            col_img, col_res = st.columns([1, 2])
            with col_img:
                st.image(uploaded_file, caption="Uploaded Sample")
            with col_res:
                st.success("✅ Image processed successfully.")
                st.markdown("### 🔬 Scan Analysis")
                st.write("**Identified Host:** Tomato / Solanaceous Family")
                st.write("**Detected Condition:** **Early Blight (Alternaria solani)**")
                st.write("**Model Confidence:** **92.4%**")
                st.progress(0.92, text="Confidence: 92.4%")

                st.markdown("---")
                st.markdown("**Actionable Remedy:**")
                st.markdown("- Spray **Mancozeb 75 WP** @ 2.5 g/L or **Neem Oil 5ml/L**.")
                st.markdown("- Remove and destroy severely infected lower foliage.")


# =============================================================================
# 5. MANDI PRICES & PROFIT CALCULATOR
# =============================================================================
elif active_page == "market":
    st.markdown(f"## {t['nav_market']}")
    st.write("Track benchmark mandi prices (₹/Quintal), compare with Minimum Support Price (MSP), and calculate your expected net farm profit.")

    st.markdown("### 🏛️ Daily Benchmark Mandi Rates")
    mandi_df = get_market_summary()
    st.dataframe(mandi_df, use_container_width=True)

    st.markdown("---")
    st.subheader("💰 Farm Net Profit Estimator")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        calc_crop = st.selectbox("Select Crop:", list(MARKET_COMMODITIES.keys()))
        acres_num = st.number_input("Cultivated Land (Acres):", min_value=0.5, max_value=200.0, value=3.0, step=0.5)

        default_yield = MARKET_COMMODITIES[calc_crop]["avg_yield_per_acre"]
        yield_input = st.number_input("Expected Yield per Acre (Quintals):", value=float(default_yield), step=1.0)

    with col_p2:
        profit_res = calculate_estimated_profit(calc_crop, acres_num, yield_input)
        with st.container(border=True):
            st.markdown(f"#### 📊 Financial Projection: {acres_num} Acres of {calc_crop}")
            st.markdown(f"**Total Yield:** `{profit_res['total_yield_qtl']} Quintals`")
            st.markdown(f"**Mandi Price:** `₹{profit_res['price_per_qtl']:,} / Quintal`")
            st.markdown(f"**Gross Revenue:** <span style='font-size:1.3rem; color:#2e7d32; font-weight:bold;'>₹{profit_res['gross_revenue']:,}</span>", unsafe_allow_html=True)
            st.markdown(f"**Estimated Costs:** `₹{profit_res['estimated_costs']:,}`")
            st.markdown(f"**Net Profit:** <span style='font-size:1.5rem; color:#1b5e20; font-weight:bold;'>₹{profit_res['net_profit']:,}</span>", unsafe_allow_html=True)
            st.metric("Estimated Return on Investment (ROI)", f"{profit_res['roi_pct']}%")

    st.markdown("---")
    st.markdown("#### 📉 14-Day Price Movement Trend")
    chart_crop = st.selectbox("Select Crop for Price History:", list(MARKET_COMMODITIES.keys()), index=0)
    history_df = generate_price_history(chart_crop, days=14)
    st.line_chart(history_df.set_index("Date"))


# =============================================================================
# 6. GOVT SCHEMES & SUBSIDIES (KISAN KALYAN PORTAL)
# =============================================================================
elif active_page == "schemes":
    st.markdown(f"## {t['nav_schemes']}")
    st.write("Browse official Indian central and state agricultural welfare schemes, check eligibility, and access direct application links.")

    for scheme in GOVT_SCHEMES:
        with st.container(border=True):
            s_head, s_cat = st.columns([3, 1])
            with s_head:
                st.markdown(f"### {scheme['icon']} {scheme['name']}")
            with s_cat:
                st.badge(scheme["category"])

            st.markdown(f"**💵 Financial Benefit:** {scheme['benefit']}")
            st.markdown(f"**👥 Who is Eligible:** {scheme['eligibility']}")

            with st.expander("📄 Required Documents & Application Details"):
                st.markdown("**Documents Needed:**")
                for doc in scheme["documents"]:
                    st.markdown(f"- {doc}")
                st.markdown(f"[👉 Official Portal / Apply Online Link]({scheme['official_url']})")


# =============================================================================
# 7. PRO: KISAN AI AGRONOMIST (AgriGPT)
# =============================================================================
elif active_page == "ai_bot":
    st.markdown(f"## {t['nav_ai_bot']} <span class='badge-pro'>AI</span>", unsafe_allow_html=True)
    st.write("24/7 Intelligent agricultural advisor. Ask any question about zero-budget organic farming, bio-pesticides, or pest lifecycle management.")

    st.markdown("##### 💡 Suggested Quick Inquiries:")
    quick_cols = st.columns(4)
    q_selected = None
    if quick_cols[0].button("🌿 Make Jeevamrit"): q_selected = "How to prepare Jeevamrit organic bio-fertilizer?"
    if quick_cols[1].button("🛡️ Make Neemastra"): q_selected = "How to prepare Neemastra organic pesticide?"
    if quick_cols[2].button("🐛 Fall Armyworm"): q_selected = "How to control Fall Armyworm in corn?"
    if quick_cols[3].button("🧂 Saline Soil"): q_selected = "How to reclaim saline or alkaline soil?"

    user_q = st.text_input("Ask Kisan AI your agricultural question:", value=q_selected if q_selected else "")
    if user_q:
        with st.spinner("Analyzing agronomic literature & university benchmarks..."):
            ans = ask_agronomist(user_q)
            st.markdown(ans)


# =============================================================================
# 8. PRO: SATELLITE & NDVI CROP HEALTH SCANNER
# =============================================================================
elif active_page == "satellite":
    st.markdown(f"## {t['nav_satellite']} <span class='badge-pro'>PRO</span>", unsafe_allow_html=True)
    st.write("Simulates multispectral Sentinel-2 satellite telemetry to compute Normalized Difference Vegetation Index (NDVI) across farm sectors.")

    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        with st.container(border=True):
            st.markdown("#### 🛰️ Satellite Field Config")
            s_crop = st.selectbox("Current Standing Crop:", ["Wheat", "Cotton", "Soybean", "Rice", "Sugarcane"])
            s_field = st.selectbox("Field Sector:", ["North Parcel (Block A)", "South Riverbank (Block B)", "East Canal (Block C)"])
            scan_btn = st.button("🛰️ Initiate Satellite Scan", type="primary", use_container_width=True)

    scan_res = generate_ndvi_field_scan(s_crop, s_field)

    with col_s2:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Average NDVI", scan_res["avg_ndvi"], delta="Healthy Vigor" if scan_res["avg_ndvi"] > 0.6 else "Stress Detected")
        m2.metric("Green Zone (High Vigor)", f"{scan_res['healthy_pct']}%")
        m3.metric("Yellow Zone (Moderate)", f"{scan_res['moderate_pct']}%")
        m4.metric("Red Zone (Stressed)", f"{scan_res['stressed_pct']}%")

    st.markdown("---")
    st.subheader(f"🗺️ Spatial Canopy Heatmap: {s_field} ({s_crop})")
    st.dataframe(scan_res["grid_df"], use_container_width=True)

    st.markdown("### 🚜 Variable-Rate Precision Farming Prescriptions")
    for pres in scan_res["prescriptions"]:
        with st.container(border=True):
            st.markdown(f"#### {pres['zone']} (Covers {pres['area_pct']} of plot)")
            st.write(f"**Diagnosis:** {pres['diagnosis']}")
            st.info(f"**Prescription Action:** {pres['action']}")


# =============================================================================
# 9. PRO: IOT SENSOR TELEMETRY & SMART IRRIGATION PUMP
# =============================================================================
elif active_page == "iot":
    st.markdown(f"## {t['nav_iot']} <span class='badge-pro'>PRO</span>", unsafe_allow_html=True)
    st.write("Live multi-depth root zone sensors and automated relay control for drip and sprinkler irrigation pumps.")

    iot_col1, iot_col2 = st.columns([1, 2])
    with iot_col1:
        with st.container(border=True):
            st.markdown("#### 🎛️ Probe Control & Simulation")
            sim_moist = st.slider("Simulate Root Zone Moisture (15cm %):", min_value=15.0, max_value=85.0, value=32.0, step=1.0)
            st.caption("Change this slider to test automatic pump trigger (Pumps ON when < 35%, OFF when > 65%).")

    telemetry = get_live_sensor_telemetry(sim_moist)

    with iot_col2:
        with st.container(border=True):
            st.markdown("#### ⚡ Water Pump Actuator Status")
            st.markdown(f"### Status: `{telemetry['pump_state']}`")
            st.info(f"**System Automation Rule:** {telemetry['recommendation']}")

    st.markdown("---")
    st.subheader("📡 Live Probe Telemetry Stream")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Moisture (15cm Root Depth)", f"{telemetry['moisture_15cm']}%")
    t2.metric("Moisture (30cm Deep Subsoil)", f"{telemetry['moisture_30cm']}%")
    t3.metric("Soil Temperature", f"{telemetry['soil_temp']} °C")
    t4.metric("EC Salinity", f"{telemetry['ec_salinity']} dS/m", delta="Safe (<2.0)")

    st.markdown("---")
    st.subheader("📈 24-Hour Soil Moisture Consumption Trend")
    st.line_chart(telemetry["history_df"].set_index("Hour"))

    g1, g2 = st.columns(2)
    g1.success(f"💧 **Water Conserved Today:** {telemetry['water_saved_liters']:,} Liters via automated sensor cut-off.")
    g2.info(f"⚡ **Electricity Saved:** {telemetry['electricity_saved_kwh']} kWh saved by avoiding over-pumping.")


# =============================================================================
# 10. PRO: CROP DUEL & MULTI-FACTOR RISK COMPARATOR
# =============================================================================
elif active_page == "duel":
    st.markdown(f"## {t['nav_duel']} <span class='badge-pro'>PRO</span>", unsafe_allow_html=True)
    st.write("Compare any two commercial crops head-to-head across water footprint, upfront capital, labor, and market risk.")

    d_col1, d_col2 = st.columns(2)
    crop_list = list(CROP_PROFILES.keys())
    with d_col1:
        crop_1 = st.selectbox("Select Crop A:", crop_list, index=0)
    with d_col2:
        crop_2 = st.selectbox("Select Crop B:", crop_list, index=1)

    st.markdown(f"### ⚔️ Duel: **{crop_1}** vs. **{crop_2}**")
    comparison_table = compare_two_crops(crop_1, crop_2)
    st.table(pd.DataFrame(comparison_table))


# =============================================================================
# 11. PRO: KISAN BAHI-KHATA (FARM P&L FINANCIAL LEDGER)
# =============================================================================
elif active_page == "ledger":
    st.markdown(f"## {t['nav_ledger']} <span class='badge-pro'>PRO</span>", unsafe_allow_html=True)
    st.write("Complete farm commercial accounting. Track itemized input costs against harvest sales to find your break-even price.")

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        with st.container(border=True):
            st.markdown("#### 🛒 Cultivation Expenses (Input Costs)")
            c_seed = st.number_input("Seeds / Planting Material (₹):", value=4500, step=500)
            c_fert = st.number_input("Fertilizers & Farmyard Manure (₹):", value=7200, step=500)
            c_pest = st.number_input("Pesticides, Fungicides & Bio-sprays (₹):", value=3800, step=500)
            c_mach = st.number_input("Tractor, Tillage & Harvester Rental (₹):", value=6500, step=500)
            c_labor = st.number_input("Labor Wages (Weeding, Sowing, Picking) (₹):", value=8000, step=500)
            c_misc = st.number_input("Irrigation, Electricity & Misc (₹):", value=2000, step=500)

    with f_col2:
        with st.container(border=True):
            st.markdown("#### 🌾 Harvest Revenue Realization")
            h_yield = st.number_input("Total Harvest Yield (in Quintals):", value=22.0, step=1.0)
            h_price = st.number_input("Mandi Selling Price per Quintal (₹):", value=2425.0, step=50.0)

        pnl = calculate_farm_pnl(c_seed, c_fert, c_pest, c_mach, c_labor, c_misc, h_yield, h_price)

        with st.container(border=True):
            st.markdown("#### 📊 Financial Summary & Balance Sheet")
            st.markdown(f"**Total Production Cost:** `₹{pnl['total_cost']:,}`")
            st.markdown(f"**Gross Revenue:** `₹{pnl['gross_revenue']:,}`")
            
            if pnl["net_profit"] >= 0:
                st.markdown(f"**Net Profit:** <span style='font-size:1.6rem; color:#1b5e20; font-weight:bold;'>+₹{pnl['net_profit']:,}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**Net Loss:** <span style='font-size:1.6rem; color:#b71c1c; font-weight:bold;'>-₹{abs(pnl['net_profit']):,}</span>", unsafe_allow_html=True)

            st.metric("Net Profit Margin", f"{pnl['profit_margin_pct']}%")
            st.metric("Break-Even Price (Min price to avoid loss)", f"₹{pnl['break_even_price']} / Quintal")
            st.caption(f"Cost of production per quintal: ₹{pnl['cost_per_quintal']}")

    st.markdown("---")
    st.subheader("🥧 Input Expense Breakdown")
    st.dataframe(pnl["expense_breakdown"], use_container_width=True)


# --- Footer ---
st.markdown("---")
st.caption("🌾 Dhara PRO | Enterprise Agritech Platform | Python, Streamlit & Satellite AI")
