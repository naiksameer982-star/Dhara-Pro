# 🌾 Dhara PRO — Enterprise Kisan Intelligence & Precision Agricultural Advisory Portal

> **"Rooted in Soil, Empowered by Satellite & AI Intelligence"**  
> *ମାଟି ସହିତ ଯୋଡ଼ି, ଉପଗ୍ରହ ଏବଂ ଏଆଇ ଦ୍ୱାରା ସଶକ୍ତ | मिट्टी की शक्ति, उपग्रह एवं एआई का मार्गदर्शन*

Dhara PRO is a full-stack precision agritech decision support web application built with Python and Streamlit. It bridges laboratory agronomy, multispectral satellite vegetation telemetry, IoT hardware automation, and rural financial accounting into an intuitive multilingual platform.

---

## 🌟 Key Features & Systems (11 Modules)

### 🌾 1. Scientific Crop Recommendation
- Matches soil nutrients ($N, P, K$, $\text{pH}$) and climate parameters (Temperature, Humidity, Rainfall) against benchmark requirements for 22 commercial crops.
- Computes suitability match percentages (0 - 100%) and displays ideal crop duration and soil requirements.

### 🧪 2. Precision Fertilizer & Soil Health Advisor
- Converts raw soil test nutrient deficits into exact commercial bags:
  - **Urea** (46% Nitrogen, 45 kg bag)
  - **DAP** (Di-Ammonium Phosphate: 18% N, 46% P, 50 kg bag)
  - **MOP** (Muriate of Potash: 60% K2O, 50 kg bag)
- Generates split-dose application schedules (Basal dose vs vegetative top dressing) and organic practices.
- **1-Click WhatsApp Sharing & Downloadable Prescription Slip**.

### 🌦️ 3. Real-Time Weather & Spraying Warning System
- Free Open-Meteo satellite & meteorological API integration (No API key needed).
- Provides immediate agricultural advisories:
  - **Spraying Advisory:** Evaluates wind speed and rain probability to protect expensive chemical sprays.
  - **Irrigation Advisory:** Alerts farmers to pause irrigation when rain is expected.

### 🩺 4. Plant Health & Disease Diagnostician
- Comprehensive disease database for major commercial crops (Tomato, Potato, Wheat, Rice, Cotton, Maize).
- Interactive symptom lookup providing Organic cures, Chemical treatments, and Cultural prevention methods.
- Leaf photo scanner simulation.

### 📈 5. Mandi Rates & Farm Profitability Calculator
- Benchmark daily APMC mandi market rates compared against Government Minimum Support Price (MSP).
- 14-day price volatility history trend charts.
- Farm Profit Estimator: Gross Revenue, Production Costs, Net Profit, and ROI.

### 🏛️ 6. Government Schemes & Subsidies Portal
- Full guide and direct links for major schemes:
  - **PM-Kisan Samman Nidhi:** Direct income support (₹6,000/yr).
  - **Pradhan Mantri Fasal Bima Yojana (PMFBY):** Comprehensive crop insurance.
  - **PM-KUSUM:** 60% subsidy on standalone solar water pumps.
  - **Kisan Credit Card (KCC):** Low-interest farm loans (4% effective rate).
  - **Per Drop More Crop:** 45% - 55% micro-irrigation drip/sprinkler subsidy.

### 🤖 7. Kisan AI Agronomist (AgriGPT)
- 24/7 intelligent agricultural chat assistant.
- Explains organic formulas: **Jeevamrit** bio-fertilizer preparation, **Neemastra** natural pesticide, **Fall Armyworm** control, and **saline/alkaline soil reclamation**.

### 🛰️ 8. Satellite & NDVI Crop Health Scanner
- Simulates multispectral Sentinel-2 satellite canopy reflectance.
- Generates a **Normalized Difference Vegetation Index (NDVI)** heatmap partitioning the farm into High Vigor Green, Nitrogen-Deficient Yellow, and Water-Stressed Red zones.

### 📡 9. IoT Farm Telemetry & Smart Pump Actuator
- Live multi-depth soil moisture sensors (**15 cm root zone** & **30 cm subsoil**), temperature, and EC salinity.
- **Automated Irrigation Relay:** Automatically triggers pump **ON (< 35% moisture)** and **OFF (> 65% moisture)** to prevent water wastage and crop root rot.

### ⚖️ 10. Crop Duel & Multi-Factor Risk Comparator
- Side-by-side head-to-head comparison of any two crops across **Water Footprint**, **Upfront Capital**, **Labor Demand**, **Price Volatility**, and **MSP Safety**.

### 📒 11. Kisan Bahi-Khata (Farm P&L Ledger)
- Itemized cost tracking (Seeds, Fertilizers, Pesticides, Machinery Rental, Labor).
- Harvest income realization, Net Profit/Loss, and **Break-Even Price per Quintal**.

---

## 🌐 Multilingual Accessibility
Built specifically for rural farmers with instant 1-click language toggling:
- **English**
- **हिंदी (Hindi)**
- **ଓଡ଼ିଆ (Odia)**

---

## 🚀 How to Run Locally

### 1. Clone or Download Repository
```bash
git clone https://github.com/your-username/agrismart.git
cd agrismart
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
python -m streamlit run app.py
```
Open **http://localhost:8501** in your browser!

---

## 📂 Project Architecture

```
├── app.py                 # Core Streamlit multi-page frontend & navigation
├── crop_advisor.py        # Agronomic 22-crop matching engine & algorithms
├── fertilizer_advisor.py  # Stoichiometric N-P-K deficit & commercial fertilizer calculator
├── weather_service.py     # Open-Meteo REST API client & agricultural advisory rules
├── disease_doctor.py      # Plant pathology diagnostic database & remedies
├── market_tracker.py      # Commodity mandi prices & revenue forecasting
├── schemes_data.py        # Government agricultural welfare schemes & eligibility
├── ai_agronomist.py       # Kisan AI chatbot knowledge base & NLP matching
├── satellite_ndvi.py      # Multispectral Sentinel-2 NDVI canopy simulation
├── farm_iot.py            # IoT dual-depth telemetry & automated pump actuator
├── crop_comparator.py     # Head-to-head crop risk matrix
├── farm_ledger.py         # Farm financial accounting & break-even calculation
├── translations.py        # English, Hindi, and Odia localization dictionaries
├── run_app.bat            # 1-Click Windows desktop launcher
├── requirements.txt       # Python dependencies
└── .gitignore             # Git ignore file
```

---

## 📜 License
Open Access Agricultural Technology for Sustainable Farming.
