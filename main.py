import asyncio
import os
import signal
from dotenv import load_dotenv, set_key
from llm_chat.chat_handler import ChatHandler
from auto_coder.code_generator import CodeGenerator
from agents.agent_manager import AgentManager
from utils.helpers import setup_logging, print_colored, clear_screen
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import ast
import traceback

console = Console()

THOTH_ASCII = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⢶⣒⣒⡢⠤⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⣩⣴⣾⣿⣿⡏⠀⡴⠛⠛⢢⡀⠹⣿⣿⣷⣦⡉⠂⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠁⠀⠈⣿⣿⣿⣿⣿⡀⠘⣇⠀⠀⣠⠇⠀⣿⣿⣿⣿⣿⠀⠀⠈⢁⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠢⢙⠻⠿⣿⣷⣀⠈⠙⠋⠁⢀⣼⣿⡿⠟⣋⠥⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⢬⣛⡻⠿⠶⠶⠾⠟⢛⠡⠐⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠃⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def signal_handler(sig, frame):
    console.print("\n[bold yellow]Ctrl+C detected. Exiting gracefully...[/bold yellow]")
    raise KeyboardInterrupt

async def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
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
            console.print("5. Settings")
            console.print("6. Exit")
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "6":
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
            elif choice == "5":
                settings_mode()
    
    except KeyboardInterrupt:
        print_colored("\nGoodbye, master!", "green")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")
        console.print(traceback.format_exc())
        console.print("[yellow]Please check your internet connection and API key, then try again.[/yellow]")
    finally:
        # Burada gerekirse temizlik işlemleri yapılabilir
        pass

def select_model():
    clear_screen()
    console.print(Panel("Select a model", expand=False, border_style="cyan"))
    console.print("1. Llama 3.1 70B (Preview)")
    console.print("2. Llama 3.1 8B (Preview)")
    console.print("3. Gemini 2 9B")
    console.print("4. Gemini 7B")
    console.print("5. Gemini 1.5 Pro")
    console.print("6. Gemini 1.5 Flash")
    console.print("7. Gemini 1.0 Pro")
    console.print("8. Groq LLaMA 70B")
    console.print("9. Groq Mixtral 8x7B")
    
    model_choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    
    model_map = {
        "1": "llama-3.1-70b-versatile",
        "2": "llama-3.1-8b-instant",
        "3": "gemini2-9b-it",
        "4": "gemma-7b-it",
        "5": "gemini-1.5-pro-latest",
        "6": "gemini-1.5-flash-latest",
        "7": "gemini-1.0-pro",
        "8": "llama2-70b-4096",
        "9": "mixtral-8x7b-32768"
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
            # Önce asistan yanıtını göster
            console.print(f"[bold green]Assistant:[/bold green] {response}")
            
            # Token kullanımını göster (eğer varsa)
            if usage:
                console.print(f"[dim]Estimated Token Usage: Prompt: {usage['prompt_tokens']}, Completion: {usage['completion_tokens']}, Total: {usage['total_tokens']}[/dim]")
        else:
            console.print("[bold red]Failed to get a response from the assistant. Please try again.[/bold red]")

async def ai_coder_mode(agent_manager):
    project_path = None
    main_file = None
    
    while True:
        clear_screen()
        console.print(Panel("AI Coder Mode", expand=False, border_style="yellow"))
        console.print("1. Generate Code")
        console.print("2. Improve Code")
        console.print("3. Exit")
        
        action = Prompt.ask("Choose action", choices=["1", "2", "3"])
        
        if action == "3":
            break
        elif action == "1":
            project_name = Prompt.ask("Enter project name")
            instructions = Prompt.ask("Enter code generation instructions")
            
            project_path = os.path.join(os.getcwd(), project_name)
            os.makedirs(project_path, exist_ok=True)
            
            main_file = f"{project_name.lower().replace(' ', '_')}.py"
            file_path = os.path.join(project_path, main_file)
            
            console.print("[yellow]Generating code...[/yellow]")
            code = await agent_manager.code_generator.generate_code(instructions, file_path)
            if code:
                console.print("[green]Code generated successfully![/green]")
                console.print(code)
                
                # Kodu otomatik olarak çalıştır
                await run_and_fix_code(agent_manager, project_path, main_file)
            else:
                console.print("[red]Failed to generate code.[/red]")
        
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
                try:
                    improved_code = await agent_manager.code_generator.improve_code(existing_code, fix_instructions, file_path)
                    
                    if improved_code:
                        # Check if the improved code is valid Python
                        if is_valid_python(improved_code):
                            with open(file_path, 'w') as file:
                                file.write(improved_code)
                            console.print("[green]Code has been improved and saved.[/green]")
                        else:
                            console.print("[bold red]The improved code is not valid Python. Keeping the original version.[/bold red]")
                            console.print("[yellow]Invalid code:[/yellow]")
                            console.print(improved_code)
                    else:
                        console.print("[bold red]Failed to improve the code. Keeping the original version.[/bold red]")
                except Exception as e:
                    console.print(f"[bold red]Error while trying to improve code: {str(e)}[/bold red]")
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

def settings_mode():
    clear_screen()
    console.print(Panel("Settings", expand=False, border_style="cyan"))
    console.print("1. Set Groq API Key")
    console.print("2. Set OpenAI API Key")
    console.print("3. Set Gemini API Key")
    console.print("4. Back to Main Menu")
    
    choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"])
    
    if choice == "1":
        set_api_key("GROQ_API_KEY")
    elif choice == "2":
        set_api_key("OPENAI_API_KEY")
    elif choice == "3":
        set_api_key("GEMINI_API_KEY")
    elif choice == "4":
        return

def set_api_key(key_name):
    api_key = Prompt.ask(f"Enter your {key_name}", password=True)
    # Tırnak işaretlerini kaldır ve boşlukları temizle
    api_key = api_key.strip().strip("'\"")
    # API anahtarını doğrudan kaydet, tırnak işareti ekleme
    set_key(".env", key_name, api_key, quote_mode="never")
    console.print(f"[green]{key_name} has been updated.[/green]")
    input("Press Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())