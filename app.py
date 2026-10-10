import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from drift_tracker import get_drift_history, save_drift, calculate_drift
from fact_extractor import extract_facts
from memory_store import store_fact, get_all_facts, clear_memory
from drift_detector import detect_forgetting
from reinjector import build_memory_summary
from llm_wrapper import LLMWrapper


# ---------------- LLM ----------------

llm = LLMWrapper(
    provider="groq",
    api_key="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"   # ⚠️ replace later with env variable
)


# ---------------- Session ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "turn" not in st.session_state:
    st.session_state.turn = 1

if "initialized" not in st.session_state:
    clear_memory()
    st.session_state.initialized = True


# ---------------- Sidebar Controls ----------------

if st.sidebar.button("🧹 Clear Memory"):
    clear_memory()
    st.session_state.messages = []
    st.session_state.turn = 1
    st.success("Memory cleared!")


# ---------------- Chat System ----------------

def chat_system(user_input, turn):

    # 🔹 Extract facts
    facts = extract_facts(user_input)

    # 🔹 Store facts
    for f in facts:
        store_fact(turn, f["entity"], f["value"])

    # 🔹 Get memory
    all_facts = get_all_facts()
    memory = build_memory_summary(all_facts)

    # 🔹 Stronger prompt
    prompt = (
        "Important facts (must follow):\n"
         + "All prices MUST be shown ONLY in Indian Rupees (₹).\n"
         + "DO NOT use dollars ($) anywhere.\n"
         + "Example: ₹50000, not $50000.\n\n"
         + memory
         + "\nUser: "
         + user_input
)

    # 🔹 First response
    response = llm.generate(prompt)

    # 🔹 Detect drift
    missed = detect_forgetting(response, all_facts, user_input)
    wrong = []

    # 🔹 Calculate drift
    drift_score = calculate_drift(missed, wrong)

    # 🔹 Save drift
    save_drift(turn, drift_score)

    # 🔹 Drift alerts
    if drift_score > 70:
        st.error("🚨 High Drift!")
    elif drift_score > 30:
        st.warning("⚠️ Medium Drift")
    elif drift_score > 0:
        st.info("ℹ️ Low Drift")

    # 🔹 Fix response if drift
    if missed:
        response = llm.generate(prompt)

    return response


# ---------------- UI ----------------

st.title("🧠 Conversational Context Integrity Monitor")

user_input = st.chat_input("Type your message...")

if user_input:

    st.session_state.messages.append(("user", user_input))

    response = chat_system(user_input, st.session_state.turn)

    st.session_state.messages.append(("ai", response))

    st.session_state.turn += 1


# ---------------- Chat Display ----------------

for role, msg in st.session_state.messages:

    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)


# ---------------- Memory ----------------

st.sidebar.title("📊 Memory")
st.sidebar.write(get_all_facts())


# ---------------- BAR GRAPH ----------------

st.subheader("📊 Memory Drift Variation")

data = get_drift_history()

if data:

    df = pd.DataFrame(data)

    # 🔹 Sort turns properly
    df = df.sort_values(by="turn")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(df["turn"], df["score"])

    ax.set_xlabel("Question Number (Turn)")
    ax.set_ylabel("Drift Level (%)")
    ax.set_title("Drift per Question")

    ax.set_ylim(0, 100)
    ax.set_xticks(df["turn"])

    ax.grid(axis="y")

    st.pyplot(fig)

else:
    st.info("No drift data available yet")


# ---------------- LINE GRAPH ----------------

st.subheader("📈 Drift Trend")

if data:
    df = pd.DataFrame(data)
    df = df.sort_values(by="turn")

    st.line_chart(
        df.set_index("turn")["score"]
    )


# ---------------- DEBUG ----------------

st.write("🔍 Drift Data:", data)
