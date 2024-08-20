import streamlit as st
import json
import plotly.graph_objects as go
import os
import matplotlib.pyplot as plt
from openai import OpenAI
from datetime import datetime

# Set up your OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

# Initialize session state for messages and generated content
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []

def show_top_bar():
    account_name = st.session_state.get('account_name', 'Guest')
    st.markdown(f"""
        <div class="top-bar">
            <div class="user-info">Logged in as: <strong>{account_name}</strong></div>
            <a href="#" class="button">Request Access</a>
        </div>
        <style>
        .top-bar {{
            background-color: #007bff;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            font-size: 1rem;
            position: sticky;
            top: 0;
            z-index: 999;
            width: 100%;
        }}
        .top-bar .button {{
            background-color: white;
            color: #007bff;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-decoration: none;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }}
        .top-bar .button:hover {{
            background-color: #e0e0e0;
        }}
        .top-bar .user-info {{
            font-size: 1rem;
            font-weight: 600;
        }}
        </style>
    """, unsafe_allow_html=True)

# Example for setting account_name
st.session_state['account_name'] = 'John Doe'

def load_json_data():
    with open('DigitalProductPassport.json') as json_file:
        data = json.load(json_file)
    return data

def apply_custom_styles():
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
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
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
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
        .card-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }
        h1, h2, h3, h4, h5, h6, p {
            color: #333 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize session state for messages and generated content
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []

def create_gauge_chart(value, title):
    score_map = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}
    numeric_value = score_map.get(value, 0)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=numeric_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1], 'color': 'red'},
                {'range': [1, 2], 'color': 'orange'},
                {'range': [2, 3], 'color': 'yellow'},
                {'range': [3, 4], 'color': 'lightgreen'},
                {'range': [4, 5], 'color': 'green'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': numeric_value}}))
    fig.update_layout(height=300)
    return fig

def show_dpp_dashboard():
    show_top_bar()
    apply_custom_styles()
    data = load_json_data()

    st.title("Digital Product Passport")
    st.markdown(f"ID: {st.session_state.get('dpp_id', 'CX:MPI7654:DPPV-0001')}")
    
    # General Information Section
    st.markdown("## General Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="card"><span class="info-header">Product Name</span><span class="info-value">{data["identification"]["type"]["nameAtManufacturer"]}</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><span class="info-header">Manufacturer ID</span><span class="info-value">{data["operation"]["manufacturer"]["manufacturer"]}</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card"><span class="info-header">Current Version</span><span class="info-value">{data["metadata"]["version"]}</span></div>', unsafe_allow_html=True)

    # Sustainability Overview Section
    st.markdown("## Sustainability Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(create_gauge_chart(data["sustainability"]["reparabilityScore"], "Reparability Score"), use_container_width=True)
    with col2:
        st.plotly_chart(create_gauge_chart(data["sustainability"]["durabilityScore"], "Durability Score"), use_container_width=True)
    with col3:
        st.markdown(f'<div class="card"><span class="info-header">Total CO2 footprint</span><span class="info-value">{data["sustainability"]["productFootprint"]["carbon"][0]["value"]} {data["sustainability"]["productFootprint"]["carbon"][0]["unit"]}</span></div>', unsafe_allow_html=True)

    # Tabs for detailed sections
    tabs = st.tabs(["Product Details", "Sustainability", "Commercial", "Materials", "Handling", "Additional Data", "Operation", "Documentation"])

    # Product Details Tab
    with tabs[0]:
        st.markdown("### Product Specifications")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="card"><span class="info-header">Product Type</span><span class="info-value">{data["identification"]["type"]["manufacturerPartId"]}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><span class="info-header">Serial Number</span><span class="info-value">{data["identification"]["serial"][0]["value"]}</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><span class="info-header">Weight</span><span class="info-value">{data["characteristics"]["physicalDimension"]["weight"]["value"]} {data["characteristics"]["physicalDimension"]["weight"]["unit"]}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><span class="info-header">Physical State</span><span class="info-value">{data["characteristics"]["physicalState"]}</span></div>', unsafe_allow_html=True)

    # Sustainability Tab
    with tabs[1]:
        st.markdown("### Sustainability Details")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="info-header">Carbon Footprint</span><span class="info-value">{data["sustainability"]["productFootprint"]["carbon"][0]["value"]} {data["sustainability"]["productFootprint"]["carbon"][0]["unit"]}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="info-header">Durability Score</span><span class="info-value">{data["sustainability"]["durabilityScore"]}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="info-header">Reparability Score</span><span class="info-value">{data["sustainability"]["reparabilityScore"]}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Commercial Information Tab
    with tabs[2]:
        st.markdown("### Commercial Information")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="info-header">Placed on Market</span><span class="info-value">{data["commercial"]["placedOnMarket"]}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="info-header">Purpose</span><span class="info-value">{", ".join(data["commercial"]["purpose"])}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Materials Tab (Extended for Substances of Concern)
    with tabs[3]:
        st.markdown("### Materials and Substances of Concern")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        if data['materials']['substancesOfConcern']['applicable']:
            for substance in data['materials']['substancesOfConcern']['content']:
                st.markdown(f'<div class="card"><span class="info-header">Substance</span><span class="info-value">{substance["id"][0]["name"]}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card"><span class="info-header">Concentration</span><span class="info-value">{substance["concentration"]} {substance["unit"]}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card"><span class="info-header">Hazard Classification</span><span class="info-value">{substance["hazardClassification"]["class"]} - {substance["hazardClassification"]["statement"]}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Handling Tab
    with tabs[4]:
        st.markdown("### Handling Information")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        for producer in data["handling"]["content"]["producer"]:
            st.markdown(f'<div class="card"><span class="info-header">Producer ID</span><span class="info-value">{producer["id"]}</span></div>', unsafe_allow_html=True)
        for spare_part in data["handling"]["content"]["sparePart"]:
            st.markdown(f'<div class="card"><span class="info-header">Spare Part</span><span class="info-value">{spare_part["nameAtManufacturer"]} ({spare_part["manufacturerPartId"]})</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Additional Data Tab
    with tabs[5]:
        st.markdown("### Additional Data")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        for additional_data in data["additionalData"]:
            st.markdown(f'<div class="card"><span class="info-header">{additional_data["label"]}</span><span class="info-value">{additional_data["data"]}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Operation Tab
    with tabs[6]:
        st.markdown("### Operation Information")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="info-header">Manufacturer Date</span><span class="info-value">{data["operation"]["manufacturer"]["manufacturingDate"]}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><span class="info-header">Facility</span><span class="info-value">{data["operation"]["manufacturer"]["facility"][0]["facility"]}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Documentation Tab
    with tabs[7]:
        st.markdown("### Documentation and Sources")
        st.markdown('<div class="card-group">', unsafe_allow_html=True)
        for source in data["sources"]:
            st.markdown(f'<div class="card"><span class="info-header">{source["header"]}</span><span class="info-value"><a href="{source["content"]}" target="_blank">Source Link</a></span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Chat Section
    st.markdown("## 🤖 Chat with AI Assistant")
    st.markdown("Ask any questions or generate content (like charts)!")
    
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

if __name__ == "__main__":
    show_dpp_dashboard()
