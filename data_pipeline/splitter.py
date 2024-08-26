from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter

def split_by_recursive_splitter(docs, chunk_size, chunk_overlap):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\\n\\n", "\\n", "(?<=\\. )", " ", ""]
    )

    splits = splitter.split_documents(docs)

    print('Split count: ', len(splits))

    return splits

def split_by_token(docs, chunk_size, chunk_overlap):
    text_splitter = TokenTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
    return text_splitter.split_documents(docs)
