import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data from the part-00000 file (already containing 5% of orders)
data = pd.read_csv('/root/datavolume1/part-00000', sep='\t', header=None, names=['city', 'quantity_sum', 'timbrecde_sum'])

# Plotting the pie chart
plt.figure(figsize=(10, 8))  # Adjust the size for better readability

# Create a pie chart
wedges, texts, autotexts = plt.pie(
    data['quantity_sum'],
    labels=data['city'],
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 8},  # Adjust text size for readability
    wedgeprops={'edgecolor': 'black'}  # Add edge color to wedges for better separation
)

# Ensure that the pie chart is drawn as a circle
plt.axis('equal')

# Create a legend outside the pie chart
plt.legend(wedges, data['city'], title="Cities", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

# Set a title for the pie chart
plt.title("Distribution of Top 5% Sales by City")

# Save the plot to a PDF
output_pdf_path = os.getenv('OUTPUT_PDF_PATH', '/root/datavolume1/distributionaleatoiredestopdesventes.pdf')
plt.savefig(output_pdf_path, bbox_inches='tight', format='pdf')
plt.close()
