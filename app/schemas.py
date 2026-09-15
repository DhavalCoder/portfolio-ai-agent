from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str = Field(
        ..., 
        description="The question from the user on the portfolio",
        min_length=1, 
        max_length=500 # Prevents malicious users from sending massive payloads
    )
    history: Optional[List[Message]] = Field(default=[], description="The conversational history")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="The AI's generated response")
