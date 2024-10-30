import streamlit as st
import pandas as pd
from datetime import datetime
from firebase_config import db  # import the Firestore db

st.title("Vehicle Maintenance Tracker")
st.write("Track and manage your vehicle's maintenance.")

# Function to log a new service entry
def log_service(user_id, description, mileage, cost, next_service_date=None, next_service_mileage=None):
    try:
        doc_ref = db.collection("users").document(user_id).collection("maintenance_records").document()
        doc_ref.set({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": description,
            "mileage": mileage,
            "cost": cost,
            "next_service_date": next_service_date.strftime("%Y-%m-%d") if next_service_date else None,
            "next_service_mileage": next_service_mileage if next_service_mileage else None
        })
        st.success("Service entry added!")
    except Exception as e:
        st.error(f"An error occurred while adding the service entry: {e}")

# Form to log a new service entry
st.subheader("Log a New Service/Modification")
with st.form("log_form"):
    user_id = st.text_input("User ID", help="Enter your unique user ID")
    description = st.text_input("Description of Service/Modification", help="E.g., Oil Change, Brake Replacement")
    mileage = st.number_input("Mileage at Service", min_value=0, help="Current mileage of the vehicle")
    cost = st.number_input("Cost of Service ($)", min_value=0.0, help="Cost of the service in USD")
    next_service_date = st.date_input("Next Service Date (optional)", help="When the next service is due")
    next_service_mileage = st.number_input("Next Service Mileage (optional)", min_value=0, help="Mileage at which next service is due")

    submitted = st.form_submit_button("Add Entry")
    if submitted:
        if user_id and description:
            log_service(user_id, description, mileage, cost, next_service_date, next_service_mileage)
        else:
            st.warning("User ID and Description are required fields.")

# Function to retrieve maintenance history
def get_maintenance_history(user_id):
    try:
        records = db.collection("users").document(user_id).collection("maintenance_records").stream()
        data = [{"id": record.id, **record.to_dict()} for record in records]
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"An error occurred while retrieving maintenance history: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Display maintenance history
st.subheader("Maintenance History")
user_id = st.text_input("Enter User ID to View History", help="Enter your unique user ID to view past services")
if user_id:
    df = get_maintenance_history(user_id)
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No maintenance records found for this User ID.")
