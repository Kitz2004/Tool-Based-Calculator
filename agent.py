from dotenv import load_dotenv
load_dotenv()

import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# ---------------- LLM ----------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# ---------------- AGENT 1: ADD ----------------
@tool
def add(expression: str) -> str:
    """Add two numbers (example: 2+3)."""
    try:
        a, b = map(float, expression.split("+"))
        return str(a + b)
    except:
        return "Invalid addition"

# ---------------- AGENT 2: SUBTRACT ----------------
@tool
def subtract(expression: str) -> str:
    """Subtract two numbers (example: 5-2)."""
    try:
        a, b = map(float, expression.split("-"))
        return str(a - b)
    except:
        return "Invalid subtraction"

# ---------------- AGENT 3: MULTIPLY ----------------
@tool
def multiply(expression: str) -> str:
    """Multiply two numbers (example: 4*3)."""
    try:
        a, b = map(float, expression.split("*"))
        return str(a * b)
    except:
        return "Invalid multiplication"

# ---------------- AGENT 4: DIVIDE ----------------
@tool
def divide(expression: str) -> str:
    """Divide two numbers (example: 8/2)."""
    try:
        a, b = map(float, expression.split("/"))
        return str(a / b)
    except:
        return "Invalid division"

# ---------------- PROMPT (ONLY TOOL SELECTION) ----------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a router. Extract the math expression exactly as written. "
     "Return ONLY the expression (example: 8/2, 4+5, 6*7, 9-3)."),
    ("human", "{input}")
])

# ---------------- ROUTER (DECIDES WHICH AGENT) ----------------
def route(expression: str) -> str:
    if "+" in expression:
        return add.invoke(expression)
    if "-" in expression:
        return subtract.invoke(expression)
    if "*" in expression:
        return multiply.invoke(expression)
    if "/" in expression:
        return divide.invoke(expression)
    return "Unsupported operation"

# ---------------- LANGCHAIN AGENT PIPELINE ----------------
chain = (
    prompt
    | llm
    | RunnableLambda(lambda msg: route(msg.content.strip()))
)

def run_agent(user_input: str) -> str:
    return chain.invoke({"input": user_input})
