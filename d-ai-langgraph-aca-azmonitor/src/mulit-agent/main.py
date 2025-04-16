from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
import datetime
from colorama import init, Fore, Style

from agents import agents, system_prompt
from config import log_file_path, itinerary_file_path, current_document_path, user_message
from utils import clear_file, append_log, append_iteration, print_agent_message, print_supervisor_message

# --- Initialization ---
load_dotenv()
init(autoreset=True)

options = list(agents.keys())

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to finish."""
    next: Literal[*options]
    supervisor_message: str  # Message from supervisor to the worker

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2024-08-01-preview",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

class State(MessagesState):
    next: str
    supervisor_message: str = ""
    current_document: str = ""  # Track the current version of the document
    conversation_summary: str = ""  # Track the conversation summary

def supervisor_node(state: State) -> Command[Literal[*agents.keys(), "__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    
    # Add current document as context if it exists
    if state["current_document"]:
        messages.append({"role": "system", "content": f"Current travel itinerary document:\n\n{state['current_document']}"})
    
    # Update conversation summary with all non-user messages
    new_messages = state["messages"][1:]  # exclude the first user message
    if new_messages:
        messages_text = "\n".join(f"{msg.name}: {msg.content}" for msg in new_messages)
        summary_prompt = (
            f"Update the conversation summary. Existing summary:\n{state.get('conversation_summary', '')}\n\n"
            f"New messages:\n{messages_text}\n\n"
            "Ensure key information is stored: who suggested what, key dates, places, entities, main ideas. "
            "Provide the updated summary."
        )
        summary_response = llm.invoke([{"role": "system", "content": summary_prompt}])
        updated_summary = summary_response.content
        state["conversation_summary"] = updated_summary
        # Remove all messages except the first user message
        state["messages"] = state["messages"][:1]
    
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    supervisor_message = response["supervisor_message"]
    
    # Add supervisor message to the conversation
    supervisor_msg = HumanMessage(content=supervisor_message, name="supervisor")
    
    return Command(
        goto=goto, 
        update={
            "next": goto,
            "supervisor_message": supervisor_message,
            "messages": state["messages"] + [supervisor_msg]
        }
    )


def create_agent_node(agent_name: str):
    # Enhance system prompt to make sure worker understands messages from supervisor
    enhanced_prompt = agents[agent_name]["system_prompt"] + f"""   
When responding, remember to identify yourself clearly as {agent_name}.
Messages from the supervisor will be directing you to specific tasks or asking for particular information.
"""
    agent = create_react_agent(llm, tools=[], prompt=enhanced_prompt)

    def agent_node(state: State) -> Command[Literal["supervisor", "__end__"]]:
        if agent_name != "writer":
            context = (
                f"Current travel itinerary document:\n\n{state.get('current_document', '')}\n\n"
                f"Current conversation summary:\n\n{state.get('conversation_summary', '')}"
            )
            context_message = HumanMessage(content=context, name="context")
            state = {**state, "messages": state["messages"] + [context_message]}
        
        result = agent.invoke(state)
        next_step = "supervisor" if agent_name != "finish" else END

        # Get response content
        response_content = result["messages"][-1].content
        
        # If this is the writer agent, update the current document
        if agent_name == "writer":
            # Save the document to file and update state
            with open(itinerary_file_path, "w", encoding="utf-8") as itinerary_file:
                itinerary_file.write(response_content)
            
            return Command(
                update={
                    "messages": [HumanMessage(content=response_content, name=agent_name)],
                    "current_document": response_content
                },
                goto=next_step,
            )
        elif agent_name == "finish":
            # Final save of the document
            with open(itinerary_file_path, "w", encoding="utf-8") as itinerary_file:
                itinerary_file.write(state["current_document"])
                
        return Command(
            update={
                "messages": [
                    HumanMessage(content=response_content, name=agent_name)
                ]
            },
            goto=next_step,
        )

    return agent_node

def main():
    builder = StateGraph(State)
    builder.add_edge(START, "supervisor")
    builder.add_node("supervisor", supervisor_node)

    for agent_name in agents.keys():
        builder.add_node(agent_name, create_agent_node(agent_name))

    graph = builder.compile()

    # Clear and initialize files
    clear_file(log_file_path, f"# Travel Itinerary Log\n\n**User Request:** {user_message}\n\n")
    clear_file(itinerary_file_path, "")

    for s in graph.stream(
        {"messages": [("user", user_message)], "current_document": ""}, subgraphs=True
    ):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if isinstance(s, tuple) and len(s) == 2:
            _, data = s
            for agent, content in data.items():
                if "messages" in content and "next" not in content:
                    for message_obj in content["messages"]:
                        if getattr(message_obj, "name", None) is None:
                            continue
                        message = message_obj.content
                        agent_name = message_obj.name
                        short_message = (message[:97] + "...") if len(message) > 100 else message
                        if agent_name != "supervisor":
                            print_agent_message(agent_name, short_message, timestamp)
                            append_log(log_file_path, agent_name, message, timestamp)
                elif "next" in content:
                    next_agent = content["next"]
                    supervisor_message = content.get("supervisor_message", "")
                    if not supervisor_message and "messages" in content and len(content["messages"]) > 0:
                        supervisor_message = content["messages"][-1].content
                    print_supervisor_message(next_agent, supervisor_message, timestamp)
                    append_log(log_file_path, f"SUPERVISOR asks {next_agent.upper()}", supervisor_message, timestamp)
                    with open(itinerary_file_path, "r", encoding="utf-8") as doc_file:
                        current_doc = doc_file.read()
                    append_iteration(current_document_path, current_doc, timestamp)

if __name__ == "__main__":
    main()