def format_context(results: list[dict]) -> str:
    if not results:
        return "No relevant information was found."

    parts = []

    for i, result in enumerate(results, start=1):
        parts.append(
            f"""Source {i}
Title: {result["title"]}
Source: {result["source"]}
Content:
{result["content"]}
"""
        )

    return "\n\n".join(parts)