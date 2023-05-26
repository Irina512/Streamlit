import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors

# Set default retention rates and number of years
default_retention_rates = [0.5, 0.7, 0.9]
default_num_years = 5

# Create a custom color map from green to red based on quartiles
color_map = mcolors.LinearSegmentedColormap.from_list('green_to_red', ['green', 'yellow', 'red'])

def calculate_powers(retention_rates, num_years):
    powers = np.arange(0, num_years + 1)
    results_data = []

    # Create the figure object
    fig, ax = plt.subplots(figsize=(8, 6))

    for idx, rate in enumerate(retention_rates):
        results = np.round((rate ** powers) * 100).astype(int)
        quartiles = np.percentile(results, [25, 50, 75])
        colors = [color_map((val - quartiles[0]) / (quartiles[2] - quartiles[0])) for val in results]

        ax.plot(powers, results, label=f'Retention Rate: {rate}', color=colors[0])

        # Append results to the data list
        results_data.append([f'Retention Rate: {rate}'] + results.tolist())

    plt.xlabel('Years', fontsize=12)
    plt.ylabel('Customers', fontsize=12)
    plt.title('Customer Retention Over Years', fontsize=14)
    plt.legend()

    # Set x-axis tick locations and labels
    plt.xticks(powers)

    # Set the y-axis lower limit to zero
    plt.ylim(0, None)

    # Display the line chart
    st.pyplot(fig)

    # Create the results table
    results_df = pd.DataFrame(results_data, columns=['Retention Rate'] + powers.tolist())
    results_df = results_df.set_index('Retention Rate')
    st.table(results_df)

def main():
    # Ask for user input
    retention_rates = [
        st.number_input("Retention Rate 1:", min_value=0.0, max_value=1.0, value=default_retention_rates[0], step=0.01),
        st.number_input("Retention Rate 2:", min_value=0.0, max_value=1.0, value=default_retention_rates[1], step=0.01),
        st.number_input("Retention Rate 3:", min_value=0.0, max_value=1.0, value=default_retention_rates[2], step=0.01)
    ]
    num_years = st.number_input("Number of Years:", min_value=1, max_value=10, value=default_num_years, step=1)

    # Calculate powers and display the line chart and results table
    calculate_powers(retention_rates, num_years)

if __name__ == "__main__":
    main()
