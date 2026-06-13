"""
Fallback mock agent — detects product type from filename and returns relevant demo data.
"""

PRODUCT_PROFILES = {
    "shoes": {
        "category": "Footwear", "type": "Casual / Sports Shoes", "brand": "StepUp",
        "material": "Mesh + Rubber Sole", "primary_color": "White",
        "secondary_colors": ["Blue", "Grey"],
        "dimensions": {"length": "30 cm", "width": "12 cm", "height": "10 cm"},
        "weight": {"value": 600, "unit": "grams"},
        "features": ["Breathable mesh upper", "Anti-slip rubber sole", "Cushioned insole for comfort", "Lightweight design", "Available in multiple sizes"],
        "marketplace_category": "Footwear > Casual Shoes",
        "tags": ["shoes", "footwear", "casual", "sports", "comfortable", "lightweight", "running", "daily wear", "men shoes", "women shoes"],
        "packaging_type": "Rigid Shoe Box with Tissue Wrap",
        "box_size": {"length": "35 cm", "width": "18 cm", "height": "14 cm"},
        "protective": ["Tissue paper wrapping", "Silica gel sachet", "Cardboard divider"],
        "low": 499, "recommended": 999, "premium": 1799,
        "cost": "~₹350", "margin": "~65%", "avg_price": "₹799 – ₹1499", "competitors": "120+ active listings",
        "improvements": ["Add extra lace pair as bundle", "Include size guide chart", "Use lifestyle/action photography", "Offer wider size range"],
        "position": "Value segment with strong potential in sports/casual category",
        "bis": False, "bis_notes": "Not mandatory for footwear",
        "fssai": False,
    },
    "shirt": {
        "category": "Apparel", "type": "Casual Shirt", "brand": "FabWear",
        "material": "100% Cotton", "primary_color": "Sky Blue",
        "secondary_colors": ["White", "Navy"],
        "dimensions": {"length": "72 cm", "width": "54 cm", "height": "1 cm"},
        "weight": {"value": 250, "unit": "grams"},
        "features": ["Soft breathable cotton", "Regular fit", "Machine washable", "Anti-wrinkle finish", "Available in S/M/L/XL/XXL"],
        "marketplace_category": "Clothing > Men > Shirts",
        "tags": ["shirt", "cotton", "casual", "men", "apparel", "daily wear", "office wear", "slim fit", "blue shirt", "FabWear"],
        "packaging_type": "Folded in Poly Bag with Cardboard Insert",
        "box_size": {"length": "30 cm", "width": "25 cm", "height": "3 cm"},
        "protective": ["Poly bag", "Cardboard insert", "Size sticker label"],
        "low": 299, "recommended": 599, "premium": 999,
        "cost": "~₹180", "margin": "~70%", "avg_price": "₹399 – ₹899", "competitors": "500+ active listings",
        "improvements": ["Add size chart in listing images", "Offer combo pack discount", "Include wash care card", "Use flat-lay + model photography"],
        "position": "High competition — differentiate via quality imagery and sizing options",
        "bis": False, "bis_notes": "Not applicable for apparel",
        "fssai": False,
    },
    "phone": {
        "category": "Consumer Electronics", "type": "Smartphone", "brand": "TechBrand",
        "material": "Gorilla Glass + Aluminium Frame", "primary_color": "Midnight Black",
        "secondary_colors": ["Silver", "Gold"],
        "dimensions": {"length": "15 cm", "width": "7 cm", "height": "0.8 cm"},
        "weight": {"value": 185, "unit": "grams"},
        "features": ["6.5 inch AMOLED display", "50MP triple camera", "5000mAh battery", "128GB internal storage", "5G connectivity"],
        "marketplace_category": "Electronics > Mobiles > Smartphones",
        "tags": ["smartphone", "5G", "mobile", "android", "camera phone", "AMOLED", "fast charging", "TechBrand", "budget phone", "best mobile"],
        "packaging_type": "Rigid Gift Box with Foam Inlay",
        "box_size": {"length": "18 cm", "width": "10 cm", "height": "5 cm"},
        "protective": ["Foam inlay", "Screen protector film", "Anti-static wrap", "Silica gel"],
        "low": 8999, "recommended": 12999, "premium": 17999,
        "cost": "~₹7000", "margin": "~46%", "avg_price": "₹10,000 – ₹15,000", "competitors": "80+ active listings",
        "improvements": ["Bundle with case and charger", "Highlight camera samples", "Add unboxing video", "Show benchmark scores"],
        "position": "Mid-range competitive segment — differentiate on camera and battery",
        "bis": True, "bis_notes": "Mandatory BIS CRS certification required for smartphones in India",
        "fssai": False,
    },
    "bag": {
        "category": "Bags & Luggage", "type": "Backpack", "brand": "CarryOn",
        "material": "Polyester 600D", "primary_color": "Black",
        "secondary_colors": ["Grey", "Red"],
        "dimensions": {"length": "45 cm", "width": "30 cm", "height": "15 cm"},
        "weight": {"value": 700, "unit": "grams"},
        "features": ["30L capacity", "USB charging port", "Waterproof exterior", "Padded laptop compartment 15.6 inch", "Ergonomic shoulder straps"],
        "marketplace_category": "Bags > Backpacks > Laptop Bags",
        "tags": ["backpack", "laptop bag", "travel bag", "waterproof", "USB charging", "college bag", "office bag", "CarryOn", "30L", "black bag"],
        "packaging_type": "Polybag with Cardboard Header",
        "box_size": {"length": "50 cm", "width": "35 cm", "height": "20 cm"},
        "protective": ["Polybag wrap", "Cardboard stiffener", "Handle tag"],
        "low": 699, "recommended": 1299, "premium": 2199,
        "cost": "~₹450", "margin": "~65%", "avg_price": "₹999 – ₹1799", "competitors": "200+ active listings",
        "improvements": ["Show interior compartment photos", "Highlight laptop compatibility", "Bundle with rain cover", "Add weight capacity spec"],
        "position": "Strong mid-range position in utility/travel segment",
        "bis": False, "bis_notes": "Not applicable for bags",
        "fssai": False,
    },
    "watch": {
        "category": "Accessories", "type": "Wristwatch", "brand": "TimeCraft",
        "material": "Stainless Steel + Mineral Glass", "primary_color": "Silver",
        "secondary_colors": ["Black", "Gold"],
        "dimensions": {"length": "4.5 cm", "width": "4 cm", "height": "1 cm"},
        "weight": {"value": 120, "unit": "grams"},
        "features": ["Analog quartz movement", "Water resistant 30m", "Stainless steel strap", "Scratch-resistant glass", "2-year battery life"],
        "marketplace_category": "Accessories > Watches > Analog",
        "tags": ["watch", "wristwatch", "analog", "stainless steel", "water resistant", "TimeCraft", "mens watch", "womens watch", "gift", "premium watch"],
        "packaging_type": "Premium Watch Box with Pillow Insert",
        "box_size": {"length": "12 cm", "width": "10 cm", "height": "6 cm"},
        "protective": ["Watch pillow", "Velvet lining box", "Polybag outer wrap"],
        "low": 799, "recommended": 1499, "premium": 2999,
        "cost": "~₹500", "margin": "~67%", "avg_price": "₹1,200 – ₹2,500", "competitors": "350+ active listings",
        "improvements": ["Include gift wrapping option", "Show close-up dial photos", "Offer couple set bundle", "Highlight water resistance"],
        "position": "Premium gift segment with strong festive season demand",
        "bis": False, "bis_notes": "Not mandatory",
        "fssai": False,
    },
    "bottle": {
        "category": "Kitchen & Dining", "type": "Water Bottle", "brand": "HydroLife",
        "material": "BPA-Free Stainless Steel", "primary_color": "Matte Blue",
        "secondary_colors": ["Silver", "Black"],
        "dimensions": {"length": "7 cm", "width": "7 cm", "height": "25 cm"},
        "weight": {"value": 300, "unit": "grams"},
        "features": ["1000ml capacity", "Double-wall insulation", "Keeps cold 24h / hot 12h", "Leak-proof lid", "BPA-free food-grade steel"],
        "marketplace_category": "Kitchen > Drinkware > Water Bottles",
        "tags": ["water bottle", "steel bottle", "insulated", "BPA free", "gym bottle", "office bottle", "HydroLife", "leak proof", "eco friendly", "1 litre"],
        "packaging_type": "Kraft Box with Foam Base",
        "box_size": {"length": "10 cm", "width": "10 cm", "height": "28 cm"},
        "protective": ["Foam base insert", "Kraft box", "Tissue wrap"],
        "low": 299, "recommended": 599, "premium": 999,
        "cost": "~₹180", "margin": "~70%", "avg_price": "₹449 – ₹799", "competitors": "600+ active listings",
        "improvements": ["Bundle with cleaning brush", "Show hot/cold test results", "Add carry pouch", "Highlight BPA-free certification"],
        "position": "High-volume commodity segment — brand story and quality imagery key differentiators",
        "bis": False, "bis_notes": "Not applicable",
        "fssai": False,
    },
}

