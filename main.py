from fact_extractor import extract_facts
from memory_store import store_fact, get_all_facts, clear_memory
from drift_detector import detect_forgetting
from reinjector import build_memory_summary
from llm_wrapper import LLMWrapper

# initialize LLM
llm = LLMWrapper(provider="groq", api_key="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")

# clear old memory
clear_memory()

turn = 1

def chat_system(user_input, turn):
    # 1. extract facts
    facts = extract_facts(user_input)
    for f in facts:
        store_fact(turn, f["entity"], f["value"])

    # 2. build memory
    all_facts = get_all_facts()
    memory = build_memory_summary(all_facts)

    # 3. generate response

    relevant_memory = ""

    if "buy" in user_input or "price" in user_input or "budget" in user_input:
       relevant_memory = memory
       prompt = relevant_memory + "\nUser: " + user_input
    else:
       prompt = "User: " + user_input

    response = llm.generate(prompt)

    # 4. detect forgetting
    missed = detect_forgetting(response, all_facts)

    if missed:
        print("\n⚠️ Drift detected → Fixing...\n")
        response = llm.generate(prompt)

    return response


# 🟢 Chat loop
while True:
    user_input = input("\nUser: ")

    if user_input.lower() == "exit":
        print("Exiting chat...")
        break

    response = chat_system(user_input, turn)

    print("\nAI:", response)

    print("\n📊 Memory:", get_all_facts())

    turn += 1
