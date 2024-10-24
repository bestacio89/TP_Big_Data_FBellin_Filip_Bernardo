from elasticsearch import Elasticsearch

# Elasticsearch connection details
ES_HOST = 'http://localhost:9200'
INDEX_NAME = 'dataw_fro03'  # Index name to be deleted
ES_USER = 'elastic'
ES_PASSWORD = '4Ex79eim'

# Create Elasticsearch client with authentication
es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USER, ES_PASSWORD)
)

try:
    # Check if the index exists
    if es.indices.exists(index=INDEX_NAME):
        # Delete the index
        es.indices.delete(index=INDEX_NAME)
        print(f"Index '{INDEX_NAME}' deleted successfully.")
    else:
        print(f"Index '{INDEX_NAME}' does not exist.")
except Exception as e:
    print(f"Error deleting index: {e}")
