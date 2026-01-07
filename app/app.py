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
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0D1B2A;
        background: linear-gradient(90deg, #0D1B2A 0%, #1a2d42 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #A78BFA;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .info-box {
        background: linear-gradient(135deg, #0D1B2A08 0%, #A78BFA15 100%);
        border-left: 4px solid #A78BFA;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #A78BFA;
        color: white;
        border: none;
        border-radius: 6px;
    }
    .stButton > button:hover {
        background-color: #9061F9;
    }
    h3 { color: #0D1B2A; }
    .stDownloadButton > button {
        background-color: #0D1B2A;
        color: white;
    }
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

# Table region
Y_START_PCT = 0.18
Y_END_PCT = 0.95

# Convert template to bboxes (v10 format)
def template_to_bboxes(template, img_w, img_h):
    """Convert to [[x, y, w, h], ...] format."""
    bboxes = []
    label_list = []

    y = int(Y_START_PCT * img_h)
    h = int((Y_END_PCT - Y_START_PCT) * img_h)

    for col in template['columns']:
        x_start = col['x_start']
        x_end = col['x_end']

        x = int(x_start * img_w)
        w = int((x_end - x_start) * img_w)

        bboxes.append([x, y, w, h])
        label_list.append(col['name'])

    return bboxes, label_list

# Convert back
def bboxes_to_template(result, img_w, original_template):
    """Convert result back to template format."""
    new_template = original_template.copy()
    new_columns = []

    orig_cols = {c['name']: c for c in original_template['columns']}

    for i, item in enumerate(result):
        bbox = item['bbox']
        label = item.get('label', f'Column_{i}')

        x, y, w, h = bbox
        x_start = x / img_w
        x_end = (x + w) / img_w

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

    # Save temp image
    temp_path = "/tmp/glass_demo.png"
    image.save(temp_path)

    # Get bboxes
    bboxes, label_list = template_to_bboxes(st.session_state.template, img_width, img_height)
    labels = list(range(len(label_list)))  # Integer indices

    # Detection component (v10 format)
    result = detection(
        image_path=temp_path,
        label_list=label_list,
        bboxes=bboxes,
        labels=labels,
        height=img_height,
        width=img_width
    )

    # Update if changed
    if result and len(result) > 0:
        new_template = bboxes_to_template(result, img_width, st.session_state.template)
        if new_template['columns'] != st.session_state.template['columns']:
            st.session_state.template = new_template
            st.rerun()

# Footer
st.markdown("---")
st.caption("GLASS Demo | Human-in-the-Loop PDF Table Extraction")
