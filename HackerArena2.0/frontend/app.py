import streamlit as st
import requests
import json
import os
from PIL import Image
import io

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Product Launch Studio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
[data-testid="stAppViewContainer"] { background: #0f0f1a; }
[data-testid="stSidebar"] { background: #1a1a2e; }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

/* Cards */
.card {
    background: #1e1e32;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid #2e2e4e;
}
.card h3 { color: #e94560; margin-top: 0; font-size: 1.05rem; }
.card p, .card li { color: #c0c0d0; font-size: 0.9rem; line-height: 1.6; }

/* Section header */
.section-header {
    background: linear-gradient(90deg, #1a1a2e, #e94560);
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 1.2rem 0 0.8rem;
}

/* Pricing cards */
.price-card {
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    color: white;
}
.price-budget  { background: linear-gradient(135deg, #11998e, #38ef7d); }
.price-recommended { background: linear-gradient(135deg, #e94560, #c0392b); }
.price-premium { background: linear-gradient(135deg, #8e44ad, #3498db); }
.price-card h2 { margin: 0; font-size: 1.8rem; }
.price-card p  { margin: 4px 0 0; font-size: 0.85rem; opacity: 0.9; }

/* Metric */
.metric-box {
    background: #1e1e32;
    border-left: 4px solid #e94560;
    padding: 0.8rem 1rem;
    border-radius: 6px;
    margin-bottom: 0.6rem;
}
.metric-box .metric-label { color: #888; font-size: 0.75rem; text-transform: uppercase; }
.metric-box .metric-value { color: #ffffff; font-size: 1.1rem; font-weight: 600; }

/* Keyword badge */
.badge {
    display: inline-block;
    background: #e94560;
    color: white;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    margin: 3px 3px;
}

/* Bullet points */
.bullet { color: #c0c0d0; padding: 4px 0; font-size: 0.9rem; }

/* Confidence bar */
.conf-bar-wrap { background: #2e2e4e; border-radius: 20px; height: 14px; width: 100%; }
.conf-bar-fill { background: linear-gradient(90deg, #e94560, #f5a623);
                  border-radius: 20px; height: 14px; }

/* Upload area */
[data-testid="stFileUploader"] {
    background: #1e1e32;
    border: 2px dashed #e94560;
    border-radius: 12px;
    padding: 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #e94560, #c0392b) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Tabs */
[data-testid="stTabs"] button { color: #c0c0d0 !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #e94560 !important;
    border-bottom: 2px solid #e94560 !important;
}

/* General text */
h1, h2, h3, h4, .stMarkdown { color: #f0f0f0; }
p { color: #c0c0d0; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def section(title: str):
    st.markdown(f'<div class="section-header">🔹 {title}</div>', unsafe_allow_html=True)


def card(title: str, content: str):
    st.markdown(f'<div class="card"><h3>{title}</h3><p>{content}</p></div>',
                unsafe_allow_html=True)


def metric_box(label: str, value: str):
    st.markdown(
        f'<div class="metric-box"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True
    )


def badges(items: list):
    html = "".join(f'<span class="badge">{i}</span>' for i in items)
    st.markdown(html, unsafe_allow_html=True)


def confidence_bar(score: float):
    pct = int(score * 100)
    color = "#27ae60" if pct >= 80 else "#f39c12" if pct >= 60 else "#e74c3c"
    st.markdown(
        f'<div class="conf-bar-wrap">'
        f'<div class="conf-bar-fill" style="width:{pct}%;background:{color};"></div>'
        f'</div><p style="color:{color};font-size:0.85rem;margin-top:4px;">{pct}% Confidence</p>',
        unsafe_allow_html=True
    )


def _fmt(val):
    if isinstance(val, dict):
        return ", ".join(f"{k}: {v}" for k, v in val.items())
    if isinstance(val, list):
        return ", ".join(str(v) for v in val)
    return str(val) if val else "—"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 AI Product Launch Studio")
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio("", ["📸 New Analysis", "📂 History"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "Powered by **Zapier AI Agents** — analyze any product image and get a "
        "complete marketplace-ready package instantly."
    )
    st.markdown("---")
    st.markdown("**Supported Platforms**")
    for p in ["🛒 Amazon", "🛍️ Flipkart", "🧵 Meesho", "🏪 Shopify"]:
        st.markdown(p)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: New Analysis
# ══════════════════════════════════════════════════════════════════════════════
if page == "📸 New Analysis":
    st.markdown("# 🚀 AI Product Launch Studio")
    st.markdown("Upload a product image to generate a complete marketplace-ready product package.")
    st.markdown("---")

    col_upload, col_preview = st.columns([1, 1])

    with col_upload:
        section("1. Upload Product Image")
        uploaded_file = st.file_uploader(
            "Drop your product image here",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )

    with col_preview:
        if uploaded_file:
            section("Product Preview")
            img = Image.open(uploaded_file)
            st.image(img, use_column_width=True)
            st.caption(f"📁 {uploaded_file.name}  |  {img.size[0]}×{img.size[1]}px")

    if uploaded_file:
        st.markdown("---")
        col_btn, col_note = st.columns([1, 3])
        with col_btn:
            analyze_clicked = st.button("⚡ Analyze Product", use_container_width=True)
        with col_note:
            st.info("Analysis typically takes 10–30 seconds via the AI Agent pipeline.")

        if analyze_clicked:
            with st.spinner("🤖 AI Agents are analyzing your product..."):
                uploaded_file.seek(0)
                resp = requests.post(
                    f"{API_BASE}/analyze",
                    files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
                    timeout=180,
                )

            if resp.status_code != 200:
                st.error(f"Analysis failed: {resp.text}")
                st.stop()

            data = resp.json()
            st.session_state["result"] = data
            st.success("✅ Analysis complete!")

    # ── Display Results ────────────────────────────────────────────────────────
    if "result" in st.session_state:
        data = st.session_state["result"]
        record_id = data.get("id")

        tabs = st.tabs([
            "🔍 Vision", "📝 Listing", "📦 Packaging",
            "⚖️ Compliance", "💰 Pricing", "📊 Competitors",
            "📣 Marketing", "📤 Export"
        ])

        # ── Tab 1: Vision Analysis ─────────────────────────────────────────────
        with tabs[0]:
            section("Vision Analysis")
            va = data.get("vision_analysis") or {}
            c1, c2, c3 = st.columns(3)
            with c1:
                metric_box("Product Name", va.get("product_name", "—"))
                metric_box("Brand", va.get("brand", "—"))
                metric_box("Material", va.get("material", "—"))
            with c2:
                metric_box("Category", va.get("product_category", "—"))
                metric_box("Type", va.get("product_type", "—"))
                metric_box("Primary Color", va.get("primary_color", "—"))
            with c3:
                metric_box("Dimensions", _fmt(va.get("estimated_dimensions")))
                metric_box("Weight", _fmt(va.get("estimated_weight")))
                metric_box("Secondary Colors", _fmt(va.get("secondary_colors")))

            st.markdown("**Confidence Score**")
            confidence_bar(va.get("confidence_score", 0))

            if va.get("key_features"):
                st.markdown("**Key Features**")
                for feat in va.get("key_features", []):
                    st.markdown(f'<div class="bullet">✅ {feat}</div>', unsafe_allow_html=True)

            with st.expander("📋 Raw JSON"):
                st.json(va)

        # ── Tab 2: Listing ─────────────────────────────────────────────────────
        with tabs[1]:
            section("SEO Listing Generation")
            li = data.get("listing") or {}

            card("🏷️ SEO Optimized Title", li.get("seo_optimized_title", "—"))

            st.markdown("**Product Description**")
            st.markdown(
                f'<div class="card"><p>{li.get("product_description", "—")}</p></div>',
                unsafe_allow_html=True
            )

            st.markdown("**Bullet Points**")
            for bp in li.get("bullet_points", []):
                st.markdown(f'<div class="bullet">{bp}</div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**SEO Keywords**")
                badges(li.get("seo_keywords", []))
            with c2:
                st.markdown("**Search Tags**")
                badges(li.get("search_tags", []))

            metric_box("Marketplace Category", li.get("marketplace_category", "—"))
            with st.expander("📋 Raw JSON"):
                st.json(li)

        # ── Tab 3: Packaging ───────────────────────────────────────────────────
        with tabs[2]:
            section("Packaging Suggestions")
            pk = data.get("packaging") or {}

            c1, c2 = st.columns(2)
            with c1:
                metric_box("Packaging Type", pk.get("recommended_packaging_type", "—"))
                metric_box("Box Size", _fmt(pk.get("recommended_box_size")))
            with c2:
                st.markdown("**Protective Materials**")
                for mat in pk.get("protective_material", []):
                    st.markdown(f'<div class="bullet">📦 {mat}</div>', unsafe_allow_html=True)

            st.markdown("**Shipping Recommendations**")
            shipping = pk.get("shipping_recommendations", {})
            if isinstance(shipping, dict):
                cols = st.columns(len(shipping)) if shipping else [st]
                for i, (k, v) in enumerate(shipping.items()):
                    with cols[i] if shipping else st:
                        metric_box(k.replace("_", " ").title(), str(v))
            else:
                st.write(shipping)

            with st.expander("📋 Raw JSON"):
                st.json(pk)

        # ── Tab 4: Compliance ──────────────────────────────────────────────────
        with tabs[3]:
            section("Compliance Report")
            co = data.get("compliance") or {}

            for label, key, icon in [
                ("BIS Requirement", "bis_requirement", "🏛️"),
                ("FSSAI Requirement", "fssai_requirement", "🥗"),
                ("Barcode Requirement", "barcode_requirement", "📊"),
                ("MRP Label Requirement", "mrp_label_requirement", "🏷️"),
                ("Product Label Information", "product_label_information", "📋"),
            ]:
                val = co.get(key, {})
                if isinstance(val, dict):
                    req = val.get("required")
                    status = "✅ Required" if req is True else ("❌ Not Required" if req is False else "ℹ️ See details")
                    notes = val.get("notes", "")
                    extra = {k: v for k, v in val.items() if k not in ("required", "notes")}
                    content = f"{status}<br/>{notes}"
                    if extra:
                        content += "<br/>" + ", ".join(f"<b>{k}</b>: {_fmt(v)}" for k, v in extra.items())
                    st.markdown(
                        f'<div class="card"><h3>{icon} {label}</h3><p>{content}</p></div>',
                        unsafe_allow_html=True
                    )
                else:
                    card(f"{icon} {label}", str(val))

            with st.expander("📋 Raw JSON"):
                st.json(co)

        # ── Tab 5: Pricing ─────────────────────────────────────────────────────
        with tabs[4]:
            section("Pricing Analysis")
            pr = data.get("pricing") or {}

            def price_str(p):
                if isinstance(p, dict):
                    return f"₹{p.get('amount', '—')}"
                return str(p)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f'<div class="price-card price-budget">'
                    f'<p>Budget</p><h2>{price_str(pr.get("low_price"))}</h2>'
                    f'<p>{pr.get("low_price", {}).get("label", "") if isinstance(pr.get("low_price"), dict) else ""}</p>'
                    f'</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(
                    f'<div class="price-card price-recommended">'
                    f'<p>⭐ Recommended</p><h2>{price_str(pr.get("recommended_selling_price"))}</h2>'
                    f'<p>{pr.get("recommended_selling_price", {}).get("label", "") if isinstance(pr.get("recommended_selling_price"), dict) else ""}</p>'
                    f'</div>', unsafe_allow_html=True)
            with c3:
                st.markdown(
                    f'<div class="price-card price-premium">'
                    f'<p>Premium</p><h2>{price_str(pr.get("premium_price"))}</h2>'
                    f'<p>{pr.get("premium_price", {}).get("label", "") if isinstance(pr.get("premium_price"), dict) else ""}</p>'
                    f'</div>', unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)
            pa = pr.get("pricing_analysis", {})
            if isinstance(pa, dict):
                c1, c2 = st.columns(2)
                items = list(pa.items())
                half = len(items) // 2
                with c1:
                    for k, v in items[:half + 1]:
                        metric_box(k.replace("_", " ").title(), str(v))
                with c2:
                    for k, v in items[half + 1:]:
                        metric_box(k.replace("_", " ").title(), str(v))

            with st.expander("📋 Raw JSON"):
                st.json(pr)

        # ── Tab 6: Competitor Analysis ─────────────────────────────────────────
        with tabs[5]:
            section("Competitor Analysis")
            ca = data.get("competitor_analysis") or {}

            c1, c2, c3 = st.columns(3)
            with c1:
                metric_box("Avg Market Price", ca.get("average_market_price", "—"))
            with c2:
                metric_box("Competitor Count", ca.get("competitor_count", "—"))
            with c3:
                metric_box("Market Position", ca.get("market_position", "—"))

            if ca.get("suggested_improvements"):
                st.markdown("**Suggested Improvements**")
                for s in ca.get("suggested_improvements", []):
                    st.markdown(f'<div class="bullet">💡 {s}</div>', unsafe_allow_html=True)

            with st.expander("📋 Raw JSON"):
                st.json(ca)

        # ── Tab 7: Marketing Content ───────────────────────────────────────────
        with tabs[6]:
            section("Marketing Content")
            mk = data.get("marketing_content") or {}

            m1, m2 = st.columns(2)
            with m1:
                st.markdown("**📸 Instagram Post**")
                st.markdown(
                    f'<div class="card"><p>{mk.get("instagram_post", "—").replace(chr(10), "<br/>")}</p></div>',
                    unsafe_allow_html=True)

                st.markdown("**💬 WhatsApp Promotion**")
                st.markdown(
                    f'<div class="card"><p>{mk.get("whatsapp_promotion", "—").replace(chr(10), "<br/>")}</p></div>',
                    unsafe_allow_html=True)

            with m2:
                st.markdown("**👥 Facebook Post**")
                st.markdown(
                    f'<div class="card"><p>{mk.get("facebook_post", "—").replace(chr(10), "<br/>")}</p></div>',
                    unsafe_allow_html=True)

                st.markdown("**📧 Email Campaign**")
                st.markdown(
                    f'<div class="card"><p>{mk.get("email_campaign", "—").replace(chr(10), "<br/>")}</p></div>',
                    unsafe_allow_html=True)

            with st.expander("📋 Raw JSON"):
                st.json(mk)

        # ── Tab 8: Export Center ───────────────────────────────────────────────
        with tabs[7]:
            section("Export Center")

            if not record_id:
                st.warning("Save the analysis first before exporting.")
            else:
                st.markdown("### 📄 PDF Report")
                if st.button("📄 Generate & Download PDF Report", use_container_width=True):
                    with st.spinner("Generating PDF..."):
                        r = requests.post(f"{API_BASE}/generate-pdf/{record_id}", timeout=60)
                    if r.status_code == 200:
                        st.download_button(
                            "⬇️ Download PDF",
                            data=r.content,
                            file_name=f"product_report_{record_id}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                    else:
                        st.error("PDF generation failed.")

                st.markdown("---")
                st.markdown("### 📊 CSV Exports")
                if st.button("📊 Generate & Download CSV", use_container_width=True):
                    with st.spinner("Generating CSV..."):
                        r = requests.post(f"{API_BASE}/export-csv/{record_id}", timeout=60)
                    if r.status_code == 200:
                        st.download_button(
                            "⬇️ Download Master CSV",
                            data=r.content,
                            file_name=f"product_analysis_{record_id}.csv",
                            mime="text/csv",
                            use_container_width=True,
                        )
                        st.info(
                            "📁 Marketplace-specific CSVs (Amazon, Flipkart, Meesho, Shopify) "
                            "have been saved to **exports/csv/** folder."
                        )
                    else:
                        st.error("CSV export failed.")

                st.markdown("---")
                st.markdown("### 📋 Raw JSON")
                with st.expander("View Complete JSON Response"):
                    st.json(data)
                json_str = json.dumps(data, indent=2)
                st.download_button(
                    "⬇️ Download JSON",
                    data=json_str,
                    file_name=f"product_analysis_{record_id}.json",
                    mime="application/json",
                    use_container_width=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: History
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📂 History":
    st.markdown("# 📂 Analysis History")
    st.markdown("Previously analyzed products.")
    st.markdown("---")

    resp = requests.get(f"{API_BASE}/history", timeout=30)
    if resp.status_code != 200:
        st.error("Could not fetch history from API.")
        st.stop()

    records = resp.json()
    if not records:
        st.info("No analyses yet. Upload a product image to get started!")
        st.stop()

    for rec in records:
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 1, 1])
            with c1:
                st.markdown(f"**{rec.get('product_name', 'Unknown Product')}**")
                st.caption(f"📁 {rec.get('image_filename', '')} · ID #{rec.get('id')}")
            with c2:
                st.caption(f"🗂️ {rec.get('product_category', '—')}")
            with c3:
                score = rec.get("confidence_score", 0)
                st.caption(f"🎯 Confidence: {int(score * 100)}%")
            with c4:
                created = rec.get("created_at", "")[:10] if rec.get("created_at") else "—"
                st.caption(f"📅 {created}")
            with c5:
                if st.button("View", key=f"view_{rec['id']}"):
                    r = requests.get(f"{API_BASE}/analysis/{rec['id']}", timeout=30)
                    if r.status_code == 200:
                        st.session_state["result"] = r.json()
                        st.session_state["_page_redirect"] = "new"
                        st.rerun()
            st.markdown("---")
