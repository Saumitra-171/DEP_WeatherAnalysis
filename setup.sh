#!/bin/bash

# ════════════════════════════════════════════════════════════════════════════════
# Mini Project 3: Quick Setup Script
# ════════════════════════════════════════════════════════════════════════════════

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║          MINI PROJECT 3: WEATHER API ANALYSIS - SETUP WIZARD              ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python installation
echo "📍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -q requests pandas matplotlib seaborn numpy flask flask-cors

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "⚠️  Some dependencies may have failed. Trying with --user flag..."
    pip install --user -q requests pandas matplotlib seaborn numpy flask flask-cors
fi

echo ""

# Create directories
echo "📁 Creating project directories..."
mkdir -p templates
mkdir -p static/plots
mkdir -p weather_plots

echo "✅ Directories created:"
echo "   • templates/"
echo "   • static/plots/"
echo "   • weather_plots/"
echo ""

# Check if files exist
echo "🔍 Checking project files..."
FILES=("weather_analyzer.py" "app.py" "dashboard.html" "requirements.txt" "README.md")

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
    fi
done

echo ""

# Get API key
read -p "🔑 Enter your OpenWeatherMap API key (or press Enter to skip): " API_KEY

if [ -z "$API_KEY" ]; then
    echo ""
    echo "⚠️  No API key provided."
    echo ""
    echo "📖 To get an API key:"
    echo "   1. Visit: https://openweathermap.org/api"
    echo "   2. Sign up for a free account"
    echo "   3. Go to API Keys tab"
    echo "   4. Copy your key"
    echo "   5. Note: Keys take 10-60 minutes to activate"
    echo ""
else
    echo "✅ API key saved!"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""
echo "🚀 SETUP COMPLETE!"
echo ""
echo "Choose how to run the project:"
echo ""
echo "Option 1 - Web Dashboard (Recommended):"
echo "   $ python app.py"
echo "   Then open: http://localhost:5000"
echo ""
echo "Option 2 - Command Line:"
echo "   $ python weather_analyzer.py"
echo "   (Follow the prompts, paste your API key when asked)"
echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Offer to start Flask
echo "Would you like to start the web server now? (y/n)"
read -p "> " START_SERVER

if [ "$START_SERVER" = "y" ] || [ "$START_SERVER" = "Y" ]; then
    echo ""
    echo "🌐 Starting Flask server..."
    echo "   • Dashboard: http://localhost:5000"
    echo "   • Press Ctrl+C to stop"
    echo ""
    python app.py
else
    echo "✅ Setup complete! Run 'python app.py' when you're ready."
fi
