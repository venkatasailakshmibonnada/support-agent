# Persona-Adaptive Customer Support Agent

## Project Overview
An intelligent customer support agent that automatically detects customer personas and adapts its response tone accordingly. Built with RAG (Retrieval-Augmented Generation), it retrieves relevant information from a knowledge base and escalates to human support when needed.

## Tech Stack
- Python 3.14
- Streamlit (UI)
- Ollama + LLaMA 3.2 (Local LLM - Free)
- ChromaDB (Vector Database)
- LangChain Community (Document Loading, Text Splitting)
- Sentence Transformers - all-MiniLM-L6-v2 (Embeddings)
- PyPDF (PDF Loading)

## Architecture
User Query

↓

Persona Detection (LLaMA 3.2)

↓

RAG Retrieval (ChromaDB Vector Search)

↓

Adaptive Response Generation (LLaMA 3.2)

↓

Escalation Check

↓

Response / Human Handoff Summary

## Persona Detection Strategy
The system classifies users into 3 personas using LLaMA 3.2:
- TECHNICAL_EXPERT: Uses technical terms, asks about APIs/logs/configs
- FRUSTRATED_USER: Emotional language, complaints, urgent tone
- BUSINESS_EXECUTIVE: Outcome-focused, asks about impact/timeline

## RAG Pipeline Design
- Chunking: RecursiveCharacterTextSplitter (chunk_size=500, overlap=50)
- Embedding Model: sentence-transformers/all-MiniLM-L6-v2
- Vector Database: ChromaDB (local persistent storage)
- Retrieval: Top-4 similar chunks using cosine similarity

## Escalation Logic
Escalation triggers:
- No relevant documents found in knowledge base
- Low retrieval confidence (score > 1.2)
- Sensitive keywords detected (billing, refund, legal, fraud)
- User dissatisfied for 2+ consecutive turns

## Setup Instructions

### 1. Clone the repository
`ash
git clone https://github.com/YOUR_USERNAME/support-agent.git
cd support-agent
`

### 2. Create virtual environment
`ash
python -m venv venv
venv\Scripts\activate
`

### 3. Install dependencies
`ash
python -m pip install -r requirements.txt
`

### 4. Install and start Ollama
Download from https://ollama.com
`ash
ollama pull llama3.2
ollama serve
`

### 5. Ingest knowledge base
`ash
python ingest.py
`

### 6. Run the app
`ash
python -m streamlit run app.py
`

## Environment Variables
No API keys required - uses free local Ollama LLM.
Optional: Create .env file with:
ANTHROPIC_API_KEY=your_key_here

## Example Queries

1. Technical Expert:
   "Can you explain the OAuth token expiry and how to refresh it using the API?"

2. Frustrated User:
   "I've tried everything and nothing works! I cannot log in at all!"

3. Business Executive:
   "What is the business impact of a P1 outage and when will it be resolved?"

4. Escalation trigger:
   "I need a refund for my last invoice, this is unacceptable"

5. General support:
   "How do I reset my password? The reset email is not coming through."

## Knowledge Base Documents
- account_management.md
- api_authentication_guide.md
- billing_policy.md
- data_privacy_guide.md
- error_codes.md
- integrations_guide.md
- onboarding_guide.md
- password_reset_guide.md
- security_compliance.md
- sla_policy.md
- troubleshooting_guide.pdf (PDF document)

## Known Limitations
- LLaMA 3.2 is slower than cloud LLMs (5-15 seconds per response)
- Persona detection accuracy depends on message clarity
- Knowledge base limited to 11 documents
- No persistent conversation history between sessions

## Future Improvements
- Add sentiment analysis
- Multi-language support
- Dashboard with analytics
- Faster LLM model integration
