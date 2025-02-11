# COVID-19 Data Analysis and Visualization

## 📌 Overview
This project is a COVID-19 data analysis and visualization dashboard built using Python, Pandas, Seaborn, and Django. The web-based dashboard provides insights into COVID-19 cases using various visualizations.

## 🔥 Features
- **Data Cleaning:** Preprocessing raw COVID-19 data.
- **Exploratory Data Analysis (EDA):** Statistical summaries and visualizations.
- **Web Dashboard:** Interactive UI to explore visualizations.
- **Visualizations:** Correlation matrix, histograms, time series analysis, etc.
- **Logging:** Error tracking and debugging logs.

## 📂 Folder Structure
```
.
├── assgn_1_corona
│   ├── data
│   │   ├── 01-01-2021.csv  # Raw COVID-19 data
│   │   ├── processed_data.csv  # Cleaned dataset
│   ├── README.md
│   ├── src
│   └── web_dashboard
│       ├── dashboard
│       │   ├── admin.py
│       │   ├── apps.py
│       │   ├── models.py
│       │   ├── tests.py
│       │   ├── urls.py
│       │   ├── views.py  # Handles web requests
│       │   ├── templates/dashboard  # HTML templates
│       │   ├── utils  # Helper functions
│       │   │   ├── analysis.py  # Data analysis
│       │   │   ├── cleaner.py  # Data cleaning
│       │   │   ├── logger.py  # Logging module
│       ├── logs  # Log files
│       ├── manage.py  # Django management script
│       ├── web_dashboard
│       │   ├── settings.py  # Django settings
│       │   ├── urls.py  # URL routing
│       │   ├── wsgi.py  # WSGI entry point
├── LICENSE
├── README.md
├── requirements.txt  # Dependencies
```

## ⚙️ Installation
### Prerequisites
- Python 3.10+
- Django
- Pandas
- Seaborn

### Setup Steps
```sh
# Clone the repository
git clone https://github.com/strange051/OSTDS-Projects-Sem-6.git
cd OSTDS-Projects-Sem-6

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Django server
cd assign_1_corona/web_dashboard
python manage.py runserver
```

## 📊 Visualizations Included
- **Correlation Matrix**
- **Histogram Analysis**
- **Time Series of Confirmed Cases**
