from anthropic import Anthropic

from tools.definitions import TOOL_DEFINITIONS
from tools.fetch_page import fetch_page
from tools.get_area_data import get_data
from tools.web_search import search

# Arbitrary number
MAX_TOOL_CALLS = 10
client = Anthropic()

async def run_agent(user_input, messages):
    # Add the user's message to the conversation history
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Send the full conversation history (including tool definitions) to Claude
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        tools=TOOL_DEFINITIONS,
        messages=messages
        # system=system_message todo
    )
    num_tool_calls = 0

    # Agentic loop: keep going until Claude is done (end_turn).
    # Each iteration either handles a final text response or processes tool calls
    # and sends the results back to Claude for another round.
    while True:
        if num_tool_calls >= MAX_TOOL_CALLS:
            messages.append({
                "role": "assistant",
                "content": f"The number of tool calls reached the maximum allowed limit: {MAX_TOOL_CALLS}. Interrupting the process."
            })
            break
        if response.stop_reason == "end_turn":
            # Claude is done — extract the text and add it to conversation history
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            yield response.content[0].text
            break
        elif response.stop_reason == "tool_use":
            # Add the full assistant response to history. Must use response.content
            # (the entire content block array), not just the text — the API needs to
            # see the ToolUseBlocks so it can match them with the tool results below.
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # response.content is a list that can mix TextBlocks and ToolUseBlocks.
            # We iterate through all of them, yielding any text to the client and
            # executing any tool calls.
            tool_response_results = []
            for block in response.content:
                if block.type == "text":
                    response_text = block.text
                    yield response_text
                elif block.type == "tool_use":
                    num_tool_calls += 1
                    tool_id = block.id
                    tool_name = block.name
                    tool_input = block.input
                    tool_result = call_tool(tool_name, tool_input)

                    # Each result must reference the tool_use_id so Claude knows
                    # which tool call this result belongs to.
                    tool_response_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": tool_result
                    })

            # Send all tool results back in a single "user" message.
            # The API expects: assistant (with ToolUseBlocks) -> user (with tool_results).
            # If Claude called multiple tools, all results go in one message.
            messages.append({
                "role": "user",
                "content": tool_response_results
            })

        # Send updated conversation back to Claude for the next iteration.
        # If we just handled tool calls, Claude will see the results and decide
        # whether to call more tools or give a final answer (end_turn).
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=TOOL_DEFINITIONS,
            messages=messages
            # system=system_message todo
        )

def call_tool(tool_name, tool_input):
    result = None
    if tool_name == "web_search":
        result = search(tool_input["query"])
    elif tool_name == "fetch_page":
        result = fetch_page(tool_input["url"])
    elif tool_name == "get_area_data":
        result = get_data(tool_input["zip_code"], tool_input["bedroom_count"], tool_input["variables"])

    return result