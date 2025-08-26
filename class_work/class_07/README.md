## 𝟕𝐭𝐡 𝐀𝐠𝐞𝐧𝐭𝐢𝐜 𝐀𝐈 𝐂𝐥𝐚𝐬𝐬 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞𝐝!

Timing: 𝟐–𝟓 𝐏𝐌 (𝐒𝐮𝐧𝐝𝐚𝐲)
Instructor:  𝐒𝐢𝐫 𝐀𝐥𝐢 𝐉𝐚𝐰𝐰𝐚𝐝🙌

In today’s session, we learned:
🛡️ Guardrails (Input & Output)
🔁 Loop logic (for & while)
⚠️ try-except for error handling
💡 Real-world coding practice


## Guardrails

## Input GuardRails

Exercise # 1
Objective: Make a agent and make an input guardrail trigger.
Prompt: I want to change my class timings 😭😭
Outcome: After running the above prompt an InputGuardRailTripwireTriggered in except should be called. See the outcome in LOGS

Exercise # 2
Objective: Make a father agent and father guardrail. The father stopping his child to run below 26C.

Exercise # 3
Objective: Make a gate keeper agent and gate keeper guardrail. The gate keeper stopping students of other school.




Agent + Guardrails Workflow
User → Agent

User koi message / command bhejta hai.

Agent → Input Guardrail

Agent pehle apne input guardrail ko ye message deta hai.

Guardrail check karta hai:

Content safe hai?

Format sahi hai?

Policy follow ho rahi hai?

Agar pass → next step

Agar fail → tripwire trigger / block message send hota hai.

Agent → Processing

Agent LLM ko call karta hai ya required tool/logic run karta hai.

Agent output generate karta hai.

Agent → Output Guardrail

Agent ka output output guardrail ko diya jata hai.

Ye check karta hai:

Safe content?

Format correct?

No sensitive info leak?

Agar pass → next step

Agar fail → tripwire trigger / safe fallback reply.

Output → User

Final safe response user ko bhej diya jata hai.

📌 Short version flow:

pgsql
Copy
Edit
User → Input Guardrail → Agent Logic/LLM → Output Guardrail → User