import requests
from requests.auth import HTTPBasicAuth


def get_all_visualizations(kibana_url, user, password):
    """Retrieve all visualizations from Kibana."""
    headers = {
        "kbn-xsrf": "true",  # Required by Kibana API
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{kibana_url}/api/saved_objects/_find?type=visualization&per_page=10000",
        headers=headers,
        auth=HTTPBasicAuth(user, password)
    )

    if response.status_code == 200:
        visualizations = response.json()
        return visualizations['saved_objects']
    else:
        print(f"Error fetching visualizations: {response.status_code} - {response.content}")
        return []


def delete_visualization(kibana_url, user, password, visualization_id):
    """Delete a specified visualization from Kibana."""
    headers = {
        "kbn-xsrf": "true",  # Required by Kibana API
        "Content-Type": "application/json"
    }

    response = requests.delete(
        f"{kibana_url}/api/saved_objects/visualization/{visualization_id}",
        headers=headers,
        auth=HTTPBasicAuth(user, password)
    )

    if response.status_code == 200:
        print(f"Visualization '{visualization_id}' deleted successfully.")
    else:
        print(f"Error deleting visualization '{visualization_id}': {response.status_code} - {response.content}")


def delete_all_visualizations(kibana_url, user, password):
    """Delete all visualizations from Kibana."""
    visualizations = get_all_visualizations(kibana_url, user, password)

    if visualizations:
        print(f"Found {len(visualizations)} visualizations. Deleting...")
        for viz in visualizations:
            delete_visualization(kibana_url, user, password, viz['id'])
        print("All visualizations have been deleted.")
    else:
        print("No visualizations found.")


if __name__ == "__main__":
    KIBANA_URL = "http://localhost:5601"  # Change to your Kibana URL
    ES_USER = "elastic"  # Replace with your username
    ES_PASSWORD = "4Ex79eim"  # Replace with your password

    delete_all_visualizations(KIBANA_URL, ES_USER, ES_PASSWORD)
