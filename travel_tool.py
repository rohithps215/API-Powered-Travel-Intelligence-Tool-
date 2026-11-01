import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://countriesnow.space/api/v0.1/countries")

def extract_data(json_response):
    """Safely extracts a dictionary whether the API returns a dict or a list."""
    if not isinstance(json_response, dict):
        return {}
    data = json_response.get("data", {})
    if isinstance(data, list) and len(data) > 0:
        return data[0]
    elif isinstance(data, dict):
        return data
    return {}

def get_country_summary(country_name: str):
    try:
        clean_name = country_name.strip()
        headers = {"User-Agent": "TravelSnapshotTool/1.0", "Content-Type": "application/json"}

        # 1. Fetch Capital & Currency info
        curr_res = requests.post(
            f"{BASE_URL}/currency",
            json={"country": clean_name},
            headers=headers,
            timeout=10
        )
        
        if curr_res.status_code == 404:
            return f"❌ Error: Country '{clean_name}' not found. Check the spelling."
        
        curr_json = curr_res.json()
        if curr_json.get("error", False):
            return f"❌ Error: Country '{clean_name}' not found. Check the spelling."

        curr_data = extract_data(curr_json)

        # 2. Fetch Capital
        cap_res = requests.post(
            f"{BASE_URL}/capital",
            json={"country": clean_name},
            headers=headers,
            timeout=10
        )
        cap_data = extract_data(cap_res.json()) if cap_res.status_code == 200 else {}

        # 3. Fetch Population
        pop_res = requests.post(
            f"{BASE_URL}/population",
            json={"country": clean_name},
            headers=headers,
            timeout=10
        )
        pop_data = extract_data(pop_res.json()) if pop_res.status_code == 200 else {}
        pop_counts = pop_data.get("populationCounts", []) if isinstance(pop_data, dict) else []
        latest_pop = f"{pop_counts[-1]['value']:,}" if pop_counts else "N/A"

        # 4. Fetch Dial Code & Flag
        flag_res = requests.post(
            f"{BASE_URL}/flag/unicode",
            json={"country": clean_name},
            headers=headers,
            timeout=10
        )
        flag_data = extract_data(flag_res.json()) if flag_res.status_code == 200 else {}
        flag = flag_data.get("unicodeFlag", "")

        return {
            "Country": f"{curr_data.get('name', clean_name)} {flag}".strip(),
            "Capital": cap_data.get("capital", "N/A") or "N/A",
            "Currency": curr_data.get("currency", "N/A"),
            "Population": latest_pop
        }

    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. Check your internet connection."
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {e}"
    except Exception as e:
        return f"❌ Parsing error: {e}"

def save_to_file(result, filename="sample_outputs.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*35}\n")
        if isinstance(result, dict):
            f.write(f"Snapshot: {result.get('Country')}\n")
            f.write(f"{'='*35}\n")
            for k, v in result.items():
                f.write(f"{k}: {v}\n")
        else:
            f.write(f"{result}\n")
            f.write(f"{'='*35}\n")

if __name__ == "__main__":
    test_countries = ["Japan", "Germany", "Switzerland", "Atlantis"]
    
    # Reset output file
    open("sample_outputs.txt", "w", encoding="utf-8").close()

    for c in test_countries:
        print(f"Fetching {c}...")
        res = get_country_summary(c)
        save_to_file(res, "sample_outputs.txt")
        if isinstance(res, dict):
            print(f"✅ {res['Country']}: Capital={res['Capital']}, Currency={res['Currency']}, Pop={res['Population']}")
        else:
            print(res)

    print("\n🎉 Done! All 4 tests written to 'sample_outputs.txt'.")