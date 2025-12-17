"""
documentation.py
----------------
Documentation page displaying model architecture, development, and mathematical specification.
"""
import streamlit as st
from pathlib import Path
import base64
import requests
import re
import streamlit.components.v1 as components

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
    "Flowchart": "flowchart.md",
    "Mathematical Specification": "mathematical-specification.md",
    "Simulation Methodology": "simulation-methodology.md",
    "UML Classes": "uml-classes.md",
}

def render_mermaid(mermaid_code):
    """Render a mermaid diagram using HTML/JS"""
    html_code = f"""
    <div class="mermaid" style="background-color: white; padding: 20px; border-radius: 5px;">
        {mermaid_code}
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    """
    components.html(html_code, height=600, scrolling=True)

def process_markdown_with_mermaid(content):
    """Process markdown content and render mermaid diagrams separately"""
    # Split content by mermaid blocks
    mermaid_pattern = r'```mermaid\n(.*?)```'
    parts = re.split(mermaid_pattern, content, flags=re.DOTALL)
    
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Regular markdown content
            if part.strip():
                st.markdown(part)
        else:
            # Mermaid diagram
            render_mermaid(part)

# Create tabs for each document
tabs = st.tabs(list(docs.keys()))

for tab, (title, filename) in zip(tabs, docs.items()):
    with tab:
        doc_path = DOCS_DIR / filename
        
        # Handle files with mermaid diagrams
        if filename in ["flowchart.md", "uml-classes.md"] and doc_path.exists():
            content = doc_path.read_text(encoding="utf-8")
            process_markdown_with_mermaid(content)
        elif doc_path.exists():
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

# this file is same as last push "testing pdf bug:" 7730c6e 
# this one just includes the uml file as well. 
# no other differences