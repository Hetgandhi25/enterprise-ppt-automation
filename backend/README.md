# AI-Powered Service Review PPT Generation System

Backend API for automating the generation of Service Review PowerPoint presentations.

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `.\venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Install Playwright browsers: `playwright install`
5. Copy `.env.example` to `.env` and fill in your credentials.
6. Run the server: `uvicorn api.main:app --reload`
