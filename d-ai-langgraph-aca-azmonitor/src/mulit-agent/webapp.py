import streamlit as st
import os
import time
import subprocess
import sys
from pathlib import Path

# Paths to log and document files (relative to this script)
LOG_FILE = "travel_itinerary_log.md"
ITINERARY_FILE = "travel_itinerary.md"
ITERATIONS_FILE = "travel_itinerary_iterations.md"

# Add this at the top of your file (after imports)
BACKEND_PROCESS_KEY = "backend_process"

# Helper to parse log file into message blocks
def parse_log(log_path):
    if not os.path.exists(log_path):
        return []
    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()
    messages = []
    current = None
    for line in lines:
        if line.startswith("[") and ":" in line:
            if current:
                messages.append(current)
            ts_end = line.find("]")
            timestamp = line[1:ts_end]
            rest = line[ts_end+2:].strip()
            if rest.upper().startswith("SUPERVISOR ASKS "):
                agent = "SUPERVISOR"
                content = rest
            elif ":" in rest:
                agent, content = rest.split(":", 1)
                agent = agent.strip()
                content = content.strip()
            else:
                agent = "SYSTEM"
                content = rest
            current = {"timestamp": timestamp, "agent": agent, "content": content}
        elif current is not None:
            current["content"] += "\n" + line.strip()
    if current:
        messages.append(current)
    return messages

st.set_page_config(page_title="AI Multi-Agent Travel Planner", layout="wide")
st.title("🧑‍💼 AI Multi-Agent Travel Planner")

# Custom CSS for modern look
st.markdown("""
    <style>
    .agent-card {
        background: #f7fafd;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        border-left: 6px solid #4F8BF9;
    }
    .agent-title {
        font-weight: 600;
        color: #2563eb;
        font-size: 1.1rem;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .doc-panel {
        background: #f7fafd;
        border-radius: 12px;
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1.5px solid #4F8BF9;
        min-height: 400px;
    }
    .divider {
        border-left: 2px solid #e0e0e0;
        height: 100%;
        margin: 0 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Session state for user input and conversation
if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False
if "last_log_size" not in st.session_state:
    st.session_state.last_log_size = 0

# Add a button to clear logs and start over
if st.button("Clear & Start Over"):
    # Clear log and document files
    for file in [LOG_FILE, ITINERARY_FILE, ITERATIONS_FILE]:
        with open(file, "w", encoding="utf-8") as f:
            f.write("")
    st.session_state.user_question = ""
    st.session_state.conversation_started = False
    st.session_state.last_log_size = 0
    # Terminate backend process if running
    if BACKEND_PROCESS_KEY in st.session_state:
        proc = st.session_state[BACKEND_PROCESS_KEY]
        if proc and proc.poll() is None:
            proc.terminate()
        st.session_state[BACKEND_PROCESS_KEY] = None
    st.success("Logs and documents cleared. You can start a new conversation.")

# User input
with st.form("user_input_form"):
    user_question = st.text_input(
        "What is your travel question?",
        value=st.session_state.user_question or "I would like to visit Prague for 2 days.",
        key="user_question_input"
    )
    submitted = st.form_submit_button("Start Conversation")
    if submitted:
        st.session_state.user_question = user_question
        st.session_state.conversation_started = True
        # Start backend process in background
        if BACKEND_PROCESS_KEY in st.session_state and st.session_state[BACKEND_PROCESS_KEY]:
            proc = st.session_state[BACKEND_PROCESS_KEY]
            if proc.poll() is None:
                proc.terminate()
        proc = subprocess.Popen([sys.executable, "main.py"])
        st.session_state[BACKEND_PROCESS_KEY] = proc
        st.success("Conversation started! Agent responses will appear below.")

# Auto-refresh every 5 seconds if conversation is running
if st.session_state.get("conversation_started", False):
    st.experimental_rerun = st.experimental_rerun if hasattr(st, 'experimental_rerun') else lambda: None
    st_autorefresh = getattr(st, 'autorefresh', None)
    if st_autorefresh is None:
        from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=5000, key="refresh")

# Layout: left for agent messages, right for current document, with a visible divider
left_col, _, right_col = st.columns([2, 0.08, 3])

with left_col:
    st.subheader("🤖 Agent Messages")
    log_path = Path(LOG_FILE)
    if log_path.exists():
        messages = parse_log(str(log_path))
        for i, msg in enumerate(messages):
            # Emoji for agent
            agent_emoji = {
                "MR_FUN": "🎉",
                "MR_PRACTICAL": "🧑‍💼",
                "MRS_BUDGET": "💸",
                "MS_HUNGRY": "🍽️",
                "WRITER": "📝",
                "FINISH": "✅",
                "SUPERVISOR": "🕵️"
            }.get(msg["agent"].upper(), "🤖")
            # Preview
            content_lines = msg["content"].splitlines()
            preview = " ".join(content_lines[:3])
            if len(content_lines) > 3 or len(msg["content"]) > 200:
                preview = preview[:200] + ("..." if len(msg["content"]) > 200 else "")
            # Build a plain text label for the expander
            label = f"{agent_emoji} {msg['agent'].capitalize()} [{msg['timestamp']}] - {preview}"
            with st.expander(label, expanded=False):
                st.markdown(f"<div class='agent-card'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.info("Waiting for agent responses...")

with right_col:
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.subheader("📄 Current Itinerary Document")
    itinerary_path = Path(ITINERARY_FILE)
    if itinerary_path.exists():
        with open(itinerary_path, encoding="utf-8") as f:
            st.markdown(f"<div class='doc-panel'>{f.read()}</div>", unsafe_allow_html=True)
    else:
        st.info("No itinerary document yet.")

    with st.expander("Show Document Iterations"):
        iterations_path = Path(ITERATIONS_FILE)
        if iterations_path.exists():
            with open(iterations_path, encoding="utf-8") as f:
                st.markdown(f.read())
        else:
            st.info("No document iterations yet.")

st.caption("Tip: The UI now auto-refreshes every 5 seconds while a conversation is running. Click 'Clear & Start Over' to reset.")
