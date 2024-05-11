# Import necessary libraries
import pandas as pd
import joblib

label_encoder = joblib.load("app/models/label_encoder.pkl")
scaler = joblib.load("app/models/standard_scaler.pkl")
xgb_model = joblib.load("app/models/fico_model_SE.pkl")

best_features = ['disbursement_date', 'lender_insurance_premium', 'jobs_created', 'optional_revenue_yr_confirmed', 'optional_stage']

def calculate_risk(probability):
    risk_levels = {
        'Low': (0.0, 0.1),
        'Moderate': (0.1, 0.6),
        'High': (0.6, 0.8),
        'Very High': (0.8, 1.0)
    }

    for level, (min_prob, max_prob) in risk_levels.items():
        if min_prob <= probability <= max_prob:
            return level

    return 'Unknown'

def predict_fico_score(disbursement_date, lender_insurance_premium, jobs_created, optional_revenue_yr_confirmed, optional_stage):
    random_data = pd.DataFrame({
        'disbursement_date': [disbursement_date],
        'lender_insurance_premium': [lender_insurance_premium],
        'jobs_created': [jobs_created],
        'optional_revenue_yr_confirmed': [optional_revenue_yr_confirmed],
        'optional_stage': [optional_stage]
    })
    
    for column in random_data.select_dtypes(include=['object']):
        random_data[column] = label_encoder.transform(random_data[column])
    
    random_data_scaled = pd.DataFrame(scaler.transform(random_data), columns=random_data.columns)

    loan_default_probabilities = xgb_model.predict_proba(random_data_scaled[best_features])[:, 1]

    forecast_fico_scores_xg = (300 + (900 - 300) * (1 - loan_default_probabilities)).astype(int)

    fico_classes = {
        'LOW': (300, 400),
        'Fair': (401, 600),
        'Good': (601, 700),
        'Very Good': (701, 900)
    }

    forecast_fico_classes_xg = []
    for score in forecast_fico_scores_xg:
        for fico_class, score_range in fico_classes.items():
            if score_range[0] <= score <= score_range[1]:
                forecast_fico_classes_xg.append(fico_class)
                break

    forecast_with_classes_xg = pd.DataFrame({
        'FICO_Score': forecast_fico_scores_xg,
        'Loan_default_probabilities': loan_default_probabilities,
        'Risk_Level': [calculate_risk(prob) for prob in loan_default_probabilities],
        'FICO_Class': forecast_fico_classes_xg,
        'Loan_Prediction': xgb_model.predict(random_data_scaled[best_features])
    })

    return forecast_with_classes_xg