DEFAULT_PROFILE = {
    "category": "General Merchandise", "type": "Consumer Product", "brand": "BrandX",
    "material": "Mixed Materials", "primary_color": "White",
    "secondary_colors": ["Black", "Grey"],
    "dimensions": {"length": "20 cm", "width": "15 cm", "height": "10 cm"},
    "weight": {"value": 400, "unit": "grams"},
    "features": ["Durable construction", "Ergonomic design", "Universal compatibility", "Compact and lightweight", "1-year warranty"],
    "marketplace_category": "General > Products",
    "tags": ["product", "quality", "BrandX", "daily use", "durable", "lightweight", "compact", "value", "premium", "best buy"],
    "packaging_type": "Corrugated Box with Bubble Wrap",
    "box_size": {"length": "25 cm", "width": "20 cm", "height": "15 cm"},
    "protective": ["Bubble wrap", "Foam inserts", "Silica gel sachet"],
    "low": 499, "recommended": 999, "premium": 1799,
    "cost": "~₹300", "margin": "~60%", "avg_price": "₹700 – ₹1,400", "competitors": "100+ active listings",
    "improvements": ["Add high-quality lifestyle images", "Include user manual", "Bundle with accessories", "Highlight warranty prominently"],
    "position": "Mid-range with room to grow into premium segment",
    "bis": False, "bis_notes": "Verify based on product type",
    "fssai": False,
}

