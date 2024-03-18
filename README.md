# Sales Dashboard Application

This Streamlit application provides an interactive sales dashboard, showcasing revenue, expenses, profit, and orders over time with a focus on data visualization and user interaction.

## Features

- Interactive bar graphs and line charts for financial metrics
- Global orders distribution map
- Top customers by number of sales and by revenue
- Custom CSS for enhanced UI

## Installation

To run this application, you'll need to install the required Python packages.

1. Clone this repository or download the files.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Navigate to the application directory and run:

```bash
streamlit run dashboard.py
```

The application will start and automatically open in your default web browser.

## Customizing the Dashboard

- The dashboard can be customized by modifying the `dashboard.py` and `style.css` files.
- You can adjust the data source and visualization elements as needed.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests. We're always looking to improve the application and add new features.


## Customizing the Junk Data Generator
The generate_junk.py script provided with this dashboard serves as a powerful tool for creating mock data tailored to your specific testing and demonstration needs. The script generates a synthetic dataset, simulating sales transactions, which the dashboard then visualizes. Here are some tips on how you can customize this generator to fit your requirements:

## Adapting to Different Data Models
Fields Customization: You can modify the script to include additional fields relevant to your analysis, such as product categories, customer demographics, or transaction types. Adjusting the arrays and random generators will allow you to simulate a wide range of data points.

## Date Range Adjustments:
The script currently generates dates within a predefined range. You can customize this range by modifying the start_date and end_date variables. This is particularly useful for simulating data from different periods or forecasting future transactions.

## Volume and Distribution:
By altering the num_samples variable, you can control the volume of data generated. Additionally, tweaking the logic behind the random distribution of values (e.g., revenue, expenses) can help simulate more specific financial scenarios.

## Incorporating Realistic Patterns
Seasonality and Trends: Introduce functions that simulate seasonal sales patterns or long-term trends in your mock data. For example, you can increase the probability of higher sales volumes during certain months to reflect holiday seasons.

## Customer Behavior:
Simulate more complex customer behaviors by introducing logic that generates repeat purchases, customer loyalty effects, or varying order sizes based on predefined customer segments.

## Usage Instructions
After customizing the data generator script to your satisfaction, simply run it to produce a new dataset:

```bash
python generate_junk.py
```

This will output a file (e.g., junk_sales_data.tsv or junk_sales_data.csv) that can be directly used by the dashboard application for visualization.

## Extending the Dashboard
With your customized dataset, you may need to adjust the dashboard application (dashboard.py) to account for any new data fields or analysis interests. Remember to update any data loading, processing, or visualization functions accordingly to reflect your dataset's structure and goals.

