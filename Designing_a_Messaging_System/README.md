# 💬 Messenger Implementation

## 📌 Project Overview
This project is a functional prototype of a messaging system developed as part of the **"Software Design and Documentation"** course. The system is built based on the architecture designed in Laboratory Work 1, focusing on modularity, data persistence, and reliable delivery.

**Core Focus:** Implementation of **Variant 3 — Offline Message Delivery** and **Message Status Tracking**.

---

## 🚀 Key Features
* **User Management**: Creation and identification of unique users.
* **Message Persistence**: Utilizing **SQLite** to guarantee that messages are saved even after a server restart.
* **Offline Delivery**: Messages are stored with a `pending` status if the recipient is offline (according to Variant 3).
* **Status Tracking**: Full message lifecycle tracking: `pending` ➡️ `delivered` ➡️ `read`.
* **Interactive API Docs**: Automatic documentation generated via Swagger UI.
* **Integration Testing**: Automated verification of the "Create Users -> Send Message -> Check History" flow.

---

## 📂 Project Structure
The project is organized following the "Separation of Concerns" principle:

```text
/Designing_a_Messaging_System
│
├── /models          # Pydantic models for data validation (schemas.py)
├── /services        # Business logic of the system (message_service.py)
├── /storage         # Database connection and initialization (database.py)
├── /tests           # Integration tests (tests.py)
├── main.py          # FastAPI entry point and API routes
├── messenger.db     # SQLite database file (automatically generated)
├── postman_collection.json  # Pre-configured API requests for Postman
└── README.md        # Project documentation
```

🛠️ How to Run
1. Install Dependencies
Ensure you have Python 3.12+ installed. Run the following command to install the required libraries:

Bash
pip install fastapi uvicorn pydantic pytest httpx
2. Start the Server
Run the Uvicorn server from the project root directory:

Bash
uvicorn main:app --reload
The API will be available at: http://127.0.0.1:8000

3. API Testing
Swagger UI: Visit http://127.0.0.1:8000/docs for interactive testing.

Postman: Import the postman_collection.json file for ready-to-use requests.

4. Run Integration Tests
To verify the system functionality, execute:

Bash
python -m pytest tests/tests.py

📊 Data Model
The system uses a minimal data model for efficiency and reliability:

User: id (int), name (str)

Message: id, conversationId, senderId, text, status, createdAt, deliveredAt, readAt.

📝 Architecture ADR (Brief)
Decision: A Database-First approach was chosen.

Reasoning: Every message is immediately recorded in SQLite, guaranteeing its safety during network failures.

Status Handling: Asynchronous status logic is used to support the offline delivery mode.

Author: Viktoriia Kazniienko

Course: Software Design & Documentation, 2026