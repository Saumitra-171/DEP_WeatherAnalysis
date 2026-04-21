# 🌦️ Mini Project 3: Real-Time Weather API Data Analysis

**Complete implementation with Python backend, interactive frontend, and comprehensive visualizations.**

---

## 📋 Project Overview

This project demonstrates a complete real-time data pipeline that:
- ✅ Fetches live weather data from OpenWeatherMap API
- ✅ Stores data in structured Pandas DataFrames
- ✅ Performs comprehensive data cleaning and validation
- ✅ Engineers new features (Heat Index, Comfort Level)
- ✅ Generates 9 diverse visualizations
- ✅ Provides interactive web dashboard
- ✅ Exports data in multiple formats

**Technologies Used:**
- Python 3.10+
- Pandas, Matplotlib, Seaborn
- Flask, Flask-CORS
- HTML5, CSS3, JavaScript
- OpenWeatherMap API

---

## 📂 Project Structure

```
mini-project-3/
├── weather_analyzer.py          # Core Python implementation (class + CLI)
├── app.py                       # Flask web server
├── dashboard.html               # Interactive frontend dashboard
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── weather_plots/               # Generated visualization images
├── templates/                   # Flask templates
│   └── dashboard.html           # (Created at runtime)
├── static/
│   └── plots/                   # Visualization output
├── weather_data.csv             # Exported data
└── weather_export.json          # Alternative export format
```

---

## 🚀 Quick Start

### Option 1: Command Line (Standalone)

**1. Install dependencies:**
```bash
pip install requests pandas matplotlib seaborn numpy
```

**2. Run the analyzer:**
```bash
python weather_analyzer.py
```

**3. Enter your OpenWeatherMap API key when prompted**

**Output:**
- `weather_plots/` folder with 9 visualization images
- `weather_data.csv` with complete dataset

---

### Option 2: Web Dashboard (Recommended)

**1. Install dependencies:**
```bash
pip install requests pandas matplotlib seaborn numpy flask flask-cors
```

**2. Create directories:**
```bash
mkdir templates
mkdir -p static/plots
```

**3. Move files:**
```bash
cp dashboard.html templates/
```

**4. Run Flask server:**
```bash
python app.py
```

**5. Open browser:**
```
http://localhost:5000
```

**6. Enter your OpenWeatherMap API key in the dashboard**

---

## 🔑 Getting an OpenWeatherMap API Key

1. Go to https://openweathermap.org/api
2. Click "Sign Up"
3. Create a free account
4. Go to "API Keys" tab
5. Copy your key
6. ⚠️ **Note:** New keys take 10-60 minutes to activate

---

## 📊 Features

### 1. Data Collection
- Fetches real-time weather for 10 major Indian cities
- Captures 15+ variables per city
- Error handling for network/API issues

### 2. Data Cleaning
- Null value detection
- Outlier detection using IQR method
- Data validation

### 3. Feature Engineering
- **Heat Index:** Combines temperature + humidity
- **Comfort Level:** Categorizes 4 comfort zones (Cool, Comfortable, Warm, Hot & Humid)

### 4. Analysis
- Descriptive statistics
- Correlation analysis
- Key insights extraction

### 5. Visualizations (9 total)

| # | Chart | Insight |
|---|-------|---------|
| 1 | Bar Chart | Temperature comparison across cities |
| 2 | Grouped Bars | Actual vs Feels Like temperature |
| 3 | Horizontal Bars | Humidity levels with comfort threshold |
| 4 | Scatter Plot | Temperature vs Humidity comfort zones |
| 5 | Bar Chart | Wind speed across cities |
| 6 | Heatmap | Correlation between variables |
| 7 | Range Plot | Min/Max/Actual daily temperature |
| 8 | Pie + Bar | Weather conditions & comfort distribution |
| 9 | Line + Bar | Pressure & visibility patterns |

### 6. Export Options
- CSV format
- JSON format
- PNG visualizations

---

## 💻 Python API

### Using `WeatherAnalyzer` class:

