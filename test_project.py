from data_generator import generate_trial_data
from validation import validate_trial_data
from pipeline import run_sql_metrics

df, errors = generate_trial_data()

assert len(df) == 500
assert len(errors) == 25

validation = validate_trial_data(df)
assert len(validation) == 5

result = run_sql_metrics(df)

assert len(result["metrics"]) == 8
assert result["metrics"]["total_patients"] > 0
assert not result["ae"].empty

print("TrialLens checks passed.")
