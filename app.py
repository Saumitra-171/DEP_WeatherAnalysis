"""
════════════════════════════════════════════════════════════════════════════════
    MINI PROJECT 3: FLASK WEB SERVER
    Backend API for Weather Analysis Dashboard
════════════════════════════════════════════════════════════════════════════════

Provides REST API endpoints that integrate the WeatherAnalyzer class with the
HTML frontend dashboard.

Run: python app.py
Then open http://localhost:5000 in your browser
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
from weather_analyzer import WeatherAnalyzer
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global analyzer instance
analyzer = None


# ════════════════════════════════════════════════════════════════════════════════
# ROUTES
# ════════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """Serve the main dashboard."""
    return render_template('dashboard.html')


@app.route('/api/weather', methods=['POST'])
def fetch_weather():
    """
    API endpoint to fetch and analyze weather data.
    
    Request body:
        {
            "api_key": "your_openweathermap_api_key"
        }
    
    Response:
        {
            "success": true,
            "data": [...],
            "stats": {...},
            "message": "Successfully fetched X cities"
        }
    """
    global analyzer
    
    try:
        # Get API key from request
        data = request.get_json()
        api_key = data.get('api_key', '').strip()
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'API key is required'
            }), 400
        
        # Initialize analyzer
        analyzer = WeatherAnalyzer(api_key)
        
        # Fetch data
        df = analyzer.fetch_data()
        
        if len(df) == 0:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch data for any cities. Check your API key.'
            }), 400
        
        # Clean data
        analyzer.clean_data()
        
        # Analyze
        stats = analyzer.analyze()
        
        # Convert to JSON
        data = json.loads(df.to_json(orient='records'))
        
        return jsonify({
            'success': True,
            'data': data,
            'stats': stats,
            'message': f'Successfully fetched {len(data)} cities'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistical summary of current data."""
    global analyzer
    
    if analyzer is None or analyzer.df is None:
        return jsonify({
            'success': False,
            'error': 'No data loaded yet'
        }), 400
    
    try:
        stats = analyzer._get_summary_stats()
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export data as CSV file."""
    global analyzer
    
    if analyzer is None or analyzer.df is None:
        return jsonify({
            'success': False,
            'error': 'No data loaded yet'
        }), 400
    
    try:
        analyzer.export_csv('weather_export.csv')
        return jsonify({
            'success': True,
            'message': 'Data exported to weather_export.csv'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export data as JSON file."""
    global analyzer
    
    if analyzer is None or analyzer.df is None:
        return jsonify({
            'success': False,
            'error': 'No data loaded yet'
        }), 400
    
    try:
        data = analyzer.get_json()
        
        with open('weather_export.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Data exported to weather_export.json'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/visualize', methods=['GET'])
def generate_visualizations():
    """Generate visualization plots."""
    global analyzer
    
    if analyzer is None or analyzer.df is None:
        return jsonify({
            'success': False,
            'error': 'No data loaded yet'
        }), 400
    
    try:
        analyzer.visualize(output_dir='static/plots')
        return jsonify({
            'success': True,
            'message': 'Visualizations generated',
            'plots': [
                'plot1_temperature.png',
                'plot2_feelslike.png',
                'plot3_humidity.png',
                'plot4_scatter.png',
                'plot5_wind.png',
                'plot6_heatmap.png',
                'plot7_range.png',
                'plot8_distribution.png',
                'plot9_atmosphere.png',
            ]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'Weather Analysis API',
        'data_loaded': analyzer is not None and analyzer.df is not None,
        'cities_count': len(analyzer.df) if analyzer and analyzer.df is not None else 0
    }), 200


@app.route('/api/info', methods=['GET'])
def info():
    """Get information about the API."""
    return jsonify({
        'name': 'Weather Analysis API',
        'version': '1.0',
        'project': 'Mini Project 3: Real-Time API Data Analysis',
        'endpoints': {
            'GET /': 'Main dashboard',
            'POST /api/weather': 'Fetch and analyze weather data',
            'GET /api/stats': 'Get statistical summary',
            'GET /api/export/csv': 'Export data as CSV',
            'GET /api/export/json': 'Export data as JSON',
            'GET /api/visualize': 'Generate visualizations',
            'GET /api/health': 'Health check',
            'GET /api/info': 'API information'
        }
    }), 200


# ════════════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ════════════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'status': 404
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'status': 500
    }), 500


# ════════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('\n' + '='*80)
    print('🚀 MINI PROJECT 3: WEATHER ANALYSIS WEB SERVER')
    print('='*80)
    print('\n📍 Starting Flask server...')
    print('🌐 Dashboard: http://localhost:5000')
    print('📚 API Documentation: http://localhost:5000/api/info')
    print('\n⚠️  Make sure to have:')
    print('   • weather_analyzer.py in the same directory')
    print('   • dashboard.html in ./templates/ folder')
    print('   • OpenWeatherMap API key ready')
    print('\n' + '='*80 + '\n')
    
    # Create directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/plots', exist_ok=True)
    
    # Run Flask app
    app.run(debug=True, port=5000, host='0.0.0.0')
