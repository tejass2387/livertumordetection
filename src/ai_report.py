import os
import requests
import json
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ** THE FINAL FIX: This URL uses the correct, modern 'v1' endpoint **
MODEL_NAME = "gemini-pro"
URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent?key={API_KEY}"

def generate_report(detection_status, tumor_type):
    """
    Generates a summary report by sending a direct web request to the Google AI API,
    bypassing the problematic local library.
    """
    if not API_KEY:
        return "ERROR: GEMINI_API_KEY not found. Please check your .env file."

    # Create a detailed prompt for the AI
    prompt = f"""
    As a medical analysis assistant, generate a concise, professional summary based on the following detection results.
    Do not provide medical advice. Structure the output in clear sections.

    **Input Data:**
    - Detection Status: {detection_status}
    - Predicted Tumor Type: {tumor_type}

    **Required Output Format:**
    **Analysis Summary:** A brief, one-sentence summary of the findings.
    **Observations:**
    - A bullet point for the detection status.
    - If a tumor is detected, a bullet point describing the predicted type and what it generally is (in one short sentence).
    **Disclaimer:** A standard disclaimer that this is an AI-generated analysis and not a substitute for professional medical consultation.
    """

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    try:
        # Send the request directly to the correct URL
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # This will raise an error for bad responses

        result = response.json()
        report_text = result['candidates'][0]['content']['parts'][0]['text']
        return report_text

    except requests.exceptions.RequestException as e:
        print(f"Error during direct API call: {e}")
        print(f"Response content: {response.text}")
        return "An error occurred while connecting to the AI service."
    except (KeyError, IndexError) as e:
        print(f"Error parsing AI response: {e}")
        print(f"Full response: {result}")
        return "Received an invalid response from the AI service."