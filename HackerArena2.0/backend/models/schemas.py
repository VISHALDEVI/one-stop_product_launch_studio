from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class VisionAnalysis(BaseModel):
    product_name: str = ""
    product_category: str = ""
    product_type: str = ""
    brand: str = ""
    material: str = ""
    primary_color: str = ""
    secondary_colors: List[str] = []
    estimated_dimensions: Dict[str, Any] = {}
    estimated_weight: Dict[str, Any] = {}
    key_features: List[str] = []
    confidence_score: float = 0.0


class Listing(BaseModel):
    seo_optimized_title: str = ""
    product_description: str = ""
    bullet_points: List[str] = []
    seo_keywords: List[str] = []
    marketplace_category: str = ""
    search_tags: List[str] = []


class Packaging(BaseModel):
    recommended_packaging_type: str = ""
    recommended_box_size: Dict[str, Any] = {}
    protective_material: List[str] = []
    shipping_recommendations: Dict[str, Any] = {}


class Compliance(BaseModel):
    bis_requirement: Dict[str, Any] = {}
    fssai_requirement: Dict[str, Any] = {}
    barcode_requirement: Dict[str, Any] = {}
    mrp_label_requirement: Dict[str, Any] = {}
    product_label_information: Dict[str, Any] = {}


class Pricing(BaseModel):
    low_price: Dict[str, Any] = {}
    recommended_selling_price: Dict[str, Any] = {}
    premium_price: Dict[str, Any] = {}
    pricing_analysis: Dict[str, Any] = {}


class CompetitorAnalysis(BaseModel):
    average_market_price: str = ""
    competitor_count: str = ""
    suggested_improvements: List[str] = []
    market_position: str = ""


class MarketingContent(BaseModel):
    instagram_post: str = ""
    facebook_post: str = ""
    whatsapp_promotion: str = ""
    email_campaign: str = ""


class ProductAnalysisResponse(BaseModel):
    id: Optional[int] = None
    image_filename: str
    vision_analysis: Optional[VisionAnalysis] = None
    listing: Optional[Listing] = None
    packaging: Optional[Packaging] = None
    compliance: Optional[Compliance] = None
    pricing: Optional[Pricing] = None
    competitor_analysis: Optional[CompetitorAnalysis] = None
    marketing_content: Optional[MarketingContent] = None
    pdf_path: Optional[str] = None
    csv_path: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HistoryItem(BaseModel):
    id: int
    image_filename: str
    product_name: Optional[str]
    product_category: Optional[str]
    confidence_score: Optional[float]
    pdf_path: Optional[str]
    csv_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
