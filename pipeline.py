from __future__ import annotations
import sqlite3
import pandas as pd

VALID_AE = ["Serious", "Non-serious", "Treatment-emergent"]

def clean_trial_data(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out = out.dropna(
        subset=["patient_id", "age", "sex", "treatment_arm"]
    )
    out = out.drop_duplicates("patient_id", keep="first")

    out = out[
        out["systolic_bp"].between(70, 250)
        & out["diastolic_bp"].between(40, 150)
        & out["heart_rate"].between(30, 220)
    ]

    out = out[out["adverse_event"].isin(VALID_AE)]
    return out

def run_sql_metrics(df: pd.DataFrame) -> dict:
    clean = clean_trial_data(df)

    con = sqlite3.connect(":memory:")
    clean.to_sql("trial", con, index=False, if_exists="replace")

    metrics = pd.read_sql_query("""
        SELECT
            COUNT(*) AS total_patients,
            ROUND(AVG(age), 1) AS mean_age,
            SUM(CASE WHEN treatment_arm = 'Treatment' THEN 1 ELSE 0 END) AS treatment_n,
            SUM(CASE WHEN treatment_arm = 'Placebo' THEN 1 ELSE 0 END) AS placebo_n,
            ROUND(AVG(systolic_bp), 1) AS mean_systolic_bp,
            ROUND(AVG(diastolic_bp), 1) AS mean_diastolic_bp,
            ROUND(AVG(heart_rate), 1) AS mean_heart_rate,
            ROUND(
                100.0 * SUM(
                    CASE WHEN adverse_event = 'Serious' THEN 1 ELSE 0 END
                ) / COUNT(*), 2
            ) AS serious_ae_pct
        FROM trial
    """, con).iloc[0].to_dict()

    ae = pd.read_sql_query("""
        SELECT adverse_event, COUNT(*) AS patients
        FROM trial
        GROUP BY adverse_event
        ORDER BY patients DESC
    """, con)

    arm_ae = pd.read_sql_query("""
        SELECT treatment_arm, adverse_event, COUNT(*) AS patients
        FROM trial
        GROUP BY treatment_arm, adverse_event
        ORDER BY treatment_arm, patients DESC
    """, con)

    con.close()

    return {
        "clean": clean,
        "metrics": metrics,
        "ae": ae,
        "arm_ae": arm_ae,
    }
