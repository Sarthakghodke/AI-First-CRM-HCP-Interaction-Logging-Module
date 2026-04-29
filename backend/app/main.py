# from fastapi import FastAPI
# from .routes import interactions, agent

# app = FastAPI(title="AI-First CRM HCP Module")

# app.include_router(interactions.router)
# app.include_router(agent.router)


# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

from fastapi import FastAPI
from app.routes import interactions
from app.agent import agent_graph
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interactions.router)


@app.get("/")
async def root():
    return {
        "message": "AI CRM Backend Running"
    }


@app.post("/agent/chat")
async def chat(data: dict):
    result = agent_graph.invoke({
        "user_message": data["message"]
    })

    return {
        "tool_used": result.get("tool_used"),
        "response": result.get("response")
    }