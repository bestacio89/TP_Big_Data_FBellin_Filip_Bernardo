import csv
import happybase
import pandas as pd
import matplotlib.pyplot as plt


# HBase Connection
def create_hbase_table():
    connection = happybase.Connection('localhost')  # Adjust this if needed
    table_name = 'dataw_fro'

    try:
        # Check if the table exists
        if table_name.encode() in connection.tables():
            print("Table '{}' already exists. Deleting the table...".format(table_name))
            connection.delete_table(table_name, disable=True)  # Disable before deleting
            print("Table '{}' deleted successfully.".format(table_name))

        # Now create the table again
        connection.create_table(
            table_name,
            {'info': dict()}  # Define column family 'info'
        )
        print("Table '{}' created successfully.".format(table_name))

    except happybase.hbase.ttypes.AlreadyExists:
        print("Table '{}' already exists.".format(table_name))
    except Exception as e:
        print("An error occurred while creating the table: {}".format(e))
        raise e  # Re-raise the exception if it isn't a known issue

    return connection

def insert_data_into_hbase(connection):
    table = connection.table('dataw_fro')

    # Open the cleaned CSV file
    with open('../data/dataw_fro03/cleaneddata.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        count = 0  # Initialize a counter

        for row in reader:
            # Construct rowkey using 'codcli' and 'codcde'
            rowkey = "{}-{}".format(row['codcli'], row['codcde'])

            # Create a dictionary for HBase data
            data = {
                'info:{}'.format(key): value.encode()
                for key, value in row.items()
            }

            # Insert data into HBase
            table.put(rowkey, data)
            count += 1  # Increment the counter

            # Print a message every 100 rows
            if count % 100 == 0:
                print("Inserted {} rows into HBase...".format(count))

    print("Data inserted into HBase.")
    connection.close()


# Data Query from HBase and Visualization
def query_hbase_data():
    connection = happybase.Connection('localhost', 9090)  # Adjust if needed
    table = connection.table('dataw_fro')

    # Question 1: Best order from Nantes in 2020
    rows = table.scan(filter=(
        "SingleColumnValueFilter('info', 'datcde', =, 'binary:2020-01-01') AND "
        "SingleColumnValueFilter('info', 'villecli', =, 'binary:Nantes')"
    ))

    best_order = max(rows, key=lambda row: int(row[1][b'info:qte'].decode()), default=None)
    if best_order:
        print("Best order from Nantes in 2020: {}".format(best_order))
    else:
        print("No order found for Nantes in 2020.")

    # Question 2: Total number of orders from 2010 to 2015 by year
    results = {}
    for year in range(2010, 2016):
        rows = table.scan(filter=(
            "SingleColumnValueFilter('info', 'datcde', >=, 'binary:{}-01-01') AND "
            "SingleColumnValueFilter('info', 'datcde', <=, 'binary:{}-12-31')".format(year, year)
        ))
        results[year] = sum(1 for _ in rows)

    # Generate Barplot for Question 2
    plt.bar(results.keys(), results.values())
    plt.xlabel("Year")
    plt.ylabel("Number of Orders")
    plt.title("Total Orders from 2010 to 2015")
    plt.savefig("orders_by_year.pdf")  # Export barplot to PDF

    # Question 3: Client with the most 'timbrecde' fees
    client_fees = {}
    for key, data in table.scan():
        codcli = data[b'info:codcli'].decode()
        timbrecde = float(data[b'info:timbrecde'].decode())
        client_fees[codcli] = client_fees.get(codcli, 0) + timbrecde

    # Find the client with the maximum 'timbrecde' fees
    top_client = max(client_fees.items(), key=lambda x: x[1], default=None)
    if top_client:
        print("Client with most 'timbrecde' fees: {} with {:.2f} in fees.".format(top_client[0], top_client[1]))
    else:
        print("No data for 'timbrecde' fees found.")

    connection.close()
    return client_fees


# Exporting Data
def export_data_to_excel(client_fees):
    # Export the top client data to an Excel file
    df = pd.DataFrame(list(client_fees.items()), columns=['Client', 'Fees'])
    df.to_excel('client_fees.xlsx', index=False)
    print("Client fees exported to Excel.")


def main():
    # Step 1: Create HBase table and Insert Data
    connection = create_hbase_table()
    insert_data_into_hbase(connection)

    # Step 2: Query HBase and generate outputs
    client_fees = query_hbase_data()

    # Step 3: Export data to Excel and CSV
    export_data_to_excel(client_fees)


if __name__ == "__main__":
    main()
