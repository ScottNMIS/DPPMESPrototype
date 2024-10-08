#Can ignore this page, it is just styles and footer details. No technical code.
import streamlit as st
from datapages.login import init_session_state, get_login_details, logout
from datetime import date

import os


#Footer, doesn't work with image using HTML style. Not sure how to fix...
def show_footer():
    base_path = "C:/Unity/DPPMESPrototype"
    image_path = os.path.join(base_path, "images", "nmis_logo_small.png")
    footer_html = f"""
    <footer style="background-color: #00008B; color: white; padding: 40px 0; font-family: Arial, sans-serif;">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 15px; display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1; padding: 0 20px;">
                <img src="file:///{image_path}" alt="NMIS Logo" style="max-width: 100%; height: auto;">
            </div>
            <div style="flex: 2; padding: 0 20px; border-right: 1px solid rgba(255,255,255,0.1);">
                <h3 style="color: #3498db; margin-bottom: 20px;">About NMIS</h3>
                <p>National Manufacturing Institute Scotland</p>
                <p>Digital Factory</p>
                <p>Address: 3 Netherton Square, Paisley, PA3 2EF</p>
                <p>Phone: 0141 534 5200</p>
                <p>Email: afrc-digital@strath.ac.uk</p>
            </div>
            <div style="flex: 2; padding: 0 20px;">
                <h3 style="color: #3498db; margin-bottom: 20px;">ReMake Glasgow</h3>
                <p>ReMake Glasgow is a project focused on driving innovation in sustainable manufacturing.</p>
                <p>Our goal is to create circular manufacturing processes that minimise waste and maximise resource efficiency.</p>
                <p>Through this initiative, we aim to foster sustainable production methods that contribute to Scotland's transition to net-zero by 2045.</p>
                <p>Learn more about how ReMake Glasgow is shaping the future of manufacturing in Scotland.</p>
            </div>
        </div>
        <div style="text-align: center; padding-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 40px;">
            <p>&copy; {date.today().year} National Manufacturing Institute Scotland. All rights reserved.</p>
            <p>
                <a href="#" style="color: #3498db; text-decoration: none;">Privacy Policy</a> | 
                <a href="#" style="color: #3498db; text-decoration: none;">Terms of Use</a>
            </p>
            <p>Last Updated: {date.today().strftime('%Y-%m-%d')}</p>
        </div>
    </footer>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def load_css():
    st.markdown("""
        <style>
        /* Global Styles */
        .main {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            font-weight: 600;
        }
        /* Top Bar */
        .top-bar {
            background-color: #3498db;
            color: white;
            padding: 0.4rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .top-bar h1 {
            margin: 0;
            color: white;
            font-size: 2rem;
        }
        .top-bar p {
            margin: 0;
            font-size: 1rem;
            opacity: 0.8;
        }
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            background-color: #ecf0f1;
            padding: 0.5rem;
            border-radius: 10px;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 0.9rem;
            font-weight: 600;
            color: #34495e;
            background-color: transparent;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #3498db;
            color: white;
        }
        .stTabs [data-baseweb="tab-panel"] {
            background-color: white;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        /* Cards */
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        .card:hover {
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
            transform: translateY(-5px);
        }
        .info-header {
            font-weight: 600;
            color: #7f8c8d;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        .info-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: #2c3e50;
        }
        /* Metric Cards */
        .metric-card {
            background-color: #ecf0f1;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            background-color: #3498db;
        }
        .metric-card:hover .metric-value,
        .metric-card:hover .metric-label {
            color: white;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #2980b9;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #7f8c8d;
        }
        /* Tables */
        .dataframe {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        .dataframe th, .dataframe td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        .dataframe th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        .dataframe tr:last-child td {
            border-bottom: none;
        }
        /* Buttons */
        .stButton > button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #2980b9;
        }
        /* Footer */
        .footer {
            background-color: #34495e;
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-top: 2rem;
        }
        .footer h3 {
            color: white;
            margin-top: 0;
        }
        .footer ul {
            list-style-type: none;
            padding: 0;
        }
        .footer ul li {
            margin-bottom: 0.5rem;
        }
        .footer a {
            color: #3498db;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

def load_button_css():
    st.markdown("""
        <style>
        .top-banner-container {
            margin-bottom: 0rem;
        }
        .top-bar {
            background-color: #3498db;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 10px 10px 0 0;
            margin-bottom: 0.5rem;
        }
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            background-color: #f0f2f6;
            padding: 0.5rem;
            border-radius: 0 0 10px 10px;
        }
        .nav-button {
            flex-grow: 1;
            margin: 0 0.25rem;
        }
        .nav-button > button {
            width: 100%;
            background-color: #28a745;
            color: white;
            border: none;
            padding: 0.5rem;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .nav-button > button:hover {
            background-color: #218838;
        }
        </style>
    """, unsafe_allow_html=True)

def show_top_bar():
    account_name = st.session_state.get('account_name', 'Guest')
    st.markdown(f"""
        <div class="top-bar">
            <div class="user-info">Logged in as: <strong>{account_name}</strong></div>
        </div>
    """, unsafe_allow_html=True)

def add_navigation_buttons():
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Button 1", key="nav_btn1", use_container_width=True):
            st.session_state.selected_page = "Dashboard"
    with col2:
        if st.button("Button 2", key="nav_btn2", use_container_width=True):
            st.session_state.selected_page = "Advanced Dashboard"
    with col3:
        if st.button("Button 3", key="nav_btn3", use_container_width=True):
            st.session_state.selected_page = "Data Visualisation"

def top_banner_main():
    load_button_css()
    st.markdown('<div class="top-banner-container">', unsafe_allow_html=True)
    
    login_details = get_login_details()
    account_name = login_details["username"] if login_details["is_logged_in"] else "Guest"
    
    st.markdown(f"""
        <div class="top-bar">
            <div class="user-info">Logged in as: <strong>{account_name}</strong></div>
        </div>
    """, unsafe_allow_html=True)
    
    add_navigation_buttons()
    st.markdown('</div>', unsafe_allow_html=True)