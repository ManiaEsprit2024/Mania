import sys
import pandas as pd
import joblib

xgb_model = joblib.load('Models/fico_model.pkl')

best_features = ['unique_id', 'disbursement_date', 'lender_insurance_premium', 'jobs_created', 'optional_revenue_yr_confirmed', 'optional_stage']

def predict_fico_score(arg1, arg2, arg3, arg4, arg5,arg6):
    random_data = pd.DataFrame({
        'unique_id': [arg6],
        'disbursement_date': [arg1],
        'lender_insurance_premium': [arg2],
        'jobs_created': [arg3],
        'optional_revenue_yr_confirmed': [arg4],
        'optional_stage': [arg5]
    })

    random_data_processed = random_data.copy()
    random_data_processed['disbursement_date'] = pd.to_datetime(random_data_processed['disbursement_date']).astype('int64')  # Convert to int64
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
    forecast_with_classes_xg = pd.DataFrame({'unique_id': random_data['unique_id'], 'FICO_Score': forecast_fico_scores_xg, 'FICO_Class': forecast_fico_classes_xg, 'loan_prediction': xgb_model.predict(random_data_processed[best_features])})
    top_individuals_xg = forecast_with_classes_xg.head(10)
    return top_individuals_xg

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python fiscoOne.py <arg1> <arg2> <arg3> <arg4> <arg5>")
        sys.exit(1)

    arg1 = sys.argv[1]
    arg2 = float(sys.argv[2])
    arg3 = int(sys.argv[3])
    arg4 = int(sys.argv[4])
    arg5 = sys.argv[5]
    arg6 = int(sys.argv[6])

    result = predict_fico_score(arg1, arg2, arg3, arg4, arg5, arg6)
    print("Top Individuals with Deduced FICO Scores and Classes:")
    print(result)
