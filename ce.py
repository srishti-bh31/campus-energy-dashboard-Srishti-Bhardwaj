import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

# TASK 1: DATA INGESTION + CLEANING

def load_and_merge_data(data_folder="data"):
    all_files = list(Path(data_folder).glob("*.csv"))
    merged_df = pd.DataFrame()
    logs = []

    for file in all_files:
        try:
            df = pd.read_csv(file, on_bad_lines="skip")

            # Add building name from filename
            df["building"] = file.stem

            # Convert timestamp
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            else:
                logs.append(f"Missing timestamp column in {file}")
                continue

            merged_df = pd.concat([merged_df, df], ignore_index=True)

        except Exception as e:
            logs.append(f"Error loading {file}: {e}")

    print("\n--- Ingestion Logs ---")
    for log in logs:
        print(log)

    return merged_df

# TASK 2: AGGREGATION LOGIC

def calculate_daily_totals(df):
    df = df.set_index("timestamp")
    return df.resample("D")["kwh"].sum().reset_index()

def calculate_weekly_aggregates(df):
    df = df.set_index("timestamp")
    return df.resample("W")["kwh"].mean().reset_index()

def building_wise_summary(df):
    summary = df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])
    summary.rename(columns={"sum": "total"}, inplace=True)
    return summary


# TASK 3: OOP DESIGN

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        return f"Building {self.name} total energy: {self.calculate_total_consumption()} kWh"

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_reading(self, building_name, reading):
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)
        self.buildings[building_name].add_reading(reading)

# TASK 4: VISUALIZATIONS

def generate_dashboard(df_daily, df_weekly, df_combined):
    plt.figure(figsize=(15, 12))

    # 1. Line Chart
    plt.subplot(3, 1, 1)
    plt.plot(df_daily["timestamp"], df_daily["kwh"])
    plt.title("Daily Electricity Consumption")
    plt.xlabel("Date")
    plt.ylabel("kWh")

    # 2. Bar Chart (Weekly)
    plt.subplot(3, 1, 2)
    plt.bar(df_weekly["timestamp"], df_weekly["kwh"])
    plt.title("Weekly Average Usage")
    plt.xlabel("Week")
    plt.ylabel("Avg kWh")

    # 3. Scatter Plot (Peak Load)
    plt.subplot(3, 1, 3)
    plt.scatter(df_combined["timestamp"], df_combined["kwh"])
    plt.title("Peak Hour Consumption")
    plt.xlabel("Timestamp")
    plt.ylabel("kWh")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    print("Dashboard saved as dashboard.png")

# TASK 5: SAVE FILES + EXECUTIVE SUMMARY

def generate_summary(df, df_building_summary):
    total_consumption = df["kwh"].sum()
    highest_building = df_building_summary["total"].idxmax()
    peak_row = df.loc[df["kwh"].idxmax()]

    summary = f"""
Campus Energy Summary
Total Campus Consumption: {total_consumption:.2f} kWh
Highest Consuming Building: {highest_building}
Peak Load Time: {peak_row['timestamp']} ({peak_row['kwh']} kWh)
"""

    with open("output/summary.txt", "w") as f:
        f.write(summary)

    print(summary)

# MAIN EXECUTION PIPELINE

def main():
    os.makedirs("output", exist_ok=True)

    df = load_and_merge_data()

    df = df.dropna(subset=["timestamp", "kwh"])

    df.to_csv("output/cleaned_energy_data.csv", index=False)

    daily_df = calculate_daily_totals(df)
    weekly_df = calculate_weekly_aggregates(df)
    building_summary_df = building_wise_summary(df)

    building_summary_df.to_csv("output/building_summary.csv")

    generate_dashboard(daily_df, weekly_df, df)

    generate_summary(df, building_summary_df)


if __name__ == "__main__":
    main()