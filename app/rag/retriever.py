from app.rag.opensearch import create_client
from app.rag.embeddings import create_embedding


INDEX_NAME = "samvad_knowledge"


class KnowledgeRetriever:
    def __init__(self):
        self.client = create_client()

    def search_bm25(self, query: str, k: int = 5):
        response = self.client.search(
            index=INDEX_NAME,
            body={
                "size": k,
                "query": {
                    "match": {
                        "content": query
                    }
                }
            },
        )

        return self._extract_results(response)


    def search_semantic(self, query: str, k: int = 5):
        query_embedding = create_embedding(query)

        response = self.client.search(
            index=INDEX_NAME,
            body={
                "size": k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": query_embedding,
                            "k": k,
                        }
                    }
                },
            },
        )

        return self._extract_results(response)

    def hybrid_search(self, query: str, k: int = 3):
        bm25_results = self.search_bm25(query, k)
        semantic_results = self.search_semantic(query, k)

        rrf_scores = {}
        documents = {}

        rrf_k = 60

        for rank, result in enumerate(bm25_results, start=1):
            doc_id = result["id"]

            rrf_scores[doc_id] = (
                # pyrefly: ignore [unsupported-operation]
                rrf_scores.get(doc_id, 0)
                + 1 / (rrf_k + rank)
            )

            documents[doc_id] = result

        for rank, result in enumerate(semantic_results, start=1):
            doc_id = result["id"]

            rrf_scores[doc_id] = (
                # pyrefly: ignore [unsupported-operation]
                rrf_scores.get(doc_id, 0)
                + 1 / (rrf_k + rank)
            )

            documents[doc_id] = result

        # pyrefly: ignore [no-matching-overload]
        ranked_ids = sorted(
            rrf_scores,
            key=rrf_scores.get,
            reverse=True,
        )

        results = []

        for doc_id in ranked_ids[:k]:
            result = documents[doc_id].copy()
            result["rrf_score"] = rrf_scores[doc_id]
            results.append(result)

        return results    


    @staticmethod
    def _extract_results(response):
        results = []

        for hit in response["hits"]["hits"]:
            results.append(
                {
                    "id": hit["_id"],
                    "score": hit["_score"],
                    "content": hit["_source"]["content"],
                    "title": hit["_source"].get("title", ""),
                    "source": hit["_source"].get("source", ""),
                }
            )

        return results         
    