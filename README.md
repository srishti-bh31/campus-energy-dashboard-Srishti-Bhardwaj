# campus-energy-dashboard-Srishti-Bhardwaj
# Capstone Project

This project is part of the **Programming for Problem Solving using Python** course.  
The goal is to build an **end-to-end energy analysis pipeline** that reads electricity meter data from multiple buildings, cleans and processes it, calculates useful summaries, and generates visual dashboards along with an executive summary.

## Project Overview

The campus administration wants to identify energy-saving opportunities by analyzing electricity usage across different buildings.  
This dashboard helps visualize:

- Daily consumption trends  
- Weekly average usage  
- Peak load hours  
- Building-wise performance  

The project uses **Python, Pandas, Matplotlib, and Object-Oriented Programming (OOP)**.

## Tasks Completed

### ** Task 1 **
- Automatically loads all `.csv` files from `/data/`
- Skips bad lines and handles missing timestamps
- Adds building name from filename
- Combines all data into a single DataFrame

### ** Task 2 **
- Calculates daily total energy consumption  
- Calculates weekly average consumption  
- Creates a building-wise summary containing:
  - Mean  
  - Minimum  
  - Maximum  
  - Total kWh

### **Task 3**
Implemented three classes:

- **MeterReading** → Holds timestamp + kWh  
- **Building** → Stores readings and calculates totals  
- **BuildingManager** → Manages all building objects  

### ** Task 4**
Generated a single `dashboard.png` containing:

1. **Line Chart** – Daily consumption trend  
2. **Bar Chart** – Weekly average comparison  
3. **Scatter Plot** – Peak load hours  

All charts include proper titles, labels, and formatting.

### **✔ Task 5 — Persistence & Executive Summary**
Exported:

- Cleaned dataset  
- Building summary  
- A well-written `summary.txt` that includes:
  - Total campus consumption  
  - Highest consuming building  
  - Peak load time & value  
  - Trend observations (daily + weekly)


