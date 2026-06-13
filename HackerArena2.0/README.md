# 🚀 AI Product Launch Studio Agent

An end-to-end AI-powered product launch automation system. Upload a product image and instantly receive a complete marketplace-ready package for **Amazon, Flipkart, Meesho, and Shopify**.

---

## Architecture

```
Streamlit Frontend
      │
      ▼
FastAPI Backend  ──► MySQL Database
      │
      ▼
Zapier AI Agent (Webhook)
      │
      ▼
Multi-Agent Pipeline
  ├── Agent 1: Vision Analysis
  ├── Agent 2: Listing Generation
  ├── Agent 3: Packaging
  ├── Agent 4: Compliance
  ├── Agent 5: Pricing
  ├── Agent 6: Competitor Analysis
  └── Agent 7: Marketing Content
      │
      ▼
PDF Report + CSV Export
```

---

## Tech Stack

| Layer      | Technology                       |
|------------|----------------------------------|
| Frontend   | Streamlit                        |
| Backend    | FastAPI + Uvicorn                |
| AI         | Zapier AI Agent (Webhook)        |
| Database   | MySQL + SQLAlchemy               |
| PDF Export | ReportLab                        |
| CSV Export | Pandas                           |
| Language   | Python 3.10+                     |

---

## Project Structure

```
HackerArena2.0/
├── main.py                        # FastAPI entry point
├── setup_db.py                    # One-time DB setup
├── requirements.txt
├── .env                           # Environment variables
├── start_backend.bat              # Windows: start backend
├── start_frontend.bat             # Windows: start frontend
│
├── backend/
│   ├── database.py                # SQLAlchemy models + DB config
│   ├── agents/
│   │   ├── zapier_client.py       # Zapier webhook integration
│   │   └── mock_agent.py          # Fallback demo data
│   ├── models/
│   │   └── schemas.py             # Pydantic request/response models
│   ├── routes/
│   │   └── api.py                 # FastAPI route handlers
│   └── utils/
│       ├── csv_exporter.py        # CSV + marketplace CSV generation
│       └── pdf_generator.py       # PDF report generation
│
├── frontend/
│   └── app.py                     # Streamlit dashboard
│
└── exports/
    ├── pdfs/                      # Generated PDF reports
    └── csv/                       # Generated CSV exports
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Edit `.env`:

```env
ZAPIER_WEBHOOK_URL=https://hooks.zapier.com/hooks/catch/YOUR_ID/
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=product_launch_studio
```

> **Note:** If `ZAPIER_WEBHOOK_URL` is not set or left as placeholder, the app automatically uses built-in mock data so you can demo the full UI immediately.

### 3. Set up the database

```bash
python setup_db.py
```

### 4. Start the backend

```bash
# Option A: batch file
start_backend.bat

# Option B: manual
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Start the frontend

```bash
# Option A: batch file
start_frontend.bat

# Option B: manual
streamlit run frontend/app.py --server.port 8501
```

### 6. Open in browser

- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

---

## API Endpoints

| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| POST   | /api/v1/analyze                 | Upload image, run full AI analysis   |
| POST   | /api/v1/export-csv/{id}         | Generate & download master CSV       |
| POST   | /api/v1/generate-pdf/{id}       | Generate & download PDF report       |
| GET    | /api/v1/history                 | List all previous analyses           |
| GET    | /api/v1/analysis/{id}           | Fetch a specific analysis by ID      |

---

## Zapier Setup

1. Create a new Zap in Zapier
2. Trigger: **Webhooks by Zapier → Catch Hook**
3. Add your AI Agent action steps (one per agent)
4. Return JSON response via the webhook
5. Copy your webhook URL into `.env`

### Expected Zapier Response Format

```json
{
  "vision_analysis": { ... },
  "listing": { ... },
  "packaging": { ... },
  "compliance": { ... },
  "pricing": { ... },
  "competitor_analysis": { ... },
  "marketing_content": { ... }
}
```

---

## Export Outputs

| Format | Contents                                               |
|--------|--------------------------------------------------------|
| PDF    | Full professional report with all 7 agent outputs      |
| CSV    | Master spreadsheet + 4 marketplace-specific CSVs       |
| JSON   | Raw structured JSON downloadable from the dashboard    |

Marketplace CSVs are optimized for:
- **Amazon** — ASIN, fulfillment type, bullet points, search terms
- **Flipkart** — Listing ID, HSN code, GST%, product highlights
- **Meesho** — MRP, tags, product highlights
- **Shopify** — Handle, SEO title, SEO description, compare-at price

---

## Dashboard Sections

1. 📸 Product Image Upload & Preview
2. 🔍 Vision Analysis (with confidence bar)
3. 📝 SEO Listing Generation
4. 📦 Packaging Suggestions
5. ⚖️ Compliance Report (BIS, FSSAI, Barcode, MRP)
6. 💰 Pricing Cards (Budget / Recommended / Premium)
7. 📊 Competitor Analysis
8. 📣 Marketing Content (Instagram, Facebook, WhatsApp, Email)
9. 📤 Export Center (PDF, CSV, JSON)
