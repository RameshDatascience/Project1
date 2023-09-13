import pandas as pd
import streamlit as st

# Ensure the file read/write operations use 'openpyxl' engine
excel_file = "donations.xlsx"

def save_data(name, phone_number, donation_amount, paid_status, reminder_date):
    try:
        # Load existing data
        df = pd.read_excel(excel_file, engine='openpyxl')
    except FileNotFoundError:
        # Create new dataframe if file does not exist
        df = pd.DataFrame(columns=["Name", "Phone Number", "Donation Amount", "Paid Status", "Reminder Date"])

    # Append the new data
    new_data = {
        "Name": name,
        "Phone Number": phone_number,
        "Donation Amount": donation_amount,
        "Paid Status": paid_status,
        "Reminder Date": reminder_date
    }
    df = df.append(new_data, ignore_index=True)
    df.to_excel(excel_file, index=False, engine='openpyxl')

def app():
    st.title("Donation Data")

    # Input data
    name = st.text_input("Name")
    phone_number = st.text_input("Phone Number")
    donation_amount = st.number_input("Donation Amount", value=0.0)
    paid_status = st.selectbox("Paid Status", ["Paid", "Unpaid"])
    reminder_date = st.date_input("Reminder Date")

    if st.button("Save"):
        save_data(name, phone_number, donation_amount, paid_status, reminder_date)
        st.success("Data saved successfully!")

    # Display the data
    try:
    
        data = pd.read_excel(excel_file, engine='openpyxl')

        # Filter
        st.write("### Filter")
        universal_filter = st.text_input("Search across all columns", "")

        # Apply Filter
        if universal_filter:
            mask = data.apply(lambda row: row.astype(str).str.contains(universal_filter, case=False).any(), axis=1)
            data = data[mask]

        # Display filtered data
        st.write("### Data")
        st.write(data)

        # Display total paid and unpaid amount
        paid_amount = data[data["Paid Status"] == "Paid"]["Donation Amount"].sum()
        unpaid_amount = data[data["Paid Status"] == "Unpaid"]["Donation Amount"].sum()

        st.write(f"### Total Paid Amount: ${paid_amount}")
        st.write(f"### Total Unpaid Amount: ${unpaid_amount}")

    except FileNotFoundError:
        st.write("No data to display")

if __name__ == "__main__":
    app()
