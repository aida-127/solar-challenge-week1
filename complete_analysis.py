# complete_analysis.py - Complete missing Task 2 analyses for ALL countries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

print("🔍 COMPLETING MISSING TASK 2 ANALYSES FOR ALL COUNTRIES")
print("="*60)

# Ensure output directory exists
os.makedirs('analysis_plots', exist_ok=True)

def analyze_country(country_name, df, color):
    """Analyze one country and save plots"""
    print(f"\n📊 ANALYZING {country_name.upper()}")
    print("-" * 40)
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # ========================================================================
    # 1. CLEANING IMPACT ANALYSIS
    # ========================================================================
    if 'Cleaning' in df.columns:
        cleaning_impact = df.groupby('Cleaning')[['ModA', 'ModB']].mean()
        print(f"Cleaning impact for {country_name}:")
        print(cleaning_impact)
        
        plt.figure(figsize=(10, 6))
        cleaning_impact.plot(kind='bar')
        plt.title(f'Cleaning Impact - {country_name}')
        plt.ylabel('Average Reading (W/m²)')
        plt.xlabel('Cleaning Status')
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f'analysis_plots/{country_name}_cleaning_impact.png')
        plt.close()  # Close instead of show
    
    # ========================================================================
    # 2. SCATTER PLOTS
    # ========================================================================
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # WS vs GHI
    axes[0,0].scatter(df['WS'], df['GHI'], alpha=0.3, s=1, color=color)
    axes[0,0].set_xlabel('Wind Speed (m/s)')
    axes[0,0].set_ylabel('GHI (W/m²)')
    axes[0,0].set_title(f'WS vs GHI - {country_name}')
    
    # WSgust vs GHI
    axes[0,1].scatter(df['WSgust'], df['GHI'], alpha=0.3, s=1, color=color)
    axes[0,1].set_xlabel('Wind Gust (m/s)')
    axes[0,1].set_ylabel('GHI (W/m²)')
    axes[0,1].set_title(f'WSgust vs GHI - {country_name}')
    
    # RH vs Tamb
    axes[1,0].scatter(df['RH'], df['Tamb'], alpha=0.3, s=1, color=color)
    axes[1,0].set_xlabel('Relative Humidity (%)')
    axes[1,0].set_ylabel('Ambient Temperature (°C)')
    axes[1,0].set_title(f'RH vs Temperature - {country_name}')
    
    # RH vs GHI
    axes[1,1].scatter(df['RH'], df['GHI'], alpha=0.3, s=1, color=color)
    axes[1,1].set_xlabel('Relative Humidity (%)')
    axes[1,1].set_ylabel('GHI (W/m²)')
    axes[1,1].set_title(f'RH vs GHI - {country_name}')
    
    plt.tight_layout()
    plt.savefig(f'analysis_plots/{country_name}_scatter_plots.png')
    plt.close()
    
    # ========================================================================
    # 3. WIND & DISTRIBUTION ANALYSIS
    # ========================================================================
    plt.figure(figsize=(12, 5))
    
    # Wind Speed Histogram
    plt.subplot(1, 2, 1)
    plt.hist(df['WS'], bins=50, alpha=0.7, edgecolor='black', color=color)
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Frequency')
    plt.title(f'Wind Distribution - {country_name}')
    
    # GHI Histogram
    plt.subplot(1, 2, 2)
    plt.hist(df[df['GHI'] > 0]['GHI'], bins=50, alpha=0.7, edgecolor='black', color='orange')
    plt.xlabel('GHI (W/m²)')
    plt.ylabel('Frequency')
    plt.title(f'Solar Distribution - {country_name}')
    
    plt.tight_layout()
    plt.savefig(f'analysis_plots/{country_name}_distributions.png')
    plt.close()
    
    # ========================================================================
    # 4. TEMPERATURE ANALYSIS
    # ========================================================================
    high_rh = df[df['RH'] > 80]
    low_rh = df[df['RH'] < 30]
    
    print(f"Temperature analysis for {country_name}:")
    print(f"  High RH (>80%): Avg Temp = {high_rh['Tamb'].mean():.1f}°C")
    print(f"  Low RH (<30%):  Avg Temp = {low_rh['Tamb'].mean():.1f}°C")
    print(f"  RH-Tamb Correlation: {df['RH'].corr(df['Tamb']):.3f}")
    
    # ========================================================================
    # 5. BUBBLE CHART
    # ========================================================================
    sample_data = df.sample(1000)
    
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(sample_data['Tamb'], sample_data['GHI'], 
                         c=sample_data['RH'], s=sample_data['BP']/10, 
                         alpha=0.6, cmap='viridis')
    plt.colorbar(scatter, label='Relative Humidity (%)')
    plt.xlabel('Ambient Temperature (°C)')
    plt.ylabel('GHI (W/m²)')
    plt.title(f'Bubble Chart - {country_name}')
    plt.tight_layout()
    plt.savefig(f'analysis_plots/{country_name}_bubble_chart.png')
    plt.close()
    
    print(f"✅ {country_name} analysis completed!")

# ============================================================================
# MAIN ANALYSIS FOR ALL COUNTRIES
# ============================================================================

# Load all cleaned datasets
benin = pd.read_csv('data/clean/benin_clean.csv')
sierra = pd.read_csv('data/clean/sierra_leone_clean.csv')
togo = pd.read_csv('data/clean/togo_clean.csv')

print("✅ All country data loaded!")

# Analyze each country
analyze_country('benin', benin, 'orange')
analyze_country('sierra_leone', sierra, 'green') 
analyze_country('togo', togo, 'red')

print(f"\n🎉 TASK 2 COMPLETED FOR ALL COUNTRIES! 🎉")
print("All plots saved in 'analysis_plots/' folder")
print("Ready for Task 3: Cross-Country Comparison!")