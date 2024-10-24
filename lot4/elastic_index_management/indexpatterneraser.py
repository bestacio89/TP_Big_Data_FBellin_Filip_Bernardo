import requests
from requests.auth import HTTPBasicAuth


def get_all_indexes(es_url, user, password):
    """Retrieve all indexes from the Elasticsearch cluster."""
    response = requests.get(f"{es_url}/_cat/indices?format=json", auth=HTTPBasicAuth(user, password))
    if response.status_code == 200:
        indexes = response.json()
        return [index['index'] for index in indexes]
    else:
        print(f"Error fetching indexes: {response.status_code} - {response.content}")
        return []


def delete_index(es_url, user, password, index_name):
    """Delete a specified index from Elasticsearch."""
    response = requests.delete(f"{es_url}/{index_name}", auth=HTTPBasicAuth(user, password))
    if response.status_code == 200:
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Error deleting index '{index_name}': {response.status_code} - {response.content}")


def delete_all_data_indexes(es_url, user, password):
    """Delete all data indexes from the Elasticsearch cluster."""
    indexes = get_all_indexes(es_url, user, password)

    if indexes:
        print(f"Found {len(indexes)} indexes. Deleting...")
        for index in indexes:
            delete_index(es_url, user, password, index)
        print("All indexes have been deleted.")
    else:
        print("No indexes found.")


if __name__ == "__main__":
    ES_URL = "http://localhost:9200"  # Change to your Elasticsearch URL
    ES_USER = "elastic"  # Replace with your username
    ES_PASSWORD = "4Ex79eim"  # Replace with your password

    delete_all_data_indexes(ES_URL, ES_USER, ES_PASSWORD)
