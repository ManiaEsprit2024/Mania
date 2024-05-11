import pandas as pd
import joblib
import os
import numpy as np
import json


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

def predict_fico_score(lender_insurance_premium, jobs_created, optional_revenue_yr_confirmed, optional_stage):
    random_data = pd.DataFrame({
        'disbursement_date': 4000,
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

from datetime import datetime

def csv_to_json(csv_file):
    predictions = []
    try:
        df = csv_file
        json_data = []
        for index, row in df.iterrows():
            prediction = predict_fico_score(row['lender_insurance_premium'], row['jobs_created'], row['optional_revenue_yr_confirmed'], row['optional_stage'])
            predictions.append(prediction.iloc[0])
        predictions_df = pd.DataFrame(predictions)
        predictions_df.reset_index(drop=True, inplace=True)  
        result_df = pd.concat([df, predictions_df], axis=1)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = f"Output_{timestamp}.csv"
        
        result_df.to_csv(output_file, index=False)
        return output_file
    except Exception as e:
        return {"error": str(e)}