import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Mock data - replace with API call in the future
MOCK_DATA = {
    "productName": "High-Performance Turbine Blade",
    "partNumber": "TB-2024-X1",
    "manufacturer": "TurboCorp Industries",
    "manufacturingDate": "2024-03-15",
    "sustainabilityScore": 85,
    "reparabilityScore": 78,
    "carbonFootprint": 120.5,
    "materials": ["Nickel-based superalloy", "Ceramic coating"],
    "dimensions": {"length": "50 cm", "width": "10 cm", "height": "5 cm"},
    "weight": "2.3 kg",
    "lifecycle": {
        "expectedLifespan": "50,000 flight hours",
        "maintenanceIntervals": ["Every 5,000 hours", "Major overhaul at 25,000 hours"]
    },
    "remanufacturingData": {
        "processSteps": [
            "Inspection", "Cleaning", "Repair", "Coating", "Testing"
        ],
        "toolsRequired": [
            "Optical microscope", "Ultrasonic cleaner", "Welding equipment", 
            "Plasma spray system", "Non-destructive testing equipment"
        ],
        "averageTimeToRemanufacture": "72 hours",
        "successRate": 0.92,
        "costSavingsPercentage": 0.65
    },
    "repairHistory": [
        {"date": "2025-06-10", "type": "Minor repair", "description": "Edge refinishing"},
        {"date": "2026-09-22", "type": "Major overhaul", "description": "Coating replacement and core repair"}
    ],
    "performanceData": {
        "efficiency": [
            {"date": "2024-04-01", "value": 0.95},
            {"date": "2024-07-01", "value": 0.94},
            {"date": "2024-10-01", "value": 0.93},
            {"date": "2025-01-01", "value": 0.92},
            {"date": "2025-04-01", "value": 0.91},
            {"date": "2025-07-01", "value": 0.90}
        ],
        "vibration": [
            {"date": "2024-04-01", "value": 0.02},
            {"date": "2024-07-01", "value": 0.025},
            {"date": "2024-10-01", "value": 0.03},
            {"date": "2025-01-01", "value": 0.035},
            {"date": "2025-04-01", "value": 0.04},
            {"date": "2025-07-01", "value": 0.045}
        ]
    }
}

