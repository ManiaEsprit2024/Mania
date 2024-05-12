import os
import pandas as pd
from flask import send_file
import logging
import numpy as np
from collections import Counter
import re

# Configure logging
logging.basicConfig(filename='app/output/logfile.log', level=logging.INFO)

def upload_dataset(csv_file, folder):
    """
    Uploads a dataset CSV file to the specified folder.

    Parameters:
        csv_file (FileStorage): Uploaded CSV file object.
        folder (str): Path to the folder where the dataset will be uploaded.

    Returns:
        str: Message indicating success or failure.
    """
    try:
        if not os.path.exists("app/"+folder):
            os.makedirs("app/"+folder)
        
        csv_file.save(os.path.join("app", folder, csv_file.filename))
        
        logging.info(f"Dataset {csv_file.filename} uploaded successfully to {folder}")
        return "Dataset uploaded successfully."
    except Exception as e:
        error_msg = f"Error uploading dataset: {str(e)}"
        logging.error(error_msg)
        return error_msg
    
def extract_chart_data_from_logs(log_content):
    """
    Extracts chart data from log entries.

    Parameters:
        log_content (str): Content of the log file.

    Returns:
        dict: Dictionary containing chart data.
    """
    try:
        # Count occurrences of specific phrases in the log content
        upload_count = log_content.count("/api/upload_dataset")
        download_count = log_content.count("/api/download_csv")
        treated = log_content.count("/api/predict_fico_dataset")
        delete_count = log_content.count("/api/delete_file")

        # Construct chart data dictionary
        chart_data = {
            "Uploads": upload_count,
            "Deletes": delete_count,
            "Downloads": download_count,
            "treated": treated
        }

        return {"chart_data": chart_data}
    except Exception as e:
        # Handle exceptions
        return {"error": str(e)}

def dataset_stats(filename):
    """
    Returns statistics about a dataset along with the first 10 lines.

    Parameters:
        filename (str): Name of the dataset file.

    Returns:
        dict: Dictionary containing dataset statistics and the first 10 lines.
    """
    try:
        filepath = os.path.join("app/datasets/", filename)
        df = pd.read_csv(filepath)
        df.reset_index(drop=True, inplace=True)
        missing_values_count = df.isnull().sum().to_dict()
        numeric_stats = df.describe().to_dict()

        logging.info(f"Statistics generated for dataset: {filename}")
        return {
            "missing_values_count": missing_values_count,
            "numeric_statistics": numeric_stats
        }
    except Exception as e:
        error_msg = f"Error getting dataset statistics: {str(e)}"
        logging.error(error_msg)
        return error_msg
    
def list_files_in_folder(folder):
    """
    Lists all files in the specified folder.

    Parameters:
        folder (str): Path to the folder.

    Returns:
        list: List of file names in the folder.
    """
    try:
        files = os.listdir("app/"+folder)
        logging.info(f"List of files in folder {folder} retrieved.")
        return files
    except Exception as e:
        logging.error(f"Error listing files in folder {folder}: {str(e)}")
        return []

def get_csv_content(folder, filename):
    """
    Reads the content of a CSV file.

    Parameters:
        folder (str): Path to the folder containing the CSV file.
        filename (str): Name of the CSV file.

    Returns:
        str: Content of the CSV file.
    """
    try:
        filepath = os.path.join("app/", folder, filename)
        with open(filepath, "r") as file:
            content = file.read()
        logging.info(f"Content of CSV file {filename} read successfully.")
        return content
    except Exception as e:
        error_msg = f"Error reading CSV file: {str(e)}"
        logging.error(error_msg)
        return error_msg
    
def delete_file(folder, filename):
    """
    Deletes a file from a folder.

    Parameters:
        folder (str): Path to the folder containing the file.
        filename (str): Name of the file to be deleted.

    Returns:
        str: Message indicating success or failure.
    """
    try:
        filepath = os.path.join("app", folder, filename)
        os.remove(filepath)
        logging.info(f"File '{filename}' deleted successfully from folder {folder}.")
        return f"File '{filename}' deleted successfully."
    except Exception as e:
        error_msg = f"Error deleting file '{filename}': {str(e)}"
        logging.error(error_msg)
        return error_msg
    
def download_csv(folder, filename):
    """
    Downloads a CSV file.

    Parameters:
        folder (str): Path to the folder containing the CSV file.
        filename (str): Name of the CSV file to be downloaded.

    Returns:
        File: CSV file to be downloaded.
    """
    try:
        filepath = os.path.join("app", folder, filename)
        logging.info(f"CSV file {filename} downloaded successfully from folder {folder}.")
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        error_msg = f"Error downloading CSV file: {str(e)}"
        logging.error(error_msg)
        return error_msg
