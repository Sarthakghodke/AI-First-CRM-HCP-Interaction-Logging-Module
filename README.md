# AI-First CRM HCP Interaction Logging Module

## Project Overview
This project is an AI-first CRM module designed for Healthcare Professionals (HCPs). It allows users to log interactions using a conversational AI interface powered by LangGraph and Groq LLM.

## Features
- AI Chat Interface
- LangGraph Agent Workflow
- FastAPI Backend
- React Frontend
- Tool-Based AI Routing
- Follow-up Email Generation
- Interaction Logging
- Interaction Editing
- HCP Profile Search
- Next Best Action Suggestions

## Tech Stack
### Frontend
- React
- Axios
- Vite

### Backend
- FastAPI
- LangGraph
- Groq LLM
- Python

## AI Tools Implemented
1. Log Interaction
2. Edit Interaction
3. Search HCP Profile
4. Generate Follow-up Email
5. Suggest Next Best Action

## Backend Run
```bash
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

## Frontend Run
```bash
cd frontend
npm install
npm run dev
```

## API Endpoint
POST:
```txt
/agent/chat
```

## Example Request
```json
{
  "message": "Generate follow up email for Dr Sharma"
}
```

## Project Structure
```txt
backend/
frontend/
```