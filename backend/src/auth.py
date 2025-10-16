#!/usr/bin/env python3
"""
Authentication using Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def sign_up(email: str, password: str):
    """Register new user"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        print(f"✓ User created: {email}")
        return response
    except Exception as e:
        print(f"✗ Signup error: {e}")
        return None

def sign_in(email: str, password: str):
    """Login user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        print(f"✓ Logged in: {email}")
        return response
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def get_user(access_token: str):
    """Get user info from token"""
    try:
        response = supabase.auth.get_user(access_token)
        return response
    except Exception as e:
        print(f"✗ Auth error: {e}")
        return None

if __name__ == "__main__":
    print("Testing authentication...")
    
    # Test signup
    test_email = "paboinc69@gmail.com"
    test_password = "MadJustis077&"
    
    print(f"\n1. Signing up user: {test_email}")
    signup_response = sign_up(test_email, test_password)
    
    if signup_response:
        print("\n2. Signing in...")
        signin_response = sign_in(test_email, test_password)
        
        if signin_response:
            print("\n✓ Authentication working!")
            print(f"Access token: {signin_response.session.access_token[:20]}...")