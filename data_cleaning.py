import pandas as pd

df = pd.read_csv("wikipedia_citations.csv")

df.dropna(inplace = True) #drop rows with empty cells

df = df.rename(columns={"article": "article_name"}) #clearer name

df = df.drop_duplicates(subset=["citation_link"]) #remove duplicate citations 

df = df[df["citation_link"].str.startswith("http", na=False)] #remove invalid links

df["citation_link"] = df["citation_link"].str.strip() #remove whitespace from links
df["citation_link"] = df["citation_link"].str.replace("https://www.", "https://", regex=False) #lowercase domains
df["citation_link"] = df["citation_link"].str.replace("http://www.", "http://", regex=False) #lowercase domains

df["is_archive_link"] = df["citation_link"].str.match(r"^https?://web\.archive\.org/web/", na=False) #flag if citation is already an Internet Archive link



df.to_csv("wikipedia_citations_clean.csv", index=False) #save cleaned version
df[~df["is_archive_link"]].to_csv("wikipedia_citations_clean_non_archive.csv", index=False)  # will use this one for waybackAPI calls
