## Obstacle Log

1. **API Changes & Access**: The original countries API was deprecated and blocked without keys.  
   *Fix*: Switched to a free, keyless API (`countriesnow.space`) and managed URLs in `.env`.

2. **Inconsistent Data Formats**: Some endpoints returned dictionaries, while others returned lists.  
   *Fix*: Added a helper function to safely extract data from either format without errors.

3. **Invalid Inputs**: Unknown countries could crash the app.  
   *Fix*: Used `try/except` and status checks to display clear error messages (e.g., testing "Atlantis").