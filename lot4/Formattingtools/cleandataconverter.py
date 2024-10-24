import pandas as pd
import json
import os

def csv_to_json(csv_file, json_file):
    """Convert cleaned CSV file to JSON format.

    Args:
        csv_file (str): Path to the cleaned CSV file.
        json_file (str): Path to the output JSON file.
    """
    try:
        # Read the cleaned CSV file
        df = pd.read_csv(csv_file)

        # Transform DataFrame to a list of dictionaries
        records = df.to_dict(orient='records')

        # Write records to a JSON file
        with open(json_file, 'w', encoding='utf-8') as f:
            for record in records:
                # Add Elasticsearch bulk insert format
                f.write(json.dumps({"index": {}}) + '\n')  # Index action
                f.write(json.dumps(record) + '\n')  # Document

        print(f"Successfully converted '{csv_file}' to '{json_file}'.")

    except Exception as e:
        print(f"An error occurred while converting CSV to JSON: {e}", file=sys.stderr)

# Usage
csv_file_path = '../../data/dataw_fro03/cleaneddata.csv'  # Path to your cleaned CSV file
json_file_path = '../../data/dataw_fro03/cleaneddata.json'  # Desired path for the output JSON file

csv_to_json(csv_file_path, json_file_path)
