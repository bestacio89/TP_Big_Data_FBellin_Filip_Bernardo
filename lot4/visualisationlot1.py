import requests
import json

# Configuration
KIBANA_URL = 'http://localhost:5601'  # Replace with your Kibana URL
KIBANA_USER = 'elastic'
KIBANA_PASSWORD = '4Ex79eim'  # Your Kibana password
INDEX_PATTERN = 'dataw_fro03'  # Your actual index pattern

# Function to create a visualization
def create_visualization(title, vis_type, aggs, params, visualization_id=None, query=None):
    url = f"{KIBANA_URL}/api/saved_objects/visualization"
    headers = {
        "kbn-xsrf": "true",
        "Content-Type": "application/json"
    }

    # Building the searchSourceJSON with a query (optional)
    search_source_json = {
        "index": INDEX_PATTERN,
        "query": {
            "query": query,  # Replace with your actual KQL query (optional)
            "language": "kuery"  # Default query language
        },
        "filter": []  # Add any specific filters if needed
    }

    data = {
        "attributes": {
            "title": title,
            "visState": json.dumps({
                "title": title,
                "type": vis_type,
                "params": params,
                "aggs": aggs
            }),
            "searchSourceJSON": json.dumps(search_source_json),
            "uiStateJSON": "{}",
            "version": 1
        }
    }

    if visualization_id:
        data["id"] = visualization_id

    response = requests.post(url, headers=headers, json=data, auth=(KIBANA_USER, KIBANA_PASSWORD))

    if response.status_code == 200:
        print(f"Visualization '{title}' created successfully.")
        return response.json()  # Return the created visualization object
    else:
        print(f"Error creating visualization '{title}': {response.text}")
        return None

# Function to create a dashboard
def create_dashboard(title, visualizations):
    url = f"{KIBANA_URL}/api/saved_objects/dashboard"
    headers = {
        "kbn-xsrf": "true",
        "Content-Type": "application/json"
    }
    data = {
        "attributes": {
            "title": title,
            "panelsJSON": json.dumps(visualizations),
            "version": 1
        }
    }

    response = requests.post(url, headers=headers, json=data, auth=(KIBANA_USER, KIBANA_PASSWORD))

    if response.status_code == 200:
        print(f"Dashboard '{title}' created successfully.")
    else:
        print(f"Error creating dashboard '{title}': {response.text}")

# Create the visualizations
visualizations = []

# Create the Total Quantity visualization
total_quantity_aggs = [
    {
        "id": "1",
        "enabled": True,
        "type": "sum",
        "schema": "metric",
        "params": {
            "field": "qte"  # Replace with your actual quantity field
        }
    },
    {
        "id": "2",
        "enabled": True,
        "type": "terms",
        "schema": "group",
        "params": {
            "field": "villecli.keyword",  # Replace with your city field
            "size": 100,
            "order": "desc",
            "orderBy": "1"
        }
    }
]
total_quantity_vis = create_visualization("Total Quantity by City", "bar", total_quantity_aggs, {}, query="index:dataw_fro03")
if total_quantity_vis:
    visualizations.append({
        "version": 1,
        "panelIndex": "1",
        "gridData": {"x": 0, "y": 0, "w": 12, "h": 15},  # Adjust grid as needed
        "id": total_quantity_vis['id'],
        "type": "visualization"
    })

# Create the Total Timbrecde visualization
total_timbrecde_aggs = [
    {
        "id": "1",
        "enabled": True,
        "type": "sum",
        "schema": "metric",
        "params": {
            "field": "timbrecde"  # Replace with your actual timbrecde field
        }
    },
    {
        "id": "2",
        "enabled": True,
        "type": "terms",
        "schema": "group",
        "params": {
            "field": "villecli.keyword",  # Replace with your city field
            "size": 100,
            "order": "desc",
            "orderBy": "1"
        }
    }
]
total_timbrecde_vis = create_visualization("Total Timbrecde by City", "bar", total_timbrecde_aggs, {}, query="index:dataw_fro03")
if total_timbrecde_vis:
    visualizations.append({
        "version": 1,
        "panelIndex": "2",
        "gridData": {"x": 0, "y": 15, "w": 12, "h": 15},  # Adjust grid as needed
        "id": total_timbrecde_vis['id'],
        "type": "visualization"
    })

# Create the dashboard
create_dashboard("Best Orders Dashboard", visualizations)