# NOTES & PLANNED WORK ACTIVITY FOR REMAKE DPP - Streamlit (03/09/24) - SH

#Tasks:
#1 Configure FastAPI to GET and POST data for DPPs (agree a schema with Jianfang).
#2 Store session data on FastAPI layer to avoid data loss when user refreshes page or session times out. Logic should have data pulled on login for any session data that exists, then wipe when user submits data to update/create a DPP.
#3 Update MOCK DATA with actual DPP data, use MOCK DATA throughout the app to access and retrieve data.
#4 Update API calls, putting all new API call data within api_calls.py file. 
#5 Provide ScanQR code schema to determine if QR code is valid or not. Currently the code 'test' will auto-validate and allow use of the mock_data schema for testing.
#6 Update machine data in api_calls.py to pull data from machines to assign to DPP data. Currently sample machine data is provided. This funciton needs to be re-written once a database exists to pull from._ 
#7 HTML Image footer is broken - It may need to be removed. Does not impact functional requirements.
#8 

#Note, I do not recommend the use of ChatGPT or Claude to error fix code, as they use out of date functions that are no longer supported. 