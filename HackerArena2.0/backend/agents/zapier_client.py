import os
import base64
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL", "")


def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


async def call_zapier_agent(image_bytes: bytes, filename: str) -> dict:
    """Send product image to Zapier AI Agent webhook and return structured JSON."""
    image_b64 = encode_image_to_base64(image_bytes)

    payload = {
        "image_base64": image_b64,
        "filename": filename,
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

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            ZAPIER_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()

    return _normalize_response(data)


def _normalize_response(data: dict) -> dict:
    """Ensure top-level keys exist even if Zapier returns partial data."""
    keys = ["vision_analysis", "listing", "packaging", "compliance",
            "pricing", "competitor_analysis", "marketing_content"]

    # Zapier sometimes wraps output in an 'output' or 'result' key
    if "output" in data and isinstance(data["output"], dict):
        data = data["output"]
    elif "result" in data and isinstance(data["result"], dict):
        data = data["result"]
    elif "data" in data and isinstance(data["data"], dict):
        data = data["data"]

    # If Zapier returns a JSON string inside a field, parse it
    for key in keys:
        if key in data and isinstance(data[key], str):
            try:
                data[key] = json.loads(data[key])
            except json.JSONDecodeError:
                pass

    # Ensure all keys are present
    for key in keys:
        if key not in data:
            data[key] = {}

    return data
