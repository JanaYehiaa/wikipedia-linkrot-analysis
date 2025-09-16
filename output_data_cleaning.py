import pandas as pd

df = pd.read_csv("wikipedia_citations_with_archive_status.csv")

df = df.drop_duplicates(subset=["citation_link"]) #remove duplicate links

df = df[df["citation_link"].str.startswith("http", na=False)] #remove invalid links

df["citation_link"] = df["citation_link"].str.strip()  # remove whitespace
df["citation_link"] = df["citation_link"].str.replace("https://www.", "https://", regex=False)
df["citation_link"] = df["citation_link"].str.replace("http://www.", "http://", regex=False)
df["citation_link"] = df["citation_link"].str.lower()  # lowercase entire link for consistency

df.to_csv("wikipedia_citations_final.csv", index=False)

