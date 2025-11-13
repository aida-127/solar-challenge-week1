import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Solar Potential Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 Solar Potential Comparison Dashboard")
st.markdown("Compare solar energy potential across West African countries")

# Load data
@st.cache_data
def load_comparison_data():
    try:
        return pd.read_csv('detailed_country_comparison.csv')
    except:
        # Fallback sample data
        return pd.DataFrame({
            'Country': ['Benin', 'Sierra Leone', 'Togo'],
            'Avg_GHI': [240.56, 201.96, 230.56],
            'Peak_Hours': [149168, 121006, 140965],
            'Consistency_Score': [32.52, 28.38, 31.35],
            'Avg_RH': [54.49, 79.45, 55.01]
        })

df = load_comparison_data()

# Sidebar
st.sidebar.header("🎛️ Dashboard Controls")

# Country selection
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare:",
    df['Country'].unique(),
    default=df['Country'].unique()
)

# Metric selection
metric = st.sidebar.selectbox(
    "Select Metric to Display:",
    ['Avg_GHI', 'Peak_Hours', 'Consistency_Score', 'Avg_RH']
)

# Filter data
filtered_df = df[df['Country'].isin(selected_countries)]

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Solar Metrics Comparison")
    
    if not filtered_df.empty:
        # Bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Color mapping
        colors = {'Benin': 'orange', 'Sierra Leone': 'green', 'Togo': 'red'}
        bar_colors = [colors.get(country, 'blue') for country in filtered_df['Country']]
        
        bars = ax.bar(filtered_df['Country'], filtered_df[metric], color=bar_colors, alpha=0.7)
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.set_xlabel('Country')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:,.1f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Please select at least one country to display data.")

with col2:
    st.subheader("🏆 Country Rankings")
    
    if not filtered_df.empty:
        # Rank countries by selected metric
        ranked_df = filtered_df.sort_values(metric, ascending=False)
        
        for i, (_, row) in enumerate(ranked_df.iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            st.metric(
                label=f"{medal} {row['Country']}",
                value=f"{row[metric]:.1f}"
            )

# Additional visualizations
st.subheader("📈 Detailed Analysis")

tab1, tab2, tab3 = st.tabs(["Comparison Table", "Multiple Metrics", "Insights"])

with tab1:
    st.dataframe(
        filtered_df.style.background_gradient(cmap='Blues'),
        use_container_width=True
    )

with tab2:
    if not filtered_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_to_show = ['Avg_GHI', 'Peak_Hours', 'Consistency_Score', 'Avg_RH']
        titles = ['Avg GHI (W/m²)', 'Peak Hours', 'Consistency (%)', 'Humidity (%)']
        
        for i, (metric, title) in enumerate(zip(metrics_to_show, titles)):
            with [col1, col2, col3, col4][i]:
                best_country = filtered_df.loc[filtered_df[metric].idxmax()]
                st.metric(
                    label=f"Best: {title}",
                    value=f"{best_country[metric]:.1f}",
                    delta=best_country['Country']
                )

with tab3:
    if not filtered_df.empty:
        best_ghi = filtered_df.loc[filtered_df['Avg_GHI'].idxmax()]
        best_consistent = filtered_df.loc[filtered_df['Consistency_Score'].idxmax()]
        lowest_humidity = filtered_df.loc[filtered_df['Avg_RH'].idxmin()]
        
        st.info(f"**🌞 Best for Solar Projects:** {best_ghi['Country']} (Highest GHI: {best_ghi['Avg_GHI']:.1f} W/m²)")
        st.info(f"**📈 Most Consistent:** {best_consistent['Country']} ({best_consistent['Consistency_Score']:.1f}% consistency)")
        st.warning(f"**💧 Lowest Humidity:** {lowest_humidity['Country']} ({lowest_humidity['Avg_RH']:.1f}% RH)")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Solar Challenge Week 1")