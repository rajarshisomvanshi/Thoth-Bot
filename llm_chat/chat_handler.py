import os
import google.generativeai as genai
from groq import Groq
from rich.console import Console
import time

console = Console()

class ChatHandler:
    def __init__(self, model_id):
        self.model_id = model_id
        
        if "gemini" in model_id:
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY is not set. Please set it in the Settings menu.")
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_id)
            self.chat = self.model.start_chat(history=[])
        else:
            self.api_key = os.getenv("GROQ_API_KEY")
            if not self.api_key:
                raise ValueError("GROQ_API_KEY is not set. Please set it in the Settings menu.")
            self.client = Groq(api_key=self.api_key)
        
        self.conversation_history = []

    async def send_message(self, message, system_prompt=None):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if "gemini" in self.model_id:
                    if system_prompt:
                        message = f"{system_prompt}\n\n{message}"
                    
                    response = self.chat.send_message(message)
                    if not response.text:
                        raise ValueError("Empty response from Gemini API")
                    assistant_message = response.text
                    
                    # Token sayısını hesaplamak için alternatif bir yöntem
                    prompt_tokens = len(message.split())
                    completion_tokens = len(assistant_message.split())
                    total_tokens = prompt_tokens + completion_tokens
                else:
                    messages = self.conversation_history + [{"role": "user", "content": message}]
                    if system_prompt:
                        messages.insert(0, {"role": "system", "content": system_prompt})
                    
                    chat_completion = self.client.chat.completions.create(
                        messages=messages,
                        model=self.model_id,
                        max_tokens=1024
                    )
                    assistant_message = chat_completion.choices[0].message.content
                    prompt_tokens = chat_completion.usage.prompt_tokens
                    completion_tokens = chat_completion.usage.completion_tokens
                    total_tokens = chat_completion.usage.total_tokens
                
                usage_dict = {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens
                }
                
                self.conversation_history.append({"role": "user", "content": message})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                return assistant_message, usage_dict
            except Exception as e:
                console.print(f"[bold yellow]Attempt {attempt + 1} failed: {str(e)}[/bold yellow]")
                if attempt < max_retries - 1:
                    console.print(f"[bold yellow]Retrying in 2 seconds...[/bold yellow]")
                    time.sleep(2)
                else:
                    console.print(f"[bold red]Error in ChatHandler after {max_retries} attempts: {str(e)}[/bold red]")
                    return None, None

    def reset_conversation(self):
        self.conversation_history = []
        if "gemini" in self.model_id:
            self.chat = self.model.start_chat(history=[])