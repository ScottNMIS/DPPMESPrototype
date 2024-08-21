import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from datapages.generic_data import show_footer, load_css
from datapages.dataholder import MOCK_DATA


# Add CSS for making buttons full-width, green, and with a height of 100px
def load_button_css():
    st.markdown("""
        <style>
        .full-width-button > button {
            width: 100%;
            height: 100px;  /* Set the height to 100px */
            background-color: #28a745; /* Green background */
            color: white;  /* White text */
            border: none;
            font-size: 16px; /* Adjust font size */
            border-radius: 8px; /* Optional: Rounded corners */
        }
        .full-width-button > button:hover {
            background-color: #218838; /* Darker green on hover */
        }
        </style>
    """, unsafe_allow_html=True)

# Add buttons in full-width columns with the green color and height adjustment
def add_buttons():
    # Load the CSS for full-width, green, and height-100px buttons
    load_button_css()
    col1, col2, col3 = st.columns(3)  # Equal column width
    with col1:
        if st.button("Button 1", key="btn1", help="Click to interact", use_container_width=True):
            st.write("Button 1 clicked")
    with col2:
        if st.button("Button 2", key="btn2", help="Click to interact", use_container_width=True):
            st.write("Button 2 clicked")
    with col3:
        if st.button("Button 3", key="btn3", help="Click to interact", use_container_width=True):
            st.write("Button 3 clicked")



