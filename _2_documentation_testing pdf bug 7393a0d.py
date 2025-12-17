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
                # Quick test: embed the PDF from the public GitHub raw URL in an iframe.
                # Use the repository raw URL for the flowchart (user-provided).
                if filename == 'flowchart.pdf':
                    # Raw URL (pinned to the commit the user supplied)
                    pdf_url = (
                        "https://raw.githubusercontent.com/1Ramirez7/draft_des/"
                        "2e0dff8f22a5450e08dcfd3d1a87594933c5af13/docs/flowchart.pdf"
                    )
                    try:
                        import streamlit.components.v1 as components

                        components.iframe(pdf_url, width=1000, height=800)
                    except Exception:
                        # Fallback to download button if embedding fails on runtime
                        with open(doc_path, "rb") as f:
                            pdf_bytes = f.read()

                        st.download_button(
                            label=f"Download {filename}",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                        )
                        st.markdown(
                            "Could not embed PDF via iframe — use the download button above.",
                        )
                else:
                    # Non-flowchart PDFs: provide a download button (reliable)
                    with open(doc_path, "rb") as f:
                        pdf_bytes = f.read()

                    st.download_button(
                        label=f"Download {filename}",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf",
                    )
            else:
                # Display markdown files
                content = doc_path.read_text(encoding="utf-8")
                st.markdown(content)
        else:
            st.error(f"Documentation file not found: {filename}")

st.markdown("---")
st.page_link("main.py", label="← Back to Home", icon="🏠")


# this file just downloads a pdf copy of the flowcharts, no visual