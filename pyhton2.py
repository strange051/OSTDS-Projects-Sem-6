import os
import pandas as pd

# Define the folder containing the CSV files
FOLDER_PATH = "assgn_1_corona/data/csse_covid_19_daily_reports"  # Change this to your actual folder path

def load_multiple_csvs(folder_path):
    """Reads all CSV files from a folder and combines them into a single DataFrame."""
    all_dataframes = []

    # Iterate through each file in the folder
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):  # Process only CSV files
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(file_path)
                all_dataframes.append(df)
                print(f"✅ Loaded: {file} ({df.shape[0]} rows, {df.shape[1]} columns)")
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")

    # Combine all dataframes into one
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        print(f"\n📊 Final Dataset Shape: {combined_df.shape}")
        return combined_df
    else:
        print("⚠ No CSV files found!")
        return None

def preprocess_data(df):
    """Performs basic preprocessing on the dataset."""
    print("\n🔍 Checking for missing values:")
    print(df.isnull().sum())

    # Fill missing values (if any)
    df.fillna(0, inplace=True)

    # Convert categorical variables to numeric (if needed)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('category').cat.codes

    print("\n✅ Data preprocessing complete.")
    return df

def analyze_data(df):
    """Basic analysis for classification problems."""
    print("\n📈 Dataset Overview:")
    print(df.describe())

    print("\n🔢 Checking class distribution (if applicable)...")
    if "Target" in df.columns:  # Assuming 'Target' column exists
        print(df["Target"].value_counts())

    print("\n✅ Data analysis complete.")

if __name__ == "__main__":
    df = load_multiple_csvs(FOLDER_PATH)
    if df is not None:
        df = preprocess_data(df)
        analyze_data(df)
