from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are SamvadAI, an enterprise college admission assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not invent information.
- If the context does not contain enough information, say that you do not have enough information.
- Do not use outside knowledge.
- Give a clear and concise answer.
- Do not mention the retrieval system or internal architecture.

Context:
{context}
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


chain = prompt | llm

def generate_answer(
    question: str,
    context: str,
) -> str:
    response = chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    # pyrefly: ignore [bad-return]
    return response.content


