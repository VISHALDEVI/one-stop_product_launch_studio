@echo off
echo Starting AI Product Launch Studio Frontend...
cd /d %~dp0
python -m streamlit run frontend/app.py --server.port 8501
pause
