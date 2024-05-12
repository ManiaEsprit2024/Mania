import logging
from flask import Blueprint, request, jsonify
from app.libs.fiscoSE import predict_fico_score 
from app.libs.fiscoBME import predict_fico_score_bme
from app.libs.fiscoSE import get_fico_score_by_unique_id
from app.libs.fiscoSE import csv_to_json 
import os
import pandas as pd

logger = logging.getLogger(__name__)

logging.basicConfig(filename='app/output/logfile.log', level=logging.INFO)

fico = Blueprint('fico', __name__)

@fico.route('/predict_fico_se', methods=['POST'])
def predict():
    try:
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
        
        # Log prediction request
        logger.info("Prediction request processed successfully")

        return result.to_json(orient='records'), 200
    except Exception as e:
        error_msg = f"Error predicting FICO score: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@fico.route('/predict_fico_bme', methods=['POST'])
def predict_bme():
    try:
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

        # Log prediction request
        logger.info("BME prediction request processed successfully")

        return result.to_json(orient='records'), 200
    except Exception as e:
        error_msg = f"Error predicting FICO score (BME): {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@fico.route('/predict_fico_dataset', methods=['POST'])
def predict_dataset():
    try:
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
        
        # Log prediction request
        logger.info("Dataset prediction request processed successfully")

        return predictions, 200
    except Exception as e:
        error_msg = f"Error predicting FICO score (dataset): {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@fico.route('/get_fico_by_unique_id', methods=['POST'])
def get_fico_by_unique_id():
    try:
        data = request.get_json()

        if 'output_file' not in data or 'unique_id' not in data:
            return jsonify({'error': 'output_file or unique_id not provided'}), 400

        output_file = data['output_file']
        unique_id = data['unique_id']

        fico_score = get_fico_score_by_unique_id(output_file, unique_id)

        # Log request
        logger.info("FICO score by unique ID request processed successfully")

        return jsonify({'fico_score': fico_score}), 200
    except Exception as e:
        error_msg = f"Error getting FICO score by unique ID: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
