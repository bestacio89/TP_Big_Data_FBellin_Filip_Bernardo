import pandas as pd
import os

def process_line_to_dict(line):
    """Processes a single line of text to extract city, quantity, and timbre."""
    try:
        # Split the line by tab character
        parts = line.split("\t")

        # Initialize dictionary to hold valid data
        data = {}
        valid_parts = []  # This will store the non-empty parts we find

        # Loop through the parts and collect only non-empty ones
        for part in parts:
            stripped_part = part.strip()
            if stripped_part:  # Only consider non-empty parts
                valid_parts.append(stripped_part)

        # We want at least 3 valid parts to proceed
        if len(valid_parts) >= 3:
            data['City'] = valid_parts[0]  # 1st valid part
            data['Quantity'] = int(valid_parts[1]) if valid_parts[1].isdigit() else 0  # 2nd valid part
            data['Avg_Quantity'] = float(valid_parts[2]) if valid_parts[2].replace('.', '', 1).isdigit() else 0.0  # 3rd valid part
        else:
            print("Not enough valid data parts found in line: {}".format(line))  # Debug output

        print("Processing: {}".format(data))  # Updated for Python 3.5.2
        return data

    except ValueError as e:
        print("Error processing line: {} | Error: {}".format(line, e))  # Debugging output for conversion issues
        return None


def convert_text_to_excel(input_file, output_file):
    """Converts a tab-separated text file to an Excel file, processing each line individually."""
    try:
        # Prepare an empty list to store the rows
        rows = []

        # Open the input file and process each line
        with open(input_file, 'r') as file:
            for line in file:
                # Process each line and append the result if valid
                result = process_line_to_dict(line.strip())
                if result:  # Only append if the result is not None
                    rows.append(result)

        if not rows:
            print("No data to write to Excel.")  # Updated for Python 3.5.2
        else:
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(rows)

            # Debug: Print DataFrame content to ensure it's correct
            print(df.head())  # This line can remain as is; no formatting necessary

            # Export the DataFrame to Excel
            df.to_excel(output_file, index=False)
            print("Data exported to {} successfully.".format(output_file))  # Updated for Python 3.5.2

    except Exception as e:
        print("An error occurred: {}".format(e))  # Updated for Python 3.5.2


def main():
    # Specify the path to your input text file
    input_file = os.path.join("lot2", "results", "part-00000")  # Change this to your text file path
    output_file = os.path.join("lot2", "results", "Analysed_Datalot2.xlsx")  # Desired output Excel file name

    convert_text_to_excel(input_file, output_file)


if __name__ == "__main__":
    main()
