import streamlit as st
import json
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datapages.dpp_advanceddashboard import show_advanced_dpp_dashboard, MOCK_DATA
from datetime import datetime
import os
from openai import OpenAI
from decouple import config 
from datapages.generic_data import show_footer, show_top_bar
from datapages.dataholder import MOCK_DATA

# Set up your OpenAI API key using the .env file
client = OpenAI(api_key=config('OPENAI_API_KEY'))

# Initialize session state
if 'account_name' not in st.session_state:
    st.session_state['account_name'] = 'John Doe'
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []

def load_json_data():
    with open('DigitalProductPassport.json') as json_file:
        data = json.load(json_file)
    return data

# Define your functions (unchanged)
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
            },
            "required": ["location"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Get the current time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "generate_pie_chart",
        "description": "Generate a pie chart with given labels and sizes",
        "parameters": {
            "type": "object",
            "properties": {
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels for the pie chart segments"
                },
                "sizes": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Sizes for each pie chart segment"
                }
            },
            "required": ["labels", "sizes"]
        }
    }
]

# Mock functions (unchanged)
def get_weather(location):
    temp = 25  # Mock temperature
    return f"The weather in {location} is sunny and {temp} degrees."

def get_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"The current time is {current_time}."

def generate_pie_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.session_state.generated_content.append({"type": "pie_chart", "title": "Pie Chart", "figure": fig})
    return "Pie chart displayed successfully."

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
            margin-bottom: 1rem;
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
            display: block;
        }
        .info-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: #2c3e50;
            display: block;
        }
        /* Chat Section */
        .chat-container {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 1rem;
            height: 300px;
            overflow-y: auto;
        }
        .chat-message {
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-radius: 5px;
        }
        .user-message {
            background-color: #e8f4f8;
            text-align: right;
        }
        .assistant-message {
            background-color: #f0f0f0;
        }
        </style>
    """, unsafe_allow_html=True)

def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
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
    fig.update_layout(height=300)
    return fig

def show_dpp_dashboard():
    #show_top_bar()
    if st.button("Request Access to Advanced Digital Product Data"):
        st.session_state['request_access_clicked'] = True
        st.rerun()
    load_css()
    data = MOCK_DATA  # Use the provided mock data

    st.title("Digital Product Passport")
    st.markdown(f"ID: {data['partNumber']}")

    # General Information Section
    st.markdown("## General Information")
    col1, col2 = st.columns(2)  # Since there are only two available fields, reduced to two columns.
    with col1:
        st.markdown(f'<div class="card"><span class="info-header">Product Name</span><span class="info-value">{data["productName"]}</span></div>', unsafe_allow_html=True)
    with col2:
        # Removed "Manufacturer ID" as it's not in the mock data and corrected to "Manufacturer"
        st.markdown(f'<div class="card"><span class="info-header">Manufacturer</span><span class="info-value">{data["manufacturer"]}</span></div>', unsafe_allow_html=True)

    # No "Current Version" available in the mock data, so this is removed.

    # Sustainability Overview Section
    st.markdown("## Sustainability Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        # Use the "reparabilityScore" from mock data
        st.plotly_chart(create_gauge_chart(int(data["reparabilityScore"]), "Reparability Score"), use_container_width=True)
    with col2:
        # Use "sustainabilityScore" instead of "durabilityScore", as there is no durability score in the mock data
        st.plotly_chart(create_gauge_chart(int(data["sustainabilityScore"]), "Sustainability Score"), use_container_width=True)
    with col3:
        # Use the "carbonFootprint" from mock data
        st.markdown(f'<div class="card"><span class="info-header">Total CO2 Footprint</span><span class="info-value">{data["carbonFootprint"]} kg CO2e</span></div>', unsafe_allow_html=True)

    # Tabs for detailed sections
    tabs = st.tabs(["AI Assistant", "Product Details", "Sustainability", "Commercial", "Materials", "Handling", "Additional Data", "Operation", "Documentation"])

    # AI Assistant Tab
    with tabs[0]:
       # st.markdown("## 🤖 Chat with AI Assistant")
       # st.markdown("Ask any questions or generate content (like charts)!")
        
        col1, col2 = st.columns([2, 1])
        
        # Left column: Chat interface
        with col1:
            st.markdown("### Chat")
            chat_display = st.container(height=300)
            with chat_display:
                for chat in st.session_state.messages:
                    if chat["role"] == "user":
                        st.markdown(f"**User:** {chat['content']}")
                    else:
                        st.markdown(f"**Assistant:** {chat['content']}")
            user_input = st.text_input("Type your message:", key="user_input", label_visibility="collapsed", placeholder="Ask anything...", max_chars=200)
            if st.button("Send", key="send_button"):
                if user_input:
                    st.session_state.messages.append({"role": "user", "content": user_input})

                    # OpenAI client call
                    try:
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": user_input}],
                            functions=functions,
                            function_call="auto"
                        )
                        function_call = response.choices[0].message.function_call
                        if function_call and function_call.name:
                            arguments = json.loads(function_call.arguments)
                            function_name = function_call.name
                            function_to_call = globals().get(function_name)

                            if function_to_call:
                                result = function_to_call(**arguments)
                                if result:
                                    st.session_state.messages.append({"role": "assistant", "content": result})
                            else:
                                st.session_state.messages.append({"role": "assistant", "content": "Function not found."})
                        else:
                            st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

                        st.rerun()

                    except Exception as e:
                        st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})

        # Right column: Generated Content
        with col2:
            st.markdown("### Generated Content")
            content_container = st.container(height=300)
            with content_container:
                if len(st.session_state.generated_content) > 0:
                    for idx, content in enumerate(st.session_state.generated_content):
                        st.markdown(f"**{idx + 1}. {content['title']}**")
                        if content["type"] == "pie_chart":
                            st.pyplot(content["figure"])
                else:
                    st.markdown("No content generated yet.")

    # Product Details Tab
    with tabs[1]:
        st.markdown("### Product Specifications")
        col1, col2 = st.columns(2)
        with col1:
            # Use 'partNumber' for Product Type
            st.markdown(f'<div class="card"><span class="info-header">Product Type</span><span class="info-value">{MOCK_DATA["partNumber"]}</span></div>', unsafe_allow_html=True)
            # Serial number is not in the mock data, so we will remove this line.
        with col2:
            # Use 'weight' from MOCK_DATA
            st.markdown(f'<div class="card"><span class="info-header">Weight</span><span class="info-value">{MOCK_DATA["weight"]}</span></div>', unsafe_allow_html=True)
            # Remove physical state as it's not in the mock data or define it as Solid
            st.markdown(f'<div class="card"><span class="info-header">Physical State</span><span class="info-value">Solid</span></div>', unsafe_allow_html=True)

    # Sustainability Tab
    with tabs[2]:
        st.markdown("### Sustainability Details")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        # Carbon footprint
        st.markdown(f'<div class="card"><span class="info-header">Carbon Footprint</span><span class="info-value">{MOCK_DATA["carbonFootprint"]} kg CO2e</span></div>', unsafe_allow_html=True)
        # Sustainability score
        st.markdown(f'<div class="card"><span class="info-header">Sustainability Score</span><span class="info-value">{MOCK_DATA["sustainabilityScore"]}</span></div>', unsafe_allow_html=True)
        # Reparability score
        st.markdown(f'<div class="card"><span class="info-header">Reparability Score</span><span class="info-value">{MOCK_DATA["reparabilityScore"]}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Commercial Information Tab
    with tabs[3]:
        st.markdown("### Commercial Information")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        # Since there is no "Placed on Market" or "Purpose" in the mock data, we will skip these fields.

    # Materials Tab
    with tabs[4]:
        st.markdown("### Materials")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        # Listing materials from MOCK_DATA['materials']
        for material in MOCK_DATA['materials']:
            st.markdown(f'<div class="card"><span class="info-header">Material</span><span class="info-value">{material}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Handling Tab
    with tabs[5]:
        st.markdown("### Handling Information")
        # No handling data is available in the mock data, so this tab will be skipped.

    # Additional Data Tab
    with tabs[6]:
        st.markdown("### Additional Data")
        # No additional data in the mock data, so we will skip this tab.

    # Operation Tab
    with tabs[7]:
        st.markdown("### Operation Information")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        # Manufacturing date
        st.markdown(f'<div class="card"><span class="info-header">Manufacturing Date</span><span class="info-value">{MOCK_DATA["manufacturingDate"]}</span></div>', unsafe_allow_html=True)
        # No facility information in the mock data, so we will skip that field.
        st.markdown('</div>', unsafe_allow_html=True)

    # Documentation Tab
    with tabs[8]:
        st.markdown("### Documentation and Sources")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        # Displaying available documentation and sources with links
        for source in MOCK_DATA["dppResources"]:
            st.markdown(f'<div class="card"><span class="info-header">{source["title"]}</span><span class="info-value"><a href="{source["url"]}" target="_blank">Source Link</a></span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)



if __name__ == "__main__":
    show_dpp_dashboard()