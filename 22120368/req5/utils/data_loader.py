import csv
import os

class DataLoader:
    """Utility class to load test data from CSV files"""
    
    @staticmethod
    def load_csv_data(file_path):
        """
        Reads CSV file and returns list of dictionaries
        :param file_path: Path to CSV file relative to project root or absolute path
        :return: List of dictionaries where keys are header names
        """
        # If path is not absolute, assume it's relative to project root
        if not os.path.isabs(file_path):
            # Get the project root directory (assuming utils/data_loader.py is structure)
            # path/to/project/utils/data_loader.py -> path/to/project
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, file_path)
            
        data_list = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data_list.append(row)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            raise
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            raise
            
        return data_list
