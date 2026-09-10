import streamlit as st
import plotly.express as px

from data_generator import generate_trial_data
from validation import validate_trial_data
from pipeline import run_sql_metrics
from ai_storyboard import generate_storyboard

st.set_page_config(
    page_title="TrialLens",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 TrialLens")
st.caption("Clinical Trial Data Quality & GenAI Storyboard Generator — synthetic data only")

df, seeded_errors = generate_trial_data()
validation = validate_trial_data(df)
result = run_sql_metrics(df)
m = result["metrics"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Valid patients", f"{int(m['total_patients']):,}")
c2.metric("Mean age", f"{m['mean_age']:.1f}")
c3.metric("Serious AE", f"{m['serious_ae_pct']:.2f}%")
c4.metric("Seeded errors", f"{len(seeded_errors):,}")

st.subheader("Data-quality checks")
st.dataframe(validation, use_container_width=True, hide_index=True)

st.info(
    "25 deliberately seeded errors (5%) are inserted before validation. "
    "The five checks run before the reporting dataset is visualized."
)

left, right = st.columns(2)

with left:
    st.subheader("Adverse-event categories")
    fig = px.bar(
        result["ae"],
        x="adverse_event",
        y="patients",
        text="patients",
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("AE profile by treatment arm")
    fig = px.bar(
        result["arm_ae"],
        x="adverse_event",
        y="patients",
        color="treatment_arm",
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Eight safety metrics")

metric_rows = [
    ("Total valid patients", m["total_patients"]),
    ("Mean age", m["mean_age"]),
    ("Treatment N", m["treatment_n"]),
    ("Placebo N", m["placebo_n"]),
    ("Mean systolic BP", m["mean_systolic_bp"]),
    ("Mean diastolic BP", m["mean_diastolic_bp"]),
    ("Mean heart rate", m["mean_heart_rate"]),
    ("Serious AE %", m["serious_ae_pct"]),
]

st.dataframe(
    metric_rows,
    use_container_width=True,
    hide_index=True,
)

st.subheader("GenAI 3-slide cohort storyboard")
st.markdown(generate_storyboard(result))

with st.expander("Validated analysis dataset"):
    st.dataframe(
        result["clean"],
        use_container_width=True,
        hide_index=True,
    )
