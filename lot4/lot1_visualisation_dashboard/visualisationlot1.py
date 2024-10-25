import requests
import json

# Kibana connection details
KIBANA_URL = "http://localhost:5601"  # Your Kibana URL
ES_USER = "elastic"  # Username
ES_PASSWORD = "4Ex79eim"  # Password

# Define headers for Kibana API
headers = {
    "kbn-xsrf": "true",  # Required header for Kibana API requests
    "Content-Type": "application/json"
}

# Step 1: Create the data view for `dataw_fro03`
data_view_payload = {
    "attributes": {
        "title": "DataTestVis",  # Data view name (same as the index name)
        "timeFieldName": "datcde",  # Replace with your actual date field
        "IndexPattern": "dataw_fro03"  # The index pattern name
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

# Step 2: Create visualization for top 100 sales
visualization_payload = {
  "attributes": {
    "title": "Top 100 Sales - Departments 53, 61, 28 (2006-2010)",  # Visualization title
    "visState": json.dumps({
      "title": "Top 100 Sales",
      "type": "table",  # Type of visualization (could be bar, line, etc.)
      "params": {
        "perPage": 100,  # Show top 100 sales
        "showMetricsAtAllLevels": False,
        "showPartialRows": False,
        "showTotal": False,
        "totalFunc": "sum"
      },
      "aggs": [
        {
          "id": "1",
          "enabled": True,
          "type": "terms",
          "schema": "bucket",
          "params": {
            "field": "codcde",  # Group by sale code
            "size": 100,  # Top 100
            "order": "desc",
            "orderBy": "2"
          }
        },
        {
          "id": "2",
          "enabled": True,
          "type": "sum",
          "schema": "metric",
          "params": {
            "field": "qte"  # Replace with your quantity field
          }
        },
        {
          "id": "3",
          "enabled": True,
          "type": "sum",
          "schema": "metric",
          "params": {
            "field": "timbrecde"  # Replace with your timbrecde field
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
        "index": "DataTestVis",  # The Elasticsearch index
        "filter": [
          {
            "range": {
              "datcde": {
                "gte": "2006-01-01",
                "lte": "2010-12-31",
                "format": "yyyy-MM-dd"
              }
            }
          },
          {
            "bool": {
              "should": [
                {"prefix": {"cpcli": "53"}},
                {"prefix": {"cpcli": "61"}},
                {"prefix": {"cpcli": "28"}}
              ]
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
