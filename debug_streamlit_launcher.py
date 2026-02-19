"""
One-off diagnostic for Streamlit launcher "Unable to create process" error.
Writes NDJSON to debug-2881c1.log for hypotheses H1–H5.
"""
import os
import sys
import shutil
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug-2881c1.log")
PY312_PYTHON = r"C:\Users\Blue\AppData\Local\Programs\Python\Python312\python.exe"
PY312_STREAMLIT = r"C:\Users\Blue\AppData\Local\Programs\Python\Python312\Scripts\streamlit.exe"

def log(hypothesis_id: str, message: str, data: dict):
    payload = {
        "sessionId": "2881c1",
        "hypothesisId": hypothesis_id,
        "location": "debug_streamlit_launcher.py",
        "message": message,
        "data": data,
        "timestamp": int(datetime.utcnow().timestamp() * 1000),
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write("\n" + __import__("json").dumps(payload))

# H1: Python312 python.exe exists?
log("H1", "Check Python312 python.exe", {"path": PY312_PYTHON, "exists": os.path.isfile(PY312_PYTHON)})

# H2: Python312 Scripts streamlit.exe exists?
log("H2", "Check Python312 streamlit.exe", {"path": PY312_STREAMLIT, "exists": os.path.isfile(PY312_STREAMLIT)})

# H3: Current Python and streamlit resolution
current_python = sys.executable
streamlit_which = shutil.which("streamlit")
log("H3", "Current Python vs streamlit in PATH", {
    "sys.executable": current_python,
    "shutil.which('streamlit')": streamlit_which,
    "same_as_py312": streamlit_which and os.path.normpath(PY312_STREAMLIT) == os.path.normpath(streamlit_which) if streamlit_which else False,
})

# H4: CWD and path with spaces
log("H4", "CWD and path with space", {"cwd": os.getcwd(), "has_space": " " in os.getcwd()})

# H5: Can we import streamlit and where is it?
try:
    import streamlit as st_mod
    st_file = getattr(st_mod, "__file__", None)
    log("H5", "Streamlit import and location", {"streamlit.__file__": st_file, "import_ok": True})
except Exception as e:
    log("H5", "Streamlit import failed", {"error": str(e), "import_ok": False})

# Extra: script dir (for streamlit run path)
log("EXTRA", "Script directory for streamlit run", {"script_dir": os.path.dirname(os.path.abspath(__file__))})
