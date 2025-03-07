from django.shortcuts import render
import pandas as pd
import os
import logging
import json
from django.conf import settings

# Setup logging
logger = logging.getLogger(__name__)

# Path to the folder containing CSV files
DATA_FOLDER_PATH = os.path.join(settings.BASE_DIR, "assgn_1_corona", "data", "csse_covid_19_daily_reports")

def load_all_datasets():
    """Load, merge, and clean all CSV files in the data folder."""
    all_files = [os.path.join(DATA_FOLDER_PATH, f) for f in os.listdir(DATA_FOLDER_PATH) if f.endswith('.csv')]
    df_list = []
    
    for file in all_files:
        try:
            df = pd.read_csv(file, delimiter=',', encoding="utf-8")
            df["Date"] = os.path.basename(file).split('.')[0]  # Extract date from filename
            df_list.append(df)
        except Exception as e:
            logger.error(f"Error loading {file}: {e}")

    if not df_list:
        logger.warning("No CSV files found or failed to load.")
        return None
    
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Handling missing values
    combined_df.fillna(0, inplace=True)  # Replace NaN with 0 for numerical stability
    
    # Keep only relevant columns
    important_columns = ['Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Date']
    combined_df = combined_df[important_columns]
    
    # Ensure numeric columns are properly formatted
    for col in ['Confirmed', 'Deaths', 'Recovered']:
        combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce').fillna(0).astype(int)
    
    return combined_df

# Load dataset once
logger.info("Loading datasets...")
df_cache = load_all_datasets()

def dashboard_view(request):
    logger.info("Rendering dashboard view")
    return render(request, 'dashboard/dashboard.html')

def pie_chart_view(request):
    """Render pie chart based on confirmed cases by country."""
    pie_data = {}
    if df_cache is not None and not df_cache.empty:
        pie_data = df_cache.groupby('Country_Region')['Confirmed'].sum().nlargest(10).to_dict()
    
    return render(request, 'dashboard/pie_chart.html', {'pie_data': json.dumps(pie_data)})

def bar_chart_view(request):
    """Render bar chart based on deaths by country."""
    bar_data = {}
    if df_cache is not None and not df_cache.empty:
        bar_data = df_cache.groupby('Country_Region')['Deaths'].sum().to_dict()
    
    return render(request, 'dashboard/bar_chart.html', {'bar_data': json.dumps(bar_data)})

def histogram_view(request):
    """Render histogram chart based on active cases by country."""
    histogram_data = {}
    if df_cache is not None and not df_cache.empty:
        df_cache['Active'] = df_cache['Confirmed'] - df_cache['Recovered'] - df_cache['Deaths']
        histogram_data = df_cache.groupby('Country_Region')['Active'].sum().nlargest(10).to_dict()
    
    return render(request, 'dashboard/histogram.html', {'histogram_data': json.dumps(histogram_data)})

def area_chart_view(request):
    """Render an area chart showing confirmed cases over time."""
    area_data = {}
    if df_cache is not None and not df_cache.empty:
        area_data = df_cache.groupby('Date')['Confirmed'].sum().to_dict()
    
    return render(request, 'dashboard/area_chart.html', {'area_data': json.dumps(area_data)})
