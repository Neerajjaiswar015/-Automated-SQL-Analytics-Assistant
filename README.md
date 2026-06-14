# 🚀 Automated SQL Analytics Assistant
An AI-powered business intelligence web application that democratizes data analysis. This tool allows non-technical users to query a relational database using natural, everyday English. The system translates the text into optimized SQL, executes it safely, and automatically renders the results into interactive dashboards and downloadable reports.

## 🌟 Key Features

* **Natural Language to SQL:** Integrates with the Google Gemini API to dynamically generate syntactically correct SQLite queries based on user intent and a hardcoded schema.
* **Intelligent Auto-Visualization:** Inspects the shape of the returning data frame and automatically renders the appropriate graph (Bar or Line charts) using Chart.js.
* **Strict Security Guardrails:** Implements backend regex validation to block destructive SQL operations (`DROP`, `DELETE`, `UPDATE`, `INSERT`), ensuring a strictly read-only execution environment.
* **Self-Healing AI Loop:** Features an automated error-recovery system. If the LLM generates an invalid SQL query, the backend catches the execution error and asks the AI to self-correct the typo before returning a response to the user.
* **One-Click CSV Export:** Allows business users to instantly download their queried data into spreadsheet format.

## 🛠️ Technology Stack

* **Backend:** Python, Flask, Pandas, SQLite3
* **AI Orchestration:** Google Gemini API (`google-generativeai`)
* **Frontend:** HTML5, Tailwind CSS (via CDN), Vanilla JavaScript
* **Visualizations:** Chart.js

## 📂 Project Structure

```text
sql-analytics-assistant/
├── app.py                 # Main Flask server and API routing
├── db_handler.py          # Safe database connection and security guardrails
├── llm_helper.py          # Gemini API integration and schema-aware prompting
├── seed_db.py             # Script to generate the mock Cloud Kitchen database
├── cloud_kitchens.db      # Local SQLite database (generated)
├── templates/
│   └── index.html         # Frontend UI, auto-charting logic, and CSV export
└── README.md
