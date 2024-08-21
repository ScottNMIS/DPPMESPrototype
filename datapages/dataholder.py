import streamlit as st


MOCK_DATA = {
    "productName": "High-Performance Turbine Blade",
    "partNumber": "TB-2024-X1",
    "manufacturer": "National Manufacturing Institute Scotland",
    "manufacturingDate": "2024-03-15",
    "sustainabilityScore": 85,
    "reparabilityScore": 78,
    "carbonFootprint": 120.5,
    "materials": ["Nickel-based superalloy", "Ceramic coating"],
    "dimensions": {"length": "50 cm", "width": "10 cm", "height": "5 cm"},
    "weight": "2.3 kg",
    "lifecycle": {
        "expectedLifespan": "50,000 flight hours",
        "maintenanceIntervals": ["Every 5,000 hours", "Major overhaul at 25,000 hours"]
    },
    "remanufacturingData": {
        "processSteps": [
            "Inspection", "Cleaning", "Repair", "Coating", "Testing"
        ],
        "toolsRequired": [
            "Optical microscope", "Ultrasonic cleaner", "Welding equipment", 
            "Plasma spray system", "Non-destructive testing equipment"
        ],
        "averageTimeToRemanufacture": "72 hours",
        "successRate": 0.92,
        "costSavingsPercentage": 0.65
    },
    "repairHistory": [
        {"date": "2025-06-10", "type": "Minor repair", "description": "Edge refinishing"},
        {"date": "2026-09-22", "type": "Major overhaul", "description": "Coating replacement and core repair"}
    ],
    "performanceData": {
        "efficiency": [
            {"date": "2024-04-01", "value": 0.95},
            {"date": "2024-07-01", "value": 0.94},
            {"date": "2024-10-01", "value": 0.93},
            {"date": "2025-01-01", "value": 0.92},
            {"date": "2025-04-01", "value": 0.91},
            {"date": "2025-07-01", "value": 0.90}
        ],
        "vibration": [
            {"date": "2024-04-01", "value": 0.02},
            {"date": "2024-07-01", "value": 0.025},
            {"date": "2024-10-01", "value": 0.03},
            {"date": "2025-01-01", "value": 0.035},
            {"date": "2025-04-01", "value": 0.04},
            {"date": "2025-07-01", "value": 0.045}
        ]
    },
    "contactInfo": {
        "email": "contact@strath.ac.uk",
        "phone": "+44 141 548 3623",
        "website": "https://www.strath.ac.uk/research/advancedformingresearchcentre/"
    },
    "dppResources": [
        {"title": "Introduction to Digital Product Passports", "url": "#"},
        {"title": "DPP Implementation Guide", "url": "#"},
        {"title": "DPP Standards and Regulations", "url": "#"},
        {"title": "Case Studies: DPP in Manufacturing", "url": "#"}
    ]
}