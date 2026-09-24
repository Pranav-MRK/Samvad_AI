# from app.agent.graph import agent


# result = agent.invoke({
#     "user_input": "What is my application status??",
#     "intent": "",
#     "context": "",
#     "tool_result": "",
#     "response": "",
#     "confidence": 0.0,
# })

# print(result)


# from app.rag.embeddings import create_embedding


# text = "What documents are required for admission?"

# embedding = create_embedding(text)

# print("Embedding dimensions:", len(embedding))
# print("First 5 values:", embedding[:5])







# from app.rag.retriever import KnowledgeRetriever


# retriever = KnowledgeRetriever()

# query = "Which papers do I need for B.Tech admission?"


# print("\n========== BM25 ==========")

# bm25_results = retriever.search_bm25(query)

# for result in bm25_results:
#     print("Title:", result["title"])
#     print("Score:", result["score"])
#     print("Source:", result["source"])
#     print()


# print("\n======= SEMANTIC =========")

# semantic_results = retriever.search_semantic(query)

# for result in semantic_results:
#     print("Title:", result["title"])
#     print("Score:", result["score"])
#     print("Source:", result["source"])
#     print()

from app.rag.retriever import KnowledgeRetriever


retriever = KnowledgeRetriever()


queries = [
    "Which documents do I need for B.Tech admission?",
    "What papers should I submit?",
    "Do I need an income certificate for a scholarship?",
    "What should I do if I cannot upload my documents?",
]


for query in queries:
    print("\n" + "=" * 60)
    print("QUERY:", query)
    print("=" * 60)

    results = retriever.hybrid_search(query, k=3)

    for rank, result in enumerate(results, start=1):
        print(f"\nRank {rank}")
        print("Title:", result["title"])
        print("Chunk:", result["chunk_id"])
        print("RRF Score:", result["rrf_score"])
        print("Content:", result["content"][:250])