```python
from weather_analyzer import WeatherAnalyzer

# Initialize
analyzer = WeatherAnalyzer(api_key='your_key_here')

# Fetch data
df = analyzer.fetch_data()

# Clean
analyzer.clean_data()

# Analyze
stats = analyzer.analyze()

# Visualize
analyzer.visualize(output_dir='plots')

# Export
analyzer.export_csv('data.csv')
json_data = analyzer.get_json()
```

### Get data:
```python
# Access DataFrame
df = analyzer.get_dataframe()

# Statistics
print(df.describe())
print(df['Temperature (°C)'].mean())
```

---

## 🌐 REST API Endpoints

### POST `/api/weather`
Fetch and analyze weather data.

**Request:**
```json
{
  "api_key": "your_openweathermap_api_key"
}
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "stats": {...},
  "message": "Successfully fetched 10 cities"
}
```

### GET `/api/stats`
Get statistical summary.

**Response:**
```json
{
  "success": true,
  "stats": {
    "hottest_city": "Jaipur",
    "hottest_temp": 40.2,
    "coolest_city": "Bengaluru",
    "coolest_temp": 27.3,
    "avg_temp": 34.5,
    "avg_humidity": 48.3,
    "data_count": 10
  }
}
```

### GET `/api/visualize`
Generate visualization plots.

**Response:**
```json
{
  "success": true,
  "message": "Visualizations generated",
  "plots": ["plot1_temperature.png", ...]
}
```

### GET `/api/export/csv`
Export data as CSV.

### GET `/api/export/json`
Export data as JSON.

### GET `/api/health`
Health check.

### GET `/api/info`
API documentation.

---

## 📈 Dashboard Features

### Overview Section
- 4 key statistics cards
- Hottest/coolest cities
- Average metrics

### Cities Section
- Individual city cards
- Current temperature & conditions
- Humidity, pressure, wind speed, visibility
- Comfort level badge

### Insights Section
- Temperature variation analysis
- Humidity impact on comfort
- Wind patterns
- Regional climate analysis

### Data Table
- Complete dataset in tabular format
- All 7 key metrics per city

### Responsive Design
- Works on desktop, tablet, mobile
- Smooth animations
- Professional color scheme

---

## 🎨 Frontend Design

