import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import date as dt

# Define your Google Sheets credentials JSON file (replace with your own)
credentials_path = 'collection20-aa5f3fb7835e.json'

# Authenticate with Google Sheets using the credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://spreadsheets.google.com/feeds'])

# Authenticate with Google Sheets using gspread
gc = gspread.authorize(credentials)

# Your Google Sheets URL
url = "https://docs.google.com/spreadsheets/d/1i5HsneT9vpPREVo-ED_HwLLkPpsSjKVY0vuilehDXxg/edit#gid=0"

# Open the Google Sheets spreadsheet
worksheet = gc.open_by_url(url).worksheet("assign")

# Add a sidebar
st.sidebar.image('corplogo.PNG', use_column_width=True)

# Main Streamlit app code
def main(): 
    # Create a sidebar to switch between views
    view = st.sidebar.radio("View", ["Dashboard", "New Record", "Records"])

    if view == "Dashboard":
        st.subheader("PREMIUM COLLECTION UPDATE APPLICATION")
              
        
    
    elif view == "New Record":
        # Add the dashboard elements here
        st.subheader("NEW ITEM")

        # Create form fields for user input
        date = st.date_input("Date")
        intermediary = st.text_input("Intermediary")
        persons = st.selectbox("Persons Allocated:",["Samuel Kangi", "David Masui", "Chrispus Boro", "Collins Chetekei", "Dennis Amdany"])
        outstanding = st.number_input("Outstanding Amount")
        collected = st.number_input("Amount Collected")

        # Check if the user has entered data and submitted the form
        if st.button("Submit"):
            # Convert the date object to a string
            date_str = date.strftime("%Y-%m-%d")

            # Create a new row of data to add to the Google Sheets spreadsheet
            new_data = [date_str, intermediary, persons, outstanding, collected]

            # Append the new row of data to the worksheet
            worksheet.append_row(new_data)

    elif view == "Records":
        # Show the saved data from the Google Sheets worksheet
        st.subheader("RECORDS")
        data = worksheet.get_all_values()
        st.dataframe(data)

if __name__ == "__main__":
    main()
