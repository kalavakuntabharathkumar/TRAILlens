from __future__ import annotations
import pandas as pd

VALID_AE = ["Serious", "Non-serious", "Treatment-emergent"]

def validate_trial_data(df: pd.DataFrame) -> pd.DataFrame:
    checks = []

    checks.append({
        "check": "Missing required values",
        "rows_flagged": int(
            df[["patient_id", "age", "sex", "treatment_arm"]]
            .isna()
            .any(axis=1)
            .sum()
        ),
    })

    checks.append({
        "check": "Duplicate patient IDs",
        "rows_flagged": int(df["patient_id"].duplicated(keep=False).sum()),
    })

    checks.append({
        "check": "Blood pressure range",
        "rows_flagged": int(
            (
                (df["systolic_bp"] < 70)
                | (df["systolic_bp"] > 250)
                | (df["diastolic_bp"] < 40)
                | (df["diastolic_bp"] > 150)
            ).sum()
        ),
    })

    checks.append({
        "check": "Heart-rate range",
        "rows_flagged": int(
            ((df["heart_rate"] < 30) | (df["heart_rate"] > 220)).sum()
        ),
    })

    checks.append({
        "check": "Adverse-event category validity",
        "rows_flagged": int(
            (~df["adverse_event"].isin(VALID_AE)).sum()
        ),
    })

    out = pd.DataFrame(checks)
    out["status"] = out["rows_flagged"].map(
        lambda x: "PASS" if x == 0 else "FLAG"
    )
    return out
