from flask import Blueprint, request, jsonify
from app.libs.fiscoSE import predict_fico_score 
from app.libs.fiscoBME import predict_fico_score_bme
from app.libs.fiscoSE import csv_to_json 
import os
fico = Blueprint('fico', __name__)
import pandas as pd
@fico.route('/predict_fico_se', methods=['POST'])
def predict():
    data = request.get_json()

    required_fields = ['lender_insurance_premium', 'jobs_created', 'optional_revenue_yr_confirmed', 'optional_stage']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    lender_insurance_premium = data['lender_insurance_premium']
    jobs_created = data['jobs_created']
    optional_revenue_yr_confirmed = data['optional_revenue_yr_confirmed']
    optional_stage = data['optional_stage']

    result = predict_fico_score(
        lender_insurance_premium,
        jobs_created,
        optional_revenue_yr_confirmed,
        optional_stage
    )

    return result.to_json(orient='records'), 200

@fico.route('/predict_fico_bme', methods=['POST'])
def predict_bme():
    data = request.get_json()

    required_fields = [
        'revenue',
        'naics_code',
        'lender_type_category',
        'optional_primary_use_of_funds'
    ]

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    revenue = data['revenue']
    naics_code = data['naics_code']
    lender_type_category = data['lender_type_category']
    optional_primary_use_of_funds = data['optional_primary_use_of_funds']

    result = predict_fico_score_bme(
        revenue,
        naics_code,
        lender_type_category,
        optional_primary_use_of_funds
    )

    return result.to_json(orient='records'), 200

@fico.route('/predict_fico_dataset', methods=['POST'])
def predict_dataset():
    data = request.get_json()

    if 'dataset_name' not in data:
        return jsonify({'error': 'Dataset name not provided'}), 400

    dataset_name = data['dataset_name']

    dataset_path = os.path.join('app/datasets', f'{dataset_name}')
    if not os.path.exists(dataset_path):
        existing_files = os.listdir('app/datasets')
        return jsonify({'error': f'Dataset "{dataset_name}" not found', 'available_datasets': existing_files}), 404
    
    try:
        dataset = pd.read_csv(dataset_path)
    except Exception as e:
        return jsonify({'error': f'Error reading dataset: {str(e)}'}), 500

    predictions = csv_to_json(dataset)
    return predictions, 200


