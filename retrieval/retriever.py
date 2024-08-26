import os

from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, ConversationalRetrievalChain

llm_name = os.environ.get('LLM_MODEL')

def retrieve_relavent_docs_by_self_query(db, llm, question):
    metadata = [
        AttributeInfo(
            name="source",
            description="The lecture the chunk is from, should be one of `docs/pdfs/MachineLearning-Lecture01.pdf`, `docs/pdfs/MachineLearning-Lecture02.pdf`, or `docs/pdfs/MachineLearning-Lecture03.pdf`",
            type="string",
        ),
        AttributeInfo(
            name="page",
            description="The page from the lecture",
            type="integer",
        ),
    ]
        
    document_content_description = "Lecture notes"    
    retriever = SelfQueryRetriever.from_llm(
        llm,
        db,
        document_content_description,
        metadata,
        verbose=True
    )

    return retriever.get_relevant_documents(question)


def retrieve_relavent_docs_by_compression(db, llm, question):
    compressor = LLMChainExtractor.from_llm(llm)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=db.as_retriever(search_type = "mmr")
    )

    return compression_retriever.get_relevant_documents(question)

def retrieve_by_refine_chain_type(db, question):
    llm = ChatOpenAI(model_name=llm_name, temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=db.as_retriever(),
        return_source_documents=True,
        chain_type="refine"
    )

    return qa_chain({"query": question})

def get_retriever(db, llm_name, chain_type, k):
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": k})
    
    # create a chatbot chain. Memory is managed externally.
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0), 
        chain_type=chain_type, 
        retriever=retriever, 
        return_source_documents=True,
        return_generated_question=True,
    )

    return qa 
