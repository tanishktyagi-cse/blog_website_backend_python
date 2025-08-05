Blog Website Backend (Python + FastAPI)
This is the backend for a Blogging Website, built using FastAPI and MongoDB.
I developed this project as part of my internship, focusing on creating a scalable and modular API for handling blog posts, comments, and authentication.

✨ Features
RESTful API with FastAPI

MongoDB integration for data storage

JWT Authentication (Login/Signup)

Swagger UI for API documentation

Easily deployable via Docker & Docker Compose

📄 API Documentation
Once the app is running locally, visit:

arduino
Copy
Edit
http://127.0.0.1:8000/docs
to access the Swagger UI for testing all endpoints.

🛠️ Prerequisites
MongoDB

You need a running MongoDB instance (local or remote).

Configure your .env file using the sample keys from .env.example.

Python Environment Setup

bash
Copy
Edit
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload
🐳 Docker Deployment (Optional)
This project supports Docker + Docker Compose with two services:

FastAPI Backend

MongoDB Database

Steps
Build & Start Containers

bash
Copy
Edit
docker-compose up --build
Access the API

arduino
Copy
Edit
http://127.0.0.1:8000/docs
Stopping Containers

bash
Copy
Edit
docker-compose down
📂 Project Structure
pgsql
Copy
Edit
blog_website_backend_python/
│-- app/
│   ├── routes/        # API routes (auth, posts, comments)
│   ├── schemas/       # Pydantic schemas
│   ├── models/        # MongoDB models
│   ├── core/          # Configuration & utilities
│   ├── security/      # JWT & password hashing
│   └── main.py        # Entry point of FastAPI
│
│-- tests/             # Test files
│-- venv/              # Virtual environment
│-- requirements.txt   # Python dependencies
│-- Dockerfile
│-- docker-compose.yml
│-- .env.example
│-- README.md
🚀 Future Improvements
Google OAuth for login

Email verification

Media uploads using MinIO
