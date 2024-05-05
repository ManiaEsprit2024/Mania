import pandas as pd
import joblib
import os

# Load the pre-trained model
# Use absolute path to ensure portability
MODEL_PATH = os.path.abspath('app/models/fico_model.pkl')
xgb_model = joblib.load(MODEL_PATH)

# Define the best features used by the model
best_features = ['unique_id', 'disbursement_date', 'lender_insurance_premium', 'jobs_created', 'optional_revenue_yr_confirmed', 'optional_stage']

# Function to predict FICO score
def predict_fico_score(disbursement_date, lender_insurance_premium, jobs_created, optional_revenue_yr_confirmed, optional_stage, unique_id):
    random_data = pd.DataFrame({
        'unique_id': [unique_id],
        'disbursement_date': [disbursement_date],
        'lender_insurance_premium': [lender_insurance_premium],
        'jobs_created': [jobs_created],
        'optional_revenue_yr_confirmed': [optional_revenue_yr_confirmed],
        'optional_stage': [optional_stage]
    })

    # Process the data as needed
    random_data_processed = random_data.copy()
    random_data_processed['disbursement_date'] = pd.to_datetime(random_data_processed['disbursement_date']).astype('int64')
    random_data_processed['optional_stage'] = pd.Categorical(random_data_processed['optional_stage']).codes

    loan_default_probabilities = xgb_model.predict_proba(random_data_processed[best_features])[:, 1]
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
        'unique_id': random_data['unique_id'],
        'FICO_Score': forecast_fico_scores_xg,
        'FICO_Class': forecast_fico_classes_xg,
        'loan_prediction': xgb_model.predict(random_data_processed[best_features])
    })

    return forecast_with_classes_xg
    