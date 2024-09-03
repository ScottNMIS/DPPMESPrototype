#This script should be used to house all api calls throughout the application
import requests
import io

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

#TODO method to get machine data from database or table. Currently returns sample data.
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

#Placeholder function to get pre-loaded DPP data
#In the future, this should fetch data from a real API or database
#TODO Update DataHolder for MockData
def get_dpp_data():
    # Mock data for demonstration
    return {
        "part_number": "PN12345",
        "mass": 10.5,
        "hardness": 150,
        "part_description": "Sample part for demonstration",
        "material": "Aluminum",
        "start_time": "2024-08-27 09:00:00",
        "end_time": "2024-08-27 11:30:00",
        "mes_part_number": "MES-PN12345",
        "operation_name": "Milling",
        "operation_time": "2:30:00",
        "machines_used": ["Machine001", "Machine003"],
        "cad_file": io.BytesIO(b"Mock CAD file content").getvalue(),
        "mbd_qif_file": io.BytesIO(b"Mock MBD QIF file content").getvalue(),
        "pdf_3d": io.BytesIO(b"Mock 3D PDF content").getvalue(),
        "cad_file_remake": io.BytesIO(b"Mock CAD file remake content").getvalue(),
        "mbd_qif_file_remake": io.BytesIO(b"Mock MBD QIF file remake content").getvalue(),
        "pdf_3d_remake": io.BytesIO(b"Mock 3D PDF remake content").getvalue(),
        "excel_report": io.BytesIO(b"Mock Excel report content").getvalue(),
        "repair_guideline": io.BytesIO(b"Mock repair guideline content").getvalue(),
        "repair_images": [io.BytesIO(b"Mock repair image 1 content").getvalue(), io.BytesIO(b"Mock repair image 2 content").getvalue()],
        "qif_results_file": io.BytesIO(b"Mock QIF results file content").getvalue(),
        "audit_report": io.BytesIO(b"Mock audit report content").getvalue(),
    }
