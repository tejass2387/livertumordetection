import os
import sys
from dotenv import load_dotenv

print("--- Starting Final API Test ---")

try:
    import google.generativeai as genai
    print(f"Library version: {genai.__version__}")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found.")
    
    genai.configure(api_key=api_key)
    print("API key configured.")

    # ** THE FIX: Use a model name confirmed to be available by the API **
    model = genai.GenerativeModel('gemini-pro')
    print("Model 'gemini-pro' initialized. Sending test prompt...")
    
    response = model.generate_content("test")
    
    if response.text:
        print("\n--- TEST SUCCESSFUL! ---")
        print("Successfully received a response from the Google AI API.")
    else:
        print("\n--- TEST FAILED: Received an empty response. ---")

except Exception as e:
    print("\n--- TEST FAILED WITH AN ERROR ---")
    print(f"An error occurred: {e}")