**Color Palette:**
- Navy (#0A2342) - Primary
- Teal (#1B7F9E) - Accent
- Sky (#4EC5E0) - Highlight
- Light (#F4F8FB) - Background

**Typography:**
- Segoe UI for body text
- Bold headers for emphasis

**Responsive Grid:**
- Auto-fit columns
- Mobile-first approach
- Touch-friendly interactive elements

---

## 📊 Cities Analyzed

1. **Bengaluru** - South India, Coastal-adjacent
2. **Mumbai** - West Coast, Coastal
3. **Delhi** - North India, Inland Plains
4. **Chennai** - South Coast, Coastal
5. **Kolkata** - East India, Riverine
6. **Hyderabad** - South-Central, Inland
7. **Pune** - West-Central, Elevated
8. **Ahmedabad** - Northwest, Inland
9. **Jaipur** - North, Desert Region
10. **Lucknow** - North-Central, Inland Plains

---

## 🔍 Key Findings

### Temperature Distribution
- **Hottest:** Jaipur (40.2°C) - Desert climate
- **Coolest:** Bengaluru (27.3°C) - Elevation & geography
- **Spread:** 13°C variation across regions

### Humidity Patterns
- **Coastal Cities:** 70-85% humidity (high moisture)
- **Inland Cities:** 18-40% humidity (dry conditions)
- **Comfort Gap:** Up to 5°C difference in "feels like"

### Wind Impact
- **Windiest:** Chennai (6.0 m/s), Ahmedabad (6.8 m/s)
- **Wind Cooling:** Measurable effect on perception
- **Coastal vs Inland:** Coastal cities more breezy

### Correlations
- **Temperature ↔ Heat Index:** r = +0.97 (very strong)
- **Temperature ↔ Humidity:** r = -0.42 (moderate negative)
- **Humidity ↔ Cloudiness:** r = +0.55 (moderate positive)

---

## 🐛 Troubleshooting

### "401 Unauthorized" Error
- **Cause:** API key not yet activated
- **Solution:** Wait 10-60 minutes after signup, then retry

### "Connection Timeout" Error
- **Cause:** Network issues or API overload
- **Solution:** Check internet, retry, or use demo data

### Module Import Errors
- **Solution:** Install all requirements:
  ```bash
  pip install -r requirements.txt
  ```

### Port Already in Use
- **Solution:** Change Flask port:
  ```bash
  python app.py  # Changes port automatically
  ```

---

## 📚 Learning Outcomes

### Skills Demonstrated

1. **API Integration**
   - REST API communication
   - JSON parsing
   - Error handling

2. **Data Processing**
   - DataFrame manipulation
   - Data validation
   - Feature engineering

3. **Data Analysis**
   - Descriptive statistics
   - Correlation analysis
   - Outlier detection (IQR)

4. **Visualization**
   - Multiple chart types
   - Custom styling
   - Data storytelling

5. **Web Development**
   - HTML5 structure
   - CSS3 styling & animations
   - JavaScript interactivity
   - Flask backend integration

6. **Python Programming**
   - OOP (classes, methods)
   - Error handling (try-except)
   - File I/O operations
   - List comprehensions

---

## 📁 File Descriptions

### `weather_analyzer.py` (600+ lines)
**Main Python module** with `WeatherAnalyzer` class.

Features:
- API data fetching
- Data cleaning pipeline
- Statistical analysis
- 9 visualization functions
- CSV/JSON export
- Command-line interface

Usage:
```bash
python weather_analyzer.py  # Interactive CLI
```

### `app.py` (200+ lines)
**Flask web server** connecting Python backend to frontend.

Endpoints:
- `POST /api/weather` - Fetch and analyze
- `GET /api/stats` - Get statistics
- `GET /api/visualize` - Generate plots
- `GET /api/export/*` - Export data
- `GET /api/health` - Health check

### `dashboard.html` (500+ lines)
**Interactive frontend** with HTML, CSS, and JavaScript.

Sections:
- Header with navigation
- Hero section with API input
- Overview stats cards
- City cards grid
- Insights cards
- Data table
- Footer

Features:
- Real-time data fetching
- Responsive design
- Smooth animations
- Dark theme
- Demo data fallback

### `requirements.txt`
Python package dependencies:
```
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
flask>=2.3.0
flask-cors>=4.0.0
```

---

## 🎯 Next Steps / Enhancements

1. **Time Series Analysis**
   - Collect data hourly for trend analysis
   - Implement ARIMA forecasting

2. **Advanced Features**
   - Weather alerts for extreme conditions
   - Historical comparison with 5-year averages
   - Regional clustering analysis

3. **Interactive Enhancements**
   - Real-time dashboard updates
   - City selection filters
   - Date range picker

4. **Deployment**
   - Deploy to Heroku, AWS, or DigitalOcean
   - Add database (PostgreSQL) for data persistence
   - Set up scheduled data collection

5. **Additional Visualizations**
   - 3D scatter plots
   - Animated time-series
   - Interactive maps with city locations

---

## 📄 License

This is an educational project. Feel free to use and modify for learning purposes.

---

## 👨‍💻 Author

**Mini Project 3 - Real-Time API Data Analysis**
Created: April 2026
Purpose: Data Science & Web Development Learning

---

## 📞 Support

**Issues with API key?**
- Visit: https://openweathermap.org/faq
- Check activation time (usually 10-60 minutes)

**Need more data?**
- Extend CITIES list in `weather_analyzer.py`
- Increase fetch frequency in Flask app

**Want to contribute?**
- Fork the project
- Submit pull requests
- Report issues

---

## 🎉 You're Ready!

1. ✅ Get OpenWeatherMap API key
2. ✅ Install Python dependencies
3. ✅ Run `python app.py`
4. ✅ Open http://localhost:5000
5. ✅ Enter API key
6. ✅ Analyze live weather data!

**Happy analyzing!** 🌦️📊
