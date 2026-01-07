"""
GLASS Demo - Human-in-the-Loop Column Refinement

Based on v10 interactive overlay system.
"""

import json
import streamlit as st
from PIL import Image
from pathlib import Path
from streamlit_image_annotation import detection

# Page config
st.set_page_config(
    page_title="GLASS Demo",
    page_icon=":",
    layout="wide"
)

# Custom CSS - Design System: Navy #0D1B2A, Purple #A78BFA
# Force light mode and mobile-friendly styling
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff !important;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #0D1B2A !important;
    }
    .sub-header {
        font-size: 1rem;
        color: #A78BFA !important;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .info-box {
        background-color: #f8f9fa !important;
        border-left: 4px solid #A78BFA;
        padding: 0.75rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        color: #0D1B2A !important;
    }
    h3 { color: #0D1B2A !important; }
    p, span, div { color: #0D1B2A; }
    .stMarkdown { color: #0D1B2A !important; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">GLASS</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Geometric Layout Analysis & Structuring System</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<strong>How it works:</strong> The system proposes column boundaries.
Drag boxes to adjust. Template saved for zero-cost extraction on similar documents.
</div>
""", unsafe_allow_html=True)

# Load data
DATA_DIR = Path(__file__).parent.parent / "data"
SAMPLE_IMAGE = DATA_DIR / "sample_page.png"
SAMPLE_TEMPLATE = DATA_DIR / "sample_template.json"

# Initialize
if 'template' not in st.session_state:
    with open(SAMPLE_TEMPLATE) as f:
        st.session_state.template = json.load(f)

# Load image
image = Image.open(SAMPLE_IMAGE)
img_width, img_height = image.size

# Scale for display
DISPLAY_SCALE = 0.50
display_width = int(img_width * DISPLAY_SCALE)
display_height = int(img_height * DISPLAY_SCALE)

# Table region
Y_START_PCT = 0.18
Y_END_PCT = 0.95

# Convert template to bboxes (v10 format) - uses display dimensions
def template_to_bboxes(template, disp_w, disp_h):
    """Convert to [[x, y, w, h], ...] format for display size."""
    bboxes = []
    label_list = []

    y = int(Y_START_PCT * disp_h)
    h = int((Y_END_PCT - Y_START_PCT) * disp_h)

    for col in template['columns']:
        x_start = col['x_start']
        x_end = col['x_end']

        # Calculate full width then reduce for less intrusive display
        full_w = (x_end - x_start) * disp_w
        w = int(full_w * 0.53)  # 53% of original width
        # Center the narrower box within the column
        x = int(x_start * disp_w + full_w * 0.235)

        bboxes.append([x, y, w, h])
        label_list.append(col['name'])

    return bboxes, label_list

# Convert back - uses display width for normalization
def bboxes_to_template(result, disp_w, original_template):
    """Convert result back to template format."""
    new_template = original_template.copy()
    new_columns = []

    orig_cols = {c['name']: c for c in original_template['columns']}

    for i, item in enumerate(result):
        bbox = item['bbox']
        label = item.get('label', f'Column_{i}')

        x, y, w, h = bbox
        x_start = x / disp_w
        x_end = (x + w) / disp_w

        orig = orig_cols.get(label, {})
        new_columns.append({
            'name': label,
            'x_start': round(x_start, 3),
            'x_end': round(x_end, 3),
            'data_type': orig.get('data_type', 'text')
        })

    new_columns.sort(key=lambda c: c['x_start'])
    new_template['columns'] = new_columns
    return new_template

# Layout
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### Columns")
    for col in st.session_state.template['columns']:
        st.write(f"**{col['name']}**: {col['x_start']:.0%} - {col['x_end']:.0%}")

    st.markdown("---")
    template_json = json.dumps(st.session_state.template, indent=2)
    st.download_button("Download Template", template_json, "template.json", "application/json")

with col1:
    st.markdown("### Document View")
    st.caption("Drag column boundaries to adjust")

    # Resize image for display
    display_image = image.resize((display_width, display_height))
    temp_path = "/tmp/glass_demo.png"
    display_image.save(temp_path)

    # Get bboxes using display dimensions
    bboxes, label_list = template_to_bboxes(st.session_state.template, display_width, display_height)
    # Add dummy labels to access more colors in palette, then use specific indices
    # to avoid duplicate colors (library has ~10 color palette)
    extended_labels = label_list + ["_d1", "_d2", "_d3", "_d4", "_d5"]
    # Map columns to different color slots: skip indices to get distinct colors
    labels = [0, 1, 3, 4, 6, 7, 9, 10, 12]  # 9 columns mapped to spread-out colors

    # Detection component (v10 format) with display dimensions
    result = detection(
        image_path=temp_path,
        label_list=extended_labels,
        bboxes=bboxes,
        labels=labels,
        height=display_height,
        width=display_width,
        line_width=2
    )

    # Update if changed
    if result and len(result) > 0:
        new_template = bboxes_to_template(result, display_width, st.session_state.template)
        if new_template['columns'] != st.session_state.template['columns']:
            st.session_state.template = new_template
            st.rerun()

# Footer
st.markdown("---")
st.caption("GLASS Demo | Human-in-the-Loop PDF Table Extraction")
