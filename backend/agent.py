import os

import anthropic

from tools.definitions import TOOL_DEFINITIONS

async def run_agent(user_input, messages):
    messages.append({
        "role": "user",
        "content": user_input
    })

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=TOOL_DEFINITIONS,
        messages=messages
        # system=system_message todo
    )
    return response
