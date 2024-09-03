import streamlit as st
from vedo import Plotter, Mesh
import tempfile
import trimesh

def load_model(file_path, file_type):
    """
    Load a 3D model from a given file path based on the file type.
    Handles different types of 3D model files.
    """
    try:
        model = trimesh.load(file_path, file_type=file_type)
        return model, None
    except Exception as e:
        return None, str(e)

def display_model(model):
    """
    Display 3D model using vedo.
    """
    if model is not None:
        st.success("Model loaded successfully!")
        st.write(f"Vertices: {model.vertices.shape[0]}")
        st.write(f"Faces: {len(model.faces)}")

        # Convert trimesh model to vedo Mesh
        vedo_mesh = Mesh([model.vertices, model.faces])

        # Create vedo Plotter and add the mesh
        plotter = Plotter(offscreen=True)
        plotter += vedo_mesh
        plotter.show(interactive=False)

        # Export the plot to a static image
        image_path = plotter.screenshot("screenshot.png")

        # Display the image in Streamlit
        st.image(image_path, caption='3D Model')

def show_model_viewer():
    st.title('3D Model Viewer')

    uploaded_file = st.file_uploader("Upload a 3D model file", type=["stl", "obj", "ply", "glb", "gltf"])

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file_type) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        model, error = load_model(tmp_file_path, file_type)
        if error:
            st.error(error)
        else:
            display_model(model)

if __name__ == "__main__":
    show_model_viewer()