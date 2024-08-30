import asyncio
import os
from dotenv import load_dotenv
from llm_chat.chat_handler import ChatHandler
from auto_coder.code_generator import CodeGenerator
from agents.agent_manager import AgentManager
from utils.helpers import setup_logging, print_colored, clear_screen
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import ast

console = Console()

THOTH_ASCII = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⢶⣒⣒⡢⠤⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠄⣊⣥⣶⡿⠛⠛⠛⠻⢿⣶⣬⡑⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⣩⣴⣾⣿⣿⡏⠀⡴⠛⠛⢢⡀⠹⣿⣿⣷⣦⡉⠂⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠁⠀⠈⣿⣿⣿⣿⣿⡀⠘⣇⠀⠀⣠⠇⠀⣿⣿⣿⣿⣿⠀⠀⠈⢁⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠢⢙⠻⠿⣿⣷⣀⠈⠙⠋⠁⢀⣼⣿⡿⠟⣋⠥⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⢬⣛⡻⠿⠶⠶⠾⠟⢛⠡⠐⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠃⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

async def main():
    try:
        load_dotenv()
        setup_logging()
        
        while True:
            clear_screen()
            console.print(THOTH_ASCII, style="cyan")
            print_colored("Welcome to Thoth Bot", "green")
            console.print(Panel("Main Menu", expand=False, border_style="cyan"))
            console.print("1. Chat")
            console.print("2. AI Coder")
            console.print("3. Agents")
            console.print("4. Web UI Mode")
            console.print("5. Exit")
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5"])
            
            if choice == "5":
                print_colored("Goodbye, master!", "green")
                break
            
            if choice in ["1", "2", "3"]:
                model_id = select_model()
                chat_handler = ChatHandler(model_id)
                code_generator = CodeGenerator(chat_handler)
                agent_manager = AgentManager(chat_handler, code_generator)
            
            if choice == "1":
                await chat_mode(agent_manager)
            elif choice == "2":
                await ai_coder_mode(agent_manager)
            elif choice == "3":
                await agents_mode(agent_manager)
            elif choice == "4":
                await web_ui_mode()
    
    except Exception as e:
        console.print(f"[bold red]An error occurred: {str(e)}")
        console.print_exception()

def select_model():
    clear_screen()
    console.print(Panel("Select a model", expand=False, border_style="cyan"))
    console.print("1. Llama 3.1 70B (Preview)")
    console.print("2. Llama 3.1 8B (Preview)")
    console.print("3. Gemma 2 9B")
    console.print("4. Gemma 7B")
    
    model_choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"])
    
    model_map = {
        "1": "llama-3.1-70b-versatile",
        "2": "llama-3.1-8b-instant",
        "3": "gemma2-9b-it",
        "4": "gemma-7b-it"
    }
    
    return model_map.get(model_choice, "llama-3.1-8b-instant")

async def chat_mode(agent_manager):
    clear_screen()
    console.print(Panel("Chat Mode", expand=False, border_style="green"))
    console.print("Type 'exit' to return to the main menu.")
    
    while True:
        user_input = Prompt.ask("\nYou")
        if user_input.lower() == "exit":
            break
        
        # Asistan yanıtını al
        response, usage = await agent_manager.process_chat(user_input)
        
        if response:
            # HTTP isteği bilgisini göster (bu bilgi otomatik olarak loglama sisteminden gelecek)
            
            # Önce asistan yanıtını göster
            console.print(f"[bold green]Assistant:[/bold green] {response}")
            
            # Token kullanımını göster
            if usage:
                console.print(f"[dim]Token Usage: Prompt: {usage['prompt_tokens']}, Completion: {usage['completion_tokens']}, Total: {usage['total_tokens']}[/dim]")
        
        # Yeni yanıtı sohbet geçmişine ekle
        agent_manager.chat_handler.conversation_history.append({"role": "assistant", "content": response})

