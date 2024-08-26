# Basic Chatbot
A simple chatbot application built in Python with gpt-4o

## Tech stack
1. Python
2. OpenAI
3. ChromaDB

### Dependencies
Please see the `requirements.txt` for complete list of dependencies.

### Diractory Structure
- **data_pipeline**: Contains scripts to load data, persist in database, create embeddings etc
- **retrieval**: Includes different methods to be used for document retrieval based on different techniques.
- **ui**: The user interface elements and front-end related code.
- **resources**: Resources such as data files, images.

### Key Aspects
1. `Langchain` is used to setup RAG based chat bot which provides a simplified interface to perform tasks
2. `RecursiveCharacterTextSplitter` is used to tokenize the dataset with customizable overlap.
3. `Chromadb` (with in memory setup) is used as vector db to store documents. it automatically manages embeddings for the given docs.
4. `Conversational Retrieval Chain` is setup with MMR search strategy and `refine`chain type which makes sequential calls to retrieve dataset with refined prompts
5. `Conversation History` is maintained externally to better extract response with contextual information
6. `panel` python module is used to create user interface.
7. LLM is configured through environment variables. `gpt-4o` is used as default.

## Build && Run
1. Make sure to set environment variable for `OPENAI_API_KEY` i.e `export OPENAI_API_KEY=PROJECT_BASED_OPEN_API_KEY`
2. Execute `./start.sh build` this will download required depenencies defined in `requirements.txt` and start the app in browser. OR
3. Execute `./start.sh` command to start the application (assuming all depdencies are already downloaded).

### Startup flags
The start up command (defined in `start.sh`) uses two extra flags
1. `--autoreload` reloads the changes automatically, suitable for development purpose only 
2. `--show` open up the application in browser automatically
