import ddgs
import json

def search(query):
    results = ddgs.DDGS().text(query, max_results=4)
    formatted_results = json.dumps(results, indent=2)
    return formatted_results
