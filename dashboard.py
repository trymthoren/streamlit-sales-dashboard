import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import re
import plotly.graph_objects as go


# Custom CSS to inject into the web page
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def add_custom_css():
    custom_css = """
    <style>
    .blue-header {
        color: blue;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Functions to extract product and category from the 'Order' column
def extract_product(order_str):
    match = re.match(r"Item (\w+) -", order_str)
    return match.group(1) if match else None


def extract_category(order_str):
    match = re.search(r"^(.*?) - Item", order_str)
    return match.group(1) if match else None


# Data loading and preprocessing
def read_ods(filename):
    df = pd.read_excel(filename, engine='odf')
    df['Date ordered'] = pd.to_datetime(df['Date ordered'])
    df.sort_values('Date ordered', inplace=True)
    df['Year'] = df['Date ordered'].dt.year
    df['Month'] = df['Date ordered'].dt.strftime('%B')
    df['Country'] = df['Delivery address'].apply(lambda x: x.split(',')[-1].strip())
    numeric_cols = ['Revenue', 'Expenses', 'Profit']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df['Product'] = df['Order'].apply(extract_product)
    df['Category'] = df['Order'].apply(extract_category)
    return df


# Function to create a revenue bar graph
def create_revenue_bar_graph(df, selected_year, selected_month):
    if selected_year == 'Total':
        filtered_df = df
    elif selected_month == 'Total':
        filtered_df = df[df['Year'] == selected_year]
    else:
        filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]

    # Assuming 'Date ordered' and 'Revenue' are columns in your dataframe
    bar_graph = px.bar(filtered_df.groupby('Date ordered')['Revenue'].sum().reset_index(),
                       x='Date ordered', y='Revenue',
                       title=f'Revenue Bar Graph for {selected_month} {selected_year}')

    # Adjusting title font color to blue
    bar_graph.update_layout(
        title={
            'text': f'Revenue Bar Graph for {selected_month} {selected_year}',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': "Verdana",
                'size': 20,
                'color': "blue"  # Setting the title color to blue
            }
        }
    )

    return bar_graph


# Function to create accumulated line chart
def create_accumulated_line_chart(df, selected_year):
    # Filter the DataFrame based on the selected year if not 'Total'
    if selected_year != 'Total':
        filtered_df = df[df['Year'] == selected_year]
    else:
        filtered_df = df

    # Ensure dataframe is sorted by date
    filtered_df = filtered_df.sort_values('Date ordered')
    # Calculate the cumulative sums
    filtered_df['Cumulative Revenue'] = filtered_df['Revenue'].cumsum()
    filtered_df['Cumulative Expenses'] = filtered_df['Expenses'].cumsum()
    filtered_df['Cumulative Profit'] = filtered_df['Profit'].cumsum()

    # Initialize a figure
    fig = go.Figure()

    # Add traces for Revenue, Expenses, and Profit with specific colors
    fig.add_trace(go.Scatter(x=filtered_df['Date ordered'], y=filtered_df['Cumulative Revenue'],
                             mode='lines', name='Revenue', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=filtered_df['Date ordered'], y=filtered_df['Cumulative Expenses'],
                             mode='lines', name='Expenses', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=filtered_df['Date ordered'], y=filtered_df['Cumulative Profit'],
                             mode='lines', name='Profit', line=dict(color='green')))

    # Update layout for the title to be blue and set other layout configurations
    fig.update_layout(
        title={
            'text': f'Accumulated Financial Metrics for {selected_year}',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': "Verdana",
                'size': 20,
                'color': "blue"  # Setting the title color to blue
            }
        }
    )
    return fig


# Function to display metrics vertically
def display_metrics_vertically(df, selected_year, selected_month):
    # Filter the DataFrame based on the selected year and month
    if selected_year != 'Total' and selected_month != 'Total':
        filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]
    elif selected_year != 'Total':
        filtered_df = df[df['Year'] == selected_year]
    elif selected_month != 'Total':
        filtered_df = df[df['Month'] == selected_month]
    else:
        filtered_df = df

    # Calculate metrics
    total_revenue = filtered_df['Revenue'].sum()
    total_expenses = filtered_df['Expenses'].sum()
    total_profit = filtered_df['Profit'].sum()
    total_orders = filtered_df['Order'].count()  # Assuming 'Order' column exists

    # Display metrics
    st.subheader('Key Metrics')
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    st.metric(label="Total Expenses", value=f"${total_expenses:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Total Orders", value=f"{total_orders}")


# Function to create a map of orders by country
def create_country_orders_map(df, selected_year):
    # Filter the DataFrame based on the selected year if not 'Total'
    if selected_year != 'Total':
        filtered_df = df[df['Year'] == int(selected_year)]
    else:
        filtered_df = df

    # Aggregate orders by country
    country_orders = filtered_df.groupby('Country').size().reset_index(name='Orders')

    # Use Plotly Express to create the bubble map
    fig = px.scatter_geo(country_orders,
                         locations="Country",
                         locationmode='country names',  # Ensure your country data matches Plotly's expected format
                         size="Orders",
                         hover_name="Country",
                         projection="natural earth",
                         title="Orders by Country")

    # Adjust the layout to make the title blue
    fig.update_layout(
        title={
            'text': "Orders by Country",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': "Verdana",
                'size': 20,
                'color': "blue"  # Setting the title color to blue
            }
        },
        geo=dict(bgcolor='rgba(0,0,0,0)')  # Optional: Adjusting the geo background color
    )

    return fig


# Function to load the sales data
def load_sales_data(csv_file):
    df = pd.read_csv(csv_file)
    df['Date ordered'] = pd.to_datetime(df['Date ordered'])
    return df


# Function to perform seasonal decomposition
def decompose_timeseries(df, column_name):
    decomposition = seasonal_decompose(df[column_name], period=12)  # Assuming monthly data for a yearly cycle
    decomposition.plot()
    plt.show()


def get_top_customers(df):
    top_customers_by_sales = df.groupby('Username')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
    top_customers_by_orders = df.groupby('Username').size().sort_values(ascending=False).head(10).reset_index(
        name='Number of Sales')
    return top_customers_by_sales, top_customers_by_orders


# Streamlit app layout
def app():
    st.set_page_config(layout="wide", page_title='Sales Dashboard')
    add_custom_css()
    st.markdown('<h1 class="blue-header">Sales Dashboard</h1>', unsafe_allow_html=True)

    df = read_ods('junk_sales_dataaaaa.ods')

    # Dropdown for year and month selection
    selected_year = st.sidebar.selectbox('Select Year', sorted(df['Year'].unique(), reverse=True))
    selected_month = st.sidebar.selectbox('Select Month', df['Month'].unique())

    col1, col2 = st.columns([3, 1])

    with col1:
        fig1 = create_revenue_bar_graph(df, selected_year, selected_month)
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = create_accumulated_line_chart(df, selected_year)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<h2 class="blue-header">Key Metrics</h2>', unsafe_allow_html=True)
        display_metrics_vertically(df, selected_year, selected_month)

    st.markdown('<h2 class="blue-header">Global Orders Distribution</h2>', unsafe_allow_html=True)
    bubble_map_fig = create_country_orders_map(df, selected_year)
    st.plotly_chart(bubble_map_fig, use_container_width=True)

    # Top 10 customers by number of sales and by USD sales
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<h3 class="blue-header">Top 10 Customers by Number of Sales</h3>', unsafe_allow_html=True)
        top_customers_by_orders = get_top_customers(df)[1]
        st.write(top_customers_by_orders)

    with col4:
        st.markdown('<h3 class="blue-header">Top 10 Customers by USD Sales</h3>', unsafe_allow_html=True)
        top_customers_by_sales = get_top_customers(df)[0]
        st.write(top_customers_by_sales)


if __name__ == '__main__':
    app()
