# fix_saving.py - Fix data saving issue
import pandas as pd
import os

print("🔧 FIXING DATA SAVING...")

# Ensure clean directory exists
os.makedirs('data/clean', exist_ok=True)
print("✅ Created data/clean directory")

# Load and save Benin data
print("\n💾 SAVING BENIN DATA...")
benin_df = pd.read_csv('data/raw/benin-malanville.csv')
benin_clean = benin_df.drop('Comments', axis=1)
benin_clean['Timestamp'] = pd.to_datetime(benin_clean['Timestamp'])
benin_clean.to_csv('data/clean/benin_clean.csv', index=False)
print("✅ Benin data saved!")

# Load and save Sierra Leone data
print("\n💾 SAVING SIERRA LEONE DATA...")
sierra_df = pd.read_csv('data/raw/sierraleone-bumbuna.csv')
sierra_clean = sierra_df.drop('Comments', axis=1)
sierra_clean['Timestamp'] = pd.to_datetime(sierra_clean['Timestamp'])
sierra_clean.to_csv('data/clean/sierra_leone_clean.csv', index=False)
print("✅ Sierra Leone data saved!")

# Load and save Togo data
print("\n💾 SAVING TOGO DATA...")
togo_df = pd.read_csv('data/raw/togo-dapaong_qc.csv')
togo_clean = togo_df.drop('Comments', axis=1)
togo_clean['Timestamp'] = pd.to_datetime(togo_clean['Timestamp'])
togo_clean.to_csv('data/clean/togo_clean.csv', index=False)
print("✅ Togo data saved!")

print("\n🎉 ALL CLEANED DATA SAVED SUCCESSFULLY!")
print("📁 Files saved in data/clean/")