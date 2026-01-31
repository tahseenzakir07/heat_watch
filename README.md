# 🌡️ HeatWatch: Urban Heat Island Builder Analysis Tool

**HeatWatch** is an ultra-premium, AI-powered specialized web application designed for builders and urban planners to assess the suitability of construction sites based on thermal environmental data.

---

## 🚀 Project Overview

Urban Heat Islands (UHI) significantly impact building livability, cooling costs, and long-term sustainability. **HeatWatch** bridges the gap between architectural design and environmental data, providing builders with professional-grade thermal insights before a single brick is laid.

### 🎨 Key Features

#### 1. Premium "Midnight Aurora" UI
- **Ultra-Vibrant Aesthetic:** A glassmorphism-based dark theme featuring animated "Aurora" headers and vibrant gradients.
- **Fluid Interactions:** Smooth micro-animations and transitions on every button and card.
- **Responsive Layout:** Optimized for all screen sizes with balanced padding and professional typography.

#### 2. Smart Building Analysis
- **Schematic Upload:** Drag-and-drop building designs (PNG/JPG) with instant image preview.
- **AI Feature Extraction:** Our engine scans designs to estimate heat absorption factors and potential air-flow impedance.

#### 3. Interactive Thermal Mapping
- **Dark-Themed Map:** Integrated Leaflet.js maps (no API key required) for pinpointing construction sites.
- **Animated Markers:** Custom glowing markers that bounce into place.
- **Sample Locations:** One-click shortcuts to high-heat zones like Mumbai or moderate zones like Bangalore.

#### 4. Expert AI Insights & Justification
- **Suitability Score:** A 0-100% rating based on the intersection of building design and local UHI data.
- **Expert Insight Tab:** An expandable section providing professional rationale (e.g., "A 5-storey proposal in this hotspot risks creating a 'vertical oven' effect").
- **Mitigation Tactics:** Specific, actionable strategies (e.g., "Use high-albedo materials" or "Implement vertical greening").

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Image Processing:** Pillow (PIL), NumPy
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (ES6)
- **Mapping:** Leaflet.js
- **Logic Engine:** Custom AI-driven Recommendation Engine

---

## 📂 Project Structure

```text
GIS/
├── app.py              # Flask server
├── heat_data.py        # UHI processing logic
├── building_analyzer.py # Image feature extraction
├── recommendations.py   # AI expert analysis logic
├── index.html          # Premium dashboard
├── map.html            # Interactive map selection
├── results.html        # AI report & insights
├── styles.css          # Ultra-vibrant UI styles
└── data/
    └── sample_heat_data.json # Regional thermal profiles
```

---

## 🚀 How to Run Locally

1. **Install Dependencies:**
   ```bash
   pip install flask pillow numpy werkzeug
   ```
2. **Start the Server:**
   ```bash
   python server.py
   ```
3. **Explore:** Navigate to `http://localhost:5000`.

---

## 🎯 Verification Results

- **UI/UX:** Passed (Vibrant, no placeholders, smooth animations).
- **Core Logic:** Passed (Expert insights correctly generated for high/low heat zones).
- **Reliability:** Passed (Leaflet integration eliminates Google Map API key dependency).
- **Responsiveness:** Passed (Balanced padding and centered map container).

---

Developed for **Advanced Agentic Coding** - Transforming how builders interact with the environment.
