from llm_chat.chat_handler import ChatHandler
from utils.helpers import log_token_usage
import os
from rich.console import Console

console = Console()

class CodeGenerator:
    def __init__(self, chat_handler: ChatHandler):
        self.chat_handler = chat_handler

    async def generate_code(self, instructions, file_path):
        system_prompt = f"""
        You are an AI code generator. Your task is to generate high-quality, well-structured Python code based on the given instructions.
        
        Follow these guidelines:
        1. Use appropriate naming conventions for classes, functions, and variables.
        2. Implement proper error handling and logging where necessary.
        3. Include docstrings and comments to explain complex logic or important details.
        4. Ensure that the code is modular, reusable, and follows the DRY principle.
        5. Use type hints where appropriate to improve code readability and maintainability.
        6. Implement any necessary imports at the beginning of the file.
        7. The code should be runnable as a standalone script.
        8. Include a `if __name__ == '__main__':` block to make the script executable.
        9. Do not include any markdown formatting or code block indicators (like ```python).
        10. Start the code directly without any introductory comments or docstrings.

        Generate only the code, without any additional explanations.
        """

        message = f"Generate Python code for the following task: {instructions}"

        if "gemini" in self.chat_handler.model_id:
            code = await self._generate_code_gemini(message, system_prompt)
        else:
            code, _ = await self.chat_handler.send_message(message, system_prompt)

        if code:
            # Remove any potential markdown formatting
            code = code.strip().replace("```python", "").replace("```", "").strip()

            # Create the file and write the code
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(code)

            return code
        else:
            console.print("[bold red]Failed to generate code.[/bold red]")
            return None

    async def _generate_code_gemini(self, message, system_prompt):
        try:
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_DANGEROUS",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
            ]

            response = self.chat_handler.model.generate_content(
                [system_prompt, message],
                safety_settings=safety_settings,
                generation_config={"temperature": 0.7, "top_p": 0.9, "top_k": 40},
            )

            if response.parts:
                return response.text
            elif response.prompt_feedback:
                block_reason = response.prompt_feedback.block_reason
                console.print(f"[bold yellow]Response blocked. Reason: {block_reason}[/bold yellow]")
                
                if block_reason == "SAFETY":
                    # Güvenlik ayarlarını geçici olarak daha da gevşetelim
                    relaxed_safety_settings = [
                        {
                            "category": category,
                            "threshold": "BLOCK_NONE"
                        } for category, _ in safety_settings
                    ]
                    console.print("[yellow]Attempting with relaxed safety settings...[/yellow]")
                    response = self.chat_handler.model.generate_content(
                        [system_prompt, message],
                        safety_settings=relaxed_safety_settings,
                        generation_config={"temperature": 0.7, "top_p": 0.9, "top_k": 40},
                    )
                    if response.parts:
                        return response.text
                
                raise ValueError(f"Response blocked: {block_reason}")
            else:
                raise ValueError("No valid response or feedback from Gemini API")
        except Exception as e:
            console.print(f"[bold red]Error in Gemini code generation: {str(e)}[/bold red]")
            return None

    async def improve_code(self, existing_code, instructions, file_path):
        system_prompt = """
        You are an AI code improver. Your task is to analyze the existing code and improve it based on the given instructions.
        
        Follow these guidelines:
        1. Maintain or enhance code readability and efficiency.
        2. Ensure proper error handling and logging.
        3. Improve docstrings and comments where necessary.
        4. Refactor code to be more modular and reusable if possible.
        5. Add or improve type hints where appropriate.
        6. Optimize imports if needed.
        7. If there's an error, focus on fixing it while maintaining the original functionality.
        8. Do not include any markdown formatting or code block indicators (like ```python).
        9. Provide only the improved code, without any additional explanations or comments.
        10. Do not include any introductory text like "Here's the corrected code:". Start directly with the Python code.
        """
        
        message = f"Existing code:\n\n{existing_code}\n\nInstructions for improvement:\n{instructions}"
        
        if "gemini" in self.chat_handler.model_id:
            improved_code = await self._improve_code_gemini(message, system_prompt)
        else:
            improved_code, _ = await self.chat_handler.send_message(message, system_prompt)
        
        if improved_code:
            # Remove any potential markdown formatting and introductory text
            improved_code = improved_code.strip()
            improved_code = improved_code.replace("```python", "").replace("```", "").strip()
            if improved_code.startswith("Here's the corrected code:"):
                improved_code = improved_code.replace("Here's the corrected code:", "", 1).strip()
        
            # Dosyayı güncelle
            with open(file_path, 'w') as file:
                file.write(improved_code)
        
            return improved_code
        else:
            console.print("[bold red]Failed to improve code.[/bold red]")
            return None

    async def _improve_code_gemini(self, message, system_prompt):
        try:
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_DANGEROUS",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH",
                },
            ]

            response = self.chat_handler.model.generate_content(
                [system_prompt, message],
                safety_settings=safety_settings,
                generation_config={"temperature": 0.7, "top_p": 0.9, "top_k": 40},
            )

            if response.parts:
                improved_code = response.text.strip()
                if improved_code.startswith("Here's the corrected code:"):
                    improved_code = improved_code.replace("Here's the corrected code:", "", 1).strip()
                return improved_code
            elif response.prompt_feedback:
                block_reason = response.prompt_feedback.block_reason
                console.print(f"[bold yellow]Response blocked. Reason: {block_reason}[/bold yellow]")
                
                if block_reason == "SAFETY":
                    # Güvenlik ayarlarını geçici olarak daha da gevşetelim
                    relaxed_safety_settings = [
                        {
                            "category": category,
                            "threshold": "BLOCK_NONE"
                        } for category, _ in safety_settings
                    ]
                    console.print("[yellow]Attempting with relaxed safety settings...[/yellow]")
                    response = self.chat_handler.model.generate_content(
                        [system_prompt, message],
                        safety_settings=relaxed_safety_settings,
                        generation_config={"temperature": 0.7, "top_p": 0.9, "top_k": 40},
                    )
                    if response.parts:
                        improved_code = response.text.strip()
                        if improved_code.startswith("Here's the corrected code:"):
                            improved_code = improved_code.replace("Here's the corrected code:", "", 1).strip()
                        return improved_code
                
                raise ValueError(f"Response blocked: {block_reason}")
            else:
                raise ValueError("No valid response or feedback from Gemini API")
        except Exception as e:
            console.print(f"[bold red]Error in Gemini code improvement: {str(e)}[/bold red]")
            return None