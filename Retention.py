import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Set default parameters
default_retention_rates = [50, 70, 90]
default_num_years = 5

title = "Customer retention/burn rate and LTV"

subheader = "This is a simple model that shows how customer retention rates affect LTV"

intro = '''Say, we have three companies A, B and C that all have 100 customers
and expect to renew at 50, 70 and 90 percent respectively, and we'll use a year as the renewal period.
Let's see what will happen to the initial 100 customers over 5 years.\n

These are just our assumptions for this models, but you can change the parameters here:'''

talk_about_customer_base_chart = '''If we plot how many customer each of the three companies
will have after 1 year, then 2, etc, given their respective retention rates, we will see dramatic
differences. After just one year the company with 50 percent churn will have fewer customers than
the company that keeps 90 percent of its customers after 5 years.'''

sum_of_geom_progression = '''The average customer lifetime is 1/churn rate, or 1/(1-retention rate). If it does
not seem intuitive, it is probably because it comes from high school algebra* (see caption for more). \n 
In plain English, the average customer lifetime is the number of years a customer will stay with a company.

Using a 50 percent retention rate, the life time value of a customer is 1/(1-retention rate),
or 1/(1-0.5), or 2 years. 

Using our example of 100 customers, if half of the customers leave every year meaning the average customer lifetime is
2 years, the initial 100 customers will generate revenue for 2 years. In other words, it will be equivalent 
to having 200 customers spread over time.'''

body = '''This chart shows how dramatically different customer bases will look after 5 years with
different retention rates. A company that loses half of its customers yearly will have fewer customers after just 
1 year compared to the company that loses only 10 percent even after 5 years.'''

caption = '''If you start with 100 customers and churn 50 percent every year, then the customer pool will
go from 100 to 50, to 25, to 13, etc. To add up all the customers you expect to have over the years, i.e.
100+50+25+13 ..., we use the formula for the sum of a geometric progression, where the common ratio is less than 1,
or using the retention rate, it is 1/(1-retention rate), or 1/(churn rate), or 2 years. \n
'''

# Helper function to calculate customers left for each year (initial base is 100 customers)
def calculate_customers_left(retention_rate, num_years):
    customers_left = []
    for i in range(num_years + 1):
        retention_rate_power = (retention_rate / 100) ** i
        customers_left_year = round(retention_rate_power * 100)
        customers_left.append(customers_left_year)
    return customers_left

st.title(title)
st.subheader(subheader)
st.markdown(intro)
cols = st.columns(3)

# Input parameters
retention_rates = [
    cols[0].number_input("Retention in Company A:", min_value=1, max_value=100, value=default_retention_rates[0], step=1),
    cols[1].number_input("Retention in Company B:", min_value=1, max_value=100, value=default_retention_rates[1], step=1),
    cols[2].number_input("Retention in Company C:", min_value=1, max_value=100, value=default_retention_rates[2], step=1)
]
num_years_input = st.slider("Number of Years:", min_value=1, max_value=10, value=default_num_years, step=1)

st.markdown("---")

# Calculate retention rates
customers_left = []
for rate in retention_rates:
    customers_left.append(calculate_customers_left(rate, num_years_input))

st.markdown(talk_about_customer_base_chart)

# Plotting the line chart
fig = go.Figure()
for i, rate in enumerate(customers_left):
    fig.add_trace(
        go.Scatter(
            x=list(range(num_years_input + 1)),
            y=rate,
            mode="lines",
            name=f"Retention rate {retention_rates[i]}%",
        )
    )
fig.update_layout(
    title='Customer Base Over Time',
    xaxis_title='Years',
    yaxis_title='Customers Remaining',
    font_color="red",
)

st.plotly_chart(fig)

st.markdown(body)

st.markdown(sum_of_geom_progression)
st.markdown("---")

# Generate x values between 1 and 99
x = np.arange(0, 100, 5)

# Calculate y values using the formula y = 100 / (100 - x)
y = 100 / (100 - x)

# Format the hover labels as "Retention: x"
hover_labels = [f"Retention: {x_val}" for x_val in x]

# Create a figure
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers+lines',
    hovertemplate=
    'LTV is %{y:.1f} years' +
    '<br>if retention is %{x:.f} percent <br><extra></extra>',
))

# Set the layout properties
fig.update_layout(
    title='Customer Lifetime Value',
    xaxis=dict(
        title='Retention rate, percent',
        tickvals=x,
        ticktext=[str(val) for val in x]
    ),
    yaxis=dict(
        title='LTV, years'
    ),
    font_color="blue",
    hoverlabel=dict(
        bgcolor="white",
        font_size=18,
        font_color="black",
        font_family="Rockwell"
    )
)
# Create Streamlit app
st.plotly_chart(fig)
st.markdown('---')
st.caption(caption)
