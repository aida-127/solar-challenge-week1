import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_country_data():
    """Load cleaned data for all three countries with proper validation"""
    countries = {
        'Benin': 'data/clean/benin_clean.csv',
        'Sierra Leone': 'data/clean/sierra_leone_clean.csv', 
        'Togo': 'data/clean/togo_clean.csv'
    }
    
    country_data = {}
    for country, file_path in countries.items():
        try:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                # Basic data validation
                required_columns = ['GHI', 'DNI', 'DHI', 'RH', 'Tamb']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    print(f"⚠️  {country} missing columns: {missing_columns}")
                    continue
                
                country_data[country] = df
                print(f"✅ Loaded {country} data: {len(df):,} rows, {len(df.columns)} columns")
            else:
                print(f"❌ File not found: {file_path}")
                # Try alternative path without clean subdirectory
                alt_path = file_path.replace('clean/', '')
                if os.path.exists(alt_path):
                    df = pd.read_csv(alt_path)
                    country_data[country] = df
                    print(f"✅ Loaded {country} data from alternative path: {len(df):,} rows")
                
        except Exception as e:
            print(f"❌ Error loading {country}: {e}")
    
    return country_data

def calculate_detailed_metrics(df, country_name):
    """Calculate comprehensive solar metrics for a country"""
    metrics = {}
    
    # Basic statistics
    metrics['Country'] = country_name
    metrics['Total_Records'] = len(df)
    
    # GHI metrics
    metrics['Avg_GHI'] = df['GHI'].mean()
    metrics['Median_GHI'] = df['GHI'].median()
    metrics['Max_GHI'] = df['GHI'].max()
    metrics['Std_GHI'] = df['GHI'].std()
    metrics['GHI_CV'] = (df['GHI'].std() / df['GHI'].mean()) * 100  # Coefficient of variation
    
    # DNI metrics
    metrics['Avg_DNI'] = df['DNI'].mean()
    metrics['Max_DNI'] = df['DNI'].max()
    metrics['Std_DNI'] = df['DNI'].std()
    
    # DHI metrics  
    metrics['Avg_DHI'] = df['DHI'].mean()
    metrics['Max_DHI'] = df['DHI'].max()
    metrics['Std_DHI'] = df['DHI'].std()
    
    # Environmental metrics
    metrics['Avg_RH'] = df['RH'].mean()
    metrics['Avg_Tamb'] = df['Tamb'].mean()
    metrics['Max_Tamb'] = df['Tamb'].max()
    metrics['Std_Tamb'] = df['Tamb'].std()
    
    # Solar potential metrics
    # Peak sun hours (GHI > 400 W/m² - good solar radiation)
    peak_sun_hours = len(df[df['GHI'] > 400])
    metrics['Peak_Hours'] = peak_sun_hours
    metrics['Peak_Hours_Percent'] = (peak_sun_hours / len(df)) * 100
    
    # Excellent solar hours (GHI > 600 W/m²)
    excellent_hours = len(df[df['GHI'] > 600])
    metrics['Excellent_Hours'] = excellent_hours
    metrics['Excellent_Hours_Percent'] = (excellent_hours / len(df)) * 100
    
    # Low solar hours (GHI < 200 W/m²)
    low_hours = len(df[df['GHI'] < 200])
    metrics['Low_Hours'] = low_hours
    metrics['Low_Hours_Percent'] = (low_hours / len(df)) * 100
    
    # Consistency metric (percentage of time with decent solar)
    decent_hours = len(df[df['GHI'] > 300])
    metrics['Consistency_Score'] = (decent_hours / len(df)) * 100
    
    # Clearness index approximation (GHI/Max_GHI)
    metrics['Clearness_Index'] = df['GHI'].mean() / df['GHI'].max()
    
    return metrics

