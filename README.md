# AIFlow SaaS Backend 🚀

A production-grade, asynchronous REST API built to power an AI SaaS platform. This backend features robust Role-Based Access Control (RBAC), atomic database transactions for AI billing, strict rate limiting to prevent brute-force attacks, and seamless integration with Google's Gemini 3.5 Flash model.

## 🏗️ Architecture & Tech Stack

* **Framework:** FastAPI (Python 3.10+)
* **Database:** PostgreSQL (Hosted via Supabase)
* **ORM:** SQLAlchemy 2.0 (Asyncpg Engine)
* **Migrations:** Alembic
* **AI Integration:** Google GenAI SDK (Gemini 3.5 Flash)
* **Security:** JWT (JSON Web Tokens), bcrypt
* **Rate Limiting:** SlowAPI
* **Deployment:** Render (CI/CD connected to GitHub)

## ✨ Core Features

* **Zero-Trust Security:** Global interceptors and JWT-based authentication secure all routes.
* **Strict RBAC:** Granular access control separating Basic Users, Moderators, Admins, and Super Admins.
* **Atomic AI Billing:** API requests to Google Gemini are wrapped in ACID-compliant database transactions. If the AI fails, credits are never deducted.
* **Anti-Abuse Systems:** In-memory IP rate limiting blocks brute-force login attempts and API spam.
* **Connection Pooling:** Optimized database sessions configured for serverless scaling.

## 📂 Project Structure

```text
backend/
├── alembic/                # Database migration environment
├── app/
│   ├── auth/               # JWT handling and RBAC dependencies
│   ├── config/             # Environment variable management (Pydantic)
│   ├── database/           # Async engine and session local setup
│   ├── models/             # SQLAlchemy schemas (User, Role, Usage)
│   ├── routes/             # API endpoints (Auth, AI, Admin, Users)
│   ├── services/           # External API integrations (Gemini transaction logic)
│   └── main.py             # FastAPI app factory, CORS, and Exception Handlers
├── seed.py                 # Script to inject RBAC roles into the database
├── promote.py              # Developer script to grant Super Admin privileges
├── requirements.txt        # Frozen dependencies
└── alembic.ini             # Migration configuration