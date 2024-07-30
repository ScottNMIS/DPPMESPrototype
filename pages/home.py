import streamlit as st

def show_home():
    st.subheader("Welcome to the MES Dashboard")
    st.write("""
    This dashboard is developed by the National Manufacturing Institute Scotland. This platform provides comprehensive insights into the manufacturing process, allowing for detailed data input, real-time monitoring, and in-depth visualisation of key metrics.
    """)

# Streamlit component calls
st.button('Hit me')

st.checkbox('Check me out')
st.radio('Pick one:', ['nose','ear'])
st.selectbox('Select', [1,2,3])
st.multiselect('Multiselect', [1,2,3])
st.slider('Slide me', min_value=0, max_value=10)
st.select_slider('Slide to select', options=[1,'2'])
st.text_input('Enter some text')
st.number_input('Enter a number')
st.text_area('Area for textual entry')
st.date_input('Date input')
st.time_input('Time entry')
st.file_uploader('File uploader')
st.download_button('On the dl', data=b'Some data to download')

st.color_picker('Pick a color')

