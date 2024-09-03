import streamlit as st
from openai_api import call_openai_function, fetch_data

def show_customisation():
    st.title("Customisation")
    st.write("Ask a question about the data, and AI will generate the required components.")
    
    question = st.text_input("Ask a question about the data")
    
    if st.button("Generate Components"):
        if question:
            with st.spinner("Generating components..."):
                try:
                    ai_response = call_openai_function(question)
                    
                    if ai_response is None:
                        st.error("No valid response from AI.")
                        return
                    
                    st.write(f"Debug: AI Response - {ai_response}")  # Debug output of AI response
                    
                    function_name = ai_response.get('function')
                    arguments = ai_response.get('arguments')
                    
                    st.write(f"Debug: Function Name - {function_name}")  # Debug output of function name
                    st.write(f"Debug: Arguments - {arguments}")  # Debug output of arguments
                    
                    data = fetch_data()
                    
                    # Call the function dynamically and handle exceptions for each case
                    if function_name in globals():
                        try:
                            globals()[function_name](data, **arguments)
                        except Exception as e:
                            st.error(f"Error executing {function_name}: {e}")
                            st.write(f"Debug: Error Details - {str(e)}")  # More detailed error message
                    else:
                        st.error("Function not implemented")
                except Exception as e:
                    st.error(f"Error generating components: {e}")
                    st.write(f"Debug: Exception Details - {str(e)}")  # General exception details
        else:
            st.error("Please provide a question.")

if __name__ == "__main__":
    show_customisation()
