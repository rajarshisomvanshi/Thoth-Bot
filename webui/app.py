from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
from agents.agent_manager import AgentManager

def create_app(agent_manager: AgentManager):
    app = FastAPI()

    app.mount("/static", StaticFiles(directory="webui/static"), name="static")

    @app.get("/")
    async def get():
        with open("webui/templates/index.html", "r") as f:
            content = f.read()
        return HTMLResponse(content)

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await agent_manager.add_task("chat", message=data)
            response = await asyncio.wait_for(get_next_response(agent_manager), timeout=30.0)
            await websocket.send_text(response)

    async def get_next_response(agent_manager):
        while True:
            await agent_manager.process_next_task()
            if agent_manager.chat_handler.conversation_history:
                last_message = agent_manager.chat_handler.conversation_history[-1]
                if last_message["role"] == "assistant":
                    return last_message["content"]
            await asyncio.sleep(0.1)

    return app