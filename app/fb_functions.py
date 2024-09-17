from firebase_admin import auth, credentials, initialize_app, db
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
cred = credentials.Certificate('serviceAccountKey.json')
default_app = initialize_app(cred, {
    'databaseURL': 'https://invoicetracker-8b4e8-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Create a user
def create_user(email, password, name, license_no, phone_no):
    try:
        user = auth.create_user(email=email, password=password)
        uid = user.uid
        ref = db.reference(f'users/{uid}')
        ref.set({
            'name': name,
            'email': email,
            'license_no': license_no,
            'phone_no': phone_no
        })
        return 0
    except Exception as e:
        return 1

# Login a user
def login_with_email_password(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    
    # Request payload
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    # Send POST request to Firebase Authentication API
    response = requests.post(url, json=payload)
    
    # Check if login was successful
    if response.status_code == 200:
        data = response.json()
        id_token = data['idToken']
        print(f"Login successful! User ID Token: {id_token}")
        return id_token
    else:
        print(f"Error: {response.json()}")
        return None
    
def verify_id_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid']
    except Exception as e:
        return None