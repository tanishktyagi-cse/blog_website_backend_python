# Blog Website Backend (Python + FastAPI)
This is the backend for a Blogging Website, built using FastAPI and MongoDB.
I developed this project as part of my internship, focusing on creating a scalable and modular API for handling blog posts, comments, and authentication.

✨ Features
RESTful API with FastAPI

MongoDB integration for data storage

JWT Authentication (Login/Signup)

Swagger UI for API documentation

Easily deployable via Docker & Docker Compose

# 📄 API Documentation
Once the app is running locally, visit:

http://127.0.0.1:8000/docs
to access the Swagger UI for testing all endpoints.

# 🛠️ Prerequisites
MongoDB

You need a running MongoDB instance (local or remote).

Configure your .env file using the sample keys from .env.example.



# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload

🐳 Docker Deployment (**Recommended**)
This project supports Docker + Docker Compose with two services:

FastAPI Backend + MongoDB Database

Steps
Build & Start Containers  or use my docker image **tanishqtyagi/python:Backend_Blog_1.0**

docker-compose up -d
Access the API

http://127.0.0.1:8000/docs

Stopping Containers

docker-compose down



# 🚀 Future Improvements
Google OAuth for login

Email verification

Media uploads using MinIO/AWS S3 Bucket

Redis for Memory caching
