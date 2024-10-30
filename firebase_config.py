# firebase_config.py
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("vehicle-maintenance-trac-4a63d-firebase-adminsdk-rj4dk-345c5c9b06.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
