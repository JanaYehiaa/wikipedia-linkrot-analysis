import pandas as pd
import requests
from tqdm import tqdm
from urllib.parse import urlparse
import os
import time
import ctypes, atexit   #added for windows keep-awake

# --- Prevent Windows from sleeping while running ---
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

def restore():
    """Restore normal sleep behavior on exit."""
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

atexit.register(restore)
# ---------------------------------------------------

ERROR_LOG_FILE = "errors.log"

def log_error(message: str):
    """Append error messages to a log file with timestamp."""
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def check_archive(link: str, category: str, article_name: str, retries: int = 3, backoff: int = 5):
    """Check Wayback availability API with retries."""
    AVAILABILITY_API_URL = "http://archive.org/wayback/available?url=" + link

    for attempt in range(retries):
        try:
            R = requests.get(AVAILABILITY_API_URL, timeout=10)
            break
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                wait = backoff * (2 ** attempt)  # exponential backoff
                print(f"Error {e} for {link}, retrying in {wait}s...")
                time.sleep(wait)
            else:
                msg = f"Failed after {retries} retries: {link}"
                print(msg)
                log_error(msg)
                return {
                    "citation_link": link,
                    "article_name": article_name,
                    "category": category,
                    "domain": None,
                    "found": False,
                    "archive_url": None,
                    "timestamp": None
                }

    try:
        domain = urlparse(link).netloc.lower()
    except Exception:
        domain = None

    result = {
        "citation_link": link,
        "article_name": article_name,
        "category": category,
        "domain": domain,
        "found": False,
        "archive_url": None,
        "timestamp": None
    }

    if R.status_code == 200:
        data = R.json()
        if "archived_snapshots" in data and "closest" in data["archived_snapshots"]:
            closest = data["archived_snapshots"]["closest"]
            if closest.get("available"):
                result["found"] = True
                result["archive_url"] = closest.get("url")
                result["timestamp"] = closest.get("timestamp")
    else:
        msg = f"Error {R.status_code} for {link}"
        print(msg)
        log_error(msg)

    return result


# --- Main Script ---
input_file = "wikipedia_citations_clean_non_archive.csv"
output_file = "wikipedia_citations_with_archive_status.csv"

df = pd.read_csv(input_file)

# Resume support: load existing results if file exists
if os.path.exists(output_file):
    df_done = pd.read_csv(output_file)
    done_links = set(df_done["citation_link"])
    print(f"Resuming from {len(done_links)} already processed links.")
else:
    df_done = pd.DataFrame()
    done_links = set()

# Process only remaining links
df_remaining = df[~df["citation_link"].isin(done_links)]

with open(output_file, "a", encoding="utf-8", newline="") as f:
    for i, (_, row) in enumerate(tqdm(df_remaining.iterrows(), total=len(df_remaining)), start=1):
        link = row["citation_link"]
        category = row["category"]
        article_name = row["article_name"]

        res = check_archive(link, category, article_name)
        pd.DataFrame([res]).to_csv(f, header=(f.tell() == 0), index=False)

        # Polite delay after successful request
        time.sleep(0.5)

        # Checkpoint flush every 100 requests
        if i % 100 == 0:
            f.flush()
            os.fsync(f.fileno())
            print(f"Progress saved at {i} requests.")

print("Done. Results saved to", output_file)
print(f"Any errors were logged in {ERROR_LOG_FILE}")
