from flask import Blueprint, request, jsonify
from app.libs.datasetloader import extract_chart_data_from_logs,download_csv,upload_dataset, get_csv_content, list_files_in_folder ,dataset_stats
import os
api = Blueprint('api', __name__)

@api.route('/validate_mania', methods=['POST'])
def validate_mania():
    
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if username == 'mania' and password == 'mania':
        return jsonify({"message": "OK"}), 200 
    else:
        return jsonify({"error": "Invalid credentials"}), 401
    
@api.route('/upload_dataset', methods=['POST'])
def upload_dataset_route():
    
    if 'csv_file' not in request.files or 'folder' not in request.form:
        return jsonify({'error': 'csv_file or folder not provided'}), 400

    csv_file = request.files['csv_file']
    folder = request.form['folder']
    if csv_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not csv_file.filename.endswith('.csv'):
        return jsonify({'error': 'Uploaded file is not a CSV file'}), 400
    try:
        upload_dataset(csv_file, folder)
        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error uploading file: {str(e)}'}), 500

@api.route('/get_csv_content', methods=['POST'])
def return_csv_content():
    data = request.get_json()
    if 'folder' not in data or 'filename' not in data:
        return jsonify({'error': 'folder or filename not provided'}), 400

    folder = data['folder']
    filename = data['filename']

    content = get_csv_content(folder, filename)
    return jsonify({'content': content}), 200

@api.route('/list_files_in_folder', methods=['POST'])
def list_files_in_folder_route():
    data = request.get_json()
    if 'folder' not in data:
        return jsonify({'error': 'folder not provided'}), 400

    folder = data['folder']

    files = list_files_in_folder(folder)
    return jsonify({'files': files}), 200

@api.route('/delete_file', methods=['POST'])
def delete_file_route():
    data = request.get_json()
    if 'folder' not in data or 'filename' not in data:
        return jsonify({'error': 'folder or filename not provided'}), 400

    folder = data['folder']
    filename = data['filename']

    try:
        filepath = os.path.join("app", folder, filename)
        os.remove(filepath)
        return jsonify({'message': f"File '{filename}' deleted successfully."}), 200
    except Exception as e:
        return jsonify({'error': f"Error deleting file '{filename}': {str(e)}"}), 500

@api.route('/dataset_stats', methods=['POST'])
def dataset_stats_route():
    data = request.get_json()
    if 'filename' not in data:
        return jsonify({'error': 'folder or filename not provided'}), 400

    filename = data['filename']

    stats = dataset_stats(filename)
    return jsonify(stats), 200

@api.route('/download_csv', methods=['POST'])
def download_csv_route():
    """
    Endpoint to download a CSV file.
    """
    data = request.get_json()
    if 'folder' not in data or 'filename' not in data:
        return jsonify({'error': 'folder or filename not provided'}), 400

    folder = data['folder']
    filename = data['filename']

    try:
        return download_csv(folder, filename)
    except Exception as e:
        return jsonify({'error': f"Error downloading file '{filename}': {str(e)}"}), 500
    
@api.route('/chart_data_from_logs', methods=['GET'])
def chart_data_from_logs():
    """
    Endpoint to extract chart data from logs.
    """
    try:
        log_file_path = 'app/output/logfile.log'
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                log_content = log_file.read()

            chart_data = extract_chart_data_from_logs(log_content)
            if chart_data:
                return jsonify({'chart_data': chart_data}), 200
            else:
                return jsonify({'error': 'Failed to extract chart data from logs'}), 500
        else:
            return jsonify({'error': 'Log file not found'}), 404
    except Exception as e:
        return jsonify({'error': f"Error extracting chart data from logs: {str(e)}"}), 500

    
@api.route('/download_log_file', methods=['GET'])
def download_log_file():
    """
    Endpoint to download the log file.
    """
    try:
        log_file_path = 'app/output/logfile.log'
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                log_content = log_file.read()
            return jsonify({'log_content': log_content}), 200
        else:
            return jsonify({'error': 'Log file not found'}), 404
    except Exception as e:
        return jsonify({'error': f"Error downloading log file: {str(e)}"}), 500