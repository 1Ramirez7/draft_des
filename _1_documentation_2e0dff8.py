"""
documentation.py
----------------
Documentation page displaying model architecture, development, and mathematical specification.
"""
import streamlit as st
from pathlib import Path
import base64

st.set_page_config(
    page_title="Documentation - DES",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 Documentation")
st.markdown("---")

# Define the docs to display
DOCS_DIR = Path(__file__).parent.parent / "docs"

docs = {
    "User Guide": "user-guide.md",
    "Variable Reference": "VARIABLE_REFERENCE.md",
    "Architecture": "architecture.md",
    "Development": "development.md",
    "Event Types": "event_type.md",
    "Flowchart": "flowchart.pdf",
    "Mathematical Specification": "mathematical-specification.md",
    "Simulation Methodology": "simulation-methodology.md",
    "UML Classes": "uml-classes.md",
}

# Create tabs for each document
tabs = st.tabs(list(docs.keys()))

for tab, (title, filename) in zip(tabs, docs.items()):
    with tab:
        doc_path = DOCS_DIR / filename
        if doc_path.exists():
            # Handle PDF files differently from markdown files
            if filename.endswith('.pdf'):
                # Read PDF as binary and display in iframe
                with open(doc_path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                # Display markdown files
                content = doc_path.read_text(encoding="utf-8")
                st.markdown(content)
        else:
            st.error(f"Documentation file not found: {filename}")

st.markdown("---")
st.page_link("main.py", label="← Back to Home", icon="🏠")
