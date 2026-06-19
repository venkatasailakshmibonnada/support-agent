ESCALATION_KEYWORDS = [
    "billing", "refund", "charge", "invoice", "legal", "lawsuit",
    "fraud", "account suspended", "data breach", "cancel account"
]
LOW_CONFIDENCE_THRESHOLD = 1.2
MAX_DISSATISFIED_TURNS = 2

def should_escalate(query: str, chunks: list, persona: str,
                    turn_count: int, dissatisfied_count: int) -> dict:
    reasons = []

    if not chunks:
        reasons.append("No relevant knowledge base articles found.")

    if chunks and all(c["score"] > LOW_CONFIDENCE_THRESHOLD for c in chunks):
        reasons.append("Low retrieval confidence — no closely matching documents.")

    query_lower = query.lower()
    matched = [kw for kw in ESCALATION_KEYWORDS if kw in query_lower]
    if matched:
        reasons.append(f"Sensitive topic detected: {', '.join(matched)}.")

    if persona == "FRUSTRATED_USER" and dissatisfied_count >= MAX_DISSATISFIED_TURNS:
        reasons.append(f"User has been dissatisfied for {dissatisfied_count} consecutive turns.")

    return {
        "should_escalate": len(reasons) > 0,
        "reasons": reasons
    }

def generate_handoff_summary(persona: str, query: str, history: list,
                              chunks: list, attempted_steps: list,
                              escalation_reasons: list) -> dict:
    sources = list(set(c["source"] for c in chunks)) if chunks else []
    history_summary = [
        f"Turn {i+1} - {m['role'].upper()}: {m['content'][:100]}"
        for i, m in enumerate(history[-8:])
    ]
    return {
        "persona": persona,
        "issue": query,
        "escalation_reasons": escalation_reasons,
        "conversation_history": history_summary,
        "documents_used": sources,
        "attempted_steps": attempted_steps or ["Initial knowledge base lookup"],
        "recommendation": "Route to Tier-2 human support agent for manual investigation.",
    }