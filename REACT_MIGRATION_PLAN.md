# Future Plan: React Migration

The current frontend (`index.html`) is a single-file chat UI for testing the agent backend. Once the backend is stable, the plan is to migrate to a React app with a different UX model.

## Goals

- Replace the full-screen chat window with a **search bar + results grid** layout
- Display rental listings as cards (image, price, beds, location, link)
- Learn React in the process — this is a hands-on learning project, not a Claude Code task

## What Changes

- **Input**: Chat textarea becomes a search/query bar
- **Output**: Message bubbles become a responsive card grid of listings
- **Backend contract**: Return structured listing data (`{ listings: [...] }`) instead of plain text responses
- **State**: Query string, loading flag, results array — simple enough for `useState`

## What Stays the Same

- Single-page app, no routing needed
- POST to the same backend endpoint
- Natural language queries as input

## Notes

- No timeline — this happens after the agent backend is functional and tested
- Keep it simple: no Redux, no heavy dependencies
- The current `index.html` stays around for basic conversational testing
