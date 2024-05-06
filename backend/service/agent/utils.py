import json


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def escape_str(normal_str: str):
    return  json.dumps(normal_str)

