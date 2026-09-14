from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ChatRequest, ChatResponse
from app.agent.agent import PortfolioAgent
from app.config import FRONTEND_URL

# Initialize the web application
app = FastAPI(title="Portfolio AI Agent API")

# Configure Security / CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False, # Fixes strict browser CORS blocking
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the brain (our RAG agent) once when the server boots
agent = PortfolioAgent()

@app.get("/health")
async def health_check():
    """
    Used by hosting platforms (like Render or Railway) to verify 
    the server is actually alive and running.
    """
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    The main endpoint. Your Vercel frontend will send HTTP POST requests here.
    """
    try:
        # Hand the validated string to the Agent we built in Stage 7
        answer = agent.ask(request.message)
        
        # Wrap the string in our Pydantic response model
        return ChatResponse(answer=answer)
    except Exception as e:
        # Proper HTTP error handling preventing the server from crashing
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
