"""Quick smoke test — run: python test_gen.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from backend.agents.mock_agent import get_mock_analysis
from backend.utils.pdf_generator import generate_pdf
from backend.utils.csv_exporter import generate_csv, generate_marketplace_csvs

data = get_mock_analysis("wireless_earbuds.jpg")

pdf = generate_pdf(data, 999)
csv = generate_csv(data, 999)
mp  = generate_marketplace_csvs(data, 999)

print(f"PDF : {pdf}  | exists={os.path.exists(pdf)}")
print(f"CSV : {csv}  | exists={os.path.exists(csv)}")
print(f"Marketplace CSVs: {list(mp.keys())}")
print("\nAll exports generated successfully!")
