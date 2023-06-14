import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Set default parameters
default_retention_rates = [50, 70, 90]
default_num_years = 5
default_ave_rev = 100

# Customizable model parameters
st.sidebar.title('Model assumptions')
retention_rates = [
    st.sidebar.number_input("Retention rate in Company A", min_value=1, max_value=100, value=default_retention_rates[0], step=1),
    st.sidebar.number_input("Retention rate in Company B", min_value=1, max_value=100, value=default_retention_rates[1], step=1),
    st.sidebar.number_input("Retention rate in Company C", min_value=1, max_value=100, value=default_retention_rates[2], step=1)
]
num_years_input = st.sidebar.slider("Number of Years", min_value=1, max_value=10, value=default_num_years, step=1)
ave_rev = st.sidebar.number_input("Average revenue per customer", value=default_ave_rev, step=1)

title = "Customer Retention And LTV"
summary = "This simple model focuses on the positive, but non-linear relationship between retention rates and LTV. LTV goes up as retention rate improves, but disproportionately more at higher retention levels."
byline = "by [Irina Magyer](https://www.linkedin.com/in/irinamagyer/)"

intro = '''Suppose we have three companies, A, B, and C, each initially having 100 customers. These companies anticipate renewal rates of 50%, 70%, and 90% respectively, with a renewal period of one year and the average annual revenue per customer of $100. These are our assumptions for this model, but feel free to change them in the sidebar*.
'''

talk_about_customer_base_chart = '''First, let's look at the number of customers each company will have year after year if their retention rates remain the same. 

Hover over the nodes to see the numbers.'''

explain_customer_base_chart = '''All companies will lose customers over time but at very different speeds. Due to the compounding nature of the loss, the company with the lowest retention will lose customers the fastest.

For example, Company A will lose half of its customers in the first year, while Company C will still have more than half of its customers after 5 years.
'''

explain_life_span=''' Despite customer churn, all three companies will continue to have some customers for a period of time. By adding up those customers across all years, we can determine the customer lifespan for the initial customer base of 100 people, measured in renewal periods such as years, months, or weeks. Putting math aside, the customer lifespan can be thought of as the number of times the initial group of customers will be repeat customers.

The customer lifespan is calculated using either the formula 1/(1 - retention_rate) or 1/churn_rate.

For a 50 percent retention rate, the customer lifespan is calculated as 1/(1 - 0.5) = 2 years.
For a 70 percent retention rate, it is 3.3 years, and for a 90 percent retention rate, it is 10 years. '''

expander = '''Learn more about how customer lifespan is calculated (a throwback to high school algebra!)'''

formula_explanation=''' As the chart above shows, the initial 100 customers with 50 percent retention will become 50, then 25, then 13, etc. If we add them all up, i.e. 100+50+25+13+..., we will know the total number of customers spread over time. 

Such a sequence is called geometric progression where each element is the product of the previous element and a constant. When that constant is less than 1, meaning each sequence element is less than the previous one, it is possible to calculate the sum of an infinite number of elements as the Nth element approaches zero. The formula is 1/(1-r), where r is the common ratio, or the retention rate.
'''

explain_LTV = '''Next, let's introduce the average annual revenue per customer to translate the customer life span into dollars. The customer lifetime value (LTV) is the total amount of revenue a company expects to generate per customer over the entire period they stay with the company for a given pool of customers with a given retention rate.

A simple way to calculate LTV is to multiply the average annual revenue per customer by the customer lifespan. 

LTV = average_annual_revenue_per_customer * customer_life_span.

Tying the average annual revenue per customer to the customer lifespan tells us that a group of 100 customers will generate 2 years of revenue for company A, 3.3 years for company B, and 10 years for company C.'''




tie_retention_to_ltv = '''Finally, let's zoom out and look at the continuum of retention rate and their corresponding LTVs, plotted below.

Hover over the nodes to see the numbers.'''

talk_about_retention_ltv = '''What do we see in this plot? The relationship between the retention rates and customer life spans is positive but nonlinear. Improving retention rates leads to higher LTV regardless of the starting point, but incremental improvements in retention have a much higher impact on customer life span starting at 80 percent. The most dramatic increase is from 90 to 95 percent retention, which doubles customer life span. LTV increases very slowly at low retention rates.

In our example, for company A to double LTV, it needs to improve its retention by 25 percentage points, from 50 to 75 percent. For company B, it would be 15 percentage points, from 70 to 85. For company C, it would be 5 percentage points, from 90 to 95 percent.

There are different ways to look at it, but the highest return on improving retention rates pays off the greatest for companies that already have higher retention rates. 

Likewise, retention rates below 60 percent alone do not offer an "easy" way to generate money. In order to grow customer base and revenue, companies with lower retention rates must attract new customers.'''

