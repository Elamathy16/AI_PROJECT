# src/agent.py

from core_agent import Agent
from hsn_utils import validate_hsn_code, suggest_hsn_codes

agent = Agent()

@agent.on_message
def handle_message(msg):
    user_input = msg.text.strip()
    
    if user_input.isdigit():
        return validate_hsn_code(user_input)
    else:
        return suggest_hsn_codes(user_input)

# Mandatory for ADK
root_agent = agent
