from flask import Blueprint, request, jsonify
from app.libs.fiscoSE import predict_fico_score 
from app.libs.fiscoBME import predict_fico_score_bme

fico = Blueprint('fico', __name__)

@fico.route('/predict_fico_se', methods=['POST'])
def predict():
    data = request.get_json()

    required_fields = ['disbursement_date', 'lender_insurance_premium', 'jobs_created', 'optional_revenue_yr_confirmed', 'optional_stage', 'unique_id']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    disbursement_date = data['disbursement_date']
    lender_insurance_premium = data['lender_insurance_premium']
    jobs_created = data['jobs_created']
    optional_revenue_yr_confirmed = data['optional_revenue_yr_confirmed']
    optional_stage = data['optional_stage']
    unique_id = data['unique_id']

    result = predict_fico_score(
        disbursement_date,
        lender_insurance_premium,
        jobs_created,
        optional_revenue_yr_confirmed,
        optional_stage,
        unique_id
    )

    return result.to_json(orient='records'), 200

@fico.route('/predict_fico_bme', methods=['POST'])
def predict_bme():
    data = request.get_json()

    required_fields = [
        'disbursement_date',
        'revenue',
        'naics_code',
        'lender_type_category',
        'optional_primary_use_of_funds'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    disbursement_date = data['disbursement_date']
    revenue = data['revenue']
    naics_code = data['naics_code']
    lender_type_category = data['lender_type_category']
    optional_primary_use_of_funds = data['optional_primary_use_of_funds']

    result = predict_fico_score_bme(
        disbursement_date,
        revenue,
        naics_code,
        lender_type_category,
        optional_primary_use_of_funds
    )

    # Return the result as a JSON response
    return result.to_json(orient='records'), 200