def create_gauge_chart(value: int, title: str) -> go.Figure:
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24, 'color': '#2c3e50'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2c3e50"},
            'bar': {'color': "#3498db"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#7f8c8d",
            'steps': [
                {'range': [0, 20], 'color': '#e74c3c'},
                {'range': [20, 40], 'color': '#e67e22'},
                {'range': [40, 60], 'color': '#f1c40f'},
                {'range': [60, 80], 'color': '#2ecc71'},
                {'range': [80, 100], 'color': '#27ae60'}],
            'threshold': {
                'line': {'color': "#2c3e50", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

def show_top_bar(data: dict):
    st.markdown(f"""
        <div class="top-bar">
            <h1>{data['productName']}</h1>
            <p>Part Number: {data['partNumber']} | Manufacturer: {data['manufacturer']}</p>
        </div>
    """, unsafe_allow_html=True)

def show_overview_tab(data: dict):
    st.header("Product Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(create_gauge_chart(data['sustainabilityScore'], "Sustainability Score"), use_container_width=True)
    with col2:
        st.plotly_chart(create_gauge_chart(data['reparabilityScore'], "Reparability Score"), use_container_width=True)
    with col3:
        st.markdown(f"""
            <div class="card">
                <span class="info-header">Key Information</span>
                <p><strong>Manufacturing Date:</strong> {data['manufacturingDate']}</p>
                <p><strong>Expected Lifespan:</strong> {data['lifecycle']['expectedLifespan']}</p>
                <p><strong>Weight:</strong> {data['weight']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Performance Metrics")
    col1, col2 = st.columns(2)
    with col1:
        efficiency_df = pd.DataFrame(data['performanceData']['efficiency'])
        efficiency_df['date'] = pd.to_datetime(efficiency_df['date'])
        fig = px.line(efficiency_df, x='date', y='value', title='Efficiency Over Time')
        fig.update_layout(
            yaxis_title='Efficiency', 
            xaxis_title='Date',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        vibration_df = pd.DataFrame(data['performanceData']['vibration'])
        vibration_df['date'] = pd.to_datetime(vibration_df['date'])
        fig = px.line(vibration_df, x='date', y='value', title='Vibration Over Time')
        fig.update_layout(
            yaxis_title='Vibration (mm/s)', 
            xaxis_title='Date',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)

def show_technical_data_tab(data: dict):
    st.header("Technical Specifications")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="card">
                <span class="info-header">Dimensions</span>
                <p><strong>Length:</strong> {data['dimensions']['length']}</p>
                <p><strong>Width:</strong> {data['dimensions']['width']}</p>
                <p><strong>Height:</strong> {data['dimensions']['height']}</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="card">
                <span class="info-header">Materials</span>
                <ul>
                    {"".join(f"<li>{material}</li>" for material in data['materials'])}
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.subheader("CAD Files")
    st.markdown("""
        <div class="card">
            <h3 style="margin-top: 0;">3D Model Viewer</h3>
            <p>The 3D model viewer would be embedded here. For this mock-up, imagine an interactive 3D model of the turbine blade.</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download CAD File", data="CAD file content", file_name="turbine_blade.stp", mime="application/stp")
    with col2:
        st.download_button("Download 3D Model", data="3D model content", file_name="turbine_blade.obj", mime="application/obj")

def show_manufacturing_tab(data: dict):
    st.header("Manufacturing & Supply Chain")
    st.subheader("Operation Routing")
    
    operations = [
        {"step": 1, "operation": "Material preparation", "time": "2 hours"},
        {"step": 2, "operation": "Casting", "time": "4 hours"},
        {"step": 3, "operation": "Heat treatment", "time": "6 hours"},
        {"step": 4, "operation": "Machining", "time": "3 hours"},
        {"step": 5, "operation": "Coating application", "time": "2 hours"},
        {"step": 6, "operation": "Quality control", "time": "1 hour"}
    ]
    
    df = pd.DataFrame(operations)
    st.table(df)
    
    st.download_button("Download Full Operation Routing", data=df.to_csv(index=False), file_name="operation_routing.csv", mime="text/csv")
    
    st.subheader("Bill of Materials")
    bom_data = pd.DataFrame({
        'Component': ['Blade Core', 'Ceramic Coating', 'Root Attachment'],
        'Material': ['Nickel Alloy', 'Ceramic Compound', 'Titanium Alloy'],
        'Quantity': [1, 1, 1],
        'Supplier': ['AlloyTech Inc.', 'CeramicPro', 'TitaniumSolutions']
    })
    st.table(bom_data)
    st.download_button("Download Full BOM", data=bom_data.to_csv(index=False), file_name="bill_of_materials.csv", mime="text/csv")

def show_sustainability_tab(data: dict):
    st.header("Sustainability & Environmental Impact")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['carbonFootprint']} kg</div>
                <div class="metric-label">Carbon Footprint (CO2e)</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">72%</div>
                <div class="metric-label">Recyclability Score</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">85%</div>
                <div class="metric-label">Energy Efficiency</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Material Composition")
    fig = go.Figure(data=[go.Pie(labels=data['materials'], values=[70, 30])])
    fig.update_layout(
        title='Material Composition',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Lifecycle Assessment")
    lifecycle_data = pd.DataFrame({
        'Stage': ['Raw Material', 'Manufacturing', 'Use', 'End-of-Life'],
        'Carbon Footprint (kg CO2e)': [40, 30, 45, 5.5],
        'Water Usage (m3)': [2, 1.5, 0.5, 0.1],
        'Energy Consumption (MWh)': [5, 3, 1.5, 0.2]
    })
    st.table(lifecycle_data)
    
    st.subheader("Environmental Certifications")
    certifications = [
        "ISO 14001:2015 Environmental Management",
        "LEED Gold Certified Manufacturing Facility",
        "Carbon Trust Standard"
    ]
    for cert in certifications:
        st.markdown(f"<div class='card'><p>{cert}</p></div>", unsafe_allow_html=True)

def show_remanufacturing_tab(data: dict):
    st.header("Remanufacturing & Repair")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['remanufacturingData']['averageTimeToRemanufacture']}</div>
                <div class="metric-label">Avg. Time to Remanufacture</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['remanufacturingData']['successRate']*100:.1f}%</div>
                <div class="metric-label">Remanufacturing Success Rate</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['remanufacturingData']['costSavingsPercentage']*100:.1f}%</div>
                <div class="metric-label">Cost Savings vs. New</div>
            </div>
        """, unsafe_allow_html=True)

    st.subheader("Remanufacturing Process")
    process_df = pd.DataFrame({"Step": data['remanufacturingData']['processSteps']})
    st.table(process_df)

    st.subheader("Required Tools and Equipment")
    col1, col2 = st.columns(2)
    for i, tool in enumerate(data['remanufacturingData']['toolsRequired']):
        if i % 2 == 0:
            with col1:
                st.markdown(f"<div class='card'><p>{tool}</p></div>", unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(f"<div class='card'><p>{tool}</p></div>", unsafe_allow_html=True)

    st.subheader("Repair History")
    repair_df = pd.DataFrame(data['repairHistory'])
    repair_df['date'] = pd.to_datetime(repair_df['date'])
    st.table(repair_df)

    st.subheader("Remanufacturing Guidelines")
    st.markdown("""
        <div class="card">
            <h4 style="margin-top: 0;">Key Considerations for Remanufacturing:</h4>
            <ul>
                <li>Ensure all safety protocols are followed during the remanufacturing process.</li>
                <li>Use only approved materials and replacement parts.</li>
                <li>Follow the step-by-step process outlined in the detailed remanufacturing guide.</li>
                <li>Perform all required quality checks and tests before returning the part to service.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.download_button("Download Remanufacturing Guide", data="Detailed remanufacturing guide content", file_name="remanufacturing_guide.pdf", mime="application/pdf")

def show_maintenance_tab(data: dict):
    st.header("Maintenance & Service")
    
    st.subheader("Maintenance Schedule")
    for interval in data['lifecycle']['maintenanceIntervals']:
        st.markdown(f"<div class='card'><p>{interval}</p></div>", unsafe_allow_html=True)
    
    st.subheader("Recommended Inspections")
    inspections = [
        {"type": "Visual Inspection", "frequency": "Every 1,000 hours", "description": "Check for visible damage or wear"},
        {"type": "Non-Destructive Testing", "frequency": "Every 5,000 hours", "description": "Perform ultrasonic and eddy current tests"},
        {"type": "Performance Test", "frequency": "Every 2,500 hours", "description": "Verify efficiency and vibration levels"}
    ]
    st.table(pd.DataFrame(inspections))

    st.subheader("Lubrication Points")
    st.markdown("""
        <div class="card">
            <p>An interactive diagram would be displayed here, showing the lubrication points on the turbine blade.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Spare Parts Catalog")
    spare_parts = pd.DataFrame({
        'Part Name': ['Blade Tip', 'Coating Kit', 'Root Seal', 'Cooling Channel Insert'],
        'Part Number': ['BT-2024-X1', 'CK-2024-X1', 'RS-2024-X1', 'CCI-2024-X1'],
        'Lead Time': ['2 weeks', '1 week', '3 weeks', '4 weeks'],
        'Inventory Status': ['In Stock', 'Low Stock', 'In Stock', 'Out of Stock']
    })
    st.table(spare_parts)
    st.download_button("Download Full Spare Parts Catalog", data=spare_parts.to_csv(index=False), file_name="spare_parts_catalog.csv", mime="text/csv")

def show_documentation_tab():
    st.header("Documentation & Resources")

    st.subheader("Technical Documents")
    tech_docs = [
        {"name": "User Manual", "description": "Complete guide for operation and basic maintenance"},
        {"name": "Technical Specifications", "description": "Detailed product specifications and performance data"},
        {"name": "Installation Guide", "description": "Step-by-step installation instructions"},
    ]
    for doc in tech_docs:
        st.markdown(f"""
            <div class="card">
                <h4>{doc['name']}</h4>
                <p>{doc['description']}</p>
                <button class="streamlit-button primary">Download {doc['name']}</button>
            </div>
        """, unsafe_allow_html=True)

    st.subheader("Compliance & Certification")
    compliance_docs = [
        {"name": "ISO 9001 Certificate", "validity": "Valid until 2026-12-31"},
        {"name": "Environmental Compliance Report", "validity": "Updated annually"},
        {"name": "Safety Certification", "validity": "Valid until 2025-06-30"},
    ]
    for doc in compliance_docs:
        st.markdown(f"""
            <div class="card">
                <h4>{doc['name']}</h4>
                <p>{doc['validity']}</p>
                <button class="streamlit-button primary">Download {doc['name']}</button>
            </div>
        """, unsafe_allow_html=True)

    st.subheader("Training Resources")
    st.markdown("""
        <div class="card">
            <h4 style="margin-top: 0;">Available Training Modules:</h4>
            <ul>
                <li>Basic Maintenance Procedures</li>
                <li>Advanced Troubleshooting Techniques</li>
                <li>Remanufacturing Process Training</li>
                <li>Safety Protocols for Handling and Maintenance</li>
            </ul>
            <p>Contact your account manager to schedule training sessions.</p>
        </div>
    """, unsafe_allow_html=True)

def create_scrollable_charts():
    charts = [
        ("Efficiency Over Time", create_efficiency_chart()),
        ("Vibration Over Time", create_vibration_chart()),
        ("Material Composition", create_material_composition_chart()),
        ("Carbon Footprint by Lifecycle Stage", create_carbon_footprint_chart())
    ]
    
    st.markdown("""
        <style>
        .scroll-container {
            overflow: hidden;
            position: relative;
        }
        .scroll-chart {
            transition: transform 0.3s ease;
        }
        .scroll-button {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            z-index: 10;
            background-color: rgba(255,255,255,0.7);
            border: none;
            padding: 10px;
            cursor: pointer;
        }
        .scroll-button:hover {
            background-color: rgba(255,255,255,0.9);
        }
        .scroll-button.left { left: 10px; }
        .scroll-button.right { right: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
    
    for i, (title, chart) in enumerate(charts):
        st.markdown(f'<div class="scroll-chart" id="chart-{i}">', unsafe_allow_html=True)
        st.subheader(title)
        st.plotly_chart(chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <button class="scroll-button left" onclick="scrollCharts(-1)">←</button>
        <button class="scroll-button right" onclick="scrollCharts(1)">→</button>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <script>
        let currentChart = 0;
        const totalCharts = 4;
        
        function scrollCharts(direction) {
            currentChart = (currentChart + direction + totalCharts) % totalCharts;
            for (let i = 0; i < totalCharts; i++) {
                const chart = document.getElementById(`chart-${i}`);
                chart.style.transform = `translateX(${(i - currentChart) * 100}%)`;
            }
        }
        </script>
    """, unsafe_allow_html=True)

def create_efficiency_chart():
    efficiency_df = pd.DataFrame(MOCK_DATA['performanceData']['efficiency'])
    efficiency_df['date'] = pd.to_datetime(efficiency_df['date'])
    fig = px.line(efficiency_df, x='date', y='value', title='Efficiency Over Time')
    fig.update_layout(
        yaxis_title='Efficiency', 
        xaxis_title='Date',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    return fig

def create_vibration_chart():
    vibration_df = pd.DataFrame(MOCK_DATA['performanceData']['vibration'])
    vibration_df['date'] = pd.to_datetime(vibration_df['date'])
    fig = px.line(vibration_df, x='date', y='value', title='Vibration Over Time')
    fig.update_layout(
        yaxis_title='Vibration (mm/s)', 
        xaxis_title='Date',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    return fig

def create_material_composition_chart():
    fig = go.Figure(data=[go.Pie(labels=MOCK_DATA['materials'], values=[70, 30])])
    fig.update_layout(
        title='Material Composition',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def create_carbon_footprint_chart():
    lifecycle_data = pd.DataFrame({
        'Stage': ['Raw Material', 'Manufacturing', 'Use', 'End-of-Life'],
        'Carbon Footprint (kg CO2e)': [40, 30, 45, 5.5],
    })
    fig = px.bar(lifecycle_data, x='Stage', y='Carbon Footprint (kg CO2e)', title='Carbon Footprint by Lifecycle Stage')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    return fig

def show_overview_tab(data: dict):
    st.header("Product Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(create_gauge_chart(data['sustainabilityScore'], "Sustainability Score"), use_container_width=True)
    with col2:
        st.plotly_chart(create_gauge_chart(data['reparabilityScore'], "Reparability Score"), use_container_width=True)
    with col3:
        st.markdown(f"""
            <div class="card">
                <span class="info-header">Key Information</span>
                <p><strong>Manufacturing Date:</strong> {data['manufacturingDate']}</p>
                <p><strong>Expected Lifespan:</strong> {data['lifecycle']['expectedLifespan']}</p>
                <p><strong>Weight:</strong> {data['weight']}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Performance Metrics")
    create_scrollable_charts()



def show_advanced_dpp_dashboard():
    load_css()
    
    data = MOCK_DATA
    
    #show_top_bar(data)

    tabs = st.tabs(["Overview", "Technical Data", "Manufacturing", "Remanufacturing", "Sustainability", "Maintenance", "Documentation"])

    with tabs[0]:
        show_overview_tab(data)
    with tabs[1]:
        show_technical_data_tab(data)
    with tabs[2]:
        show_manufacturing_tab(data)
    with tabs[3]:
        show_remanufacturing_tab(data)
    with tabs[4]:
        show_sustainability_tab(data)
    with tabs[5]:
        show_maintenance_tab(data)
    with tabs[6]:
        show_documentation_tab()

    add_buttons()

    #show_footer(data)

if __name__ == "__main__":
    show_advanced_dpp_dashboard()