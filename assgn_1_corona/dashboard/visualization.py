import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import base64
from io import BytesIO

def generate_plot(df):
    plt.figure(figsize=(10, 5))

    # Ensure 'last_update' is used as the x-axis (converted to date format)
    df["date"] = df["last_update"].dt.date
    daily_cases = df.groupby("date")["confirmed"].sum().reset_index()

    # Seaborn Line Plot
    sns.lineplot(data=daily_cases, x="date", y="confirmed", marker="o")
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Confirmed Cases")
    plt.title("Daily COVID-19 Cases")

    # Convert plot to base64 for HTML rendering
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    return f"data:image/png;base64,{encoded_img}"
