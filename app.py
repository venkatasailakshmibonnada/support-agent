import streamlit as st
import json
from dotenv import load_dotenv
load_dotenv()

from src.agent import SupportAgent

st.set_page_config(page_title="Support Agent", page_icon="🤖", layout="wide")
st.title("🤖 Persona-Adaptive Customer Support Agent")

PERSONA_ICONS = {
    "TECHNICAL_EXPERT": "🔧",
    "FRUSTRATED_USER": "😤",
    "BUSINESS_EXECUTIVE": "💼"
}

if "agent" not in st.session_state:
    st.session_state.agent = SupportAgent()
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Session Info")
    if st.session_state.get("agent"):
        agent = st.session_state.agent
        st.metric("Turn", agent.turn_count)
        st.metric("Persona", agent.current_persona)
        st.metric("Dissatisfied turns", agent.dissatisfied_count)
    if st.button("Reset conversation"):
        st.session_state.agent = SupportAgent()
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("meta"):
            meta = msg["meta"]
            icon = PERSONA_ICONS.get(meta["persona"], "👤")
            st.caption(f"{icon} **{meta['persona']}** — {meta['persona_reason']}")

            if meta.get("sources"):
                with st.expander("📚 Retrieved sources"):
                    for c in meta["sources"]:
                        st.markdown(f"**{c['source']}** | page {c['page']} | score {c['score']}")
                        st.text(c["content"][:200] + "...")

            if meta.get("escalated"):
                st.error("🚨 Escalated to human support")
                with st.expander("📋 Handoff summary"):
                    st.json(meta["handoff_summary"])

if prompt := st.chat_input("Type your support question..."):
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        result = st.session_state.agent.chat(prompt)

    meta = {
        "persona": result["persona"],
        "persona_reason": result["persona_reason"],
        "sources": result["sources"],
        "escalated": result["escalated"],
        "escalation_reasons": result["escalation_reasons"],
        "handoff_summary": result.get("handoff_summary")
    }

    with st.chat_message("assistant"):
        icon = PERSONA_ICONS.get(result["persona"], "👤")
        st.caption(f"{icon} **{result['persona']}** — {result['persona_reason']}")
        st.write(result["response"])

        if result["sources"]:
            with st.expander("📚 Retrieved sources"):
                for c in result["sources"]:
                    st.markdown(f"**{c['source']}** | page {c['page']} | score {c['score']}")
                    st.text(c["content"][:200] + "...")

        if result["escalated"]:
            st.error("🚨 Escalated to human support")
            with st.expander("📋 Handoff summary"):
                st.json(result["handoff_summary"])

    st.session_state.messages.append({"role": "user", "content": prompt, "meta": None})
    st.session_state.messages.append({"role": "assistant", "content": result["response"], "meta": meta})