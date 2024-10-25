import requests
import json
import random

# Kibana connection details
KIBANA_URL = "http://localhost:5601"  # Your Kibana URL
ES_USER = "elastic"  # Username
ES_PASSWORD = "4Ex79eim"  # Password

# Define headers for Kibana API
headers = {
    "kbn-xsrf": "true",  # Required header for Kibana API requests
    "Content-Type": "application/json"
}

# Step 1: Create the data view for `Lot2DataView`
data_view_payload = {
    "attributes": {
        "title": "Lot2DataView",  # Data view name (same as the index name)
        "timeFieldName": "datcde",  # Date field
        "indexPattern": "my_index"  # The index pattern name
    }
}

# Make the request to create the data view
response_data_view = requests.post(
    f"{KIBANA_URL}/api/saved_objects/index-pattern",
    auth=(ES_USER, ES_PASSWORD),
    headers=headers,
    data=json.dumps(data_view_payload)
)

if response_data_view.status_code == 200:
    print("Data view created successfully!")
else:
    print(f"Failed to create data view: {response_data_view.status_code}")
    print(response_data_view.text)
    # Exit the script if data view creation fails
    exit(1)

# Step 2: Create visualization for pie charts (total and average qte)
visualization_payload = {
  "attributes": {
    "title": "Sales Data (2011-2016) - Average and Total Quantity",  # Visualization title
    "visState": json.dumps({
      "title": "Sales Data (2011-2016)",
      "type": "pie",  # Type of visualization
      "params": {
        "shareYAxis": True,
        "addTooltip": True,
        "addLegend": True,
        "isDonut": False  # Set to True for a donut chart
      },
      "aggs": [
        {
          "id": "1",
          "enabled": True,
          "type": "terms",
          "schema": "segment",
          "params": {
            "field": "city",  # Group by city
            "size": 100  # Show top 100 orders
          }
        },
        {
          "id": "2",
          "enabled": True,
          "type": "avg",
          "schema": "metric",
          "params": {
            "field": "qte"  # Show average quantity per order (avg)
          }
        },
        {
          "id": "3",
          "enabled": True,
          "type": "sum",
          "schema": "metric",
          "params": {
            "field": "qte"  # Show total quantity (sum)
          }
        }
      ],
      "listeners": {}
    }),
    "uiStateJSON": "{}",
    "description": "",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": json.dumps({
        "index": "dataw_fro03",  # The Elasticsearch index (same as the data view)
        "filter": [
          {
            "range": {
              "datcde": {
                "gte": "2011-01-01",
                "lte": "2016-12-31",
                "format": "yyyy-MM-dd"
              }
            }
          },
          {
            "bool": {
              "should": [
                {"prefix": {"cpcli": "22"}},  # Department 22
                {"prefix": {"cpcli": "49"}},  # Department 49
                {"prefix": {"cpcli": "53"}}   # Department 53
              ]
            }
          },
          {
            "bool": {
              "must_not": {
                "exists": {
                  "field": "timbrecli"  # Exclude if timbrecli is missing or zero
                }
              }
            }
          },
          {
            "range": {
              "timbrecli": {
                "lte": 0
              }
            }
          }
        ],
        "query": {
          "query_string": {
            "query": "*"
          }
        }
      })
    }
  }
}

# Make a POST request to save the visualization in Kibana
response_visualization = requests.post(
    f"{KIBANA_URL}/api/saved_objects/visualization",
    auth=(ES_USER, ES_PASSWORD),
    headers=headers,
    data=json.dumps(visualization_payload)
)

# Check if the request was successful
if response_visualization.status_code == 200:
    print("Visualization created successfully!")
else:
    print(f"Failed to create visualization: {response_visualization.status_code}")
    print(response_visualization.text)

# Step 3: Randomly select 5% of the top 100 orders
# Simulate random selection of 5% of the top 100 orders (for illustration purposes)
top_100_orders = list(range(1, 101))  # Assuming we have the top 100 orders indexed
random_selection = random.sample(top_100_orders, k=int(0.05 * len(top_100_orders)))

print(f"Randomly selected 5% of top 100 orders: {random_selection}")
