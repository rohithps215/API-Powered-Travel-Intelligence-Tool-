# API-Powered Travel Intelligence Tool

A Python CLI tool that fetches key travel data (capital, currency, population, and flag) for any country using a public REST API and saves the results to a file.

---

## Features
- **Public API Integration:** Retrieves live country data via REST endpoints.
- **Graceful Error Handling:** Handles unknown countries, network drops, and schema mismatches without crashing.
- **External Configuration:** Uses `.env` to store the API base URL.
- **Automatic Export:** Writes query outputs directly into `sample_outputs.txt`.

---

## Setup & Usage

1. **Install dependencies:**
   ```bash
   pip install requests python-dotenv