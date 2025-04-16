from colorama import Fore, Style

def clear_file(path: str, initial_content: str = ""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(initial_content)

def append_log(path: str, agent_name: str, message: str, timestamp: str):
    with open(path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {agent_name.upper()}:\n{message}\n\n")

def append_iteration(path: str, document: str, timestamp: str):
    with open(path, "a", encoding="utf-8") as iter_file:
        iter_file.write(f"[{timestamp}] Current Document:\n{document}\n\n")

def print_agent_message(agent_name: str, message: str, timestamp: str):
    if agent_name == "writer":
        agent_display = Fore.GREEN + agent_name.upper() + Style.RESET_ALL
    elif agent_name == "finish":
        agent_display = Fore.MAGENTA + agent_name.upper() + Style.RESET_ALL
    else:
        agent_display = Fore.BLUE + agent_name.upper() + Style.RESET_ALL
    print(f"[{timestamp}] {agent_display}: {message}")

def print_supervisor_message(next_agent: str, supervisor_message: str, timestamp: str):
    supervisor_display = Fore.RED + "SUPERVISOR" + Style.RESET_ALL
    print(f"[{timestamp}] {supervisor_display} asks {next_agent.upper()}: {supervisor_message}")
