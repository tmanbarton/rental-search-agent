TOOL_DEFINITIONS = [
    {
        "name": "web_search",
        "description": """
        Search the web for apartment listings and rental housing. Use this tool first when the user provides search criteria. (location, bedrooms, price.) Construct targeted queries that include location, bedroom count, and price range — for example '2 bedroom apartments Denver CO under $1800'.
        Note, the user may not provide all query parts in the search criteria (location, bedroom count, price range). If location is missing, ask the user what location they want to search in. If bedroom count is missing, don't include that in the search criteria, i.e. include all room counts. If price range is missing, don't include that in the search criteria, i.e. search for all rentals in the provided area regardless of price.  
        Do not use this tool to get pricing benchmarks or neighborhood statistics — use hud_api and census_api for those instead.
        """, #
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": """
                    A targeted search query including location, bedroom count, and price range.
                    Example: '2 bedroom apartments Denver CO under $1800 site:zillow.com OR site:apartments.com'
                    Example if location is missing: '1 bedroom apartments [current location - Denver Colorado] between $1000 and $1900 site:zillow.com OR site:apartments.com' or request location if user has turned off browser location
                    Example if bedroom count is missing: 'Apartments in Denver CO under $2000 site:zillow.com OR site:apartments.com'
                    Example if price is missing: '2 bedroom house for rent in denver CO site:zillow.com OR site:apartments.com'
                    ONLY SEARCH ON THE SITE Zillow. Other sites block access when fetching pages from Python code.
                    """
                }
            },
            "required": ["query"]
        }
    },

    {
        "name": "fetch_page",
        "description": "Fetch and extract the full content of a specific webpage. Use this after web_search returns promising listing URLs — fetch each URL to extract full details like exact price, square footage, amenities, lease terms, and contact info that doesn't appear in search snippets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL of the listing page to fetch, including https://"
                }
            },
            "required": ["url"]
        }
    },

    {
        "name": "get_area_data",
        "description": "Look up HUD Fair Market Rent and Census neighborhood data for a zip code. Use this after identifying listings to compare asking prices against the government baseline market rate and add neighborhood context. A listing significantly above FMR is overpriced; at or below FMR is a good value signal.",
        "input_schema": {
            "type": "object",
            "properties": {
                "zip_code": {
                    "type": "string",
                    "description": "5-digit US zip code as a string, e.g. '80203'."
                },
                "bedroom_count": {
                    "type": "integer",
                    "description": "Number of bedrooms (1, 2, 3, or 4). Use 0 if the user did not specify a bedroom count."
                },
                "variables": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["median_income", "commute_time", "population_density", "vacancy_rate"]
                    },
                    "description": "Neighborhood data points to retrieve. Request only what's relevant to evaluating the listing."
                }
            },
            "required": ["zip_code", "bedroom_count", "variables"]
        }
    }
]

# description — the most important field for agent behavior. This is the only prose Claude reads when deciding whether to use a tool.
#               It answers: what does this tool do, and when should I reach for it? A vague description leads to Claude misusing tools or picking the wrong one.
#               A good description also implicitly tells Claude what it can't do — e.g. "use this to fetch a specific listing URL" implies Claude shouldn't use it for general searching.
# input_schema properties description - The description here is also Claude-facing — it helps Claude know what to actually put in that
#       field, so be specific (e.g. "5-digit US zip code" is better than "location")