import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import glob
from django.shortcuts import render

def encode_plot_to_uri():
    """Encodes Matplotlib plots to a base64 URI for embedding in HTML."""
    buf = BytesIO()  # Create an in-memory buffer to save the plot
    plt.savefig(buf, format='png', bbox_inches='tight')  # Save the plot to the buffer in PNG format
    buf.seek(0)  # Rewind the buffer to the beginning
    encoded = base64.b64encode(buf.read()).decode()  # Encode the plot as base64 string
    plt.close()  # Close the plot to free up memory
    return f"data:image/png;base64,{encoded}"  # Return the base64 image URI

def clean_data(df):
    """Cleans and standardizes the dataset."""
    # Clean column names by stripping spaces and replacing spaces with underscores
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    # Convert the 'Last_Update' column to datetime, coercing errors to NaT
    df['Last_Update'] = pd.to_datetime(df['Last_Update'], errors='coerce')
    
    # Ensure all required columns are present, filling missing ones with 0
    required_columns = ['Last_Update', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Country_Region']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # Fill missing columns with default values
    
    # Drop duplicate rows from the dataframe
    df.drop_duplicates(inplace=True)
    return df

def load_cleaned_data():
    """Loads and cleans data from CSV files."""
    base_dir = os.path.dirname(__file__)  # Get the base directory of the current file
    data_dir = os.path.join(base_dir, "..", "..", "csse_covid_19_daily_reports")  # Define the directory containing CSV files
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))[:15]  # Get a list of CSV files, limit to 25 for performance

    if not csv_files:
        return pd.DataFrame(columns=['Last_Update', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Country_Region']), []

    df_list = []  # Initialize an empty list to hold dataframes
    for file in csv_files:
        try:
            # Read the CSV file, keeping only relevant columns and a subset of rows for efficiency
            temp_df = pd.read_csv(file, usecols=lambda col: col in ['Last_Update', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Country_Region'], nrows=1000)
            df_list.append(temp_df)
        except Exception as e:
            print(f"Error reading {file}: {e}")  # Print any errors encountered during reading

    # Concatenate all dataframes in the list into one dataframe
    df = pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()
    df = clean_data(df)  # Clean the combined dataframe

    # Get a sorted list of unique countries from the data
    countries = df['Country_Region'].dropna().unique().tolist() if not df.empty else []

    return df, sorted(countries)

def histogram_view(request):
    """Generates a histogram of Case Fatality Ratio with country selection."""
    df, countries = load_cleaned_data()  # Load and clean the data
    selected_country = request.GET.get('country', None)  # Get the selected country from the request

    # Filter the data if a valid country is selected
    if selected_country and selected_country in df['Country_Region'].values:
        df = df[df['Country_Region'] == selected_country]

    # Check if the data is valid and the 'Case_Fatality_Ratio' column exists
    if not df.empty and 'Case_Fatality_Ratio' in df.columns:
        sns.histplot(df['Case_Fatality_Ratio'].dropna(), kde=True)  # Generate the histogram
        image = encode_plot_to_uri()  # Encode the plot to base64 URI
    else:
        image = None  # No valid data, so no plot is generated

    # Render the histogram view template with the plot and country list
    return render(request, 'dashboard/histogram.html', {'image': image, 'countries': countries, 'selected_country': selected_country})

def correlation_view(request):
    """Generates a correlation matrix heatmap."""
    df, _ = load_cleaned_data()  # Load and clean the data
    if not df.empty:
        # Generate the correlation matrix for numerical columns and create a heatmap
        sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap='coolwarm', fmt=".2f")
    image = encode_plot_to_uri()  # Encode the plot to base64 URI
    return render(request, 'dashboard/correlation.html', {'image': image})

def time_series_view(request):
    """Generates a time series plot of confirmed COVID-19 cases."""
    df, _ = load_cleaned_data()  # Load and clean the data
    if not df.empty:
        # Group the data by 'Last_Update' and sum the confirmed cases
        df = df.groupby('Last_Update', as_index=False)['Confirmed'].sum()
        df.set_index('Last_Update', inplace=True)  # Set the 'Last_Update' as the index
        df['Confirmed'].plot(figsize=(10, 5))  # Generate the time series plot
        plt.xlabel("Date")
        plt.ylabel("Confirmed Cases")
        plt.title("COVID-19 Time Series")
    image = encode_plot_to_uri()  # Encode the plot to base64 URI
    return render(request, 'dashboard/time_series.html', {'image': image})

def bar_chart_view(request):
    """Generates a bar chart of top 10 affected countries."""
    df, countries = load_cleaned_data()  # Load and clean the data
    selected_country = request.GET.get('country', None)  # Get the selected country from the request

    # Filter the data if a valid country is selected
    if selected_country and selected_country in df['Country_Region'].values:
        df = df[df['Country_Region'] == selected_country]

    if not df.empty:
        # Group the data by 'Country_Region' and sum the confirmed cases, then generate the bar chart for the top 10 countries
        df.groupby('Country_Region', as_index=False)['Confirmed'].sum().nlargest(10, 'Confirmed').plot(x='Country_Region', y='Confirmed', kind='bar', figsize=(10, 5))
    image = encode_plot_to_uri()  # Encode the plot to base64 URI
    return render(request, 'dashboard/bar_chart.html', {'image': image, 'countries': countries, 'selected_country': selected_country})

def pie_chart_view(request):
    """Generates a pie chart of top 5 affected countries."""
    df, countries = load_cleaned_data()  # Load and clean the data
    selected_country = request.GET.get('country', None)  # Get the selected country from the request

    # Filter the data if a valid country is selected
    if selected_country and selected_country in df['Country_Region'].values:
        df = df[df['Country_Region'] == selected_country]

    if not df.empty:
        # Group the data by 'Country_Region' and sum the confirmed cases, then generate the pie chart for the top 5 countries
        df.groupby('Country_Region', as_index=False)['Confirmed'].sum().nlargest(5, 'Confirmed').set_index('Country_Region').plot(kind='pie', y='Confirmed', autopct='%1.1f%%', figsize=(7, 7))
    image = encode_plot_to_uri()  # Encode the plot to base64 URI
    return render(request, 'dashboard/pie_chart.html', {'image': image, 'countries': countries, 'selected_country': selected_country})

def box_plot_view(request):
    """Generates a box plot for confirmed COVID-19 cases."""
    df, _ = load_cleaned_data()  # Load and clean the data
    if not df.empty:
        sns.boxplot(x=df['Confirmed'])  # Generate the box plot for 'Confirmed' cases
    image = encode_plot_to_uri()  # Encode the plot to base64 URI
    return render(request, 'dashboard/box_plot.html', {'image': image})

def index(request):
    """Renders the dashboard index page."""
    # Define a list of available visualizations to display on the index page
    visualizations = [
        {'url_name': 'histogram', 'display_name': 'Histogram'},
        {'url_name': 'correlation', 'display_name': 'Correlation Matrix'},
        {'url_name': 'time_series', 'display_name': 'Time Series'},
        {'url_name': 'bar_chart', 'display_name': 'Bar Chart'},
        {'url_name': 'pie_chart', 'display_name': 'Pie Chart'},
        {'url_name': 'box_plot', 'display_name': 'Box Plot'},
    ]
    # Render the index page with the list of visualizations
    return render(request, 'dashboard/index.html', {'visualizations': visualizations})
