import pandas as pd
import os
from datetime import datetime


def _safe(val):
    if isinstance(val, (dict, list)):
        return str(val)
    return val or ""


def generate_csv(analysis: dict, record_id: int) -> str:
    va = analysis.get("vision_analysis", {})
    li = analysis.get("listing", {})
    pk = analysis.get("packaging", {})
    co = analysis.get("compliance", {})
    pr = analysis.get("pricing", {})
    ca = analysis.get("competitor_analysis", {})
    mk = analysis.get("marketing_content", {})

    rows = [
        # Vision
        ("Vision Analysis", "Product Name", _safe(va.get("product_name"))),
        ("Vision Analysis", "Category", _safe(va.get("product_category"))),
        ("Vision Analysis", "Type", _safe(va.get("product_type"))),
        ("Vision Analysis", "Brand", _safe(va.get("brand"))),
        ("Vision Analysis", "Material", _safe(va.get("material"))),
        ("Vision Analysis", "Primary Color", _safe(va.get("primary_color"))),
        ("Vision Analysis", "Secondary Colors", ", ".join(va.get("secondary_colors", []))),
        ("Vision Analysis", "Dimensions", _safe(va.get("estimated_dimensions"))),
        ("Vision Analysis", "Weight", _safe(va.get("estimated_weight"))),
        ("Vision Analysis", "Key Features", " | ".join(va.get("key_features", []))),
        ("Vision Analysis", "Confidence Score", _safe(va.get("confidence_score"))),
        # Listing
        ("Listing", "SEO Title", _safe(li.get("seo_optimized_title"))),
        ("Listing", "Description", _safe(li.get("product_description"))),
        ("Listing", "Bullet Points", " | ".join(li.get("bullet_points", []))),
        ("Listing", "SEO Keywords", ", ".join(li.get("seo_keywords", []))),
        ("Listing", "Marketplace Category", _safe(li.get("marketplace_category"))),
        ("Listing", "Search Tags", ", ".join(li.get("search_tags", []))),
        # Packaging
        ("Packaging", "Type", _safe(pk.get("recommended_packaging_type"))),
        ("Packaging", "Box Size", _safe(pk.get("recommended_box_size"))),
        ("Packaging", "Protective Materials", " | ".join(pk.get("protective_material", []))),
        ("Packaging", "Shipping Recommendations", _safe(pk.get("shipping_recommendations"))),
        # Compliance
        ("Compliance", "BIS Requirement", _safe(co.get("bis_requirement"))),
        ("Compliance", "FSSAI Requirement", _safe(co.get("fssai_requirement"))),
        ("Compliance", "Barcode Requirement", _safe(co.get("barcode_requirement"))),
        ("Compliance", "MRP Label", _safe(co.get("mrp_label_requirement"))),
        ("Compliance", "Product Label Info", _safe(co.get("product_label_information"))),
        # Pricing
        ("Pricing", "Low Price", _safe(pr.get("low_price"))),
        ("Pricing", "Recommended Price", _safe(pr.get("recommended_selling_price"))),
        ("Pricing", "Premium Price", _safe(pr.get("premium_price"))),
        ("Pricing", "Pricing Analysis", _safe(pr.get("pricing_analysis"))),
        # Competitor
        ("Competitor Analysis", "Avg Market Price", _safe(ca.get("average_market_price"))),
        ("Competitor Analysis", "Competitor Count", _safe(ca.get("competitor_count"))),
        ("Competitor Analysis", "Suggested Improvements", " | ".join(ca.get("suggested_improvements", []))),
        ("Competitor Analysis", "Market Position", _safe(ca.get("market_position"))),
        # Marketing
        ("Marketing", "Instagram Post", _safe(mk.get("instagram_post"))),
        ("Marketing", "Facebook Post", _safe(mk.get("facebook_post"))),
        ("Marketing", "WhatsApp Promotion", _safe(mk.get("whatsapp_promotion"))),
        ("Marketing", "Email Campaign", _safe(mk.get("email_campaign"))),
    ]

    df = pd.DataFrame(rows, columns=["Section", "Field", "Value"])

    os.makedirs("exports/csv", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = f"exports/csv/product_analysis_{record_id}_{timestamp}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def generate_marketplace_csvs(analysis: dict, record_id: int) -> dict:
    """Generate separate marketplace-ready CSVs for Amazon, Flipkart, Meesho, Shopify."""
    va = analysis.get("vision_analysis", {})
    li = analysis.get("listing", {})
    pr = analysis.get("pricing", {})

    base = {
        "product_name": va.get("product_name", ""),
        "category": li.get("marketplace_category", ""),
        "description": li.get("product_description", ""),
        "keywords": ", ".join(li.get("seo_keywords", [])),
        "material": va.get("material", ""),
        "color": va.get("primary_color", ""),
        "brand": va.get("brand", ""),
    }

    rsp = pr.get("recommended_selling_price", {})
    price = rsp.get("amount", "") if isinstance(rsp, dict) else rsp

    amazon_row = {**base, "asin": "", "fulfillment": "FBA", "mrp": price, "selling_price": price,
                  "bullet_point_1": li.get("bullet_points", [""] * 5)[0],
                  "bullet_point_2": li.get("bullet_points", [""] * 5)[1] if len(li.get("bullet_points", [])) > 1 else "",
                  "search_terms": ", ".join(li.get("search_tags", []))}

    flipkart_row = {**base, "listing_id": "", "selling_price": price, "mrp": price,
                    "hsn_code": "", "gst_percent": "18",
                    "product_highlights": " | ".join(li.get("bullet_points", []))}

    meesho_row = {**base, "mrp": price, "selling_price": price,
                  "product_highlights": " | ".join(li.get("bullet_points", [])),
                  "tags": ", ".join(li.get("search_tags", []))}

    shopify_row = {**base, "handle": va.get("product_name", "").lower().replace(" ", "-"),
                   "price": price, "compare_at_price": price,
                   "tags": ", ".join(li.get("search_tags", [])),
                   "seo_title": li.get("seo_optimized_title", ""),
                   "seo_description": li.get("product_description", "")[:160]}

    os.makedirs("exports/csv", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    paths = {}

    for name, row in [("amazon", amazon_row), ("flipkart", flipkart_row),
                       ("meesho", meesho_row), ("shopify", shopify_row)]:
        path = f"exports/csv/{name}_{record_id}_{timestamp}.csv"
        pd.DataFrame([row]).to_csv(path, index=False, encoding="utf-8-sig")
        paths[name] = path

    return paths
