import json
import sys

def create_bulk_index_format(input_file_path, output_file_path):
    """Creates a bulk index format for Elasticsearch from a cleaned JSON file.

    Args:
        input_file_path (str): Path to the cleaned JSON file.
        output_file_path (str): Path to save the bulk index format.
    """
    try:
        # Read the cleaned JSON file
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            data = json.load(input_file)

        # Write the bulk index format to a new file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for record in data:
                output_file.write(json.dumps({"index": {"_index": "dataw_fro"}}) + '\n')
                output_file.write(json.dumps(record) + '\n')

        print(f"Bulk index format created successfully: {output_file_path}")

    except Exception as e:
        print(f"An error occurred while creating bulk index format: {e}", file=sys.stderr)

# Example usage
input_file_path = '../../data/dataw_fro03/cleaneddata.json'  # Change this to your cleaned JSON file path
output_file_path = '../data/dataw_fro03/bulk_index_data.json'  # Desired output file path

create_bulk_index_format(input_file_path, output_file_path)
