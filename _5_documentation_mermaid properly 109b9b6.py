"""
documentation.py
----------------
Documentation page displaying model architecture, development, and mathematical specification.
"""
import streamlit as st
from pathlib import Path
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
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
    </head>
    <body style="margin: 0; padding: 0;">
        <div class="mermaid">
{mermaid_code}
        </div>
    </body>
    </html>
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
        if filename in ["flowchart.md", "uml-classes.md"]:
            content = doc_path.read_text(encoding="utf-8")
            process_markdown_with_mermaid(content)
        else:
            # Handle regular markdown files
            content = doc_path.read_text(encoding="utf-8")
            st.markdown(content)

st.markdown("---")
st.page_link("main.py", label="← Back to Home", icon="🏠")


# this is the file where i start to remove the pdf checking
# realize erros happen before this push so then doing this prechecking im doing now
# is not working out because i thought code properly work before i started removing pdf checking