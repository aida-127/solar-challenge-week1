# sierra_leone_eda.py - Solar Data Analysis for Sierra Leone
# Task 2: Data Profiling, Cleaning & EDA

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

print("🚀 Starting Sierra Leone Solar Data Analysis...")

# Load data
sierra_df = pd.read_csv('data/raw/sierraleone-bumbuna.csv')
print("✅ Sierra Leone data loaded successfully!")
print(f"Dataset shape: {sierra_df.shape}")

# ============================================================================
# TASK 2.1: Summary Statistics & Missing Values
# ============================================================================
print("\n" + "="*60)
print("📊 TASK 2.1: SUMMARY STATISTICS & MISSING VALUES")
print("="*60)

print("\nFirst 5 rows:")
print(sierra_df.head())

print("\nDataset info:")
print(sierra_df.info())

print("\nSummary statistics:")
print(sierra_df.describe())

print("\nMissing values:")
missing_values = sierra_df.isna().sum()
print(missing_values)

print("\nColumns with >5% missing values:")
missing_percent = (missing_values / len(sierra_df)) * 100
high_missing = missing_percent[missing_percent > 5]
print(high_missing)

# ============================================================================
# TASK 2.2: Data Cleaning & Outlier Detection
# ============================================================================
print("\n" + "="*60)
print("🧹 TASK 2.2: DATA CLEANING & OUTLIER DETECTION")
print("="*60)

# Drop Comments column if it exists and has 100% missing values
if 'Comments' in sierra_df.columns and sierra_df['Comments'].isna().all():
    sierra_clean = sierra_df.drop('Comments', axis=1)
    print(f"✅ Dropped 'Comments' column. New shape: {sierra_clean.shape}")
else:
    sierra_clean = sierra_df.copy()
    print("✅ No Comments column to drop")

# Convert timestamp
sierra_clean['Timestamp'] = pd.to_datetime(sierra_clean['Timestamp'])
sierra_clean['Hour'] = sierra_clean['Timestamp'].dt.hour
sierra_clean['Month'] = sierra_clean['Timestamp'].dt.month
print("✅ Converted timestamp and extracted time features")

# Outlier detection
key_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS', 'WSgust']
z_scores = np.abs(stats.zscore(sierra_clean[key_columns]))

print("\nOutliers (Z-score > 3):")
outlier_counts = (z_scores > 3).sum(axis=0)
for col, count in zip(key_columns, outlier_counts):
    print(f"  {col}: {count} outliers ({count/len(sierra_clean)*100:.2f}%)")

# Remove extreme outliers
extreme_outliers = (z_scores > 5).any(axis=1)
sierra_clean = sierra_clean[~extreme_outliers]
print(f"✅ Removed {extreme_outliers.sum()} extreme outlier rows")
print(f"📈 Final cleaned shape: {sierra_clean.shape}")

# ============================================================================
# TASK 2.3: Time Series Analysis
# ============================================================================
print("\n" + "="*60)
print("📈 TASK 2.3: TIME SERIES ANALYSIS")
print("="*60)

print(f"Data covers: {sierra_clean['Timestamp'].min()} to {sierra_clean['Timestamp'].max()}")
print(f"Total days: {(sierra_clean['Timestamp'].max() - sierra_clean['Timestamp'].min()).days}")

# Daily patterns
daytime_data = sierra_clean[sierra_clean['GHI'] > 0]
hourly_ghi = daytime_data.groupby('Hour')['GHI'].mean()

plt.figure(figsize=(10, 6))
plt.plot(hourly_ghi.index, hourly_ghi.values, marker='o', linewidth=2, color='green')
plt.title('Average Solar Radiation (GHI) by Hour - Sierra Leone')
plt.xlabel('Hour of Day')
plt.ylabel('Average GHI (W/m²)')
plt.grid(True)
plt.savefig('sierra_leone_hourly_ghi.png')
plt.show()

print(f"Peak solar hours: {hourly_ghi.nlargest(3).index.tolist()}")

# ============================================================================
# TASK 2.4: Correlation Analysis
# ============================================================================
print("\n" + "="*60)
print("🔗 TASK 2.4: CORRELATION ANALYSIS")
print("="*60)

correlation_cols = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'TModA', 'TModB']
corr_matrix = sierra_clean[correlation_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Heatmap - Sierra Leone Solar Data')
plt.tight_layout()
plt.savefig('sierra_leone_correlation_heatmap.png')
plt.show()

print("Top correlations with GHI:")
ghi_correlations = corr_matrix['GHI'].sort_values(ascending=False)
print(ghi_correlations.head(6))

# ============================================================================
# TASK 2.5: Save Cleaned Data
# ============================================================================
print("\n" + "="*60)
print("💾 TASK 2.5: SAVE CLEANED DATA")
print("="*60)

sierra_clean.to_csv('data/clean/sierra_leone_clean.csv', index=False)
print("✅ Cleaned data saved to: data/clean/sierra_leone_clean.csv")

print("\n🎉 SIERRA LEONE ANALYSIS COMPLETED! 🎉")