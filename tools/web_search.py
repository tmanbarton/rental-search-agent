s = \
{
    "name": "web_search",
    "description": "Use this tool any time the user requests data on housing...",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to search the web with."
            }
        },
        "required": ["query"]
    }
}