def perform_statistical_analysis(country_data):
    """Perform statistical tests to compare countries"""
    print("\n📊 STATISTICAL ANALYSIS")
    print("=" * 50)
    
    # Extract GHI data for ANOVA test
    ghi_data = []
    country_names = []
    
    for country, df in country_data.items():
        ghi_data.append(df['GHI'].dropna())
        country_names.append(country)
    
    # One-way ANOVA test
    if len(ghi_data) >= 2:
        try:
            f_stat, p_value = stats.f_oneway(*ghi_data)
            print(f"📈 One-way ANOVA Results (GHI):")
            print(f"   F-statistic: {f_stat:.4f}")
            print(f"   P-value: {p_value:.4f}")
            
            if p_value < 0.05:
                print("   ✅ Significant differences exist between countries (p < 0.05)")
            else:
                print("   ⚠️ No significant differences between countries (p ≥ 0.05)")
                
        except Exception as e:
            print(f"❌ ANOVA test failed: {e}")
    
    # Pairwise t-tests
    print(f"\n📊 Pairwise T-tests (GHI):")
    for i in range(len(country_names)):
        for j in range(i + 1, len(country_names)):
            t_stat, p_val = stats.ttest_ind(ghi_data[i], ghi_data[j], equal_var=False)
            significance = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "ns"
            print(f"   {country_names[i]} vs {country_names[j]}: p-value = {p_val:.4f} {significance}")

