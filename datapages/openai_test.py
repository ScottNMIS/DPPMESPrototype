import os

from datetime import datetime
import openai
from openai import OpenAI
import json
import matplotlib.pyplot as plt
import streamlit as st


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

functions = [
    # get weather Information
    {
        "name": "get_weather",  # Name of the function
        "description": "Get the current weather in a location",  # Description of what the function does
        "parameters": {  # Define the parameters the function expects
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                # The location parameter
            },
            "required": ["location"]  # The location parameter is required
        }
    },

    # get current time
    {
        "name": "get_current_time",
        "description": "Get the current time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    # Generate a pie chart
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

#prompt = "Generate a pie chart with labels Apples, Bananas, and Cherries and sizes 30, 40, 30."
prompt = "Generate a pie chart with labels Apples, Bananas, and Cherries and sizes 30, 40, 30."
#prompt = "What's the weather like in Frisco?"  # prompt to test call get_weather function

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Specify the model to use
    messages=[{"role": "user", "content": prompt}],  # The user's input message
    functions=functions,  # The list of functions defined above
    function_call="auto"  # Automatically call the appropriate function based on the user's input
)

def get_weather(location):
    #  Implement your function here
    temp = 25
    return f"The weather in {location} is sunny and {temp} degrees ."

def get_current_time():
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"The current time is {current_time}."

# Function to generate a pie chart and display it in Streamlit
def generate_pie_chart(labels, sizes):
    # Create a pie chart using matplotlib
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is drawn as a circle

    # Display the chart in Streamlit
    st.pyplot(fig)

    return "Pie chart displayed successfully."

print(response.choices[0].message)

function_call = response.choices[0].message.function_call

# Check if function_call exists and the function name is not None
if function_call and function_call.name:
    # Parse the arguments from the function call
    arguments = json.loads(function_call.arguments)

    # Use getattr to dynamically call the function by name
    function_name = function_call.name
    function_to_call = globals().get(function_name)

    if function_to_call:
        # Use **arguments to dynamically pass the arguments to the function
        result = function_to_call(**arguments)
        print(f"Result: {result}")
    else:
        print(f"Function {function_name} not found.")

'''
function_call = response.choices[0].message.function_call

if function_call and function_call.name == "get_weather":
     # Parse the arguments from the function call
     arguments = json.loads(function_call.arguments)
     # Call the get_weather function with the parsed arguments and print the result
     weather_result = get_my_weather(arguments["location"])
     print(f"Weather: {weather_result}")
'''