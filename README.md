# ResolveIQ

ResolveIQ is an AI-powered Retrieval-Augmented Generation (RAG) system
that answers application-related questions using internal documentation
as a knowledge base. It helps testers, junior developers, and new team
members resolve issues quickly without relying on senior developers.

------------------------------------------------------------------------

## Purpose

ResolveIQ reduces developer dependency bottlenecks by:

-   Providing instant answers from application documentation\
-   Assisting QA teams during testing\
-   Helping freshers understand system architecture\
-   Automating knowledge transfer

------------------------------------------------------------------------

## Core Concept

ResolveIQ uses Retrieval-Augmented Generation:

1.  Documents are ingested into a vector database\
2.  Queries retrieve relevant chunks\
3.  LLM generates answers grounded in retrieved context

------------------------------------------------------------------------

## Tech Stack

-   Python\
-   OpenAI API\
-   LangChain\
-   ChromaDB\
-   UV Package Manager

------------------------------------------------------------------------

## Features

-   Autonomous Question Answering Agent\
-   Context-aware responses\
-   Multi-document ingestion\
-   Vector similarity search\
-   Modular architecture\
-   Easily extensible

------------------------------------------------------------------------

## Project Structure

    .
    ├── config.py
    ├── constants.py
    ├── core.py
    ├── ingest.py
    ├── main.py
    ├── prompts.py
    ├── pydantic_store.py
    ├── knowledge-base/
    │   └── UOIAM/
    │       └── Application Architecture & Design Document.docx
    ├── preprocess_db/
    ├── vector_db/
    ├── requirement.txt
    ├── pyproject.toml
    └── uv.lock

------------------------------------------------------------------------

## Installation & Setup

### 1. Install dependencies

``` bash
uv pip install -r requirement.txt
```

------------------------------------------------------------------------

### 2. Add OpenAI API Key

Create a `.env` file:

    OPENAI_API_KEY=your_key_here

Ensure your OpenAI account has credits.

------------------------------------------------------------------------

### 3. Add Documents

Place application documents inside:

    knowledge-base/<ApplicationName>/

Multiple documents are supported.

------------------------------------------------------------------------

### 4. Ingest Documents

``` bash
python ingest.py
```

Builds Chroma vector database.

------------------------------------------------------------------------

### 5. Run Application

``` bash
python main.py
```

Start asking questions.

------------------------------------------------------------------------

## Architecture Flow

User Query → Retriever → Vector DB → Context → LLM → Answer

------------------------------------------------------------------------

## Future Improvements

-   LangGraph agent workflow integration\
-   UI dashboard\
-   Multi-user support\
-   Analytics logging\
-   Role-based responses\
-   Streaming output\
-   Docker deployment

------------------------------------------------------------------------

## Use Cases

-   QA debugging\
-   Developer onboarding\
-   Production support\
-   Documentation search\
-   Incident investigation

------------------------------------------------------------------------

## Security Notes

-   Never commit `.env`
-   Keep API keys private
-   Use `.gitignore`

------------------------------------------------------------------------

## License

MIT

------------------------------------------------------------------------

## Author

Abhishek Khamkar

------------------------------------------------------------------------

## Why ResolveIQ?

Developer time is expensive.\
ResolveIQ turns documentation into an intelligent assistant.
