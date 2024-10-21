import pandas as pd
import os

def convert_text_to_excel(input_file, output_file):
    """Converts a whitespace-separated text file to an Excel file.

    Args:
        input_file (str): Path to the input text file.
        output_file (str): Path for the output Excel file.
    """
    try:
        # Read the data from the text file
        df = pd.read_csv(input_file, sep='\s+', header=None, names=['City', 'Quantity', 'Timbre'], on_bad_lines='skip')

        # Convert Quantity and Timbre columns to numeric
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['Timbre'] = pd.to_numeric(df['Timbre'], errors='coerce')

        # Export to Excel
        df.to_excel(output_file, index=False)
        print(f"Data exported to {output_file} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Specify the path to your input text file
    input_file = os.path.join("lot1", "results", "part-00000.txt")  # Change this to your text file path
    output_file = os.path.join("lot1", "results", "Analysed_Datalot1.xlsx")  # Desired output Excel file name

    convert_text_to_excel(input_file, output_file)


if __name__ == "__main__":
    main()
