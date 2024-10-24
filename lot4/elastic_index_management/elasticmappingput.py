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
        "info_codcli": { "type": "long" },
        "info_genrecli": { "type": "keyword" },
        "info_nomcli": { "type": "text" },
        "info_prenomcli": { "type": "text" },
        "info_cpcli": { "type": "keyword" },
        "info_villecli": { "type": "text" },
        "info_codcde": { "type": "integer" },
        "info_datcde": { "type": "date", "format": "yyyy-MM-dd" },
        "info_timbrecli": { "type": "float" },
        "info_timbrecde": { "type": "float" },
        "info_Nbcolis": { "type": "integer" },
        "info_cheqcli": { "type": "float" },
        "info_barchive": { "type": "boolean" },
        "info_bstock": { "type": "boolean" },
        "info_codobj": { "type": "integer" },
        "info_qte": { "type": "integer" },
        "info_Colis": { "type": "integer" },
        "info_libobj": { "type": "text" },
        "info_Tailleobj": { "type": "keyword" },
        "info_Poidsobj": { "type": "float" },
        "info_points": { "type": "integer" },
        "info_indispobj": { "type": "boolean" },
        "info_condit": { "type": "text" },
        "info_rixcond": { "type": "float" },
        "info_uobj": { "type": "float" }
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
