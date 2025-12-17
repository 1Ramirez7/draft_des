"""
documentation.py
----------------
Documentation page displaying model architecture, development, and mathematical specification.
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import re

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

# Files that contain mermaid diagrams
MERMAID_FILES = {"flowchart.md", "uml-classes.md"}

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


def render_mermaid(mermaid_code: str, height: int = 500) -> None:
    """Render a mermaid diagram using the Mermaid JS library."""
    html_content = f"""
    <div class="mermaid" style="background-color: white; padding: 10px; border-radius: 5px;">
        {mermaid_code}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
    """
    components.html(html_content, height=height, scrolling=True)


def render_markdown_with_mermaid(content: str) -> None:
    """
    Render markdown content, handling mermaid code blocks separately.
    Splits content at mermaid blocks and renders each section appropriately.
    """
    # Pattern to match mermaid code blocks
    mermaid_pattern = r'```mermaid\s*([\s\S]*?)```'
    
    # Split content by mermaid blocks, keeping the mermaid code
    parts = re.split(mermaid_pattern, content)
    
    # parts will alternate: [markdown, mermaid_code, markdown, mermaid_code, ...]
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Regular markdown content
            if part.strip():
                st.markdown(part)
        else:
            # Mermaid code block
            # Estimate height based on content complexity
            line_count = part.count('\n') + 1
            height = min(max(300, line_count * 25), 800)
            render_mermaid(part.strip(), height=height)


# Create tabs for each document
tabs = st.tabs(list(docs.keys()))

for tab, (title, filename) in zip(tabs, docs.items()):
    with tab:
        doc_path = DOCS_DIR / filename
        if doc_path.exists():
            content = doc_path.read_text(encoding="utf-8")
            # Use mermaid renderer for files with mermaid diagrams
            if filename in MERMAID_FILES:
                render_markdown_with_mermaid(content)
            else:
                st.markdown(content)
        else:
            st.error(f"Documentation file not found: {filename}")

st.markdown("---")
st.page_link("main.py", label="← Back to Home", icon="🏠")