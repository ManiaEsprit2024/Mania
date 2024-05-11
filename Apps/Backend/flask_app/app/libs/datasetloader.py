import os
import shutil

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
        
        return "Dataset uploaded successfully."
    except Exception as e:
        return f"Error uploading dataset: {str(e)}"
    
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
        return files
    except Exception as e:
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
        return content
    except Exception as e:
        return f"Error reading CSV file: {str(e)}"
    
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
        return f"File '{filename}' deleted successfully."
    except Exception as e:
        return f"Error deleting file '{filename}': {str(e)}"