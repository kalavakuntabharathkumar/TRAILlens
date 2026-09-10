from __future__ import annotations
import numpy as np
import pandas as pd

AE_CATEGORIES = ["Serious", "Non-serious", "Treatment-emergent"]
SEXES = ["Female", "Male"]
ARMS = ["Treatment", "Placebo"]

def generate_trial_data(seed: int = 73, rows: int = 500, inject_errors: bool = True):
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "patient_id": [f"P{i:04d}" for i in range(1, rows + 1)],
        "age": rng.integers(18, 81, rows),
        "sex": rng.choice(SEXES, rows),
        "treatment_arm": rng.choice(ARMS, rows),
        "systolic_bp": np.round(rng.normal(122, 15, rows), 1),
        "diastolic_bp": np.round(rng.normal(78, 10, rows), 1),
        "heart_rate": np.round(rng.normal(72, 11, rows), 1),
        "adverse_event": rng.choice(
            AE_CATEGORIES, rows, p=[0.08, 0.67, 0.25]
        ),
        "ae_severity": rng.choice(
            ["Mild", "Moderate", "Severe"],
            rows,
            p=[0.55, 0.35, 0.10]
        ),
    })

    errors = []

    if inject_errors:
        picks = rng.choice(df.index, 25, replace=False)

        for i in picks[:5]:
            df.loc[i, "age"] = np.nan
            errors.append((int(i), "missing_age"))

        for i in picks[5:10]:
            df.loc[i, "patient_id"] = df.loc[max(0, i - 1), "patient_id"]
            errors.append((int(i), "duplicate_id"))

        for i in picks[10:15]:
            df.loc[i, "systolic_bp"] = 280
            errors.append((int(i), "out_of_range_bp"))

        for i in picks[15:20]:
            df.loc[i, "heart_rate"] = -5
            errors.append((int(i), "out_of_range_hr"))

        for i in picks[20:25]:
            df.loc[i, "adverse_event"] = "Unknown"
            errors.append((int(i), "invalid_ae_category"))

    return df, pd.DataFrame(
        errors,
        columns=["row_index", "error_type"]
    )
