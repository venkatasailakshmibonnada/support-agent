import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

PERSONA_TONES = {
    "TECHNICAL_EXPERT": "You are a senior technical support engineer. Be detailed and precise. Include error codes, CLI commands, and step-by-step technical fixes.",
    "FRUSTRATED_USER": "You are a warm empathetic support agent. Start by acknowledging the user's frustration. Use simple language. Be reassuring and action-oriented.",
    "BUSINESS_EXECUTIVE": "You are a concise enterprise support specialist. Be brief and outcome-focused. Use bullet points. Include estimated resolution time. No technical jargon."
}

def generate_response(query: str, persona: str, chunks: list, history: list = []) -> str:
    tone = PERSONA_TONES.get(persona, PERSONA_TONES["FRUSTRATED_USER"])
    
    if chunks:
        context = "\n\n".join([
            f"[Source: {c['source']}]\n{c['content']}"
            for c in chunks
        ])
    else:
        context = "No relevant documents found in the knowledge base."
    
    history_text = ""
    if history:
        history_text = "\n".join([
            f"{m['role'].upper()}: {m['content'][:200]}"
            for m in history[-4:]
        ])
    
    prompt = f"""{tone}

Answer ONLY using the knowledge base context below. Do not invent information.
If the answer is not in the context, say: "I don't have specific information on that. Let me connect you with a specialist."

KNOWLEDGE BASE:
{context}

{"CONVERSATION HISTORY:" + history_text if history_text else ""}

CUSTOMER QUESTION: {query}

YOUR RESPONSE:"""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        
        return response.json()["response"].strip()
    
    except Exception as e:
        return f"I'm having trouble generating a response right now. Please try again. Error: {e}"