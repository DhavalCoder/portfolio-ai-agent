import os
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
        self.model = LLM_MODEL
        
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
        
        # 3. Call the LLM
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": formatted_system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.3, # Low temperature keeps the AI factual and grounded
                max_tokens=250
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Sorry, I encountered an error connecting to my AI brain: {str(e)}"