def load_css():
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 1rem;
            font-weight: 600;
            color: #1e1e1e;
            background-color: #ffffff;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            border: 1px solid #e0e0e0;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #007bff;
            color: white;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 2rem;
            border: 1px solid #e0e0e0;
            border-radius: 0 4px 4px 4px;
            background-color: white;
        }
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            color: #333; /* Ensure text inside cards is visible */
        }
        .info-header {
            font-weight: 600;
            color: #555;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .info-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: #333;
            margin-top: 0.5rem;
            display: block;
        }
        .download-button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            color: #333; /* Ensure text in metric cards is visible */
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #007bff;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #6c757d;
        }
        /* Style for tables */
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: #ffffff;  /* Ensure tables have a white background */
            color: #333; /* Ensure text in tables is visible */
        }
        th, td {
            padding: 10px;
            border: 1px solid #dddddd;
            text-align: left;
        }
        th {
            background-color: #f8f9fa; /* Light background for headers */
            font-weight: bold;
        }
        td {
            color: #333; /* Ensure table text is visible */
        }
        /* Style for lists */
        ul {
            background-color: #ffffff; /* White background for lists */
            padding: 15px;
            border-radius: 8px;
            color: #333; /* Ensure text in lists is visible */
        }
        li {
            margin-bottom: 10px;
            color: #333; /* Ensure text in list items is visible */
        }
        /* Fix for headings (h1, h2, h3, etc.) */
        h1, h2, h3, h4, h5, h6 {
            color: #333 !important; /* Ensure all headings are visible */
        }
        </style>
    """, unsafe_allow_html=True)



def create_gauge_chart(value: int, title: str) -> go.Figure:
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 20], 'color': 'red'},
                {'range': [20, 40], 'color': 'orange'},
                {'range': [40, 60], 'color': 'yellow'},
                {'range': [60, 80], 'color': 'lightgreen'},
                {'range': [80, 100], 'color': 'green'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

def show_top_bar(data: dict):
    st.markdown(f"""
        <div style="background-color:#007bff; color:white; padding:10px; border-radius:5px; margin-bottom:20px;">
            <h1 style="margin:0;">{data['productName']}</h1>
            <p style="margin:0;">Part Number: {data['partNumber']} | Manufacturer: {data['manufacturer']}</p>
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
        fig.update_layout(yaxis_title='Efficiency', xaxis_title='Date')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        vibration_df = pd.DataFrame(data['performanceData']['vibration'])
        vibration_df['date'] = pd.to_datetime(vibration_df['date'])
        fig = px.line(vibration_df, x='date', y='value', title='Vibration Over Time')
        fig.update_layout(yaxis_title='Vibration (mm/s)', xaxis_title='Date')
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
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
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
    
    # Mock operation routing data
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
    st.dataframe(bom_data)
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
    st.plotly_chart(fig)
    
    st.subheader("Lifecycle Assessment")
    lifecycle_data = pd.DataFrame({
        'Stage': ['Raw Material', 'Manufacturing', 'Use', 'End-of-Life'],
        'Carbon Footprint (kg CO2e)': [40, 30, 45, 5.5],
        'Water Usage (m3)': [2, 1.5, 0.5, 0.1],
        'Energy Consumption (MWh)': [5, 3, 1.5, 0.2]
    })
    st.dataframe(lifecycle_data)
    
    st.subheader("Environmental Certifications")
    certifications = [
        "ISO 14001:2015 Environmental Management",
        "LEED Gold Certified Manufacturing Facility",
        "Carbon Trust Standard"
    ]
    for cert in certifications:
        st.markdown(f"- {cert}")

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
                <div class="metric-value">{data['remanufacturingData']['successRate']*100}%</div>
                <div class="metric-label">Remanufacturing Success Rate</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{data['remanufacturingData']['costSavingsPercentage']*100}%</div>
                <div class="metric-label">Cost Savings vs. New</div>
            </div>
        """, unsafe_allow_html=True)

    st.subheader("Remanufacturing Process")
    process_df = pd.DataFrame({"Step": data['remanufacturingData']['processSteps']})
    st.table(process_df)

    st.subheader("Required Tools and Equipment")
    for tool in data['remanufacturingData']['toolsRequired']:
        st.markdown(f"- {tool}")

    st.subheader("Repair History")
    repair_df = pd.DataFrame(data['repairHistory'])
    repair_df['date'] = pd.to_datetime(repair_df['date'])
    st.dataframe(repair_df)

    st.subheader("Remanufacturing Guidelines")
    st.markdown("""
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
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
        st.markdown(f"- {interval}")
    
    st.subheader("Recommended Inspections")
    inspections = [
        {"type": "Visual Inspection", "frequency": "Every 1,000 hours", "description": "Check for visible damage or wear"},
        {"type": "Non-Destructive Testing", "frequency": "Every 5,000 hours", "description": "Perform ultrasonic and eddy current tests"},
        {"type": "Performance Test", "frequency": "Every 2,500 hours", "description": "Verify efficiency and vibration levels"}
    ]
    st.table(pd.DataFrame(inspections))

    st.subheader("Lubrication Points")
    st.markdown("""
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
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
    st.dataframe(spare_parts)
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
        st.markdown(f"**{doc['name']}**: {doc['description']}")
        st.download_button(f"Download {doc['name']}", data=f"Content of {doc['name']}", file_name=f"{doc['name'].lower().replace(' ', '_')}.pdf", mime="application/pdf")
        st.markdown("---")

    st.subheader("Compliance & Certification")
    compliance_docs = [
        {"name": "ISO 9001 Certificate", "validity": "Valid until 2026-12-31"},
        {"name": "Environmental Compliance Report", "validity": "Updated annually"},
        {"name": "Safety Certification", "validity": "Valid until 2025-06-30"},
    ]
    for doc in compliance_docs:
        st.markdown(f"**{doc['name']}** - {doc['validity']}")
        st.download_button(f"Download {doc['name']}", data=f"Content of {doc['name']}", file_name=f"{doc['name'].lower().replace(' ', '_')}.pdf", mime="application/pdf")
        st.markdown("---")

    st.subheader("Training Resources")
    st.markdown("""
        <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
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

def show_footer():
    st.markdown("""
        <div style="background-color:#f0f0f0; padding:20px; border-radius:5px; margin-top:30px;">
            <h3>Additional Resources</h3>
            <ul>
                <li><a href="#">Turbine Blade Performance Optimization Guide</a></li>
                <li><a href="#">Industry Standards and Best Practices</a></li>
                <li><a href="#">Sustainability in Turbine Manufacturing</a></li>
            </ul>
            <p>Last Updated: 2024-08-20 | <a href="#">Data Sources</a> | <a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a></p>
            <p>For technical support, please contact: support@turbocorp.com</p>
        </div>
    """, unsafe_allow_html=True)

def show_advanced_dpp_dashboard():
    load_css()
    
    data = MOCK_DATA  # Replace with API call in the future
    
    show_top_bar(data)

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

    show_footer()

if __name__ == "__main__":
    show_advanced_dpp_dashboard()