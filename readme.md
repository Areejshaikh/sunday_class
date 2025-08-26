# # Jab aap Runner.run() ko call karte hain, to ek loop chalta hai jab tak humein final output nahi milta.

# # Hum LLM ko call karte hain, agent ke model aur settings ka use karte hue, aur message history ke sath.

# # LLM ek response deta hai, jo tool calls shamil kar sakta hai.

# # Agar response mein final output ho, to hum usay return karte hain aur loop end kar dete hain.

# # Agar response mein handoff ho, to hum naye agent ko set karte hain aur step 1 par wapas chale jaate hain.

# # Agar tool calls hoon, to hum unko process karte hain aur tool responses ko messages mein add karte hain. Phir se step 1 par jaate hain.

# # Ek max_turns parameter hota hai jiska use loop ke execute hone ke times ko limit karne ke liye hota hai.


# Agent Loop
# Jab Runner.run() call hota hai, ek loop start hota hai jab tak final output nahi milta.

# Har step mein LLM ko call kiya jaata hai.

# Agar response mein tool calls hoon → un tools ko run karke wapas loop mein jaaya jaata hai.

# Agar response mein handoff ho → agent change kar ke loop phir se chalu hota hai.

# max_turns parameter se loop ke dafaein limit ki ja sakti hain.

# ✅ Final Output
# Final output woh hota hai jo loop ke end mein agent return karta hai.

# Agar output_type set ho:

# Jab tak structured output us type ka nahi milta, loop chalta rahta hai.

# Agar output_type set nahi ho:

# Pehla response jo tool calls aur handoffs ke baghair ho, woh final output hota hai.

# 🧠 Common Agent Patterns
# SDK flexible hai, aap deterministic, iterative, aur complex flows bana sakte ho.

# Example patterns milte hain: examples/agent_patterns folder mein.

# 📊 Tracing
# SDK automatically har agent run ko trace karta hai.

# Yeh help karta hai debugging mein.

# Aap tracing ko customize bhi kar sakte ho.

# Support karta hai destinations jaise:

# Logfire, AgentOps, Braintrust, Scorecard, Keywords AI

# Zyada tracing settings ke liye "Tracing" section dekhein.

# 💻 Development Instructions
# (Only if you want to edit the SDK or examples)

# uv install hona chahiye
# ✅ Check: uv --version

# Dependencies install karo:

# bash
# Copy
# Edit
# make sync
# Code check/test karne ke liye:

# nginx
# Copy
# Edit
# make check  # sab kuch (tests, linter, typechecker)
# ✅ Individual commands:

# make tests → sirf tests

# make mypy → type checker

# make lint → code linting

# make format-check → style checker

# 🙏 Acknowledgements
# Agents SDK ka development open-source tools ke support se hua hai:

# Pydantic & PydanticAI

# MkDocs

# Griffe

# uv & ruff

# OpenAI ki community ko empower karne ke liye yeh SDK open-source banaaya gaya hai taake sab log mil kar isay improve kar sakein.