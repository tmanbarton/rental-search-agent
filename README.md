# Apartment Search Agent

A chat-based web tool that takes natural language input and returns a structured analysis of rental listings, combining real market data with live listing search.

Built as a learning project for agentic AI patterns — tool use, multi-step decision making, and structured output.

---

## What It Does

- Accepts natural language queries like *"find me a 2BR apartment in Denver under $1800"*
- Searches the web for live listings across Zillow, Apartments.com, and Craigslist
- Fetches full listing details from promising URLs
- Compares listing prices against HUD Fair Market Rent benchmarks
- Adds neighborhood context (median income, commute times, population density, vacancy rate) via Census ACS data
- Returns a structured JSON analysis with a summary recommendation

---

## Stack

| Layer             | Technology                                        |
|-------------------|---------------------------------------------------|
| Backend           | Python, FastAPI                                   |
| AI                | Anthropic Claude API (claude-sonnet-4-6)          |
| Frontend          | HTML, CSS, vanilla JS                             |
| Streaming         | Server-Sent Events (SSE)                          |
| Area Data         | HUD Fair Market Rents API & Census Bureau ACS API |

---

## Project Structure

```
apartment_agent/
├── backend/
│   ├── main.py              # FastAPI app and routes
│   ├── agent.py             # Agentic loop (core logic)
│   ├── output.py            # Structured JSON output
│   └── tools/
│       ├── definitions.py   # Tool schemas for Claude
│       ├── web_search.py    # Web search implementation
│       ├── fetch_page.py    # Page fetching implementation
│       ├── hud_api.py       # HUD Fair Market Rents API
│       └── census_api.py    # Census ACS API
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## Setup

### Prerequisites

- Python 3.10+
- Anthropic API key
- HUD API key — [get one here](https://www.huduser.gov/hudapi/public/register?comingfrom=fmr)
- Census Bureau API key — [get one here](https://api.census.gov/data/key_signup.html)

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/apartment-search-agent.git
cd apartment-search-agent

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the `backend/` directory:

```
ANTHROPIC_API_KEY=your_key_here
HUD_API_KEY=your_key_here
CENSUS_API_KEY=your_key_here
```

### Running the App

```bash
cd backend
uvicorn main:app --reload
```

Then open `frontend/index.html` in your browser.

---

## How It Works

### The Agentic Loop

Claude is given four tools and decides which to call, in what order, based on what it finds. The loop runs until Claude determines it has enough information to produce a final answer.

```
User query
  → Claude calls web_search
    → Claude calls fetch_page on promising URLs
      → Claude calls hud_api for each zip code
        → Claude calls census_api for neighborhood context
          → Claude produces structured JSON output
```

### Tools

| Tool | Purpose                                                                                                               |
|---|-----------------------------------------------------------------------------------------------------------------------|
| `web_search` | Find listings matching user criteria                                                                                  |
| `fetch_page` | Extract full details from a listing URL                                                                               |
| `get_area_data` | Get HUD Fair Market Rent for a zip code and bedroom count & get neighborhood data (income, commute, density, vacancy) |

### Streaming

The agent streams status updates to the frontend via Server-Sent Events as it works, so the user sees progress in real time rather than waiting for a single response.

### Output

Final output is structured JSON containing:
- Compared listings with address, price, and key details
- Price vs. HUD Fair Market Rent for each listing
- Neighborhood context for each zip code
- A summary recommendation

---

## Key Concepts Learned

- Defining tools and passing them to the Anthropic API
- Handling `tool_use` responses and returning `tool_result` messages
- Multi-step agentic loop where Claude decides what to do next
- Combining structured output with tool use
- Server-Sent Events for streaming agent status to a frontend

---

## Related Projects

This is Project 4 in a series of AI learning projects:

| # | Project | Concepts |
|---|---|---|
| 1 | CLI Chatbot | Conversation history |
| 2 | RAG Chatbot | Retrieval-augmented generation |
| 3 | Structured Output | JSON schema, structured responses |
| 4 | Apartment Search Agent | Tool use, agentic loop, SSE streaming |

---

## Status

- [x] Tool definitions (`tools/definitions.py`)
- [ ] Agent loop (`agent.py`)
- [ ] Tool implementations (`tools/*.py`)
- [ ] FastAPI backend (`main.py`)
- [ ] Structured output (`output.py`)
- [ ] Frontend (`frontend/`)
- [ ] SSE streaming