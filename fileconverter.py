import pandas as pd
import os


def process_line_to_dict(line, headers=None):
    """Processes a single line of text to extract city, codcde, quantity, and timbre, with optional headers."""
    try:
        # Split the line by tab character and strip whitespace
        parts = [part.strip() for part in line.split("\t") if part.strip()]

        # Initialize dictionary to hold valid data
        if headers:
            # Create a dictionary using headers
            data = {headers[i]: parts[i] if i < len(parts) else '' for i in range(len(headers))}
        else:
            # If headers aren't provided, treat the parts as data fields with default names
            data = {}
            if len(parts) >= 4:
                data['City'] = parts[1]
                data['Codcde'] = parts[0]
                data['Quantity'] = int(parts[2]) if parts[2].isdigit() else 0
                data['Timbre'] = float(parts[3]) if parts[3].replace('.', '', 1).isdigit() else 0.0
            else:
                if len(parts) > 0:
                    data['City'] = parts[0]
                if len(parts) > 1:
                    data['Codcde'] = parts[1]
                if len(parts) > 2:
                    data['Quantity'] = int(parts[2]) if parts[2].isdigit() else 0
                if len(parts) > 3:
                    data['Timbre'] = float(parts[3]) if parts[3].replace('.', '', 1).isdigit() else 0.0

        print("Processing: {}".format(data))  # Debug print compatible with Python 3.5
        return data

    except ValueError as e:
        print("Error processing line: {} | Error: {}".format(line, e))  # Debugging output for conversion issues
        return None


def convert_text_to_excel(input_file, output_file):
    """Converts a tab-separated text file to an Excel file, using the first line as the header."""
    try:
        # Prepare an empty list to store the rows
        rows = []
        headers = None

        # Open the input file and process each line
        with open(input_file, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()

                # Use the first line as headers
                if i == 0:
                    headers = [header.strip() for header in line.split("\t")]
                    print("Headers: {}".format(headers))  # Debugging output to check headers
                    continue

                # Process each line using headers
                result = process_line_to_dict(line, headers=headers)
                if result:  # Only append if the result is not None
                    rows.append(result)

        if not rows:
            print("No data to write to Excel.")  # Debugging check for empty rows
        else:
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(rows)

            # Debug: Print DataFrame content to ensure it's correct
            print(df.head())

            # Export the DataFrame to Excel
            df.to_excel(output_file, index=False)
            print("Data exported to {} successfully.".format(output_file))

    except Exception as e:
        print("An error occurred: {}".format(e))


def main():
    # Specify the path to your input text file
    input_file = os.path.join("datavolume1", "part-00000")  # Change this to your text file path
    output_file = os.path.join("lot1", "Analysed_Datalot1.xlsx")  # Desired output Excel file name

    convert_text_to_excel(input_file, output_file)


