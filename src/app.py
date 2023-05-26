import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV data
@st.cache
def load_data():
    df = pd.read_csv(r"/app/5-25_gym_hardstyle.csv", index_col=0)
    return df

# Load data
data = load_data()

# Select country
countries = data.index.tolist()
selected_country = st.selectbox("Select a country", countries)

# Remove unexpected columns
data = data.loc[:, ~data.columns.str.startswith('Unnamed')]

# Plot the data for the selected country
fig, ax = plt.subplots(figsize=(28, 14))  # Adjust the figure size as desired

# Select a subset of dates to display
num_dates = data.shape[1]  # Total number of dates
num_display_dates = 130  # Number of dates to display (increase this value for more dates)
display_dates = np.linspace(0, num_dates - 1, num=num_display_dates, dtype=int)  # Select evenly spaced dates
dates = data.columns[display_dates]

# Convert values to numeric
data_numeric = data.loc[selected_country, dates].apply(pd.to_numeric, errors='coerce')

ax.plot(dates, data_numeric, marker='o', linestyle='-', label='Data')
ax.set_xlabel('Date')
ax.set_ylabel('Ranking')
ax.set_title(f'{selected_country}', loc='left')

# Reduce number of visible ticks on the x-axis
num_ticks = num_display_dates
step_size = len(dates) // (num_ticks - 1)
visible_dates = dates[::step_size]
ax.set_xticks(visible_dates)
ax.tick_params(axis='x', labelsize=8)

# Set y-axis limits with padding
padding = 5  # Adjust the padding as desired
min_value = 0
max_value = np.ceil(data_numeric.max() / 5) * 5  # Round up the max value to the nearest multiple of 5
ax.set_ylim(min_value, max_value)

# Set y-axis increment marks
increment_marks = np.arange(min_value, max_value + 1, 5)  # Adjust the increment as desired
ax.set_yticks(increment_marks)

# Set y-axis minor increment marks (increment by 1)
increment_marks_minor = np.arange(min_value, max_value + 1, 1)  # Adjust the minor increment as desired
ax.set_yticks(increment_marks_minor, minor=True)
ax.yaxis.grid(True, which='minor', linestyle='--', alpha=0.5)  # Add gridlines for minor increment

# Add data point markers
ax.plot(dates, data_numeric, marker='o', linestyle='-', label='Data')

# Add grid lines
ax.grid(True, linestyle='--', alpha=0.5)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the plot using Streamlit
st.pyplot(fig)

# Select dates
dates = data.columns
start_date = st.selectbox("Select start date", dates)
end_date = st.selectbox("Select end date", dates)

# Get the ranking for the selected dates
start_ranking = data[start_date].apply(pd.to_numeric, errors='coerce')
end_ranking = data[end_date].apply(pd.to_numeric, errors='coerce')

# Find countries with rank up, rank down, and rank stays the same
countries_rank_up = end_ranking[end_ranking > start_ranking]
countries_rank_down = end_ranking[end_ranking < start_ranking]
countries_rank_same = end_ranking[end_ranking == start_ranking]

# Display changes for high priority countries
st.subheader(f"Changes in High Priority Countries from {start_date} to {end_date}")
high_priority_countries = ["United States of America", "Germany", "Brazil", "Japan", "United Kingdom", "Spain", "France", "Italy", "Australia", "Canada", "Sweden"]
change_data = {
    'Country': [],
    'Change Type': [],
    'Change Amount': []
}
for country in high_priority_countries:
    start_rank = start_ranking.loc[country]
    end_rank = end_ranking.loc[country]
    if pd.isna(start_rank) or pd.isna(end_rank):
        continue
    change = end_rank - start_rank
    change_type = 'Rank Up' if change > 0 else 'Rank Down' if change < 0 else 'No Change'
    change_data['Country'].append(country)
    change_data['Change Type'].append(change_type)
    change_data['Change Amount'].append(change)

change_df = pd.DataFrame(change_data)
st.dataframe(change_df)

# Display countries with rank up, rank down, and rank stays the same side by side
col1, col2, col3 = st.beta_columns(3)

# Display countries with rank up
with col1:
    st.subheader(f"Countries with Rank Up from {start_date} to {end_date}")
    rank_up_data = {
        'Country': [],
        'Rank Difference': []
    }
    for country, rank_up in countries_rank_up.items():
        rank_difference = rank_up - start_ranking[country]
        rank_up_data['Country'].append(country)
        rank_up_data['Rank Difference'].append(rank_difference)

    rank_up_df = pd.DataFrame(rank_up_data)
    rank_up_df = rank_up_df.sort_values(by='Rank Difference', ascending=False)  # Sort in descending order
    st.dataframe(rank_up_df)

# Display countries with rank down
with col2:
    st.subheader(f"Countries with Rank Down from {start_date} to {end_date}")
    rank_down_data = {
        'Country': [],
        'Rank Difference': []
    }
    for country, rank_down in countries_rank_down.items():
        rank_difference = start_ranking[country] - rank_down
        rank_down_data['Country'].append(country)
        rank_down_data['Rank Difference'].append(rank_difference)

    rank_down_df = pd.DataFrame(rank_down_data)
    rank_down_df = rank_down_df.sort_values(by='Rank Difference', ascending=False)  # Sort in descending order
    st.dataframe(rank_down_df)

# Display countries with rank stays the same
with col3:
    st.subheader(f"Countries with Rank Stays the Same from {start_date} to {end_date}")
    rank_same_data = {
        'Country': [],
        'Rank': []
    }
    for country, rank_same in countries_rank_same.items():
        rank_same_data['Country'].append(country)
        rank_same_data['Rank'].append(rank_same)

    rank_same_df = pd.DataFrame(rank_same_data)
    st.dataframe(rank_same_df)
