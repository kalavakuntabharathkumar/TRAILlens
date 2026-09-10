from __future__ import annotations
import os

def fallback_storyboard(result: dict) -> str:
    m = result["metrics"]
    ae = result["ae"]

    if ae.empty:
        top = "No AE category"
    else:
        row = ae.iloc[0]
        top = f"{row['adverse_event']} ({int(row['patients'])} patients)"

    return f"""
### Slide 1 — Cohort snapshot
- Valid analysis population: {int(m['total_patients'])} patients.
- Mean age: {m['mean_age']} years.
- Treatment: {int(m['treatment_n'])}; placebo: {int(m['placebo_n'])}.
- Mean vitals: BP {m['mean_systolic_bp']}/{m['mean_diastolic_bp']} mmHg; HR {m['mean_heart_rate']} bpm.

### Slide 2 — Safety profile
- Most frequent AE category: {top}.
- Serious AE rate: {m['serious_ae_pct']}%.
- AE distributions should be reviewed by treatment arm before making comparative claims.

### Slide 3 — Data-quality interpretation
- Metrics were calculated after rule-based quality screening.
- The dataset is synthetic and intended to demonstrate an analytics workflow.
- No efficacy, causal, or clinical conclusion should be inferred.
""".strip()

def generate_storyboard(result: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return fallback_storyboard(result)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = f"""
Create exactly three slide-ready sections titled Slide 1, Slide 2, and Slide 3.

Use only the supplied numbers.
Do not invent efficacy, causality, statistical significance, patient outcomes,
regulatory conclusions, or explanations not present in the data.

Slide 1: cohort profile.
Slide 2: adverse-event/safety profile.
Slide 3: data-quality and interpretation notes.

Metrics: {result["metrics"]}
AE distribution: {result["ae"].to_dict("records")}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "Create cautious analytical narratives from structured trial data."
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content or fallback_storyboard(result)

    except Exception:
        return fallback_storyboard(result)
