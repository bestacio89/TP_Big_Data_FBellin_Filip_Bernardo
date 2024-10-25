import pandas as pd
import os

def process_line_to_dict(line, headers=None):
    """Processes a single line of text to extract relevant fields, ignoring 'Rank'."""
    try:
        # Split the line by tab character and strip whitespace
        parts = [part.strip() for part in line.split("\t") if part.strip()]

        # If there are headers, skip the first 'Rank' column
        if headers:
            data = {headers[i + 1]: parts[i + 1] for i in range(len(headers) - 1)}  # Skip Rank column
        else:
            # Handle without headers by using default names for parts
            data = {}
            if len(parts) >= 4:
                data['Codcde'] = parts[1]
                data['City'] = parts[2]
                data['Quantity Sum'] = int(parts[3]) if parts[3].isdigit() else 0
                data['Timbrecde Sum'] = float(parts[4]) if parts[4].replace('.', '', 1).isdigit() else 0.0

        return data

    except ValueError as e:
        print("Error processing line: {} | Error: {}".format(line, e))
        return None

def convert_text_to_excel(input_file, output_file):
    """Converts a tab-separated text file to an Excel file, excluding 'Rank'."""
    try:
        rows = []
        headers = None

        # Open the input file and process each line
        with open(input_file, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()

                # Use the first line as headers, excluding 'Rank'
                if i == 0:
                    headers = [header.strip() for header in line.split("\t")]
                    headers = headers[1:]  # Skip 'Rank'
                    print("Headers: {}".format(headers))
                    continue

                # Process each line using headers
                result = process_line_to_dict(line, headers=headers)
                if result:  # Only append if the result is valid
                    rows.append(result)

        if not rows:
            print("No data to write to Excel.")
        else:
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(rows)

            # Save DataFrame to Excel, excluding 'Rank'
            df.to_excel(output_file, index=False)
            print("Data exported to {} successfully.".format(output_file))

    except Exception as e:
        print("An error occurred: {}".format(e))

def main():
    input_file = os.path.join("datavolume1", "part-00000")  # Update as necessary
    output_file = os.path.join("lot1", "Analysed_Datalot1.xlsx")

    convert_text_to_excel(input_file, output_file)

if __name__ == "__main__":
    main()
