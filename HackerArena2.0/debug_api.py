import traceback, json, sys
sys.stdout.reconfigure(encoding='utf-8')

from backend.routes.api import _to_response
from backend.database import get_db, ProductAnalysis, create_tables
from backend.agents.mock_agent import get_mock_analysis

create_tables()
data = get_mock_analysis('test.jpg')
va = data.get('vision_analysis', {})
print("Mock data keys:", list(data.keys()))
print("VA confidence_score:", va.get('confidence_score'), type(va.get('confidence_score')))

db = next(get_db())
record = ProductAnalysis(
    image_filename='test.jpg',
    product_name=va.get('product_name', ''),
    product_category=va.get('product_category', ''),
    confidence_score=va.get('confidence_score', 0.0),
    vision_analysis=json.dumps(va),
    listing=json.dumps(data.get('listing', {})),
    packaging=json.dumps(data.get('packaging', {})),
    compliance=json.dumps(data.get('compliance', {})),
    pricing=json.dumps(data.get('pricing', {})),
    competitor_analysis=json.dumps(data.get('competitor_analysis', {})),
    marketing_content=json.dumps(data.get('marketing_content', {})),
)
db.add(record)
db.commit()
db.refresh(record)
print("DB record ID:", record.id)

try:
    resp = _to_response(record)
    print("_to_response OK, id:", resp.id)
except Exception:
    traceback.print_exc()

db.close()
