from opensearchpy import OpenSearch

def create_client():
    return OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        use_ssl=False,
        verify_certs=False,
    )


def create_knowledge_index(client):
    index_name = "samvad_knowledge"
    
    if client.indices.exists(index=index_name):
        return

    index_body={
        "settings":{
            "index": {
                "knn": True
            }     
        },
        "mappings": {
            "properties": {
                "content": {
                    "type": "text"
                },
                "embedding": {
                    "type": "knn_vector",
                    "dimension": 384
                },
                "source": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text"
                }
            }
        }
    }     
    client.indices.create(
        index=index_name,
        body=index_body,
    )

if __name__ == "__main__":
    client = create_client()

    create_knowledge_index(client)
    print("OpenSearch knowledge index is ready")



