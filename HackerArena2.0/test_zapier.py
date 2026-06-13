"""
Run this while Zapier is waiting on 'Pick off a Child Key'.
It sends a sample payload so Zapier can detect your data structure.

Usage:
    1. Paste your Zapier webhook URL below
    2. Run: python test_zapier.py
    3. Go back to Zapier and click 'Test Trigger'
"""
import requests

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/YOUR_ID/YOUR_KEY/"  # <-- paste your URL here

payload = {
    "image_base64": "sample_base64_string",
    "filename": "test_product.jpg",
    "task": "full_product_analysis",
    "output_format": "json",
    "agents": [
        "vision_analysis",
        "listing",
        "packaging",
        "compliance",
        "pricing",
        "competitor_analysis",
        "marketing_content"
    ]
}

response = requests.post(ZAPIER_WEBHOOK_URL, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
print("\nNow go back to Zapier and click 'Test Trigger' - it should detect the fields!")
