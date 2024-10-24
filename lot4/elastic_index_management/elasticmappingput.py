from elasticsearch import Elasticsearch

# Elasticsearch connection details
ES_HOST = 'http://localhost:9200'
INDEX_NAME = 'dataw_fro03'  # Index name in Elasticsearch
ES_USER = 'elastic'
ES_PASSWORD = '4Ex79eim'

# Create Elasticsearch client with authentication
es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USER, ES_PASSWORD)
)

# Define the mapping for the index
mapping = {
    "properties": {
        "codcli": { "type": "long" },
        "genrecli": { "type": "keyword" },
        "nomcli": { "type": "text" },
        "prenomcli": { "type": "text" },
        "cpcli": { "type": "keyword" },
        "villecli": { "type": "text" },
        "codcde": { "type": "integer" },
        "datcde": { "type": "date", "format": "yyyy-MM-dd" },
        "timbrecli": { "type": "float" },
        "timbrecde": { "type": "float" },
        "Nbcolis": { "type": "integer" },
        "cheqcli": { "type": "float" },
        "barchive": { "type": "boolean" },
        "bstock": { "type": "boolean" },
        "codobj": { "type": "integer" },
        "qte": { "type": "integer" },
        "Colis": { "type": "integer" },
        "libobj": { "type": "text" },
        "Tailleobj": { "type": "keyword" },
        "Poidsobj": { "type": "float" },
        "points": { "type": "integer" },
        "indispobj": { "type": "boolean" },
        "libcondit": { "type": "text" },
        "prixcond": { "type": "float" },
        "puobj": { "type": "float" }
    }
}

try:
    # Check if the index already exists
    if not es.indices.exists(index=INDEX_NAME):
        # Create the index with the specified mapping
        es.indices.create(index=INDEX_NAME, body={"mappings": mapping})
        print(f"Index '{INDEX_NAME}' created successfully with the provided mapping.")
    else:
        # Update the existing index's mapping
        es.indices.put_mapping(index=INDEX_NAME, body=mapping)
        print(f"Index '{INDEX_NAME}' already exists. Mapping updated successfully.")
except Exception as e:
    print(f"Error processing index: {e}")
