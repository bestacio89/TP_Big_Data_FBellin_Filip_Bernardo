import requests
import json
import random

# Kibana connection details
KIBANA_URL = "http://localhost:5601"
ES_USER = "elastic"
ES_PASSWORD = "4Ex79eim"

# Define headers for Kibana API
headers = {
    "kbn-xsrf": "true",
    "Content-Type": "application/json"
}

# Step 1: Create the data view
data_view_payload = {
    "attributes": {
        "title": "Lot2DataView",
        "timeFieldName": "datcde",
        "indexPattern": "dataw_fro03"
    }
}

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
    exit(1)

# Step 2: Create visualizations and save their IDs
visualization_ids = []

# Visualization payload example (repeat for each visualization you want)
visualization_payloads = [
    {
        "attributes": {
            "title": "Top 100 Sales - Departments 53, 61, 28 (2006-2010)",
            "visState": json.dumps({
                "title": "Top 100 Sales",
                "type": "table",
                "params": {"perPage": 100, "showMetricsAtAllLevels": False},
                "aggs": [
                    {
                        "id": "1", "enabled": True, "type": "terms", "schema": "bucket",
                        "params": {"field": "codcde", "size": 100, "order": "desc", "orderBy": "2"}
                    },
                    {"id": "2", "enabled": True, "type": "sum", "schema": "metric", "params": {"field": "qte"}},
                    {"id": "3", "enabled": True, "type": "sum", "schema": "metric", "params": {"field": "timbrecde"}}
                ]
            }),
            "uiStateJSON": "{}", "description": "", "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": "dataw_fro03", "query": {"query_string": {"query": "*"}}
                })
            }
        }
    },
    {
        "attributes": {
            "title": "Sales Data (2011-2016) - Average and Total Quantity",
            "visState": json.dumps({
                "title": "Sales Data (2011-2016)", "type": "pie", "params": {"addTooltip": True, "addLegend": True},
                "aggs": [
                    {"id": "1", "enabled": True, "type": "terms", "schema": "segment", "params": {"field": "city"}},
                    {"id": "2", "enabled": True, "type": "avg", "schema": "metric", "params": {"field": "qte"}},
                    {"id": "3", "enabled": True, "type": "sum", "schema": "metric", "params": {"field": "qte"}}
                ]
            }),
            "uiStateJSON": "{}", "description": "", "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "index": "dataw_fro03", "query": {"query_string": {"query": "*"}}
                })
            }
        }
    }
]

# Post each visualization
for payload in visualization_payloads:
    response = requests.post(
        f"{KIBANA_URL}/api/saved_objects/visualization",
        auth=(ES_USER, ES_PASSWORD),
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        vis_id = response.json()["_id"]
        visualization_ids.append(vis_id)
        print(f"Visualization '{payload['attributes']['title']}' created with ID: {vis_id}")
    else:
        print(f"Failed to create visualization '{payload['attributes']['title']}': {response.status_code}")
        print(response.text)

# Step 3: Create a dashboard and add visualizations by ID
dashboard_payload = {
    "attributes": {
        "title": "Sales Dashboard",
        "hits": 0,
        "description": "Dashboard for analyzing sales data.",
        "panelsJSON": json.dumps([
            {"panelIndex": str(i + 1), "gridData": {"x": i % 6 * 6, "y": (i // 6) * 6, "w": 6, "h": 6, "i": str(i + 1)},
             "type": "visualization", "id": vis_id, "version": "7.0.0"}
            for i, vis_id in enumerate(visualization_ids)
        ]),
        "optionsJSON": "{}",
        "version": 1,
        "kibanaSavedObjectMeta": {"searchSourceJSON": "{\"query\":{\"language\":\"kuery\",\"query\":\"\"}}"}
    }
}

response_dashboard = requests.post(
    f"{KIBANA_URL}/api/saved_objects/dashboard",
    auth=(ES_USER, ES_PASSWORD),
    headers=headers,
    data=json.dumps(dashboard_payload)
)

if response_dashboard.status_code == 200:
    dashboard_id = response_dashboard.json()["_id"]
    print(f"Dashboard created successfully with ID: {dashboard_id}")
else:
    print(f"Failed to create dashboard: {response_dashboard.status_code}")
    print(response_dashboard.text)
