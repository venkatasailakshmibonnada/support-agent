import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

def detect_persona(message: str, history: list = []) -> dict:
    prompt = f"""Classify this customer support message into exactly one persona:
- TECHNICAL_EXPERT: uses technical terms, asks about APIs/logs/configs/errors
- FRUSTRATED_USER: emotional, complaints, urgent, words like "nothing works"
- BUSINESS_EXECUTIVE: outcome-focused, asks about impact/timeline/cost

Reply in EXACTLY this format (two lines only):
PERSONA: <label>
REASON: <one sentence>

Message: {message}"""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        
        text = response.json()["response"].strip()
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        
        persona = "FRUSTRATED_USER"
        reason = ""
        for line in lines:
            if line.startswith("PERSONA:"):
                persona = line.replace("PERSONA:", "").strip()
            if line.startswith("REASON:"):
                reason = line.replace("REASON:", "").strip()
        
        valid = ["TECHNICAL_EXPERT", "FRUSTRATED_USER", "BUSINESS_EXECUTIVE"]
        if persona not in valid:
            persona = "FRUSTRATED_USER"
        
        return {"persona": persona, "reason": reason}
    
    except Exception as e:
        return {"persona": "FRUSTRATED_USER", "reason": f"Detection error: {e}"}