import os
from groq import Groq
from utils.helpers import log_token_usage
from rich.console import Console

console = Console()

class ChatHandler:
    def __init__(self, model_id):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_id = model_id
        self.conversation_history = []

    async def send_message(self, message, system_prompt=None):
        messages = self.conversation_history + [{"role": "user", "content": message}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_id,
                max_tokens=8000
            )
            assistant_message = chat_completion.choices[0].message.content
            
            # Kullanıcı ve asistan mesajlarını sohbet geçmişine ekle
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # CompletionUsage nesnesini sözlüğe dönüştür
            usage_dict = {
                "prompt_tokens": chat_completion.usage.prompt_tokens,
                "completion_tokens": chat_completion.usage.completion_tokens,
                "total_tokens": chat_completion.usage.total_tokens
            }
            
            return assistant_message, usage_dict
        except Exception as e:
            console.print(f"[bold red]Error in ChatHandler: {str(e)}[/bold red]")
            return None, None

    def reset_conversation(self):
        self.conversation_history = []