import os, sys, streamlit as st

st.title("Streamlit Cloud Smoke Test")
st.write(f"Python: {sys.version}")
st.write("OPENAI_API_KEY present:",
         bool(os.getenv("OPENAI_API_KEY")) or ("OPENAI_API_KEY" in st.secrets))
st.success("If you see this page, deploy succeeded.")