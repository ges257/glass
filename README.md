![Header](https://capsule-render.vercel.app/api?type=rect&color=0D1B2A&height=120&text=GLASS&fontSize=42&fontColor=A78BFA&fontAlign=50&fontAlignY=50&desc=Geometric%20Layout%20Analysis%20%26%20Structuring%20System&descSize=18&descColor=A3B8CC&descAlign=50&descAlignY=75)

<div align="center">

**VLM/Multimodal Pipeline for PDF Table Extraction**

[![Live Demo (Click Here)](https://img.shields.io/badge/Live_Demo_(Click_Here)-HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=0D1B2A)](https://huggingface.co/spaces/ges257/glass)
[![Paper PDF](https://img.shields.io/badge/Paper-PDF-A78BFA?style=for-the-badge)](assets/GLASS_Final_Report.pdf)

![Python](https://img.shields.io/badge/Python-3.11+-A3B8CC?style=flat-square&logo=python&logoColor=0D1B2A)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-A3B8CC?style=flat-square&logo=streamlit&logoColor=0D1B2A)
![Pillow](https://img.shields.io/badge/Pillow-Imaging-A3B8CC?style=flat-square&logo=python&logoColor=0D1B2A)

</div>

---

## The Problem

Complex PDF layouts in financial reports trap critical data. Standard OCR fails because:

- **Variable table structures** across 14+ vendor layouts
- **Merged cells, multi-line headers, nested tables**
- **No consistent visual patterns** for column boundaries
- **Low-quality scans** with skewed text and artifacts

This is the "trapped data" problem: information exists in PDFs but cannot be reliably extracted.

---

## Results

| Metric | Score | Notes |
|--------|-------|-------|
| **Field-Level Accuracy** | 97% | On complex financial tables |
| **Inference Cost Reduction** | 90% | Via template reuse |
| **Rows Extracted** | 800+ | Across multiple document types |

> **Key Insight:** A reasonable system proposal + easy human adjustment outperforms attempts at fully automated extraction.

---

## Challenges Overcome

| Challenge | Solution |
|-----------|----------|
| **Pixel-Coordinate Fragility** | VLM semantic understanding vs. brittle pixel thresholds |
| **Synthetic ≠ Real Gap** | 98% synthetic accuracy failed on real data → human-in-the-loop |
| **CNN F1 = 0.003** | Replaced learned model with working heuristic |
| **14+ Vendor Layouts** | Template-based extraction with human refinement |
| **Token vs. Structure** | Abandoned token classification for spatial templates |

> See [CHALLENGES.md](CHALLENGES.md) for the full ML journey and lessons learned.

---

## Architecture

```
PDF → VLM Proposal → Human Refinement → Validated Template → Extraction
```

1. **VLM Column Detection**: Vision-Language Model identifies column structure
2. **Heuristic Boundary Detection**: X-histogram analysis proposes boundaries
3. **Human-in-the-Loop Refinement**: Streamlit overlay for drag-to-adjust
4. **Validation Gates**: Date, Currency, Alignment, CrossFoot checks
5. **Template Reuse**: Save template for zero-cost extraction on similar docs

See [ARCHITECTURE.md](ARCHITECTURE.md) for system diagrams.

---

## Key Innovation: Human-in-the-Loop Templates

Instead of attempting fully automated extraction (which fails on edge cases), GLASS uses a hybrid approach:

```
System Proposes → Human Refines → Template Saved → Reuse at Zero Cost
```

- **First document**: System proposes column boundaries, user adjusts
- **Subsequent documents**: Template applies automatically
- **Result**: 90% reduction in per-document processing cost

This design acknowledges that **100% automation is impossible** for complex layouts, but **95% automation + 5% human guidance** is achievable and practical.

---

## Repository Structure

```
glass/
├── app/
│   ├── app.py              # Streamlit demo
│   └── overlay_utils.py    # Column overlay rendering
├── data/
│   ├── sample_page.png     # Pre-rendered PDF page
│   └── sample_template.json # Column template
├── assets/
│   └── architecture.png    # System diagram
├── README.md
├── CHALLENGES.md           # ML journey and failures
├── ARCHITECTURE.md         # System design
└── LEARNINGS.md            # Design decisions
```

---

## Try the Demo

**[Live Demo on HuggingFace Spaces](https://huggingface.co/spaces/ges257/glass)**

Or run locally:

```bash
git clone https://github.com/ges257/glass.git
cd glass
pip install -r requirements.txt
cd app && streamlit run app.py
```

---

## What's NOT in This Demo

This public demo shows the **human-in-the-loop refinement concept** only.

Not included (proprietary):
- VLM-based column detection logic
- Boundary detection algorithms
- Validation gate implementations
- Multi-voter ensemble architecture
- Full coordinate canonicalization system

The demo uses a pre-generated template and sample page to demonstrate the adjustment interface.

---

## Technical Stack

- **VLM/Multimodal**: Vision-Language Model for semantic understanding
- **UI**: Streamlit + streamlit-image-annotation
- **Imaging**: Pillow, pdf2image
- **Validation**: Rule-based heuristic gates (Date, Currency, Alignment, CrossFoot)

---

## Author

**Gregory E. Schwartz**
- M.S. Artificial Intelligence (Yeshiva University)
- MBA (Cornell University)

---

![Footer](https://capsule-render.vercel.app/api?type=rect&color=0D1B2A&height=30&section=footer)
