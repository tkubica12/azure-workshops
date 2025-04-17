import logging

logger = logging.getLogger("multiagent")

# Ensure logger prints to console as well as OpenTelemetry
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


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
    logger.info(f"[{timestamp}] {agent_name.upper()}: {message}")

def print_supervisor_message(next_agent: str, supervisor_message: str, timestamp: str):
    logger.info(f"[{timestamp}] SUPERVISOR asks {next_agent.upper()}: {supervisor_message}")
