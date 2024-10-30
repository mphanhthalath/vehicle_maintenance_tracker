import streamlit as st
import pandas as pd
from datetime import datetime
from firebase_config import db  # import the Firestore db

st.title("Vehicle Maintenance Tracker")
st.write("Track and manage your vehicle's maintenance.")

def log_service(user_id, description, mileage, cost, next_service_date=None, next_service_mileage=None):
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

st.subheader("Log a New Service/Modification")

with st.form("log_form"):
    user_id = st.text_input("User ID")
    description = st.text_input("Description of Service/Modification")
    mileage = st.number_input("Mileage at Service", min_value=0)
    cost = st.number_input("Cost of Service ($)", min_value=0.0)
    next_service_date = st.date_input("Next Service Date (optional)")
    next_service_mileage = st.number_input("Next Service Mileage (optional)", min_value=0)
    
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        log_service(user_id, description, mileage, cost, next_service_date, next_service_mileage)

def get_maintenance_history(user_id):
    records = db.collection("users").document(user_id).collection("maintenance_records").stream()
    data = [{"id": record.id, **record.to_dict()} for record in records]
    return pd.DataFrame(data)

st.subheader("Maintenance History")
user_id = st.text_input("Enter User ID to View History")
if user_id:
    df = get_maintenance_history(user_id)
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No maintenance records found.")
