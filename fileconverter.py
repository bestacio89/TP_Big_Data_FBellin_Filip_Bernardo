import pandas as pd
import os


def process_line_to_dict(line):
    """Processes a single line of text to extract city, codcde, quantity, and timbre."""
    try:
        # Split the line by tab character and strip whitespace
        parts = [part.strip() for part in line.split("\t") if part.strip()]

        # Initialize dictionary to hold valid data
        data = {}

        # Check if we have enough parts to assign
        if len(parts) >= 4:
            data['City'] = parts[0]
            data['Codcde'] = parts[1]
            data['Quantity'] = int(parts[2]) if parts[2].isdigit() else 0
            data['Timbre'] = float(parts[3]) if parts[3].replace('.', '', 1).isdigit() else 0.0
        else:
            # If there are less than 4 parts, assign based on available data
            if len(parts) > 0:
                data['City'] = parts[0]
            if len(parts) > 1:
                data['Codcde'] = parts[1]
            if len(parts) > 2:
                data['Quantity'] = int(parts[2]) if parts[2].isdigit() else 0
            if len(parts) > 3:
                data['Timbre'] = float(parts[3]) if parts[3].replace('.', '', 1).isdigit() else 0.0

        print(f"Processing: {data}")  # Debug print
        return data

    except ValueError as e:
        print(f"Error processing line: {line} | Error: {e}")  # Debugging output for conversion issues
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
            print("No data to write to Excel.")  # Debugging check for empty rows
        else:
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(rows)

            # Debug: Print DataFrame content to ensure it's correct
            print(df.head())

            # Export the DataFrame to Excel
            df.to_excel(output_file, index=False)
            print(f"Data exported to {output_file} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Specify the path to your input text file
    input_file = os.path.join("lot1", "results", "part-00000")  # Change this to your text file path
    output_file = os.path.join("lot1", "results", "Analysed_Datalot1.xlsx")  # Desired output Excel file name

    convert_text_to_excel(input_file, output_file)


if __name__ == "__main__":
    main()
