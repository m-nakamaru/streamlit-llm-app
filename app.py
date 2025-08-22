# --- app.py の先頭に ---
import os, streamlit as st
if "OPENAI_API_KEY" in st.secrets and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass
# -----------------------