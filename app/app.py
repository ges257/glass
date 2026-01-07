"""
GLASS Demo - Human-in-the-Loop Column Refinement

This demo shows the core concept of GLASS:
1. System proposes column boundaries
2. User refines via drag-and-drop
3. Template saved for reuse on similar documents
"""

import json
import streamlit as st
from PIL import Image
from pathlib import Path
from streamlit_image_annotation import detection

# Import overlay utilities
from overlay_utils import draw_column_overlay, create_column_annotations, annotations_to_template

# Page config
st.set_page_config(
    page_title="GLASS Demo",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0D1B2A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .info-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #A78BFA;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .column-tag {
        display: inline-block;
        background: #A78BFA;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">GLASS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Geometric Layout Analysis & Structuring System</p>', unsafe_allow_html=True)

# Description
st.markdown("""
<div class="info-box">
<strong>How it works:</strong> The system proposes column boundaries based on document structure.
You refine them by dragging the edges. The template is then saved for zero-cost extraction on similar documents.
</div>
""", unsafe_allow_html=True)

# Load sample data
DATA_DIR = Path(__file__).parent.parent / "data"
SAMPLE_IMAGE = DATA_DIR / "sample_page.png"
SAMPLE_TEMPLATE = DATA_DIR / "sample_template.json"

# Initialize session state
if 'template' not in st.session_state:
    with open(SAMPLE_TEMPLATE) as f:
        st.session_state.template = json.load(f)

if 'adjustments_made' not in st.session_state:
    st.session_state.adjustments_made = 0

# Load image
image = Image.open(SAMPLE_IMAGE)
img_width, img_height = image.size

# Create two columns layout
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### Current Template")
    st.markdown(f"**Document:** {st.session_state.template['document_type']}")
    st.markdown(f"**Columns:** {len(st.session_state.template['columns'])}")

    st.markdown("---")
    st.markdown("**Column Layout:**")

    for col in st.session_state.template['columns']:
        st.markdown(
            f'<span class="column-tag">{col["name"]}</span>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    if st.session_state.adjustments_made > 0:
        st.success(f"Template updated ({st.session_state.adjustments_made} adjustments)")

    # Download button for template
    template_json = json.dumps(st.session_state.template, indent=2)
    st.download_button(
        label="Download Template",
        data=template_json,
        file_name="extraction_template.json",
        mime="application/json"
    )

    st.markdown("---")
    st.markdown("### Instructions")
    st.markdown("""
    1. **Drag** column edges to adjust boundaries
    2. **Click** a column to see its properties
    3. **Download** the template when satisfied

    The saved template can extract data from similar documents automatically.
    """)

with col1:
    st.markdown("### Document View")
    st.caption("Drag column boundaries to refine extraction regions")

    # Create annotations for the detection component
    annotations = create_column_annotations(
        st.session_state.template['columns'],
        img_width,
        img_height
    )

    # Get unique labels for the annotation component
    labels = [col['name'] for col in st.session_state.template['columns']]

    # Use streamlit-image-annotation for interactive editing
    result = detection(
        image_path=str(SAMPLE_IMAGE),
        bboxes=annotations,
        labels=labels,
        key="column_annotator"
    )

    # Update template if annotations changed
    if result is not None and len(result) > 0:
        new_columns = annotations_to_template(
            result,
            img_width,
            st.session_state.template['columns']
        )

        # Check if anything changed
        old_bounds = [(c['x_start'], c['x_end']) for c in st.session_state.template['columns']]
        new_bounds = [(c['x_start'], c['x_end']) for c in new_columns]

        if old_bounds != new_bounds:
            st.session_state.template['columns'] = new_columns
            st.session_state.adjustments_made += 1
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9CA3AF; font-size: 0.85rem;">
    <strong>GLASS Demo</strong> | Human-in-the-Loop PDF Table Extraction<br>
    This demo shows column refinement only. Production system includes VLM-based proposal generation and validation gates.
</div>
""", unsafe_allow_html=True)
