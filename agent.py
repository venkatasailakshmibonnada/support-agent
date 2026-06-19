from dotenv import load_dotenv
load_dotenv()

from src.persona_detector import detect_persona
from src.rag_pipeline import retrieve
from src.response_generator import generate_response
from src.escalation import should_escalate, generate_handoff_summary

DISSATISFIED_SIGNALS = [
    "still not working", "doesn't work", "not helpful", "useless",
    "still broken", "same issue", "not fixed", "nothing works", "still happening"
]

class SupportAgent:
    def __init__(self):
        self.history = []
        self.turn_count = 0
        self.dissatisfied_count = 0
        self.attempted_steps = []
        self.current_persona = "FRUSTRATED_USER"

    def chat(self, user_message: str) -> dict:
        self.turn_count += 1

        persona_result = detect_persona(user_message, self.history)
        self.current_persona = persona_result["persona"]

        chunks = retrieve(user_message, k=4)

        escalation = should_escalate(
            user_message, chunks, self.current_persona,
            self.turn_count, self.dissatisfied_count
        )

        result = {
            "persona": self.current_persona,
            "persona_reason": persona_result["reason"],
            "sources": chunks,
            "escalated": escalation["should_escalate"],
            "escalation_reasons": escalation["reasons"],
            "response": "",
            "handoff_summary": None
        }

        if escalation["should_escalate"]:
            summary = generate_handoff_summary(
                self.current_persona, user_message,
                self.history, chunks,
                self.attempted_steps, escalation["reasons"]
            )
            result["handoff_summary"] = summary
            result["response"] = (
                "I'm escalating your case to a human support specialist "
                "who can give you the dedicated attention you need. "
                "A summary of our conversation has been prepared for them."
            )
        else:
            response = generate_response(
                user_message, self.current_persona, chunks, self.history
            )
            result["response"] = response
            self.attempted_steps.append(f"Turn {self.turn_count}: {user_message[:80]}")

            if any(signal in user_message.lower() for signal in DISSATISFIED_SIGNALS):
                self.dissatisfied_count += 1
            else:
                self.dissatisfied_count = max(0, self.dissatisfied_count - 1)

        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": result["response"]})

        return result