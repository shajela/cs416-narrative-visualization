import pandas as pd
import json

# Load the CSV data
print("Loading data...")
df = pd.read_csv('Energy_Usage_2010_20250719.csv')

print(f"Data shape: {df.shape}")
print("Columns:", df.columns.tolist())

# Clean and process the data
months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
          'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']

# Fill missing values with 0
df = df.fillna(0)

# Convert numeric columns
numeric_columns = []
for month in months:
    kwh_col = f'KWH {month} 2010'
    therm_col = f'THERM {month} 2010'
    if kwh_col in df.columns:
        numeric_columns.append(kwh_col)
    if therm_col in df.columns:
        numeric_columns.append(therm_col)

numeric_columns.extend(['TOTAL KWH', 'TOTAL THERMS'])

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Process by building type
building_type_summary = {}
monthly_totals = {}
building_type_monthly = {}

print("Processing building types...")
for building_type in df['BUILDING TYPE'].unique():
    if pd.isna(building_type) or building_type == '':
        continue
    
    building_data = df[df['BUILDING TYPE'] == building_type]
    
    building_type_summary[building_type] = {
        'totalKwh': float(building_data['TOTAL KWH'].sum()),
        'totalTherms': float(building_data['TOTAL THERMS'].sum()),
        'count': len(building_data)
    }
    
    building_type_monthly[building_type] = {}
    for month in months:
        kwh_col = f'KWH {month} 2010'
        therm_col = f'THERM {month} 2010'
        
        kwh_sum = building_data[kwh_col].sum() if kwh_col in df.columns else 0
        therm_sum = building_data[therm_col].sum() if therm_col in df.columns else 0
        
        building_type_monthly[building_type][month] = {
            'kwh': float(kwh_sum),
            'therms': float(therm_sum)
        }

print("Processing monthly totals...")
for month in months:
    kwh_col = f'KWH {month} 2010'
    therm_col = f'THERM {month} 2010'
    
    kwh_total = df[kwh_col].sum() if kwh_col in df.columns else 0
    therm_total = df[therm_col].sum() if therm_col in df.columns else 0
    
    monthly_totals[month] = {
        'kwh': float(kwh_total),
        'therms': float(therm_total)
    }

# Create summary data structure
processed_data = {
    'byBuildingType': building_type_summary,
    'monthlyTotals': monthly_totals,
    'buildingTypeMonthly': building_type_monthly
}

# Save processed data as JSON
print("Saving processed data...")
with open('processed_energy_data.json', 'w') as f:
    json.dump(processed_data, f, indent=2)

print("Data processing complete!")
print("\nBuilding Types Summary:")
for bt, data in building_type_summary.items():
    print(f"  {bt}: {data['totalKwh']:,.0f} KWH, {data['totalTherms']:,.0f} Therms, {data['count']} records")

print("\nMonthly Totals (KWH):")
for month, data in monthly_totals.items():
    print(f"  {month}: {data['kwh']:,.0f} KWH")
