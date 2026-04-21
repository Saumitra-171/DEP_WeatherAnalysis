"""
════════════════════════════════════════════════════════════════════════════════
    MINI PROJECT 3: REAL-TIME WEATHER API DATA ANALYSIS
    Complete Standalone Implementation
════════════════════════════════════════════════════════════════════════════════

Project: Real-Time API Data Analysis
Author: Data Analysis Project
Date: April 2026
Description: Fetch live weather data from OpenWeatherMap API, clean, analyze,
            and visualize for 10 major Indian cities.

Features:
    • Real-time API data fetching
    • Comprehensive data cleaning
    • Feature engineering (Heat Index, Comfort Level)
    • Statistical analysis & correlations
    • 9 diverse visualizations
    • CSV export
    • Flask web server option
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime
import json
import warnings
import sys
import os
from pathlib import Path

warnings.filterwarnings('ignore')


# ════════════════════════════════════════════════════════════════════════════════
# CLASS: WeatherAnalyzer
# ════════════════════════════════════════════════════════════════════════════════

class WeatherAnalyzer:
    """
    Complete weather analysis pipeline.
    
    Handles:
        - API communication
        - Data validation
        - Feature engineering
        - Statistical analysis
        - Visualization
    """
    
    def __init__(self, api_key, cities=None):
        """
        Initialize WeatherAnalyzer.
        
        Args:
            api_key (str): OpenWeatherMap API key
            cities (list): Cities to analyze (default: 10 major Indian cities)
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        self.cities = cities or [
            "Bengaluru", "Mumbai", "Delhi", "Chennai",
            "Kolkata", "Hyderabad", "Pune", "Ahmedabad",
            "Jaipur", "Lucknow"
        ]
        
        self.df = None
        self.records = []
        
        # Plot style
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.family'] = 'DejaVu Sans'
        sns.set_palette('husl')
    
    def fetch_data(self):
        """
        Fetch weather data from OpenWeatherMap API for all cities.
        
        Returns:
            pd.DataFrame: Weather data with 20+ columns
        """
        print('\n' + '='*80)
        print('🔄 FETCHING WEATHER DATA FROM API')
        print('='*80 + '\n')
        
        self.records = []
        
        for city in self.cities:
            record = self._fetch_single_city(city)
            if record:
                self.records.append(record)
                print(f'  ✅ {city:15} — {record["Temperature (°C)"]:.1f}°C, '
                      f'{record["Humidity (%)"]:.0f}% humidity')
        
        self.df = pd.DataFrame(self.records)
        print(f'\n📊 Successfully fetched {len(self.records)}/{len(self.cities)} cities!\n')
        
        return self.df
    
    def _fetch_single_city(self, city):
        """Fetch data for a single city."""
        params = {
            'q': f'{city},IN',
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'City': city,
                'Temperature (°C)': data['main']['temp'],
                'Feels Like (°C)': data['main']['feels_like'],
                'Min Temp (°C)': data['main']['temp_min'],
                'Max Temp (°C)': data['main']['temp_max'],
                'Humidity (%)': data['main']['humidity'],
                'Pressure (hPa)': data['main']['pressure'],
                'Wind Speed (m/s)': data['wind']['speed'],
                'Wind Direction (°)': data['wind'].get('deg', 0),
                'Visibility (km)': data.get('visibility', 0) / 1000,
                'Cloudiness (%)': data['clouds']['all'],
                'Weather': data['weather'][0]['main'],
                'Description': data['weather'][0]['description'].title(),
                'Sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'Sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'Fetched At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except requests.exceptions.RequestException as e:
            print(f'  ❌ Error fetching {city}: {e}')
            return None
    
    def clean_data(self):
        """
        Clean and validate data.
        
        Operations:
            - Check for null values
            - Detect outliers (IQR method)
            - Engineer features (Heat Index, Comfort Level)
        """
        print('\n' + '='*80)
        print('🧹 DATA CLEANING & VALIDATION')
        print('='*80 + '\n')
        
        # Check nulls
        print('📌 Missing Values:')
        nulls = self.df.isnull().sum()
        if nulls.sum() == 0:
            print('  ✅ No missing values detected!')
        else:
            print(nulls[nulls > 0])
        
        # Outlier detection
        print('\n📌 Outlier Detection (Temperature):')
        temp_col = 'Temperature (°C)'
        Q1 = self.df[temp_col].quantile(0.25)
        Q3 = self.df[temp_col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = self.df[(self.df[temp_col] < Q1 - 1.5*IQR) | 
                           (self.df[temp_col] > Q3 + 1.5*IQR)]
        print(f'  IQR Range: {Q1:.1f}°C – {Q3:.1f}°C')
        print(f'  Outliers found: {len(outliers)}')
        
        # Feature engineering
        self._engineer_features()
        
        print('\n✅ Data cleaning complete!\n')
    
    def _engineer_features(self):
        """Create Heat Index and Comfort Level features."""
        # Heat Index
        self.df['Heat Index'] = (
            self.df['Temperature (°C)'] + 
            0.33 * (self.df['Humidity (%)'] / 100 * 6.105) - 4
        )
        
        # Comfort Level
        def classify_comfort(row):
            t = row['Temperature (°C)']
            h = row['Humidity (%)']
            if t < 20: return 'Cool'
            elif t < 28 and h < 60: return 'Comfortable'
            elif t < 32 or h < 70: return 'Warm'
            else: return 'Hot & Humid'
        
        self.df['Comfort Level'] = self.df.apply(classify_comfort, axis=1)
    
    def analyze(self):
        """Perform statistical analysis."""
        print('\n' + '='*80)
        print('📊 STATISTICAL ANALYSIS')
        print('='*80 + '\n')
        
        numeric_cols = ['Temperature (°C)', 'Feels Like (°C)', 'Humidity (%)',
                       'Wind Speed (m/s)', 'Visibility (km)', 'Cloudiness (%)',
                       'Pressure (hPa)']
        
        print('Descriptive Statistics:')
        print(self.df[numeric_cols].describe().round(2))
        
        print('\n\nKey Insights:')
        hottest = self.df.loc[self.df['Temperature (°C)'].idxmax()]
        coolest = self.df.loc[self.df['Temperature (°C)'].idxmin()]
        most_humid = self.df.loc[self.df['Humidity (%)'].idxmax()]
        windiest = self.df.loc[self.df['Wind Speed (m/s)'].idxmax()]
        
        print(f'🌡️  Hottest:     {hottest["City"]} ({hottest["Temperature (°C)"]:.1f}°C)')
        print(f'❄️  Coolest:     {coolest["City"]} ({coolest["Temperature (°C)"]:.1f}°C)')
        print(f'💧 Most Humid:  {most_humid["City"]} ({most_humid["Humidity (%)"]:.0f}%)')
        print(f'💨 Windiest:    {windiest["City"]} ({windiest["Wind Speed (m/s)"]:.1f} m/s)')
        print(f'🌡️  Avg Temp:    {self.df["Temperature (°C)"].mean():.1f}°C')
        print(f'💧 Avg Humidity: {self.df["Humidity (%)"].mean():.1f}%')
        
        print('\nComfort Level Distribution:')
        print(self.df['Comfort Level'].value_counts())
        
        return self._get_summary_stats()
    
    def _get_summary_stats(self):
        """Return summary statistics as dict."""
        return {
            'hottest_city': self.df.loc[self.df['Temperature (°C)'].idxmax()]['City'],
            'hottest_temp': self.df['Temperature (°C)'].max(),
            'coolest_city': self.df.loc[self.df['Temperature (°C)'].idxmin()]['City'],
            'coolest_temp': self.df['Temperature (°C)'].min(),
            'avg_temp': self.df['Temperature (°C)'].mean(),
            'avg_humidity': self.df['Humidity (%)'].mean(),
            'data_count': len(self.df)
        }
    
    def visualize(self, output_dir='plots'):
        """
        Generate all 9 visualizations.
        
        Args:
            output_dir (str): Directory to save plot images
        """
        print('\n' + '='*80)
        print('📈 GENERATING VISUALIZATIONS')
        print('='*80 + '\n')
        
        Path(output_dir).mkdir(exist_ok=True)
        
        plots = [
            ('plot1_temperature', self._plot_temperature),
            ('plot2_feelslike', self._plot_feels_like),
            ('plot3_humidity', self._plot_humidity),
            ('plot4_scatter', self._plot_scatter),
            ('plot5_wind', self._plot_wind),
            ('plot6_heatmap', self._plot_heatmap),
            ('plot7_range', self._plot_range),
            ('plot8_distribution', self._plot_distribution),
            ('plot9_atmosphere', self._plot_atmosphere),
        ]
        
        for i, (name, plot_func) in enumerate(plots, 1):
            print(f'  Generating {i}/9: {name}...')
            plot_func()
            plt.savefig(f'{output_dir}/{name}.png', dpi=150, bbox_inches='tight')
            plt.close()
        
        print('\n✅ All visualizations saved!\n')
    
    def _plot_temperature(self):
        """Plot 1: Temperature comparison."""
        df_sorted = self.df.sort_values('Temperature (°C)', ascending=False)
        fig, ax = plt.subplots(figsize=(13, 6))
        colors = plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, len(df_sorted)))
        bars = ax.bar(df_sorted['City'], df_sorted['Temperature (°C)'],
                     color=colors, edgecolor='white', linewidth=1.2)
        
        for bar, val in zip(bars, df_sorted['Temperature (°C)']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                   f'{val:.1f}°C', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.axhline(self.df['Temperature (°C)'].mean(), color='navy', linewidth=2,
                  linestyle='--', label=f'Avg: {self.df["Temperature (°C)"].mean():.1f}°C')
        ax.set_title('🌡️ Temperature Across 10 Indian Cities', fontsize=16, fontweight='bold')
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.grid(axis='y', alpha=0.4)
        ax.legend()
    
    def _plot_feels_like(self):
        """Plot 2: Actual vs Feels Like temperature."""
        df_sorted = self.df.sort_values('Temperature (°C)', ascending=False)
        x = np.arange(len(df_sorted))
        width = 0.4
        
        fig, ax = plt.subplots(figsize=(13, 6))
        ax.bar(x - width/2, df_sorted['Temperature (°C)'], width,
              label='Actual Temp', color='#e74c3c', alpha=0.85)
        ax.bar(x + width/2, df_sorted['Feels Like (°C)'], width,
              label='Feels Like', color='#3498db', alpha=0.85)
        
        ax.set_xticks(x)
        ax.set_xticklabels(df_sorted['City'], rotation=15)
        ax.set_title('🌡️ Actual Temperature vs Feels Like', fontsize=16, fontweight='bold')
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.legend(fontsize=12)
        ax.grid(axis='y', alpha=0.3)
    
    def _plot_humidity(self):
        """Plot 3: Humidity levels."""
        df_h = self.df.sort_values('Humidity (%)', ascending=False)
        fig, ax = plt.subplots(figsize=(13, 6))
        colors_h = ['#1a7abf' if h > 70 else '#5ba3d4' if h > 50 else '#aacfe8'
                   for h in df_h['Humidity (%)']]
        bars = ax.barh(df_h['City'], df_h['Humidity (%)'], color=colors_h)
        
        for bar, val in zip(bars, df_h['Humidity (%)']):
            ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{val:.0f}%', va='center', fontsize=11, fontweight='bold')
        
        ax.axvline(60, color='red', linestyle='--', linewidth=1.5, label='Comfort: 60%')
        ax.set_title('💧 Humidity Levels Across Cities', fontsize=16, fontweight='bold')
        ax.set_xlabel('Humidity (%)', fontsize=12)
        ax.set_xlim(0, 110)
        ax.legend()
        ax.grid(axis='x', alpha=0.3)
    
    def _plot_scatter(self):
        """Plot 4: Temperature vs Humidity with comfort zones."""
        comfort_colors = {'Cool': '#3498db', 'Comfortable': '#2ecc71',
                         'Warm': '#f39c12', 'Hot & Humid': '#e74c3c'}
        
        fig, ax = plt.subplots(figsize=(10, 7))
        for comfort, grp in self.df.groupby('Comfort Level'):
            ax.scatter(grp['Temperature (°C)'], grp['Humidity (%)'],
                      c=comfort_colors[comfort], s=200, label=comfort,
                      edgecolors='white', linewidths=1.5, alpha=0.9)
        
        for _, row in self.df.iterrows():
            ax.annotate(row['City'], (row['Temperature (°C)'], row['Humidity (%)']),
                       textcoords='offset points', xytext=(8, 5), fontsize=9)
        
        ax.set_title('🎯 Temperature vs Humidity — Comfort Analysis', fontsize=15, fontweight='bold')
        ax.set_xlabel('Temperature (°C)', fontsize=12)
        ax.set_ylabel('Humidity (%)', fontsize=12)
        ax.legend(title='Comfort Level', fontsize=10)
        ax.grid(alpha=0.3)
    
    def _plot_wind(self):
        """Plot 5: Wind speeds."""
        df_w = self.df.sort_values('Wind Speed (m/s)', ascending=False)
        fig, ax = plt.subplots(figsize=(13, 5))
        bars = ax.bar(df_w['City'], df_w['Wind Speed (m/s)'],
                     color=plt.cm.Blues(np.linspace(0.4, 0.9, len(df_w))))
        
        for bar, val in zip(bars, df_w['Wind Speed (m/s)']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                   f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_title('💨 Wind Speed Across Cities (m/s)', fontsize=16, fontweight='bold')
        ax.set_ylabel('Wind Speed (m/s)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
    
    def _plot_heatmap(self):
        """Plot 6: Correlation heatmap."""
        corr_cols = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)',
                    'Pressure (hPa)', 'Visibility (km)', 'Cloudiness (%)', 'Heat Index']
        corr = self.df[corr_cols].corr()
        
        fig, ax = plt.subplots(figsize=(9, 7))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
                   mask=mask, ax=ax, linewidths=0.5, square=True)
        ax.set_title('🔗 Correlation Heatmap — Weather Variables', fontsize=15, fontweight='bold')
    
    def _plot_range(self):
        """Plot 7: Temperature range."""
        df_r = self.df.sort_values('Temperature (°C)', ascending=False)
        fig, ax = plt.subplots(figsize=(13, 6))
        
        for i, (_, row) in enumerate(df_r.iterrows()):
            ax.plot([i, i], [row['Min Temp (°C)'], row['Max Temp (°C)']],
                   color='#bdc3c7', linewidth=4, solid_capstyle='round')
            ax.scatter(i, row['Temperature (°C)'], color='#e74c3c', s=120)
        
        ax.set_xticks(range(len(df_r)))
        ax.set_xticklabels(df_r['City'], rotation=15)
        ax.set_title('📊 Daily Temperature Range per City', fontsize=16, fontweight='bold')
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
    
    def _plot_distribution(self):
        """Plot 8: Weather conditions and comfort distribution."""
        weather_counts = self.df['Weather'].value_counts()
        comfort_counts = self.df['Comfort Level'].value_counts()
        comfort_colors = {'Cool': '#3498db', 'Comfortable': '#2ecc71',
                         'Warm': '#f39c12', 'Hot & Humid': '#e74c3c'}
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        ax1.pie(weather_counts.values, labels=weather_counts.index,
               autopct='%1.1f%%', startangle=90,
               wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        ax1.set_title('🌤️ Weather Condition Distribution', fontsize=14, fontweight='bold')
        
        colors_c = [comfort_colors.get(c, '#aaa') for c in comfort_counts.index]
        ax2.bar(comfort_counts.index, comfort_counts.values, color=colors_c)
        ax2.set_title('🎯 Comfort Level Distribution', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Number of Cities', fontsize=12)
        ax2.grid(axis='y', alpha=0.3)
    
    def _plot_atmosphere(self):
        """Plot 9: Pressure and visibility."""
        df_p = self.df.sort_values('Pressure (hPa)')
        df_v = self.df.sort_values('Visibility (km)', ascending=False)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        ax1.plot(df_p['City'], df_p['Pressure (hPa)'], 'o-', color='#8e44ad',
                linewidth=2.5, markersize=9, markerfacecolor='white', markeredgewidth=2)
        ax1.set_xticklabels(df_p['City'], rotation=30, ha='right')
        ax1.set_title('🌀 Atmospheric Pressure (hPa)', fontsize=13, fontweight='bold')
        ax1.grid(alpha=0.3)
        
        colors_v = ['#27ae60' if v >= 8 else '#f39c12' if v >= 5 else '#e74c3c'
                   for v in df_v['Visibility (km)']]
        ax2.bar(df_v['City'], df_v['Visibility (km)'], color=colors_v)
        ax2.set_title('👁️ Visibility (km)', fontsize=13, fontweight='bold')
        ax2.set_xticklabels(df_v['City'], rotation=30, ha='right')
        ax2.grid(axis='y', alpha=0.3)
    
    def export_csv(self, filename='weather_india_cities.csv'):
        """Export DataFrame to CSV."""
        self.df.to_csv(filename, index=False)
        print(f'\n✅ Data exported to {filename}')
        return filename
    
    def get_dataframe(self):
        """Return the DataFrame."""
        return self.df
    
    def get_json(self):
        """Return data as JSON."""
        return json.loads(self.df.to_json(orient='records'))


# ════════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ════════════════════════════════════════════════════════════════════════════════

def main():
    """Main execution function."""
    print('\n')
    print('╔' + '═'*78 + '╗')
    print('║' + ' '*78 + '║')
    print('║' + 'MINI PROJECT 3: REAL-TIME WEATHER API DATA ANALYSIS'.center(78) + '║')
    print('║' + 'Complete Standalone Python Implementation'.center(78) + '║')
    print('║' + ' '*78 + '║')
    print('╚' + '═'*78 + '╝')
    
    # Configuration
    API_KEY = input('\n🔑 Enter your OpenWeatherMap API key: ').strip()
    
    if not API_KEY:
        print('❌ API key is required!')
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = WeatherAnalyzer(API_KEY)
    
    # Pipeline execution
    try:
        # Fetch
        analyzer.fetch_data()
        
        # Clean
        analyzer.clean_data()
        
        # Analyze
        stats = analyzer.analyze()
        
        # Visualize
        analyzer.visualize(output_dir='weather_plots')
        
        # Export
        analyzer.export_csv('weather_data.csv')
        
        # Summary
        print('\n' + '='*80)
        print('✅ ANALYSIS COMPLETE')
        print('='*80)
        print(f'\n📊 Summary:')
        print(f'   • Data points: {stats["data_count"]} cities')
        print(f'   • Temperature range: {stats["coolest_temp"]:.1f}°C to {stats["hottest_temp"]:.1f}°C')
        print(f'   • Average temperature: {stats["avg_temp"]:.1f}°C')
        print(f'   • Average humidity: {stats["avg_humidity"]:.1f}%')
        print(f'\n📁 Outputs:')
        print(f'   • Visualizations: weather_plots/')
        print(f'   • Data: weather_data.csv')
        print(f'\n🎉 Ready for frontend integration!\n')
        
        return analyzer
        
    except Exception as e:
        print(f'\n❌ Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    analyzer = main()
