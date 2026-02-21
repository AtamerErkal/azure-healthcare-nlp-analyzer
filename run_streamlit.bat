@echo off
REM Run Streamlit using current Python (avoids broken launcher when streamlit.exe points to wrong Python)
python -m streamlit run ui/streamlit_demo_v1.py %*