disclaimer=''' To simplify the model to emphasize the non-linear relationship between changes in retention rates vs LTVs we made a few assumptions. 

- Focusing on one group of customers over time, aka cohort analysis, we do not mix it with the later customers. In the real world, it's a mix of old and new customers. 
- We keep retention rates constant throughout the analysis period. In the real world, retention rates will not stay the same for the same customers. Those who stay on may develop a stronger bond to the company, be exposed to product improvement, new features, etc, meaning their retention rate might not drop as fast as in the first year.
- We keep the annual average revenue per customer constant. In the real world, it may vary depending on the product, upsell, etc.
- We exclude the discount rate from the LTV calculation. All future cash is not discounted. In the real world, 100 dollars next year is worth less than 100 dollars today.
'''

# Helper function to calculate customers left for each year (initial base is 100 customers)
def calculate_customers_left(retention_rate, num_years):
    customers_left = []
    for i in range(num_years + 1):
        retention_rate_power = (retention_rate / 100) ** i
        customers_left_year = round(retention_rate_power * 100)
        customers_left.append(customers_left_year)
    return customers_left


# Function to plot customer base over time
def plot_base_over_time(x, rates):
    fig = go.Figure()
    for i, rate in enumerate(rates):
        fig.add_trace(
            go.Scatter(
                x=x,
                y=rate,
                mode="markers+lines",
                name=f"Company {chr(65 + i)} (Retention {retention_rates[i]}%)",
                # Add retention rate to the legend
                hovertemplate="%{y:.0f} customers left after<br>%{x:.f} years<br><extra></extra>"
            )
        )

    # Set the layout properties
    fig.update_layout(
        title="Customer Base Over Time",
        xaxis=dict(
            title="Years",
            tickvals=x,
            ticktext=[str(val) for val in x]
        ),
        yaxis=dict(
            title="Remaining Customers"
        ),
        font_color="blue",
        hoverlabel=dict(
            bgcolor="white",
            font_size=18,
            font_color="black",
            font_family="sans serif"
        ),
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig


st.title(title)
st.markdown(f"**{summary}**")
st.write(byline)

st.markdown("---")
st.markdown(intro)
st.markdown("---")

# Calculate retention rates
customers_left = []
for rate in retention_rates:
    customers_left.append(calculate_customers_left(rate, num_years_input))

st.markdown(talk_about_customer_base_chart)

# Generate x values for the line chart
x = np.arange(num_years_input + 1)

# Plotting the line chart
base_over_time = plot_base_over_time(x, customers_left)
st.plotly_chart(base_over_time)

st.markdown(explain_customer_base_chart)

st.markdown("---")

st.markdown(explain_life_span)

with st.expander(expander):
    st.markdown(formula_explanation)

st.markdown(explain_LTV)
st.markdown("---")

st.markdown(tie_retention_to_ltv)

# Generate data to show the link between retention rates and LTV
# Generate retention rates x with values between 1 and 99 with a step = 5
x = np.arange(0, 100, 5)

# Calculate LTV values y using the formula y = 100 / (100 - x) * ave_rev
y = 100 / (100 - x) * ave_rev

# Create a figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="markers+lines",
        hovertemplate="LTV is $%{y:.1f}" +
        "<br>if retention is %{x:.f} percent<br><extra></extra>",
    )
)

# Set the layout properties
fig.update_layout(
    title="Customer Lifetime Value",
    xaxis=dict(
        title="Retention Rate (%)",
        tickvals=x,
        ticktext=[str(val) for val in x]
    ),
    yaxis=dict(
        title="LTV ($)"
    ),
    font_color="blue",
    hoverlabel=dict(
        bgcolor="white",
        font_size=18,
        font_color="black",
        font_family="Rockwell"
    )
)

st.plotly_chart(fig)

st.markdown(talk_about_retention_ltv)
st.markdown("---")
st.caption(disclaimer)
