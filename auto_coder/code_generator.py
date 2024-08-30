from llm_chat.chat_handler import ChatHandler
from utils.helpers import log_token_usage
import os

class CodeGenerator:
    def __init__(self, chat_handler: ChatHandler):
        self.chat_handler = chat_handler

    async def generate_code(self, instructions, file_path):
        system_prompt = f"""
        You are an AI code generator. Your task is to generate high-quality, well-structured Python code based on the given instructions.
        The code will be saved in the file: {file_path}
        
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
        
        code, _ = await self.chat_handler.send_message(instructions, system_prompt)
        
        if code:
            # Remove any potential markdown formatting
            code = code.strip().replace("```python", "").replace("```", "").strip()
            
            # Dosyayı oluştur ve kodu yaz
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(code)
            
            return code
        else:
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
        """
        
        message = f"Existing code:\n\n{existing_code}\n\nInstructions for improvement:\n{instructions}"
        improved_code, _ = await self.chat_handler.send_message(message, system_prompt)
        
        if improved_code:
            # Remove any potential markdown formatting
            improved_code = improved_code.strip().replace("```python", "").replace("```", "").strip()
            
            # Dosyayı güncelle
            with open(file_path, 'w') as file:
                file.write(improved_code)
            
            return improved_code
        else:
            return None