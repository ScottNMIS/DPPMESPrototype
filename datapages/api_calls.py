import requests

# API base URL
BASE_URL = "http://130.159.132.19:8000"

def create_dpp_api(dpp_data):
    """
    Create a new DPP using the API
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dpps", json=dpp_data, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

def get_machine_data():
    """
    Placeholder function to get machine data from a SQL database
    In the future, this should connect to a real database and fetch actual data
    """
    # Placeholder data
    return {
        "Machine001": {
            "name": "CNC Milling Machine",
            "status": "Operational",
            "last_maintenance": "2024-08-15"
        },
        "Machine002": {
            "name": "3D Printer",
            "status": "Under Maintenance",
            "last_maintenance": "2024-08-20"
        },
        "Machine003": {
            "name": "Laser Cutter",
            "status": "Operational",
            "last_maintenance": "2024-08-10"
        }
    }

# Add other API call functions as needed