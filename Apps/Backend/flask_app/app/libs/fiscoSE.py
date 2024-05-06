# Import necessary libraries
import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

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

    random_data_processed = random_data.copy()
    random_data_processed['disbursement_date'] = pd.to_datetime(random_data_processed['disbursement_date']).astype('int64')

    label_encoder = LabelEncoder()

    for column in random_data_processed.select_dtypes(include=['object']):
        random_data_processed[column] = label_encoder.fit_transform(random_data_processed[column])

    loan_default_probabilities = xgb_model.predict_proba(random_data_processed[best_features])[:, 1]
    
    forecast_fico_scores_xg = (300 + (900 - 300) * (1 - loan_default_probabilities)).astype(int)

    fico_classes = {
        'LOW': (300, 400),
        'Fair': (401, 600),
        'Good': (601, 700),
        'Very Good': (701, 900)
    }

    # Assign FICO class based on FICO score
    forecast_fico_classes_xg = []
    for score in forecast_fico_scores_xg:
        for fico_class, score_range in fico_classes.items():
            if score_range[0] <= score <= score_range[1]:
                forecast_fico_classes_xg.append(fico_class)
                break

    # Create a DataFrame with the output data
    forecast_with_classes_xg = pd.DataFrame({
        'FICO_Score': forecast_fico_scores_xg,
        'Loan_default_probabilities': loan_default_probabilities,
        'Risk_Level': calculate_risk(loan_default_probabilities),
        'FICO_Class': forecast_fico_classes_xg,
        'Loan_Prediction': xgb_model.predict(random_data_processed[best_features])
    })

    return forecast_with_classes_xg