KEYWORDS = {
    "shoes": ["shoes", "sneaker", "boot", "sandal", "footwear", "slipper", "heel", "loafer", "chappal"],
    "shirt": ["shirt", "tshirt", "t-shirt", "top", "blouse", "kurta", "polo", "hoodie", "jacket", "apparel", "cloth", "wear", "dress"],
    "phone": ["phone", "mobile", "smartphone", "iphone", "samsung", "oneplus", "redmi", "realme", "device"],
    "bag": ["bag", "backpack", "purse", "handbag", "wallet", "luggage", "pouch", "satchel", "tote"],
    "watch": ["watch", "clock", "timepiece", "smartwatch", "wristwatch"],
    "bottle": ["bottle", "flask", "mug", "cup", "tumbler", "drinkware", "sipper"],
}


def _detect_profile(filename: str) -> dict:
    name_lower = filename.lower()
    for profile_key, words in KEYWORDS.items():
        if any(w in name_lower for w in words):
            return PRODUCT_PROFILES[profile_key], profile_key
    return DEFAULT_PROFILE, "product"


def get_mock_analysis(filename: str) -> dict:
    p, pkey = _detect_profile(filename)
    raw_name = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
    name = raw_name if len(raw_name) < 40 else p["type"]

    return {
        "vision_analysis": {
            "product_name": name,
            "product_category": p["category"],
            "product_type": p["type"],
            "brand": p["brand"],
            "material": p["material"],
            "primary_color": p["primary_color"],
            "secondary_colors": p["secondary_colors"],
            "estimated_dimensions": p["dimensions"],
            "estimated_weight": p["weight"],
            "key_features": p["features"],
            "confidence_score": 0.91
        },
        "listing": {
            "seo_optimized_title": f"{name} – {p['type']} | {p['primary_color']} | {p['brand']} | Best Quality",
            "product_description": (
                f"Introducing the {name} by {p['brand']} — crafted from {p['material']} for premium quality and lasting durability. "
                f"This {p['type'].lower()} is designed for everyday use, combining style and functionality seamlessly. "
                f"Featuring {p['features'][0].lower()}, {p['features'][1].lower()}, and {p['features'][2].lower()}, "
                f"it stands out in the {p['category'].lower()} category. "
                f"Available in {p['primary_color']} with {' and '.join(p['secondary_colors'][:2])} accents. "
                "Lightweight, compact, and built to last — perfect for daily use, gifting, or personal upgrade. "
                f"Backed by {p['brand']}'s quality promise and 1-year warranty. Order now and experience the difference."
            ),
            "bullet_points": [
                f"✅ Made from {p['material']} for premium durability",
                f"✅ {p['features'][0]}",
                f"✅ {p['features'][1]}",
                f"✅ {p['features'][2]}",
                f"✅ Backed by 1-year warranty from {p['brand']}"
            ],
            "seo_keywords": [
                f"buy {name}", f"{name} online", f"best {p['type'].lower()}",
                f"{p['brand']} {pkey}", f"{p['primary_color']} {pkey}",
                f"premium {p['category'].lower()}", f"{pkey} under ₹{p['recommended']}",
                f"top rated {pkey}", f"{p['material'].lower()} {pkey}", f"{pkey} India"
            ],
            "marketplace_category": p["marketplace_category"],
            "search_tags": p["tags"]
        },
        "packaging": {
            "recommended_packaging_type": p["packaging_type"],
            "recommended_box_size": p["box_size"],
            "protective_material": p["protective"],
            "shipping_recommendations": {
                "carrier": "BlueDart / Delhivery / Shiprocket",
                "mode": "Surface for domestic, Air for international",
                "fragile_label": True,
                "estimated_shipping_weight": f"{p['weight']['value'] + 200} grams (with packaging)"
            }
        },
        "compliance": {
            "bis_requirement": {
                "required": p["bis"],
                "certificate": "IS 13252 / BIS CRS" if p["bis"] else "N/A",
                "notes": p["bis_notes"]
            },
            "fssai_requirement": {
                "required": False,
                "notes": "Not applicable for non-food products"
            },
            "barcode_requirement": {
                "required": True,
                "type": "EAN-13 or UPC-A",
                "notes": "Register with GS1 India for a genuine barcode"
            },
            "mrp_label_requirement": {
                "required": True,
                "fields": ["MRP (incl. all taxes)", "Manufacturer name & address",
                           "Country of origin", "Customer care number", "Month & Year of manufacture"]
            },
            "product_label_information": {
                "generic_name": name,
                "net_quantity": "1 Unit",
                "country_of_origin": "India",
                "customer_care": "1800-XXX-XXXX"
            }
        },
        "pricing": {
            "low_price": {"amount": p["low"], "currency": "INR", "label": "Budget / Entry"},
            "recommended_selling_price": {"amount": p["recommended"], "currency": "INR", "label": "Optimal Margin"},
            "premium_price": {"amount": p["premium"], "currency": "INR", "label": "Premium / Brand"},
            "pricing_analysis": {
                "cost_of_goods": p["cost"],
                "recommended_margin": p["margin"],
                "break_even_units": 50,
                "notes": f"Recommended price offers best conversion vs. margin balance on Amazon & Flipkart for {p['category']}"
            }
        },
        "competitor_analysis": {
            "average_market_price": p["avg_price"],
            "competitor_count": p["competitors"],
            "suggested_improvements": p["improvements"],
            "market_position": p["position"]
        },
        "marketing_content": {
            "instagram_post": (
                f"✨ Meet your new favourite! 🔥\n\n"
                f"Introducing the {name} — {p['features'][0].lower()} & {p['features'][1].lower()}. 💯\n\n"
                f"Available now on Amazon & Flipkart!\n\n"
                f"#NewLaunch #{pkey.capitalize()} #{p['brand']} #MustHave #ShopNow #IndianBrand"
            ),
            "facebook_post": (
                f"🎉 Exciting Launch Alert!\n\n"
                f"We're proud to introduce the {name} — {p['type']} built for quality and comfort.\n\n"
                f"🔑 Key Highlights:\n"
                f"• {p['features'][0]}\n• {p['features'][1]}\n• {p['features'][2]}\n\n"
                f"🛒 Shop now on Amazon & Flipkart\n"
                f"📦 Fast delivery across India\n"
                f"💯 1-Year Warranty\n\nTag someone who needs this! 👇"
            ),
            "whatsapp_promotion": (
                f"🛍️ *New Launch Alert!*\n\n"
                f"*{name}* is now LIVE!\n\n"
                f"✅ {p['features'][0]}\n"
                f"✅ {p['features'][1]}\n"
                f"✅ Best Price: ₹{p['recommended']}\n\n"
                f"👉 Use code *LAUNCH10* for 10% OFF\n"
                f"_Limited stock — Order now!_ 🔥"
            ),
            "email_campaign": (
                f"Subject: 🚀 Just Launched: {name} — Exclusive Offer Inside!\n\n"
                f"Hi [Customer Name],\n\n"
                f"We're excited to introduce the {name} — our latest {p['type'].lower()} from {p['brand']}.\n\n"
                f"Here's why you'll love it:\n"
                f"• {p['features'][0]}\n• {p['features'][1]}\n• {p['features'][2]}\n\n"
                f"🎁 Exclusive launch offer: 15% OFF with code VIPEARLY15\n"
                f"⏰ Offer valid for 48 hours only.\n\n"
                f"👉 [Shop Now]\n\nWarm regards,\nThe {p['brand']} Team"
            )
        }
    }
