import json
import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.database import get_db, ProductAnalysis
from backend.agents.zapier_client import call_zapier_agent
from backend.agents.mock_agent import get_mock_analysis
from backend.utils.csv_exporter import generate_csv, generate_marketplace_csvs
from backend.utils.pdf_generator import generate_pdf
from backend.models.schemas import (
    ProductAnalysisResponse, HistoryItem,
    VisionAnalysis, Listing, Packaging, Compliance, Pricing,
    CompetitorAnalysis, MarketingContent,
)

router = APIRouter()

ZAPIER_URL = os.getenv("ZAPIER_WEBHOOK_URL", "")


@router.post("/analyze", response_model=ProductAnalysisResponse)
async def analyze_product(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = await file.read()

    # Use Zapier if configured, else fall back to mock
    if ZAPIER_URL and ZAPIER_URL.startswith("https://hooks.zapier.com"):
        analysis = await call_zapier_agent(image_bytes, file.filename)
    else:
        analysis = get_mock_analysis(file.filename)

    va = analysis.get("vision_analysis", {})

    record = ProductAnalysis(
        image_filename=file.filename,
        product_name=va.get("product_name", ""),
        product_category=va.get("product_category", ""),
        confidence_score=va.get("confidence_score", 0.0),
        vision_analysis=json.dumps(va),
        listing=json.dumps(analysis.get("listing", {})),
        packaging=json.dumps(analysis.get("packaging", {})),
        compliance=json.dumps(analysis.get("compliance", {})),
        pricing=json.dumps(analysis.get("pricing", {})),
        competitor_analysis=json.dumps(analysis.get("competitor_analysis", {})),
        marketing_content=json.dumps(analysis.get("marketing_content", {})),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # Auto-generate PDF and CSV
    try:
        pdf_path = generate_pdf(analysis, record.id)
        csv_path = generate_csv(analysis, record.id)
        record.pdf_path = pdf_path
        record.csv_path = csv_path
        db.commit()
        db.refresh(record)
    except Exception:
        pass

    return _to_response(record)


@router.post("/export-csv/{record_id}")
def export_csv(record_id: int, db: Session = Depends(get_db)):
    record = _get_record(db, record_id)
    analysis = _parse_record(record)

    paths = generate_marketplace_csvs(analysis, record_id)
    # Return the combined CSV for simplicity; marketplace CSVs are saved to disk
    csv_path = generate_csv(analysis, record_id)
    record.csv_path = csv_path
    db.commit()

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    return FileResponse(csv_path, media_type="text/csv",
                        filename=f"product_analysis_{record_id}.csv")


@router.post("/generate-pdf/{record_id}")
def export_pdf(record_id: int, db: Session = Depends(get_db)):
    record = _get_record(db, record_id)
    analysis = _parse_record(record)

    pdf_path = generate_pdf(analysis, record_id)
    record.pdf_path = pdf_path
    db.commit()

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    return FileResponse(pdf_path, media_type="application/pdf",
                        filename=f"product_report_{record_id}.pdf")


@router.get("/history")
def get_history(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    records = db.query(ProductAnalysis).order_by(
        ProductAnalysis.created_at.desc()).offset(skip).limit(limit).all()
    return [HistoryItem(
        id=r.id,
        image_filename=r.image_filename,
        product_name=r.product_name,
        product_category=r.product_category,
        confidence_score=r.confidence_score,
        pdf_path=r.pdf_path,
        csv_path=r.csv_path,
        created_at=r.created_at,
    ) for r in records]


@router.get("/analysis/{record_id}", response_model=ProductAnalysisResponse)
def get_analysis(record_id: int, db: Session = Depends(get_db)):
    return _to_response(_get_record(db, record_id))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_record(db: Session, record_id: int) -> ProductAnalysis:
    record = db.query(ProductAnalysis).filter(ProductAnalysis.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return record


def _parse_record(record: ProductAnalysis) -> dict:
    def _j(val):
        try:
            return json.loads(val) if val else {}
        except Exception:
            return {}

    return {
        "vision_analysis": _j(record.vision_analysis),
        "listing": _j(record.listing),
        "packaging": _j(record.packaging),
        "compliance": _j(record.compliance),
        "pricing": _j(record.pricing),
        "competitor_analysis": _j(record.competitor_analysis),
        "marketing_content": _j(record.marketing_content),
    }


def _to_response(record: ProductAnalysis) -> ProductAnalysisResponse:
    def _j(val):
        try:
            return json.loads(val) if val else {}
        except Exception:
            return {}

    def _safe(model, val):
        try:
            d = _j(val)
            return model(**d) if d else None
        except Exception:
            return model()

    return ProductAnalysisResponse(
        id=record.id,
        image_filename=record.image_filename,
        vision_analysis=_safe(VisionAnalysis, record.vision_analysis),
        listing=_safe(Listing, record.listing),
        packaging=_safe(Packaging, record.packaging),
        compliance=_safe(Compliance, record.compliance),
        pricing=_safe(Pricing, record.pricing),
        competitor_analysis=_safe(CompetitorAnalysis, record.competitor_analysis),
        marketing_content=_safe(MarketingContent, record.marketing_content),
        pdf_path=record.pdf_path,
        csv_path=record.csv_path,
        created_at=record.created_at,
    )
