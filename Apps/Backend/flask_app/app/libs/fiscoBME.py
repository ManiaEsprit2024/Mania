import pandas as pd
import joblib
import os

MODEL_PATH = os.path.abspath("app/models/fico_model_BME.pkl")
xgb_model = joblib.load(MODEL_PATH)

best_features = [
    'disbursement_date',
    'revenue',
    'naics_code',
    'lender_type_category',
    'optional_primary_use_of_funds'
]

fico_classes = {
    "LOW": (300, 400),
    "Fair": (401, 600),
    "Good": (601, 700),
    "Very Good": (701, 900)
}

risk_levels = {
    "Low": (0.0, 0.1),
    "Moderate": (0.1, 0.6),
    "High": (0.6, 0.8),
    "Very High": (0.8, 1.0)
}

def calculate_risk(probability):
    for level, (min_prob, max_prob) in risk_levels.items():
        if min_prob <= probability <= max_prob:
            return level
    return "Unknown"

def predict_fico_score_bme(disbursement_date,revenue,naics_code,lender_type_category,optional_primary_use_of_funds):

    input_data = pd.DataFrame({
        'disbursement_date': [disbursement_date],
        'revenue': [revenue],
        'naics_code': [naics_code],
        'lender_type_category': [lender_type_category],
        'optional_primary_use_of_funds': [optional_primary_use_of_funds]
    })

    input_data['disbursement_date'] = pd.to_datetime(input_data['disbursement_date']).astype("int64")
    input_data['naics_code'] = pd.Categorical(input_data['naics_code']).codes
    input_data['lender_type_category'] = pd.Categorical(input_data['lender_type_category']).codes
    input_data['optional_primary_use_of_funds'] = pd.Categorical(input_data['optional_primary_use_of_funds']).codes

    default_probabilities = xgb_model.predict_proba(input_data[best_features])[:, 1]

    forecast_fico_scores = (300 + (900 - 300) * (1 - default_probabilities)).astype(int)

    fico_classes_pred = []
    for score in forecast_fico_scores:
        for fico_class, (min_score, max_score) in fico_classes.items():
            if min_score <= score <= max_score:
                fico_classes_pred.append(fico_class)
                break

    results = pd.DataFrame({
        "FICO_Score": forecast_fico_scores,
        "Risk Class": [calculate_risk(prob) for prob in default_probabilities],
        "Risk": default_probabilities,
        "FICO_Class": fico_classes_pred,
        "loan_prediction": xgb_model.predict(input_data[best_features])
    })

    return results
