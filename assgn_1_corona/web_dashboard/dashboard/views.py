from django.shortcuts import render
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from dashboard.utils.cleaner import clean_data
from dashboard.utils.analysis import analyze_data

def encode_plot_to_uri():
    """Helper function to encode the current plot to a base64 URI"""
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close()
    return f"data:image/png;base64,{encoded}"

def load_cleaned_data():
    """Loads and cleans the dataset"""
    base_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(base_dir, "..", "..", "data", "01-01-2021.csv")
    df = pd.read_csv(csv_file_path)
    cleaned_data = clean_data(df)
    analyze_data(cleaned_data)
    return cleaned_data

def histogram_view(request):
    df = load_cleaned_data()
    if 'Case_Fatality_Ratio' in df.columns:
        sns.histplot(df['Case_Fatality_Ratio'].dropna(), kde=True)
    image = encode_plot_to_uri()
    return render(request, 'dashboard/histogram.html', {'image': image})

def correlation_view(request):
    df = load_cleaned_data()
    numeric_data = df.select_dtypes(include=['number'])
    sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    image = encode_plot_to_uri()
    return render(request, 'dashboard/correlation.html', {'image': image})

def time_series_view(request):
    df = load_cleaned_data()

    if 'Last_Update' in df.columns and 'Confirmed' in df.columns:
        df['Last_Update'] = pd.to_datetime(df['Last_Update'])
        df = df.groupby('Last_Update')['Confirmed'].sum().reset_index()
        df.set_index('Last_Update', inplace=True)
        
        plt.figure(figsize=(10, 5))
        df['Confirmed'].plot()
        plt.xlabel("Date")
        plt.ylabel("Confirmed Cases")
        plt.title("COVID-19 Time Series")

        image = encode_plot_to_uri()
        plt.close()
    else:
        image = None  # Handle case when columns are missing

    return render(request, 'dashboard/time_series.html', {'image': image})


def bar_chart_view(request):
    df = load_cleaned_data()
    df.groupby('Country_Region')['Confirmed'].sum().nlargest(10).plot(kind='bar', figsize=(10, 5))
    image = encode_plot_to_uri()
    return render(request, 'dashboard/bar_chart.html', {'image': image})

def pie_chart_view(request):
    df = load_cleaned_data()
    df.groupby('Country_Region')['Confirmed'].sum().nlargest(5).plot(kind='pie', autopct='%1.1f%%', figsize=(7, 7))
    image = encode_plot_to_uri()
    return render(request, 'dashboard/pie_chart.html', {'image': image})

def box_plot_view(request):
    df = load_cleaned_data()
    sns.boxplot(x=df['Confirmed'])
    image = encode_plot_to_uri()
    return render(request, 'dashboard/box_plot.html', {'image': image})

def index(request):
    return render(request, 'dashboard/index.html')
