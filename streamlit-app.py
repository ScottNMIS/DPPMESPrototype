import streamlit as st
from pythreejs import *
import ipywidgets

st.title("3D Model Viewer")

# Streamlit sidebar layout
st.sidebar.title("3D Model Viewer")
color = st.sidebar.selectbox("Pick a color:", ["white", "green", "blue"])

# Function to display a 3D model using pythreejs
def display_3d_model(file_path):
    with open(file_path, 'r') as f:
        obj_data = f.read()

    # Parse the OBJ file
    loader = OBJLoader()
    obj = loader.parse(obj_data)

    # Set the color
    if color == "white":
        obj.material.color = Color(0xffffff)
    elif color == "green":
        obj.material.color = Color(0x00ff00)
    elif color == "blue":
        obj.material.color = Color(0x0000ff)

    # Set up the scene
    scene = Scene(children=[
        obj,
        AmbientLight(color='#cccccc'),
        DirectionalLight(color='white', position=[3, 5, 1], intensity=0.6)
    ])

    # Set up the camera
    camera = PerspectiveCamera(position=[5, 5, 5], up=[0, 0, 1], children=[
        DirectionalLight(color='white', position=[3, 5, 1], intensity=0.5)
    ])

    # Set up the renderer
    renderer = Renderer(camera=camera, background='black', background_opacity=1, scene=scene, controls=[OrbitControls(controlling=camera)])

    # Display the 3D model
    return renderer

# Display the first model
col1, col2 = st.columns(2)
with col1:
    renderer1 = display_3d_model('cube.obj')
    st.components.v1.html(renderer1.to_html(), height=400)

# Display the second model
with col2:
    renderer2 = display_3d_model('3DBenchy.stl')
    st.components.v1.html(renderer2.to_html(), height=400)
