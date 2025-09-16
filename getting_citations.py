import requests
import pandas as pd

# ---- Config ----
CATEGORIES = [
    "Culture",
    "Geography",
    "Health",
    "History",
    "Human activities",
    "Mathematics",
    "Natural sciences",
    "People",
    "Philosophy",
    "Religion",
    "Society",
    "Technology",
    "General reference"
]

WIKI_API = "https://en.wikipedia.org/w/api.php"


HEADERS = {
    "User-Agent": "WikiProjectBot/1.0 (lenovo@example.com)" 
}


# ---- Helper: get 5 article titles from a category ----
def get_titles_from_category(category: str, limit: int = 5):
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": limit,
        "format": "json"
    }
    r = requests.get(WIKI_API, params=params, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        return [page["title"] for page in data["query"]["categorymembers"]]
    return []


# ---- Helper: get citation links from an article ----
def get_citations_from_article(title: str):
    params = {
        "action": "parse",
        "page": title,
        "prop": "externallinks",
        "format": "json"
    }
    r = requests.get(WIKI_API, params=params, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        if "parse" in data and "externallinks" in data["parse"]:
            return data["parse"]["externallinks"]
    return []


# ---- Main pipeline ----
def build_dataset():
    rows = []

    for category in CATEGORIES:
        print(f"Processing category: {category}")
        titles = get_titles_from_category(category, limit=5)

        for title in titles:
            citations = get_citations_from_article(title)
            for citation in citations:
                rows.append({
                    "category": category,
                    "article": title,
                    "citation_link": citation
                })

    df = pd.DataFrame(rows)
    return df


# ---- Run ----
if __name__ == "__main__":
    df = build_dataset()
    print(df.head())
    df.to_csv("wikipedia_citations.csv", index=False)
    print("Saved to wikipedia_citations.csv")
