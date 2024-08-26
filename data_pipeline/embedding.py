from langchain_openai import OpenAIEmbeddings

def get_embedding_function():
    return OpenAIEmbeddings()

def create_embeddings(docs):
    embedding = get_embedding_function()
    
    embeddings = []
    for doc in docs:
        embeddings.extend(embedding.embed_query(str(doc)))

    return embeddings