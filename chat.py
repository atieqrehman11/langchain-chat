import os

from data_pipeline import create_database
from retrieval import retrieve_by_refine_chain_type
# from logger import pretty_print_docs

llm_name = os.environ.get('LLM_MODEL')
def main():
    print ("Calling Data Pipeline")
    db = create_database()

    retriever = get_retriever(db, llm_name, 'refine')

    question = "what did they say about matlab?"
    response = retrieve_by_refine_chain_type(db, question)

    print('\n\nRetrieved Response\n\n', response["result"])
    
    print('\n\nReferences:\n\n', response["source_documents"])

main()