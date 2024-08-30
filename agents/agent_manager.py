import asyncio
from llm_chat.chat_handler import ChatHandler
from auto_coder.code_generator import CodeGenerator

class AgentManager:
    def __init__(self, chat_handler: ChatHandler, code_generator: CodeGenerator):
        self.chat_handler = chat_handler
        self.code_generator = code_generator
        self.task_queue = asyncio.Queue()

    async def add_task(self, task_type, **kwargs):
        await self.task_queue.put((task_type, kwargs))

    async def process_next_task(self):
        if self.task_queue.empty():
            return None, None

        task_type, kwargs = await self.task_queue.get()

        try:
            if task_type == "chat":
                response, usage = await self.chat_handler.send_message(kwargs["message"])
                return response, usage
            elif task_type == "generate_code":
                code = await self.code_generator.generate_code(kwargs["instructions"], kwargs["file_path"])
                if code:
                    print(f"Generated code for {kwargs['file_path']}:\n{code}")
                    return code, None
                else:
                    print(f"Failed to generate code for {kwargs['file_path']}")
                    return None, None
            elif task_type == "improve_code":
                improved_code = await self.code_generator.improve_code(kwargs["existing_code"], kwargs["instructions"], kwargs["file_path"])
                if improved_code:
                    print(f"Improved code:\n{improved_code}")
                    return improved_code, None
                else:
                    print(f"Failed to improve code for {kwargs['file_path']}")
                    return None, None
            else:
                print(f"Unknown task type: {task_type}")
                return None, None
        except Exception as e:
            print(f"Error processing task: {str(e)}")
            return None, None

    async def process_chat(self, message):
        await self.add_task("chat", message=message)
        return await self.process_next_task()

    def reset_chat(self):
        self.chat_handler.reset_conversation()