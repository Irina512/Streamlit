import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Set default parameters
default_retention_rates = [0.5, 0.7, 0.9]
default_num_years = 5

title = "Retention/burn rate and LTV"
subheader = "This is a simple model that shows how customer retention rates affect LTV"

intro = '''Say, we have three companies A, B and C that all have 100 customers and expect to renew
at 50, 70 and 90 percent respectively.\n

How will their customer bases change over several years? We use 50, 70, and 90 percent,
but feel free to change them.  \n
Also, we will use a 5-year horizon, but, again, you can extend it up to 10.'''

sum_of_geom_progression=''' The average customer lifetime is 1/churn rate, or 1/(1-retention rate). If it does
not seem intuitive, it is probably because it comes from high school algebra* (see caption for more). \n 
In plain English the average customer lifetime is the number of years a customer will stay with a company.

Using our example of 100 customers, if half of customer leave every year meaning the average customer lifeime is
is 2 years, the inital 100 customers will generate revenue of 2 years, or in words words, will be equivalent 
to having 200 customers spread over time.'''

body=''' This chart shows how dramatically different customer bases will look after 5 years with
different retention rate. Company that loses half of its customer yearly will have fewer customers after just 
1 year vs the company that loses only 10 percent even after 5 years.'''
caption=''' If you start with 100 customers and churn 50 percent every year, then the customer pool wiill
go from 100 to 50, to 25, to 13, etc. To add up all customers you expect to have over the years, i.e.
100+50+25+13 ..., we use the formula for the sum of geometric progression, where the common ratio is less than 1,
or using retention rate, it is 1/(1-retention rate), or 1/(churn rate), or 2 years.  \n
'''

# Helper function to calculate customers left for each year (initial base is 100 customers)
def calculate_customers_left(retention_rate, num_years):
    customers_left = []
    for i in range(num_years + 1):
        retention_rate_power = retention_rate ** i
        customers_left_year = round(retention_rate_power * 100)
        customers_left.append(customers_left_year)
    return customers_left


st.subheader(subheader)
st.write("---")
st.markdown(intro)
cols = st.columns(3)

# Input parameters
retention_rates = [
    cols[0].number_input("Retention Rate 1:", min_value=0.0, max_value=1.0, value=default_retention_rates[0], step=0.01),
    cols[1].number_input("Retention Rate 2:", min_value=0.0, max_value=1.0, value=default_retention_rates[1], step=0.01),
    cols[2].number_input("Retention Rate 3:", min_value=0.0, max_value=1.0, value=default_retention_rates[2], step=0.01)
]
num_years_input = st.slider("Number of Years:", min_value=1, max_value=10, value=default_num_years, step=1)

# Calculate retention rates
customers_left = []
for rate in retention_rates:
    customers_left.append(calculate_customers_left(rate, num_years_input))
st.markdown(sum_of_geom_progression)


st.subheader("Customer Base Over Time (chart)")
# Plotting the line chart
fig = go.Figure()
for i, rate in enumerate(customers_left):
    fig.add_trace(
        go.Scatter(
            x=list(range(num_years_input + 1)),
            y=rate,
            mode="lines",
            name=f"Retention rate {retention_rates[i]}",
        )
    )

st.plotly_chart(fig)

# Results table
results_data = np.array(customers_left)
df = pd.DataFrame(results_data, columns=list(range(num_years_input + 1)))
df.index = [f"Retention Rate {rate}" for rate in retention_rates]
df.index.name = "Years"

st.markdown(body)
st.subheader("Customer Base Over Time (table)")
st.dataframe(df.style.format("{:.0f}"))
st.caption(caption)
