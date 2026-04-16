CIS\_Pre-Development System\_Gemini 

I tried working with Claude and Gemini on a previous app dev project a few months ago and ended up reaching an 80% nightmare range where despite all of the great progress that was realized I kept hitting this 80% near completeness because my documentation became unwieldy or the guardrail documents I created to stay on tract consummed so much of the contet window it could not contain the guardrail and the script files at the same time. this was before I was aware of RAG and claudes projects or geminis larger context window was not available. Now I am aware of harness strategies. I need this to be implemented at ground level during this second attempt at a major application development. So as in this conversation with the 3 main frontier models I want to incorporate a local LLM system combined with the input of the 3 main platforms as well as laying down a preproduction infrastructure layer. This is the focus of the session among myself and you three platforms. I have a first rum proof that I can use 32B LLMs locally on this system. The plan is to use all intelligence resources seguencially to take advantage tof the 4090 throughput. I have discusses this skeleton pre development framework with you to use the cis plan to develop the CIS application. Now I need all of these concept brought together around a harness that will remove the 80% barrier I experienced previously. What must I do practicallly to get this started. I guy I need a pre development plan similar to the extensive CIS Formal Phased Construction Plan.md just to have the hardware and basic infrasture to begin at a semi manual level. Please deliver some documentation to give guidance of how to set this up and feel free to contribute anything I may not be considering as you interpret the depth of this question and task

Your "80% Nightmare" happened because you hit Context Rot. You were asking the AI to hold both the "Blueprint" (plans/guardrails) and the "Hammer" (the code) in its active memory at the same time. Eventually, the blueprint got too big, and the AI lost its grip on the hammer.

To break the 80% barrier, we must move the Blueprint out of the AI's "short-term memory" (the chat window) and into a Local Harness (external memory).

Here is your Phase Zero: Infrastructure & Harness Setup Plan. This is the manual layer you need to stabilize the system before we write a single line of CIS application code.

1. The "Externalized Intelligence" Architecture Instead of one massive chat, we are going to use a Tripod System where your local hardware acts as the "Private Secretary" and the frontier models act as the "Specialists."

The Private Secretary (Local 32B LLM): Use this for Context Compaction. Its only job is to summarize long terminal logs or previous chat sessions into a "State Update" that fits in a small window.

The Specialists (Gemini/Claude/GPT): They only ever see the current task and the current state summary. They never see the whole history at once.

The Harness (Obsidian \+ SQLite): This is the "Paper Trail." If the AI forgets something, it's written in the vault. The AI doesn't "know" your project; it "reads" your project's records as needed.

2. Practical "Phase Zero" Setup Documentation Step 1: The "Harness" Directory Structure Run these commands in your Ubuntu terminal to create the physical skeleton of the CIS. This ensures the AI always knows where it is.

Bash mkdir \-p \~/CIS\_CORE/{01\_PILOTS,02\_LOGS,03\_BLUEPRINTS,04\_MEMORY} mkdir \-p \~/CIS\_CORE/03\_BLUEPRINTS/{POLICIES,SCHEMAS,WORKFLOWS} Step 2: Initialize the "Global State Ledger" (The SQLite Anchor) We need a database that tracks what is "Done," "In Progress," and "Blocked." This prevents the "Where was I?" loop.

Task: Use your Local 32B or Claude to generate a init\_harness.py script.

Schema: It should have one table: session\_history with columns: timestamp, model\_used, objective, outcome, and next\_step.

Why: Before you end any session with an AI, you ask it to generate a "Handover Packet" (100 words max). You save that into this database.

Step 3: Establish the "Context Firewall" (Obsidian Setup) In Obsidian, create a "Master Guardrail" folder. Inside, create three small, atomic files:

TECH\_STACK.md: Lists the 4090, Proxmox, Ubuntu, and local LLM details.

CODING\_STANDARDS.md: Your preference for Python, FastAPI, etc.

THE\_HITCHHIKER.md: A list of the "80% failures" from your last project (the "nightmare logs").

The Protocol: You never paste your 50-page construction plan into a chat. You only paste the specific Phase/Epic you are working on, plus these three tiny "Atomic Guardrails."

3. The "Sequential Intelligence" Workflow (How to use the 4090\) Since you have a 4090, you can use Local RAG (Retrieval-Augmented Generation) to prevent context bloat.

The Ingest (Manual): Take a phase from your construction plan.

The Extraction (Local LLM): Ask your 32B model: "Extract only the technical requirements for Epic 1.1 from this text."

The Execution (Frontier Model): Give that small snippet to Claude/Gemini.

The Sanity Check (ChatGPT): Give the code to ChatGPT and ask: "Does this conflict with the hardware specs in my TECH\_STACK.md?"

The Update (Local LLM): Give the final result back to your local 32B and ask: "Write a 3-sentence summary for the SQLite State Ledger."

4. What you aren't considering (The "Missing Links") Model Context Protocol (MCP): You should look into setting up an MCP Server for your Obsidian vault. This allows Claude or Gemini to "Search" your vault without you having to copy-paste. It’s like giving the AI a pair of glasses to see your files.

"Snapshot" Backups: Because you're on Proxmox, you should take a VM Snapshot before every major "Code Push." If the AI hallucinates and ruins your Ubuntu config, you "One-Click" back to 10 minutes ago. This is your ultimate safety net.

Automated Linting: Since you aren't a developer, ask the AI to write a "Pre-flight Check" script. Before you run any code, this script checks if the file paths exist. This stops errors before they happen.

Your Next Action: Do you want the Python code to initialize the SQLite State Ledger (Step 2), or would you like a list of the 5 Key Snapshot Points for your Proxmox VM to ensure you can always "undo" a mistake?  
