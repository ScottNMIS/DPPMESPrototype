import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
import io

def draw_interactive_circle():
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.axis('equal')

    # Draw the central circle with the ID
    central_circle = plt.Circle((0, 0), 0.2, color='lightgrey', ec='black')
    ax.add_patch(central_circle)
    ax.text(0, 0, 'AF2T01LRX', horizontalalignment='center', verticalalignment='center', fontsize=12, fontweight='bold')

    # Define the properties of each sector
    sectors = [
        {"label": "0.33 CO2 eq", "icon": "🌿", "start_angle": 45, "end_angle": 135},
        {"label": "1.34 KW", "icon": "⚡", "start_angle": 135, "end_angle": 225},
        {"label": "1.61 KWh", "icon": "🔋", "start_angle": 225, "end_angle": 315},
        {"label": "4307.44 sec", "icon": "⏱️", "start_angle": 315, "end_angle": 45 + 360}
    ]

    for sector in sectors:
        wedge = Wedge((0, 0), 0.8, sector["start_angle"], sector["end_angle"], facecolor='lightgreen', edgecolor='black')
        ax.add_patch(wedge)
        angle = (sector["start_angle"] + sector["end_angle"]) / 2
        x = 0.6 * np.cos(np.radians(angle))
        y = 0.6 * np.sin(np.radians(angle))
        ax.text(x, y, sector["icon"], fontsize=18, ha='center', va='center')
        ax.text(x, y - 0.1, sector["label"], fontsize=10, ha='center', va='center')

    # Save the figure to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

def show_sustainability_info():
    st.title("Sustainability Dashboard")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(draw_interactive_circle(), use_column_width=True)
        if st.button("CO2 Emission"):
            st.write("Detailed CO2 Emission Data")
        if st.button("Power"):
            st.write("Detailed Power Data")
        if st.button("Energy"):
            st.write("Detailed Energy Data")
        if st.button("Time"):
            st.write("Detailed Time Data")

    with col2:
        # Data for visualization
        data = {
            "ID": "AF2T01LRX",
            "CO2 eq": "0.33 CO2 eq",
            "Power": "1.34 KW",
            "Energy": "1.61 KWh",
            "Time": "4307.44 sec",
            "Efficiency": "85%",
            "Waste Reduction": "20%",
            "Water Usage": "1.2 m³",
            "Renewable Energy": "70%"
        }

        icon_path = "images/home_icon.png"  # Default icon path

        st.markdown(f"### Part ID: {data['ID']}")
        st.markdown("---")

        col2_1, col2_2, col2_3 = st.columns(3)

        with col2_1:
            st.image(icon_path, width=50)
            st.metric(label="CO2 Emission", value=data["CO2 eq"], delta="2%")
            st.image(icon_path, width=50)
            st.metric(label="Power", value=data["Power"], delta="1%")
            
        with col2_2:
            st.image(icon_path, width=50)
            st.metric(label="Energy", value=data["Energy"], delta="3%")
            st.image(icon_path, width=50)
            st.metric(label="Time", value=data["Time"], delta="-5%")
        
        with col2_3:
            st.image(icon_path, width=50)
            st.metric(label="Efficiency", value=data["Efficiency"], delta="4%")
            st.image(icon_path, width=50)
            st.metric(label="Waste Reduction", value=data["Waste Reduction"], delta="10%")
            st.image(icon_path, width=50)
            st.metric(label="Water Usage", value=data["Water Usage"], delta="-2%")
            st.image(icon_path, width=50)
            st.metric(label="Renewable Energy", value=data["Renewable Energy"], delta="15%")

        st.markdown("---")

        # Add charts for a more visual representation
        st.markdown("### Performance Metrics")
        
        # Fake data for the chart
        performance_data = pd.DataFrame({
            'Metric': ['CO2 Emission', 'Power', 'Energy', 'Time', 'Efficiency', 'Waste Reduction', 'Water Usage', 'Renewable Energy'],
            'Value': [0.33, 1.34, 1.61, 4307.44, 85, 20, 1.2, 70]
        })
        
        # Bar chart
        bar_chart = alt.Chart(performance_data).mark_bar().encode(
            x='Metric',
            y='Value',
            color='Metric',
            tooltip=['Metric', 'Value']
        ).properties(
            width=600,
            height=300
        )
        
        st.altair_chart(bar_chart)

        # Progress Bars for visual effect
        st.markdown("### Efficiency Progress")
        st.progress(85)
        st.progress(20)
        st.progress(70)

        # Add a container for custom styling and layout
        with st.container():
            st.write("Visualize the sustainability metrics with icons, metrics, and charts for better clarity and presentation.")

if __name__ == "__main__":
    show_sustainability_info()
