import pandas as pd

def create_dummy_data():
    data = {
        'Machine': ['Machine A', 'Machine B', 'Machine C'],
        'Start Time': ['2024-07-23 08:00', '2024-07-23 09:00', '2024-07-23 10:00'],
        'Stop Time': ['2024-07-23 08:30', '2024-07-23 09:30', '2024-07-23 10:30'],
        'Status': ['Completed', 'In progress', 'Scheduled'],
        'Output': [20, 15, 25],
        'Energy Consumption': [5.0, 4.5, 6.0],  # in kWh
        'Carbon Footprint': [10.0, 9.0, 12.0]  # in kg CO2
    }
    return pd.DataFrame(data)

def add_new_entry(data, machine, start_time, stop_time, status, output, energy, carbon):
    new_entry = pd.DataFrame({
        'Machine': [machine],
        'Start Time': [start_time],
        'Stop Time': [stop_time],
        'Status': [status],
        'Output': [output],
        'Energy Consumption': [energy],
        'Carbon Footprint': [carbon]
    })
    return pd.concat([data, new_entry], ignore_index=True)
