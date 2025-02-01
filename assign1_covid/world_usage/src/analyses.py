import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def convert_columns_to_numeric(df, column_list):
    for column in column_list:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


def analyze_data(file_path):
    data = pd.read_csv(file_path)
    # Convert specific columns to numeric
    # Adjust this list based on your dataset
    columns_to_convert = data.select_dtypes(
        include=['object']).columns.tolist()
    data = convert_columns_to_numeric(data, columns_to_convert)
    data = data.dropna()  # Drop rows with non-convertible values
    # Basic EDA
    summary = data.describe()
    print(summary)
    # Correlation analysis
    correlation = data.corr()
    print("Correlation Matrix:\n", correlation)
    # Visualization
    sns.heatmap(correlation, annot=True, cmap='coolwarm')
    plt.show()


if __name__ == "__main__":
    analyze_data(
        r'C:\Users\aquil\ostds\assign1_covid\world_usage\processed_data.csv')