async def ai_coder_mode(agent_manager):
    project_path = None
    main_file = None
    
    while True:
        clear_screen()
        console.print(Panel("AI Coder Mode", expand=False, border_style="yellow"))
        action = Prompt.ask("Choose action", choices=["generate", "improve", "exit"])
        if action == "exit":
            break
        elif action == "generate":
            project_name = Prompt.ask("Enter project name")
            instructions = Prompt.ask("Enter code generation instructions")
            
            project_path = os.path.join(os.getcwd(), project_name)
            os.makedirs(project_path, exist_ok=True)
            
            main_file = f"{project_name.lower().replace(' ', '_')}.py"
            file_path = os.path.join(project_path, main_file)
            
            await agent_manager.add_task("generate_code", instructions=instructions, file_path=file_path)
            await agent_manager.process_next_task()
            
            await run_and_fix_code(agent_manager, project_path, main_file)
            
        elif action == "improve":
            if not project_path or not main_file:
                console.print("[bold red]No project generated yet. Please generate a project first.[/bold red]")
                input("Press Enter to continue...")
                continue
            
            file_path = os.path.join(project_path, main_file)
            with open(file_path, 'r') as file:
                existing_code = file.read()
            instructions = Prompt.ask("Enter improvement instructions")
            await agent_manager.add_task("improve_code", existing_code=existing_code, instructions=instructions, file_path=file_path)
            await agent_manager.process_next_task()
            
            await run_and_fix_code(agent_manager, project_path, main_file)
        
        input("Press Enter to continue...")

async def run_and_fix_code(agent_manager, project_path, main_file):
    max_attempts = 3
    for attempt in range(max_attempts):
        file_path = os.path.join(project_path, main_file)
        if not os.path.exists(file_path):
            console.print(f"[bold red]Error: File {file_path} does not exist.[/bold red]")
            return

        console.print(f"[bold green]Running {main_file} (Attempt {attempt + 1}/{max_attempts})...[/bold green]")
        process = subprocess.Popen(["python", main_file], cwd=project_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            console.print("[bold green]Code ran successfully![/bold green]")
            console.print(stdout)
            break
        else:
            console.print(f"[bold red]Error occurred (Attempt {attempt + 1}/{max_attempts}):[/bold red]")
            console.print(stderr)
            
            if attempt < max_attempts - 1:
                console.print("[yellow]Attempting to fix the error...[/yellow]")
                
                with open(file_path, 'r') as file:
                    existing_code = file.read()
                
                fix_instructions = f"Fix the following error in the code:\n\n{stderr}\n\nExisting code:\n\n{existing_code}"
                await agent_manager.add_task("improve_code", existing_code=existing_code, instructions=fix_instructions, file_path=file_path)
                improved_code, _ = await agent_manager.process_next_task()
                
                if improved_code:
                    # Check if the improved code is valid Python
                    if is_valid_python(improved_code):
                        with open(file_path, 'w') as file:
                            file.write(improved_code)
                        console.print("[green]Code has been improved and saved.[/green]")
                    else:
                        console.print("[bold red]The improved code is not valid Python. Keeping the original version.[/bold red]")
                else:
                    console.print("[bold red]Failed to improve the code. Keeping the original version.[/bold red]")
            else:
                console.print("[bold red]Failed to fix the code after maximum attempts.[/bold red]")
    
    input("Press Enter to continue...")

def is_valid_python(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

async def agents_mode(agent_manager):
    clear_screen()
    console.print(Panel("Agents Mode", expand=False, border_style="magenta"))
    console.print("Agents mode is not implemented yet.")
    input("Press Enter to return to the main menu...")

async def web_ui_mode():
    clear_screen()
    console.print(Panel("Web UI Mode", expand=False, border_style="blue"))
    try:
        subprocess.Popen(["npm", "run", "dev"], cwd="webui")
        console.print("Web UI development server started. Access it at http://localhost:3000")
        console.print("Press Ctrl+C to stop the server and return to the main menu.")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        console.print("Stopping Web UI server...")
    except FileNotFoundError:
        console.print("[bold red]Error: npm command not found. Make sure Node.js and npm are installed.")
    input("Press Enter to return to the main menu...")

if __name__ == "__main__":
    asyncio.run(main())