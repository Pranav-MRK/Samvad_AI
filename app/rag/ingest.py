from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from app.rag.opensearch import create_client, create_knowledge_index


INDEX_NAME = "samvad_knowledge"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

#  load a raw documents from the docs folder

def load_documents() -> list[Document]:
    documents = []

    for path in Path("docs").glob("*.txt"):
        content = path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": path.name,
                    "title": path.stem,
                },
            )
        )

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_documents(documents)


def create_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}, # distance  scores stay consistent during cosine similarity matching.
    )


def index_documents(
    client,
    documents: list[Document],
    embeddings,
):
    for chunk_id, document in enumerate(documents):
        vector = embeddings.embed_query(document.page_content)

        body = {
            "content": document.page_content,
            "embedding": vector,
            "title": document.metadata["title"],
            "source": document.metadata["source"],
            "chunk_id": chunk_id,
        }

        client.index(
            index=INDEX_NAME,
            body=body,
        )

    client.indices.refresh(index=INDEX_NAME)


def main():
    client = create_client()
    create_knowledge_index(client)
    documents = load_documents()

    if not documents:
        raise RuntimeError("No documents found in docs")

    chunks = split_documents(documents)

    embeddings = create_embeddings()

    index_documents(
        client,
        chunks,
        embeddings,
    )

    print(f"Indexed {len(documents)} document(s)")
    print(f"Created {len(chunks)} chunks")


if __name__ == "__main__":
    main()