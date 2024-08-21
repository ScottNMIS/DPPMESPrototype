import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
from typing import Dict, Any

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
    }
}

def load_css():
    st.markdown("""
        <style>
        .main {background-color: #f0f2f6; padding: 2rem;}
        .stTabs [data-baseweb="tab-list"] {gap: 24px;}
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 1rem; font-weight: 600; color: #1e1e1e;
            background-color: #ffffff; border-radius: 4px;
            padding: 0.5rem 1rem; border: 1px solid #e0e0e0;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #007bff; color: white;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 2rem; border: 1px solid #e0e0e0;
            border-radius: 0 4px 4px 4px; background-color: white;
        }
        .card {
            background-color: white; padding: 1.5rem; border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 1.5rem;
        }
        .info-header {
            font-weight: 600; color: #555; font-size: 0.9rem;
            text-transform: uppercase; letter-spacing: 0.5px;
        }
        .info-value {
            font-size: 1.2rem; font-weight: 700; color: #333; margin-top: 0.5rem;
        }
        .download-button {
            background-color: #4CAF50; border: none; color: white;
            padding: 10px 20px; text-align: center; text-decoration: none;
            display: inline-block; font-size: 16px; margin: 4px 2px;
            cursor: pointer; border-radius: 4px;
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

def show_top_bar(data: Dict[str, Any]):
    st.markdown(f"""
        <div style="background-color:#007bff; color:white; padding:10px; border-radius:5px; margin-bottom:20px;">
            <h1 style="margin:0;">{data['productName']}</h1>
            <p style="margin:0;">Part Number: {data['partNumber']} | Manufacturer: {data['manufacturer']}</p>
        </div>
    """, unsafe_allow_html=True)

def show_overview_tab(data: Dict[str, Any]):
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

def show_technical_data_tab(data: Dict[str, Any]):
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
    st.button("Download CAD File", key="cad_download")
    
    st.subheader("3D Model")
    st.write("3D model viewer would be embedded here")
    st.button("Download 3D Model", key="3d_model_download")

def show_manufacturing_tab():
    st.header("Manufacturing & Supply Chain")
    st.subheader("Operation Routing")
    st.write("Operation routing details would be displayed here")
    st.button("Download Operation Routing", key="routing_download")
    
    st.subheader("Bill of Materials")
    bom_data = pd.DataFrame({
        'Component': ['Blade Core', 'Ceramic Coating', 'Root Attachment'],
        'Material': ['Nickel Alloy', 'Ceramic Compound', 'Titanium Alloy'],
        'Quantity': [1, 1, 1]
    })
    st.dataframe(bom_data)
    st.button("Download Full BOM", key="bom_download")

def show_sustainability_tab(data: Dict[str, Any]):
    st.header("Sustainability & Environmental Impact")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Carbon Footprint", f"{data['carbonFootprint']} kg CO2e")
    with col2:
        st.metric("Recyclability Score", "72%")
    
    st.subheader("Material Composition")
    fig = go.Figure(data=[go.Pie(labels=data['materials'], values=[70, 30])])
    st.plotly_chart(fig)

def show_maintenance_tab(data: Dict[str, Any]):
    st.header("Maintenance & Repair")
    st.subheader("Maintenance Schedule")
    for interval in data['lifecycle']['maintenanceIntervals']:
        st.write(f"- {interval}")
    
    st.subheader("Repair Guidelines")
    st.write("Detailed repair instructions would be provided here")
    st.button("Download Repair Guidelines", key="repair_guide_download")
    
    st.subheader("Spare Parts Catalog")
    spare_parts = pd.DataFrame({
        'Part Name': ['Blade Tip', 'Coating Kit', 'Root Seal'],
        'Part Number': ['BT-2024-X1', 'CK-2024-X1', 'RS-2024-X1'],
        'Availability': ['In Stock', 'On Order', 'In Stock']
    })
    st.dataframe(spare_parts)

def show_documentation_tab():
    st.header("Documentation")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("User Manuals")
        st.button("Download User Manual", key="user_manual_download")
    with col2:
        st.subheader("Safety Data Sheets")
        st.button("Download Safety Data Sheet", key="sds_download")
    
    st.subheader("Compliance Documents")
    compliance_docs = ['ISO 9001 Certificate', 'Environmental Compliance', 'Quality Assurance Report']
    for doc in compliance_docs:
        st.button(f"Download {doc}", key=f"{doc.lower().replace(' ', '_')}_download")

def show_footer():
    st.markdown("""
        <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; margin-top:20px;">
            <p style="margin:0;">Last Updated: 2024-08-20 | <a href="#">Data Sources</a> | <a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a></p>
        </div>
    """, unsafe_allow_html=True)

def show_advanced_dpp_dashboard():
    st.set_page_config(page_title="Advanced DPP Dashboard", layout="wide")
    load_css()
    
    data = MOCK_DATA  # Replace with API call in the future
    
    show_top_bar(data)

    tabs = st.tabs(["Overview", "Technical Data", "Manufacturing", "Sustainability", "Maintenance", "Documentation"])

    with tabs[0]:
        show_overview_tab(data)
    with tabs[1]:
        show_technical_data_tab(data)
    with tabs[2]:
        show_manufacturing_tab()
    with tabs[3]:
        show_sustainability_tab(data)
    with tabs[4]:
        show_maintenance_tab(data)
    with tabs[5]:
        show_documentation_tab()

    show_footer()

if __name__ == "__main__":
    show_advanced_dpp_dashboard()