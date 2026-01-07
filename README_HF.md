---
title: GLASS
emoji: 🔍
colorFrom: indigo
colorTo: purple
sdk: streamlit
sdk_version: 1.29.0
app_file: app/app.py
pinned: false
license: mit
---

# GLASS - Geometric Layout Analysis & Structuring System

**VLM/Multimodal Pipeline for PDF Table Extraction**

## Demo

This demo shows the **human-in-the-loop refinement concept** of GLASS:

1. **System proposes** column boundaries based on document structure
2. **User refines** by dragging column edges
3. **Template saved** for zero-cost extraction on similar documents

## How to Use

1. View the pre-loaded document page
2. See the proposed column boundaries (purple overlays)
3. Drag column edges to adjust boundaries
4. Download the refined template

## Results

| Metric | Score |
|--------|-------|
| **Field-Level Accuracy** | 97% |
| **Inference Cost Reduction** | 90% |
| **Rows Extracted** | 800+ |

## What's NOT Included

This demo shows column refinement only. Not included:
- VLM-based column detection
- Boundary detection algorithms
- Validation gates
- Full extraction pipeline

## Learn More

- [GitHub Repository](https://github.com/ges257/glass)
- [Challenges Overcome](https://github.com/ges257/glass/blob/main/CHALLENGES.md)
- [Architecture](https://github.com/ges257/glass/blob/main/ARCHITECTURE.md)

---

**Author:** Gregory E. Schwartz
M.S. Artificial Intelligence (Yeshiva University) | MBA (Cornell University)
