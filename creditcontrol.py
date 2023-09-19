import streamlit as st
import pandas as pd
import gspread
import plotly.express as px
from google.oauth2 import service_account
import base64

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Define your Google Sheets credentials JSON file (replace with your own)
credentials_path = 'collection20-aa5f3fb7835e.json'

# Authenticate with Google Sheets using the credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=['https://spreadsheets.google.com/feeds'])

# Authenticate with Google Sheets
gc = gspread.authorize(credentials)

url = "https://docs.google.com/spreadsheets/d/1i5HsneT9vpPREVo-ED_HwLLkPpsSjKVY0vuilehDXxg/edit#gid=0"

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

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

        # Read data from the Google Sheets worksheet
        data = worksheet.get_all_values()

        # Prepare data for Plotly
        headers = data[0]
        data = data[1:]
        x_data = [row[2] for row in data]  # Assuming date is in the first column
        y_data = [float(row[3]) for row in data]  # Assuming Outstanding Amount is in the fourth column

        highest_collector = data["Person Allocated"].mode().values[0]
        frequent_category_count = data[data['Category'] == highest_collector].shape[0]

        st.markdown(
            f'<hr style="margin-bottom: 20px;">'  # Add a horizontal line for spacing
            f'<div style= "display: flex; flex-direction: row;">'  # Container with flex layout
            f'<div style="background-color: #f19584; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
            f'<strong style="color: black;"></strong> <br>'
            f"{highest_collector}<br>"
            f"{frequent_category_count} times<br>"
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Create a Plotly scatter plot
        fig = px.bar(x=x_data, y=y_data, labels={'x': headers[2], 'y': headers[3]})
        fig.update_layout(title="OUTSTANDING AMOUNTS PER PERSON ALLOCATED")

        # Display the Plotly plot in Streamlit
        st.plotly_chart(fig)

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

            date_str = date.strftime("%Y-%m-%d")

            # Create a new row of data to add to the Google Sheets spreadsheet
            new_data = [date_str, intermediary, persons, outstanding, collected]

            # Append the new row of data to the worksheet
            worksheet.append_row(new_data)

            # Write the new data to the Google Sheets spreadsheet
            #conn.write(spreadsheet=url, data=new_data, worksheet="assign")

        # Create a form to input data for the new entry

    elif view == "Records":
        # Show the saved DataFrame here
        data = worksheet.get_all_values()

        st.subheader("RECORDS") 
        st.dataframe(data)     

if __name__ == "__main__":
    main()