def create_comprehensive_visualizations(comparison_df, country_data):
    """Create comprehensive comparison visualizations"""
    print("\n📈 CREATING COMPREHENSIVE VISUALIZATIONS...")
    
    try:
        # Set up color scheme
        colors = ['orange', 'green', 'red']
        country_names = comparison_df['Country'].values
        
        # 1. Main comparison figure
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Comprehensive Solar Potential Comparison: Benin vs Sierra Leone vs Togo', 
                    fontsize=16, fontweight='bold')
        
        # Plot 1: Average GHI Comparison
        bars1 = axes[0, 0].bar(country_names, comparison_df['Avg_GHI'], color=colors, alpha=0.7)
        axes[0, 0].set_title('Average Global Horizontal Irradiance (GHI)\n(Higher is Better)', fontweight='bold')
        axes[0, 0].set_ylabel('GHI (W/m²)')
        axes[0, 0].grid(True, alpha=0.3)
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}', ha='center', va='bottom')
        
        # Plot 2: Peak Sun Hours
        bars2 = axes[0, 1].bar(country_names, comparison_df['Peak_Hours'], color=colors, alpha=0.7)
        axes[0, 1].set_title('Annual Peak Sun Hours (GHI > 400 W/m²)\n(Higher is Better)', fontweight='bold')
        axes[0, 1].set_ylabel('Hours')
        axes[0, 1].grid(True, alpha=0.3)
        for bar in bars2:
            height = bar.get_height()
            axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:,}', ha='center', va='bottom')
        
        # Plot 3: Consistency Score
        bars3 = axes[0, 2].bar(country_names, comparison_df['Consistency_Score'], color=colors, alpha=0.7)
        axes[0, 2].set_title('Solar Consistency Score (% time GHI > 300 W/m²)\n(Higher is Better)', fontweight='bold')
        axes[0, 2].set_ylabel('Percentage (%)')
        axes[0, 2].grid(True, alpha=0.3)
        for bar in bars3:
            height = bar.get_height()
            axes[0, 2].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}%', ha='center', va='bottom')
        
        # Plot 4: Relative Humidity
        bars4 = axes[1, 0].bar(country_names, comparison_df['Avg_RH'], color=colors, alpha=0.7)
        axes[1, 0].set_title('Average Relative Humidity\n(Lower is Better for Solar)', fontweight='bold')
        axes[1, 0].set_ylabel('Relative Humidity (%)')
        axes[1, 0].grid(True, alpha=0.3)
        for bar in bars4:
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}%', ha='center', va='bottom')
        
        # Plot 5: GHI Variability (Coefficient of Variation)
        bars5 = axes[1, 1].bar(country_names, comparison_df['GHI_CV'], color=colors, alpha=0.7)
        axes[1, 1].set_title('GHI Variability (Coefficient of Variation)\n(Lower is Better)', fontweight='bold')
        axes[1, 1].set_ylabel('CV (%)')
        axes[1, 1].grid(True, alpha=0.3)
        for bar in bars5:
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}%', ha='center', va='bottom')
        
        # Plot 6: Excellent Solar Hours
        bars6 = axes[1, 2].bar(country_names, comparison_df['Excellent_Hours_Percent'], color=colors, alpha=0.7)
        axes[1, 2].set_title('Excellent Solar Hours (% time GHI > 600 W/m²)\n(Higher is Better)', fontweight='bold')
        axes[1, 2].set_ylabel('Percentage (%)')
        axes[1, 2].grid(True, alpha=0.3)
        for bar in bars6:
            height = bar.get_height()
            axes[1, 2].text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('comprehensive_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ Comprehensive comparison chart saved as: comprehensive_comparison.png")
        plt.close()
        
        # 2. Boxplot comparison
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # Prepare data for boxplots
        ghi_data = [country_data[country]['GHI'] for country in country_names]
        dni_data = [country_data[country]['DNI'] for country in country_names]
        dhi_data = [country_data[country]['DHI'] for country in country_names]
        
        # Boxplot 1: GHI distribution
        box1 = axes[0].boxplot(ghi_data, labels=country_names, patch_artist=True)
        # Set colors
        for patch, color in zip(box1['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        axes[0].set_title('GHI Distribution Comparison', fontweight='bold')
        axes[0].set_ylabel('GHI (W/m²)')
        axes[0].grid(True, alpha=0.3)
        
        # Boxplot 2: DNI distribution
        box2 = axes[1].boxplot(dni_data, labels=country_names, patch_artist=True)
        for patch, color in zip(box2['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        axes[1].set_title('DNI Distribution Comparison', fontweight='bold')
        axes[1].set_ylabel('DNI (W/m²)')
        axes[1].grid(True, alpha=0.3)
        
        # Boxplot 3: DHI distribution
        box3 = axes[2].boxplot(dhi_data, labels=country_names, patch_artist=True)
        for patch, color in zip(box3['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        axes[2].set_title('DHI Distribution Comparison', fontweight='bold')
        axes[2].set_ylabel('DHI (W/m²)')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('distribution_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ Distribution comparison saved as: distribution_comparison.png")
        plt.close()
        
        # 3. Radar chart for multi-metric comparison
        create_radar_chart(comparison_df)
        
        # 4. Correlation heatmap for each country
        create_correlation_heatmaps(country_data)
        
    except Exception as e:
        print(f"❌ Visualization error: {e}")

def create_radar_chart(comparison_df):
    """Create a radar chart for multi-dimensional comparison"""
    try:
        # Select key metrics for radar chart
        metrics = ['Avg_GHI', 'Peak_Hours_Percent', 'Consistency_Score', 'Avg_DNI', 'Excellent_Hours_Percent']
        metric_labels = ['Avg GHI', 'Peak Hours %', 'Consistency %', 'Avg DNI', 'Excellent Hours %']
        
        # Normalize data for radar chart (0-1 scale)
        normalized_data = []
        for metric in metrics:
            min_val = comparison_df[metric].min()
            max_val = comparison_df[metric].max()
            normalized = (comparison_df[metric] - min_val) / (max_val - min_val)
            normalized_data.append(normalized.values)
        
        # Set up radar chart
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        colors = ['orange', 'green', 'red']
        country_names = comparison_df['Country'].values
        
        for i, country in enumerate(country_names):
            values = [data[i] for data in normalized_data]
            values += values[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, label=country, color=colors[i])
            ax.fill(angles, values, alpha=0.1, color=colors[i])
        
        # Add metric labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metric_labels)
        ax.set_ylim(0, 1)
        ax.set_title('Solar Potential Radar Chart\n(Normalized Metrics Comparison)', size=14, fontweight='bold')
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.savefig('radar_chart_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ Radar chart saved as: radar_chart_comparison.png")
        plt.close()
        
    except Exception as e:
        print(f"⚠️ Radar chart creation skipped: {e}")

def create_correlation_heatmaps(country_data):
    """Create correlation heatmaps for each country"""
    try:
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Correlation Heatmaps by Country', fontsize=16, fontweight='bold')
        
        countries = list(country_data.keys())
        colors = ['Oranges', 'Greens', 'Reds']
        
        for idx, (country, color) in enumerate(zip(countries, colors)):
            df = country_data[country]
            # Select numeric columns for correlation
            numeric_cols = ['GHI', 'DNI', 'DHI', 'RH', 'Tamb']
            corr_data = df[numeric_cols].corr()
            
            # Create heatmap
            im = axes[idx].imshow(corr_data, cmap=color, vmin=-1, vmax=1, aspect='auto')
            axes[idx].set_xticks(range(len(numeric_cols)))
            axes[idx].set_yticks(range(len(numeric_cols)))
            axes[idx].set_xticklabels(numeric_cols, rotation=45)
            axes[idx].set_yticklabels(numeric_cols)
            axes[idx].set_title(f'{country} Correlations')
            
            # Add correlation values as text
            for i in range(len(numeric_cols)):
                for j in range(len(numeric_cols)):
                    axes[idx].text(j, i, f'{corr_data.iloc[i, j]:.2f}', 
                                  ha='center', va='center', fontweight='bold')
        
        # Add colorbar
        cbar = fig.colorbar(im, ax=axes, shrink=0.6)
        cbar.set_label('Correlation Coefficient')
        
        plt.tight_layout()
        plt.savefig('correlation_heatmaps.png', dpi=300, bbox_inches='tight')
        print("✅ Correlation heatmaps saved as: correlation_heatmaps.png")
        plt.close()
        
    except Exception as e:
        print(f"⚠️ Correlation heatmaps skipped: {e}")

def generate_insights_report(comparison_df):
    """Generate actionable insights from the comparison"""
    print("\n💡 ACTIONABLE INSIGHTS & RECOMMENDATIONS")
    print("=" * 60)
    
    # Rank countries by different metrics
    ghi_rank = comparison_df.sort_values('Avg_GHI', ascending=False)['Country'].values
    consistency_rank = comparison_df.sort_values('Consistency_Score', ascending=False)['Country'].values
    peak_hours_rank = comparison_df.sort_values('Peak_Hours', ascending=False)['Country'].values
    low_variability_rank = comparison_df.sort_values('GHI_CV')['Country'].values  # Lower CV is better
    
    print(f"🏆 COUNTRY RANKINGS:")
    print(f"   By Average GHI:          1. {ghi_rank[0]} → 2. {ghi_rank[1]} → 3. {ghi_rank[2]}")
    print(f"   By Consistency:          1. {consistency_rank[0]} → 2. {consistency_rank[1]} → 3. {consistency_rank[2]}")
    print(f"   By Peak Hours:           1. {peak_hours_rank[0]} → 2. {peak_hours_rank[1]} → 3. {peak_hours_rank[2]}")
    print(f"   By Low Variability:      1. {low_variability_rank[0]} → 2. {low_variability_rank[1]} → 3. {low_variability_rank[2]}")
    
    print(f"\n📊 KEY FINDINGS:")
    
    # GHI Analysis
    best_ghi = comparison_df.loc[comparison_df['Avg_GHI'].idxmax()]
    worst_ghi = comparison_df.loc[comparison_df['Avg_GHI'].idxmin()]
    ghi_diff = best_ghi['Avg_GHI'] - worst_ghi['Avg_GHI']
    print(f"   • {best_ghi['Country']} has the highest average GHI ({best_ghi['Avg_GHI']:.1f} W/m²)")
    print(f"   • {worst_ghi['Country']} has the lowest average GHI ({worst_ghi['Avg_GHI']:.1f} W/m²)")
    print(f"   • Difference between highest and lowest: {ghi_diff:.1f} W/m² ({ghi_diff/best_ghi['Avg_GHI']*100:.1f}%)")
    
    # Consistency Analysis
    best_consistency = comparison_df.loc[comparison_df['Consistency_Score'].idxmax()]
    worst_consistency = comparison_df.loc[comparison_df['Consistency_Score'].idxmin()]
    print(f"   • {best_consistency['Country']} has the most consistent solar resource ({best_consistency['Consistency_Score']:.1f}% of time)")
    print(f"   • {worst_consistency['Country']} has the least consistent resource ({worst_consistency['Consistency_Score']:.1f}% of time)")
    
    # Humidity Impact
    highest_humidity = comparison_df.loc[comparison_df['Avg_RH'].idxmax()]
    lowest_humidity = comparison_df.loc[comparison_df['Avg_RH'].idxmin()]
    print(f"   • {highest_humidity['Country']} has highest humidity ({highest_humidity['Avg_RH']:.1f}%) - may affect panel efficiency")
    print(f"   • {lowest_humidity['Country']} has most favorable humidity levels ({lowest_humidity['Avg_RH']:.1f}%)")
    
    # Variability Analysis
    most_stable = comparison_df.loc[comparison_df['GHI_CV'].idxmin()]
    most_variable = comparison_df.loc[comparison_df['GHI_CV'].idxmax()]
    print(f"   • {most_stable['Country']} has most stable solar resource (CV: {most_stable['GHI_CV']:.1f}%)")
    print(f"   • {most_variable['Country']} has most variable resource (CV: {most_variable['GHI_CV']:.1f}%)")
    
    print(f"\n🎯 RECOMMENDATIONS:")
    print(f"   • For maximum output: Consider {ghi_rank[0]} (highest average GHI)")
    print(f"   • For reliability: Consider {consistency_rank[0]} (most consistent)")
    print(f"   • For large-scale projects: {peak_hours_rank[0]} offers most peak hours")
    print(f"   • For predictable output: {low_variability_rank[0]} has most stable resource")
    
    # Calculate overall score (simple weighted average)
    comparison_df['Overall_Score'] = (
        comparison_df['Avg_GHI'] / comparison_df['Avg_GHI'].max() * 0.3 +
        comparison_df['Consistency_Score'] / 100 * 0.25 +
        comparison_df['Peak_Hours_Percent'] / 100 * 0.2 +
        (1 - comparison_df['GHI_CV'] / 100) * 0.15 +  # Lower CV is better
        (1 - comparison_df['Avg_RH'] / 100) * 0.1     # Lower humidity is better
    ) * 100
    
    best_overall = comparison_df.loc[comparison_df['Overall_Score'].idxmax()]
    print(f"\n🏅 OVERALL BEST PERFORMER: {best_overall['Country']} (Score: {best_overall['Overall_Score']:.1f}/100)")

def main():
    print("🌍 TASK 3: COMPREHENSIVE CROSS-COUNTRY SOLAR ANALYSIS")
    print("=" * 65)
    
    # Load country data
    country_data = load_country_data()
    
    if len(country_data) < 2:
        print("❌ Need at least 2 countries for comparison!")
        return
    
    print(f"\n✅ Successfully loaded {len(country_data)} countries")
    
    # Calculate detailed metrics for each country
    all_metrics = []
    for country, df in country_data.items():
        metrics = calculate_detailed_metrics(df, country)
        all_metrics.append(metrics)
    
    # Create comparison DataFrame
    comparison_df = pd.DataFrame(all_metrics)
    
    # Display comprehensive comparison table
    print("\n📊 COMPREHENSIVE SOLAR POTENTIAL COMPARISON:")
    display_columns = ['Country', 'Avg_GHI', 'Median_GHI', 'Max_GHI', 'Std_GHI', 'Avg_RH', 
                      'Peak_Hours', 'Peak_Hours_Percent', 'Consistency_Score', 'GHI_CV']
    print(comparison_df[display_columns].round(2).to_string(index=False))
    
    # Perform statistical analysis
    perform_statistical_analysis(country_data)
    
    # Create comprehensive visualizations
    create_comprehensive_visualizations(comparison_df, country_data)
    
    # Generate insights and recommendations
    generate_insights_report(comparison_df)
    
    # Save detailed comparison to CSV
    comparison_df.to_csv('detailed_country_comparison.csv', index=False)
    print(f"\n💾 Detailed comparison saved as: detailed_country_comparison.csv")
    
    print(f"\n🎯 TASK 3 COMPLETED SUCCESSFULLY!")
    print(f"📁 Generated files:")
    print(f"   • comprehensive_comparison.png")
    print(f"   • distribution_comparison.png") 
    print(f"   • radar_chart_comparison.png")
    print(f"   • correlation_heatmaps.png")
    print(f"   • detailed_country_comparison.csv")
    print(f"\n📊 Next steps:")
    print(f"   • Review the generated visualizations")
    print(f"   • Use insights for solar project planning")
    print(f"   • Consider additional factors like infrastructure and policies")

if __name__ == "__main__":
    main()