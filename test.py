import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_duration(start_time_str, end_time_str, time_format='%Y-%m-%d %H:%M:%S'):
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)
    duration_sec = (end_time - start_time).total_seconds()
    return duration_sec

# Load data
df = pd.read_csv('data/jiodata1.csv')

screen_name = ['Mobile', 'Fiber', 'Music', 'TV', 'Shop', 'UPI', 'Bank', 
               'play&Win', 'Health', 'Movies', 'Events', 'JioStore', 'Pharmacy',
               'Banner1', 'Banner2', 'Banner3', 'Banner4', 'Banner5', 'Banner6', 
               'Banner7', 'Banner8', 'Banner9', 'nonjio_no', 'port_no', 'bookfiber', 
               'getjofiber', 'getprepaid', 'getpostpaid', 'porttojio']

# Store histograms in a dictionary
histograms = {}

# Create histograms for each screen
for screen in screen_name:
    screen_times = []
    start_time = None

    for index, row in df.iterrows():
        if row['Screen'] == screen:
            if start_time is None:
                start_time = row['Time']
        elif row['Screen'] == 'App Kill' and start_time is not None:
            end_time = row['Time']
            duration_sec = calculate_duration(start_time, end_time)
            screen_times.append(duration_sec)
            start_time = None

    if screen_times:
        plt.figure(figsize=(12, 8))
        plt.hist(screen_times, bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Frequency')
        plt.title(f'Time spent on {screen}')
        plt.grid(axis='y')
        plt.tight_layout()
        
        # Store the plot in the dictionary
        histograms[screen] = plt
    else:
        print(f"No data found for {screen}.")

# Streamlit app
st.title('Screen Time Analysis')

# Dropdown to select the desired chart
selected_chart = st.selectbox('Select a Screen', screen_name)

# Display the selected chart
if selected_chart in histograms:
    st.pyplot(histograms[selected_chart])
else:
    st.write("No data found for the selected screen.")
