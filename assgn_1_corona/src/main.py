# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# def clean_data(df):     
#     df.dropna(inplace=True)  # Example: Drop missing values 
#     df['Last_Update'] = pd.to_datetime(df['Last_Update'])  # Convert date columns to datetime
#     # TODO extract only US data
#     return df 
#     # Add more cleaning steps as needed 

# data = pd.read_csv("D:\\Home\\Desktop\\OSTDS\\assgn_1_corona\\data\\01-01-2021.csv")
# df = pd.DataFrame(data)
  
# cleaned_data = clean_data(df) 
# cleaned_data.to_csv('D:\\Home\\Desktop\\OSTDS\\assgn_1_corona\\data\\processed_data.csv', index=False) 

# plt.figure(figsize=(10, 6))
# # sns.heatmap(correlation, annot=True, cmap='coolwarm')
# plt.show()

# # summary = cleaned_data.describe() 
# # # TODO correlation = cleaned_data.corr() 
# # print(summary) 
# # print(correlation) 

# # TODO omit long,lat,fix correlation, get statewise summary data, get insight into deaths, recovered, case fatality ratio
# # TODO exception handling, relative path, logging(logging library)(set log level), output beautificaiton and visual dashboard


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from logger import setup_logger
 
 
# logging.basicConfig(level=logging.INFO)
 
def clean_data(df):    
    df.dropna(inplace=True)  
    df['Last_Update'] = pd.to_datetime(df['Last_Update'])  
   
     
    logger.info(f"Columns in the dataset: {df.columns.tolist()}")
   
     
    if 'Country_Region' in df.columns:
        df = df[df['Country_Region'] == 'US']  
    else:
        logger.error("'Country_Region' column not found.")
        return df  
   
     
    exclude_columns = ['Long_', 'Lat']
    df = df.drop(columns=exclude_columns, errors='ignore')  
   
    return df
 
if __name__ == '__main__':

    logger = setup_logger(log_level = "DEBUG")
    csv_file_path = "D:\\Home\\Desktop\\OSTDS\\assgn_1_corona\\data\\01-01-2021.csv"
    logger.warning(f"Running analysis on singal file only")
 
    try:       
        data = pd.read_csv(csv_file_path)
        df = pd.DataFrame(data)
        logger.info("Data successfully loaded")
    except FileNotFoundError:
        logger.error(f"File not found at path: {csv_file_path}. Please check the file path.")
        df = None  
    except pd.errors.ParserError:
        logger.error("Error reading the CSV file. It may be malformed.")
        df = None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        df = None
 
   
    if df is not None:
       
        cleaned_data = clean_data(df)
 
       
        processed_file_path = "C:\\Users\\hp\\Desktop\\OSTDS\\assgn_1_corona\\data\\processed_data.csv"
        cleaned_data.to_csv(processed_file_path, index=False)
        logger.info(f"Cleaned data saved to {processed_file_path}")
 
       
        if 'Province_State' in cleaned_data.columns:
            statewise_summary = cleaned_data.groupby('Province_State').describe()    
            print(statewise_summary)
 
       
        if 'Deaths' in cleaned_data.columns and 'Confirmed' in cleaned_data.columns:
            cleaned_data['Case_Fatality_Ratio'] = (cleaned_data['Deaths'] / cleaned_data['Confirmed']) * 100
           
            plt.figure(figsize=(10, 6))
            sns.histplot(cleaned_data['Case_Fatality_Ratio'], kde=True)
            plt.title("Distribution of Case Fatality Ratio")
            plt.xlabel("Case Fatality Ratio (%)")
            plt.show()
 
       
        numeric_data = cleaned_data.select_dtypes(include=['float64', 'int64'])  
        correlation = numeric_data.corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm')
        plt.title("Correlation Matrix")
        plt.show()
 
    else:
        logger.error("Data loading failed. Exiting the script.")
 
 
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
 
# def convert_columns_to_numeric(df, column_list):
#     for column in column_list:
#         df[column] = pd.to_numeric(df[column], errors='coerce')
#     return df
 
# def analyze_data(file_path):
#     data = pd.read_csv(file_path)
#     # Convert specific columns to numeric
#     columns_to_convert = data.select_dtypes(include=['object']).columns.tolist() # Adjust this list based on your dataset
#     data = convert_columns_to_numeric(data, columns_to_convert)
#     data = data.dropna()  # Drop rows with non-convertible values
#     # Basic EDA
#     summary = data.describe()
#     print(summary)
#     # Correlation analysis
#     correlation = data.corr()
#     print("Correlation Matrix:\n", correlation)
#     # Visualization
#     sns.heatmap(correlation, annot=True, cmap='coolwarm')
#     plt.show()
 
# if __name__ == "__main__":
#     analyze_data('C:\\Users\\hp\\Desktop\\OSTDS\\assgn_1_corona\\data\\processed_data.csv')