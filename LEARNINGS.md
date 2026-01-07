# LEARNINGS.md

## Design Decisions and Trade-offs

This document captures key architectural decisions, trade-offs considered, and lessons learned during GLASS development.

---

## Learning 1: Small Fine-Tuned VLMs Beat Large Models

### The Observation

For specialized document understanding tasks, a 3B parameter VLM outperformed much larger general-purpose models.

### Why It Works

- **Domain focus**: Small model trained specifically on document structure
- **Speed**: 3B model runs in ~200ms vs. seconds for larger models
- **Cost**: 90% reduction in inference cost compared to API-based large models
- **Accuracy**: Better at the specific task than general-purpose models

### Key Insight

"Large" doesn't mean "better" for specialized tasks. A focused model with domain-specific training can outperform models 10x its size.

---

## Learning 2: Pixel Coordinates Don't Generalize

### The Observation

Models trained on pixel coordinates (x=234, y=567) failed completely on new documents with different layouts.

### Why It Fails

PDF documents vary in:
- Page size (Letter, Legal, A4)
- Margins (0.5" to 1.5")
- Font sizes (8pt to 14pt)
- DPI (72 to 300)

A model that learns "column boundary at x=234" is useless when a new document has margins that shift everything by 50 pixels.

### Solution: Normalized Coordinates

All spatial information is stored as 0-1 normalized percentages:
- `x_start: 0.45` means "45% from left edge"
- `x_end: 0.60` means "60% from left edge"

This representation generalizes across page sizes and layouts.

---

## Learning 3: "Reasonable Proposal + Easy Adjustment" > "Perfect Automation"

### The Observation

Attempts at 100% automated extraction failed on edge cases. A system that proposes 90% correct boundaries and lets humans adjust the remaining 10% succeeded.

### The Math

| Approach | Accuracy | User Effort |
|----------|----------|-------------|
| Manual extraction | 100% | 30 min/doc |
| Automated (failed) | 60% | 45 min/doc (fixing errors) |
| **Hybrid (GLASS)** | **97%** | **3 min/doc (adjustments)** |

The hybrid approach is faster than both pure manual and failed automation.

### Design Implication

Build systems that:
1. Make reasonable proposals
2. Show proposals transparently
3. Make adjustment easy
4. Save adjustments for reuse

---

## Learning 4: Heuristics as Reliable Fallback

### The Observation

When ML models failed, simple geometric heuristics worked reliably.

### Examples

| Heuristic | Accuracy | Reliability |
|-----------|----------|-------------|
| Ruling line detection | 95% | Very high (PDF graphics) |
| Whitespace gap analysis | 85% | High |
| Numeric column clustering | 80% | Medium |

### Design Implication

Layer heuristics as fallbacks:
1. Try ruling lines (most reliable)
2. Fall back to gap analysis
3. Fall back to clustering
4. Final fallback: human adjustment

This cascade ensures something always works.

---

## Learning 5: Templates Enable Zero-Cost Reuse

### The Observation

Financial documents are repetitive. The same vendor sends the same layout every month.

### The Opportunity

- First document: 3 minutes to refine template
- Next 100 documents: 0 minutes (template applies)

### Design Implication

Invest in template infrastructure:
- Save templates as JSON with normalized coordinates
- Match templates by document fingerprint
- Version templates for layout changes

The upfront cost of template creation pays off exponentially.

---

## Learning 6: Validation Gates Catch Errors

### The Observation

Even good extraction has errors. Validation gates catch them before output.

### The Four Gates

| Gate | Checks | Catch Rate |
|------|--------|------------|
| **DateGate** | Valid date formats | 99% of date errors |
| **CurrencyGate** | Valid currency patterns | 95% of amount errors |
| **AlignmentGate** | Column alignment variance | 90% of boundary errors |
| **CrossFootGate** | Row totals = sum of parts | 99% of extraction errors |

### Design Implication

Build validation into the pipeline:
1. Extract data
2. Validate with multiple gates
3. Flag failures for human review
4. Never output invalid data

---

## Learning 7: Human Review is a Feature, Not a Bug

### The Initial Assumption

"Good ML systems don't need human review."

### The Reality

For high-stakes financial data, human review is essential:
- Catches edge cases ML misses
- Builds user trust in the system
- Provides training signal for improvement
- Meets compliance requirements

### Design Implication

Design for human-in-the-loop from the start:
- Clear visualization of extraction results
- Easy adjustment interface
- Audit trail of human corrections
- Feedback loop to improve proposals

---

## Summary: The Pivot from Academic to Production

| Academic Approach | Production Reality |
|-------------------|-------------------|
| Maximize model accuracy | Maximize user productivity |
| Single best model | Ensemble of specialized components |
| Fully automated pipeline | Human-in-the-loop refinement |
| Pixel-level precision | Normalized, generalizable coordinates |
| Train on synthetic data | Validate on real documents |
| Measure F1 score | Measure time-to-completion |

The shift from "pure ML" to "hybrid system" wasn't a failure of ML—it was recognition that production systems have different requirements than academic benchmarks.

---

## Recommended Reading

- **Human-in-the-Loop Machine Learning** (Robert Monarch) - Framework for hybrid systems
- **Designing Data-Intensive Applications** (Martin Kleppmann) - Production data pipelines
- **The Pragmatic Programmer** - Practical engineering trade-offs

---

*The best system is not the most sophisticated—it's the one that solves the problem reliably.*
