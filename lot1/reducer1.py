#!/usr/bin/env python
import sys
import heapq

def reducer():
    current_key = None  # To track the current 'codcde' (order code)
    current_city = None  # To store the city associated with the current 'codcde'
    total_quantity = 0  # To accumulate the total quantity for each 'codcde'
    total_timbrecde = 0.0  # To accumulate the total 'timbrecde' for each 'codcde'
    top_orders = []  # A heap to store the top 100 best orders

    # Read input lines from the mapper (each line corresponds to a single 'codcde' entry)
    for line in sys.stdin:
        try:
            key, value = line.strip().split("\t")
            quantity, timbrecde, city = value.split(",")
            quantity = float(quantity)
            timbrecde = float(timbrecde)
        except ValueError:
            continue  # Skip any malformed lines

        # If still processing the same 'codcde', aggregate the data
        if current_key == key:
            total_quantity += quantity
            total_timbrecde += timbrecde
        else:
            # Push the aggregated data for the previous 'codcde' into the heap
            if current_key:
                heapq.heappush(top_orders, (total_quantity, round(total_timbrecde, 2), current_key, current_city))
                if len(top_orders) > 100:
                    heapq.heappop(top_orders)  # Ensure the heap only contains the top 100 orders

            # Start processing the new 'codcde'
            current_key = key
            current_city = city
            total_quantity = quantity
            total_timbrecde = timbrecde

    # Add the last 'codcde' after reading all lines
    if current_key:
        heapq.heappush(top_orders, (total_quantity, round(total_timbrecde, 2), current_key, current_city))
        if len(top_orders) > 100:
            heapq.heappop(top_orders)

    # Sort the top orders by total quantity first, then by 'timbrecde'
    top_orders = sorted(top_orders, reverse=True)

    # Output the top 100 orders in the required format
    print("Rank\tCodcde\tCity\tQuantity Sum\tTimbrecde Sum")
    for i, (quantity, timbrecde, key, city) in enumerate(top_orders, start=1):
        print("{}\t{}\t{}\t{}\t{}".format(i, key, city, quantity, timbrecde))


if __name__ == "__main__":
    reducer()
