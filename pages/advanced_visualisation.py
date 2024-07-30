import streamlit as st
import pandas as pd
import numpy as np

def show_advanced_visualisation():
    st.title("Advanced Data Visualisation for Factory Monitoring")

    # Generate fake data
    np.random.seed(42)
    categories = ['A', 'B', 'C', 'D', 'E']
    df = pd.DataFrame({
        'Category': categories,
        'Values': np.random.randint(10, 100, len(categories))
    })

    df_time = pd.DataFrame({
        'Date': pd.date_range(start='2022-01-01', periods=100),
        'Value': np.random.randn(100).cumsum()
    })

    # 1. Line Chart
    st.subheader("Line Chart")
    st.line_chart(df_time.set_index('Date'))

    # 2. Bar Chart
    st.subheader("Bar Chart")
    st.bar_chart(df.set_index('Category'))

    # 3. Area Chart
    st.subheader("Area Chart")
    st.area_chart(df_time.set_index('Date'))

    # 4. Scatter Plot (Using Vega-Lite)
    st.subheader("Scatter Plot")
    scatter_data = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'size': np.random.rand(100) * 100,
        'color': np.random.choice(categories, 100)
    })
    st.vega_lite_chart(scatter_data, {
        'mark': {'type': 'point', 'tooltip': True},
        'encoding': {
            'x': {'field': 'x', 'type': 'quantitative'},
            'y': {'field': 'y', 'type': 'quantitative'},
            'size': {'field': 'size', 'type': 'quantitative'},
            'color': {'field': 'color', 'type': 'nominal'}
        }
    })

    # 5. Histogram
    st.subheader("Histogram")
    st.write("Histogram (Values)")
    st.bar_chart(np.histogram(df['Values'], bins=10)[0])

    # 6. Map
    st.subheader("Map")
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon']
    )
    st.map(map_data)

    # 7. Pie Chart
    st.subheader("Pie Chart")
    pie_data = pd.DataFrame({
        'category': categories,
        'value': np.random.randint(10, 100, len(categories))
    })
    st.vega_lite_chart(pie_data, {
        'mark': {'type': 'arc', 'innerRadius': 50},
        'encoding': {
            'theta': {'field': 'value', 'type': 'quantitative'},
            'color': {'field': 'category', 'type': 'nominal'}
        }
    })

    # 8. Line Chart with Multiple Lines
    st.subheader("Multi-Line Chart")
    multi_line_data = pd.DataFrame({
        'Date': pd.date_range(start='2022-01-01', periods=100),
        'Value1': np.random.randn(100).cumsum(),
        'Value2': np.random.randn(100).cumsum()
    }).set_index('Date')
    st.line_chart(multi_line_data)

    # 9. Box Plot
    st.subheader("Box Plot")
    box_data = pd.DataFrame({
        'Category': np.random.choice(categories, 100),
        'Value': np.random.randn(100)
    })
    st.vega_lite_chart(box_data, {
        'mark': 'boxplot',
        'encoding': {
            'x': {'field': 'Category', 'type': 'nominal'},
            'y': {'field': 'Value', 'type': 'quantitative'}
        }
    })

    # 11. Bubble Chart
    st.subheader("Bubble Chart")
    bubble_data = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'size': np.random.rand(100) * 100,
        'color': np.random.choice(categories, 100)
    })
    st.vega_lite_chart(bubble_data, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'x', 'type': 'quantitative'},
            'y': {'field': 'y', 'type': 'quantitative'},
            'size': {'field': 'size', 'type': 'quantitative'},
            'color': {'field': 'color', 'type': 'nominal'}
        }
    })

    # 12. Streamlit Metrics
    st.subheader("Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind Speed", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    # 13. Progress Bar
    st.subheader("Progress Bar")
    st.write("Loading progress...")
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)

    # 14. Dataframe with conditional formatting

    # 15. Sparklines
    st.subheader("Sparklines")
    spark_data = pd.DataFrame(np.random.randn(10, 3), columns=['A', 'B', 'C'])
    st.line_chart(spark_data)

    # 16. Streamlit Bar Chart with Aggregated Data
    st.subheader("Aggregated Bar Chart")
    agg_data = pd.DataFrame({
        'Product': np.random.choice(['A', 'B', 'C'], 100),
        'Sales': np.random.randint(1, 100, 100)
    })
    agg_chart = agg_data.groupby('Product').sum().reset_index()
    st.bar_chart(agg_chart.set_index('Product'))

    # 17. Streamlit Area Chart with Aggregated Data
    st.subheader("Aggregated Area Chart")
    st.area_chart(agg_chart.set_index('Product'))

    # 18. Pie Chart with Aggregated Data
    st.subheader("Aggregated Pie Chart")
    pie_agg_data = agg_data.groupby('Product').sum().reset_index()
    st.vega_lite_chart(pie_agg_data, {
        'mark': {'type': 'arc', 'innerRadius': 50},
        'encoding': {
            'theta': {'field': 'Sales', 'type': 'quantitative'},
            'color': {'field': 'Product', 'type': 'nominal'}
        }
    })


    # 20. Data Visualization with Expander
    st.subheader("Data Visualization with Expander")
    with st.expander("See the data"):
        st.dataframe(df)

# Function call for testing in standalone mode
if __name__ == "__main__":
    show_advanced_visualisation()
