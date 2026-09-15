import os
import json
import urllib.parse
from openai import OpenAI
from app.rag.retriever import ResumeRetriever
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.guardrails import SecurityGuardrail
from app.config import GROQ_API_KEY, LLM_MODEL

class PortfolioAgent:
    def __init__(self):
        """
        Initializes the agent. 
        We use the standard OpenAI python client, but we point the base_url 
        directly to Groq's insanely fast API!
        """
        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        self.retriever = ResumeRetriever()
        
        # We must use a model that supports Tool Calling! 
        self.model = "qwen/qwen3.8-27b"
        
        # Initialize our new security layer
        self.guardrail = SecurityGuardrail(self.client, self.model)

    def ask(self, user_question: str) -> str:
        """
        The core RAG loop:
        1. Guardrail Security Check.
        2. Search the vector database for resume chunks.
        3. Inject chunks into the System Prompt.
        4. Send the Prompt + User Question to the LLM.
        5. Return the conversational answer.
        """
        # 1. Security Check (Block bad behavior instantly)
        if not self.guardrail.is_safe(user_question):
            return "I am a professional portfolio assistant. I cannot fulfill that request."

        # 2. Retrieve context
        context = self.retriever.retrieve_context(user_question)
        
        # 2. Format the system prompt with our retrieved context
        formatted_system_prompt = SYSTEM_PROMPT.format(context=context)
        
        # Define our image generation tool
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_image",
                    "description": "Call this tool IMMEDIATELY if the user asks you to generate, draw, or create a picture/image. Provide a highly detailed, comma-separated prompt.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "A highly detailed, professional image generation prompt. Add descriptors like '8k resolution, highly detailed, cinematic lighting'."
                            }
                        },
                        "required": ["prompt"]
                    }
                }
            }
        ]
        
        # 3. Call the LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": formatted_system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.3, # Low temperature keeps the AI factual and grounded
                max_tokens=250,
                tools=tools,
                tool_choice="auto"
            )
            
            # 4. Check if the LLM decided to use our tool!
            response_message = response.choices[0].message
            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                if tool_call.function.name == "generate_image":
                    args = json.loads(tool_call.function.arguments)
                    detailed_prompt = args.get("prompt", "a futuristic cyberpunk landscape")
                    
                    # URL encode the prompt for Pollinations
                    encoded_prompt = urllib.parse.quote(detailed_prompt)
                    
                    # Create the Pollinations URL
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
                    
                    # Return special markdown that the frontend will parse into an image
                    return f"I generated the image for you:\n\n![Generated Image]({image_url})"
            
            return response_message.content
        except Exception as e:
            return f"Sorry, I encountered an error connecting to my AI brain: {str(e)}"
