import os
from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    user_message: str
    tool_used: str
    response: str


def log_interaction_tool(message: str) -> str:
    return f"Interaction logged from chat: {message}"


def edit_interaction_tool(message: str) -> str:
    return f"Interaction edited based on: {message}"


def search_hcp_profile_tool(message: str) -> str:
    return f"HCP profile lookup result for: {message}"


def generate_follow_up_email_tool(message: str) -> str:
    return f"Draft follow-up email generated for: {message}"


def suggest_next_best_action_tool(message: str) -> str:
    return f"Suggested next best action for: {message}"


def route_node(state: AgentState):
    text = state["user_message"].lower()
    if "edit" in text or "update" in text:
        tool, output = "edit_interaction", edit_interaction_tool(state["user_message"])
    elif "profile" in text or "hcp" in text:
        tool, output = "search_hcp_profile", search_hcp_profile_tool(state["user_message"])
    elif "email" in text or "follow" in text:
        tool, output = "generate_follow_up_email", generate_follow_up_email_tool(state["user_message"])
    elif "next" in text or "suggest" in text:
        tool, output = "suggest_next_best_action", suggest_next_best_action_tool(state["user_message"])
    else:
        tool, output = "log_interaction", log_interaction_tool(state["user_message"])

    return {"tool_used": tool, "response": output}


def enrich_with_llm(state: AgentState):
    model = os.getenv("GROQ_MODEL", "gemma2-9b-it")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"response": f"{state['response']} (LLM disabled: missing GROQ_API_KEY)"}
    llm = ChatGroq(model=model, api_key=api_key)
    prompt = (
        "You are a life-sciences CRM copilot. Improve this short tool output into a concise sales note: "
        f"{state['response']}"
    )
    completion = llm.invoke(prompt)
    return {"response": completion.content}


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("route", route_node)
    g.add_node("llm_enrich", enrich_with_llm)
    g.add_edge(START, "route")
    g.add_edge("route", "llm_enrich")
    g.add_edge("llm_enrich", END)
    return g.compile()


agent_graph = build_graph()