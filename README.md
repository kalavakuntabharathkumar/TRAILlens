# TrialLens — Clinical Trial Data Quality & GenAI Storyboard Generator

Portfolio-ready Streamlit application demonstrating clinical-trial data quality,
SQL safety analytics, visualization, and GenAI narrative generation.

## What it demonstrates
- 500 synthetic patient records.
- 3 adverse-event categories.
- SQLite SQL pipeline extracting 8 safety metrics.
- 5 rule-based data-quality checks.
- 25 seeded errors (5% by design).
- Plotly visualization.
- OpenAI-generated 3-slide cohort storyboard.
- Deterministic fallback storyboard when no API key exists.

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Optional OpenAI integration:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_key"
```

> Synthetic data only. This project is not intended for clinical decision-making,
> patient care, regulatory submission, or medical advice.
