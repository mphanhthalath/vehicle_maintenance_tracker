import os
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# Access Firebase credentials from Streamlit secrets
cred_dict = st.secrets["firebase"]

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
