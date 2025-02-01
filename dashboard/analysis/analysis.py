import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64


# Function to clean and filter data
def clean_data(df):
    df.dropna(inplace=True)
    df['Last_Update'] = pd.to_datetime(df['Last_Update'])

    if 'Country_Region' not in df.columns:
        return pd.DataFrame()

    df = df[df['Country_Region'] == 'US']
    df.drop(columns=['Long_', 'Lat'], errors='ignore', inplace=True)

    return df


# Load dataset
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


# Generate case fatality ratio histogram
def plot_case_fatality_ratio(cleaned_data):
    if 'Deaths' in cleaned_data.columns and 'Confirmed' in cleaned_data.columns:
        cleaned_data['Case_Fatality_Ratio'] = cleaned_data.apply(
            lambda row: (row['Deaths'] / row['Confirmed'] *
                         100) if row['Confirmed'] > 0 else 0,
            axis=1
        )

        plt.figure(figsize=(10, 6))
        sns.histplot(cleaned_data['Case_Fatality_Ratio'], kde=True)
        plt.title("Distribution of Case Fatality Ratio")
        plt.xlabel("Case Fatality Ratio (%)")

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return base64.b64encode(image_png).decode('utf-8')


# Generate correlation matrix heatmap
def plot_correlation_matrix(cleaned_data):
    numeric_data = cleaned_data.select_dtypes(include=['float64', 'int64'])
    correlation = numeric_data.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return base64.b64encode(image_png).decode('utf-8')


# Main function to process data and generate charts
def analyze_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(
        base_dir, r"C:\Users\aquil\ostds\assign1_covid\world_usage\processed_data.csv")  # Place your CSV here

    df = load_data(file_path)
    if df is not None:
        cleaned_data = clean_data(df)
        if not cleaned_data.empty:
            hist_img = plot_case_fatality_ratio(cleaned_data)
            heatmap_img = plot_correlation_matrix(cleaned_data)
            return hist_img, heatmap_img
    return None, None
