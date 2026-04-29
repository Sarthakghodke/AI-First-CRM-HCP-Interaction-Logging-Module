from pydantic import BaseModel


class InteractionCreate(BaseModel):
    hcp_name: str
    channel: str
    summary: str
    next_step: str = ""


class InteractionUpdate(BaseModel):
    summary: str | None = None
    next_step: str | None = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    tool_used: str
    response: str