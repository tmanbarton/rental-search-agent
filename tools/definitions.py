TOOL_DEFINITIONS = [
    {
        "name": "web_search",
        "description": """
        Search the web for apartment listings and rental housing. Use this tool first when the user provides search criteria. (location, bedrooms, price.) Construct targeted queries that include location, bedroom count, and price range — for example '2 bedroom apartments Denver CO under $1800'.
        Note, the user may not provide all query parts in the search criteria (location, bedroom count, price range). If location is missing, use the browser default location. If the user has that feature turned off, ask the user what location they want to search in. If bedroom count is missing, don't include that in the search criteria, i.e. include all room counts. If price ranch is missing, don't include that in the search criteria, i.e. search for all rentals in the provided area regardless of price.  
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
        "name": "hud_api",
        "description": "Look up the official HUD Fair Market Rent for a specific zip code and bedroom count. Use this after identifying listings to compare their asking price against the government's baseline market rate. A listing significantly above FMR is overpriced relative to the market; at or below FMR is a good value signal.",
        "input_schema": {
            "type": "object",
            "properties": {
                "zip_code": {
                    "type": "string",
                    "description": "5-digit US zip code as a string, e.g. '80203'. Used to determine the HUD metro area for Fair Market Rent lookup."
                },
                "bedroom_count": {
                    "type": "integer",
                    "description": "Number of bedrooms as an integer (1, 2, 3, or 4). Used to return the correct FMR for that unit size. Or 0 if no bedroom count is provided."
                }
            },
            "required": ["zip_code", "bedroom_count"]
        }
    },

    {
        "name": "census_api",
        "description": "Look up neighborhood demographic and housing dara for a zip code using the Census ACS dataset. Use this to add context about each listing's neighborhood — median income, commute times, population density, and vacancy rate. Call this after identifying specific zip codes from listings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "zip_code": {
                    "type": "string",
                    "description": "5-digit US zip code as a string, e.g. '80203'. Used to scope the ACS data to a specific neighborhood."
                },
                "variables": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["median_income", "commute_time", "population_density", "vacancy_rate"]
                    },
                    "description": "List of neighborhood data points to retrieve. Choose from: median_income, commute_time, population_density, vacancy_rate. Request only what's relevant to evaluation the listing."
                }
            },
            "required": ["zip_code", "variables"]
        }
    }
]

# description — the most important field for agent behavior. This is the only prose Claude reads when deciding whether to use a tool.
#               It answers: what does this tool do, and when should I reach for it? A vague description leads to Claude misusing tools or picking the wrong one.
#               A good description also implicitly tells Claude what it can't do — e.g. "use this to fetch a specific listing URL" implies Claude shouldn't use it for general searching.
# input_schema properties description - The description here is also Claude-facing — it helps Claude know what to actually put in that
#       field, so be specific (e.g. "5-digit US zip code" is better than "location")