import pandas as pd
import matplotlib.pyplot as plt

# --- Load datasets ---
df_clean = pd.read_csv("wikipedia_citations_clean.csv")
df_final = pd.read_csv("wikipedia_citations_final.csv")

# --- Colors ---
BEIGE = "#F3E9D7"
MAROON = "#7B2D26"  # slightly brighter for better contrast
BROWN = "#3C2C21"
HIGHLIGHT = "#C28F2C"  # muted gold accent for emphasis (optional)

# --- Font sizes (standardized) ---
TITLE_SIZE = 14
LABEL_SIZE = 12
TICK_SIZE = 10

# --- 1. Pie chart: % citations already archive links ---
counts = df_clean["is_archive_link"].fillna(False).value_counts()
plt.figure(figsize=(6,6))
plt.pie(
    counts,
    labels=["Archived Link", "Regular Link"],
    colors=[MAROON, BROWN],
    autopct="%1.1f%%",
    textprops={"color": "black", "fontsize": LABEL_SIZE}
)
plt.title("Citations That Are Already Archived", fontsize=TITLE_SIZE, fontweight="bold", color=BROWN)
plt.savefig("viz1_pie_already_archived.png", dpi=300, facecolor=BEIGE)
plt.close()

# --- 2. % regular links archived (pie) ---
total_links = len(df_final)
archived_count = df_final["found"].sum()
archived = archived_count / total_links * 100
not_archived = 100 - archived

plt.figure(figsize=(6,6))
plt.pie(
    [archived, not_archived],
    labels=["Archived", "Not Archived"],
    colors=[MAROON, BROWN],
    autopct="%1.1f%%",
    textprops={"color": "black", "fontsize": LABEL_SIZE}
)
plt.title("Archival of Regular Citation Links", fontsize=TITLE_SIZE, fontweight="bold", color=BROWN)
plt.savefig("viz2_regular_archival_pie.png", dpi=300, facecolor=BEIGE)
plt.close()

# --- 3. Archival rate by category ---
archival_rates = (
    df_final
    .groupby("category")["found"]
    .mean()
    .sort_values(ascending=False) * 100
)
plt.figure(figsize=(10,6))
archival_rates.plot(kind="bar", color=MAROON, edgecolor=BROWN)
plt.title("Archival Rate by Category", fontsize=TITLE_SIZE, fontweight="bold", color=BROWN)
plt.ylabel("Archived (%)", fontsize=LABEL_SIZE, color=BROWN)
plt.xticks(rotation=45, ha="right", color=BROWN, fontsize=TICK_SIZE)
plt.yticks(color=BROWN, fontsize=TICK_SIZE)
plt.savefig("viz3_by_category.png", dpi=300, facecolor=BEIGE)
plt.close()

# --- 4 & 5 combined: Top 10 most common domains + archival percentage ---
domain_counts = df_final["domain"].value_counts().head(10)
domain_rates = (
    df_final[df_final["domain"].isin(domain_counts.index)]
    .groupby("domain")["found"]
    .mean() * 100
)
plt.figure(figsize=(10,6))
domain_rates.sort_values(ascending=False).plot(kind="bar", color=MAROON, edgecolor=BROWN)
plt.title("Top 10 Domains (Archival %)", fontsize=TITLE_SIZE, fontweight="bold", color=BROWN)
plt.ylabel("Archived (%)", fontsize=LABEL_SIZE, color=BROWN)
plt.xticks(rotation=45, ha="right", color=BROWN, fontsize=TICK_SIZE)
plt.yticks(color=BROWN, fontsize=TICK_SIZE)
plt.savefig("viz4_top10_domains_combined.png", dpi=300, facecolor=BEIGE)
plt.close()

# --- 6. Distribution of archived timestamps by year ---
df_final["timestamp_str"] = df_final["timestamp"].astype(str).str.split(".").str[0]
df_final["timestamp_dt"] = pd.to_datetime(df_final["timestamp_str"], format="%Y%m%d%H%M%S", errors="coerce")
df_final["year"] = df_final["timestamp_dt"].dt.year
timestamps = df_final.dropna(subset=["year"])
timestamps = timestamps[timestamps["year"] >= 1996]  # start at 1996

plt.figure(figsize=(10,6))
plt.hist(
    timestamps["year"],
    bins=range(1996, int(timestamps["year"].max())+2),
    color=MAROON,
    edgecolor=BROWN,
    alpha=0.85
)
plt.title("Distribution of Archived Timestamps by Year", fontsize=TITLE_SIZE, fontweight="bold", color=BROWN)
plt.xlabel("Year", fontsize=LABEL_SIZE, color=BROWN)
plt.ylabel("Number of Citations", fontsize=LABEL_SIZE, color=BROWN)
plt.xticks(rotation=45, color=BROWN, fontsize=TICK_SIZE)
plt.yticks(color=BROWN, fontsize=TICK_SIZE)
plt.savefig("viz6_timestamp_distribution_by_year.png", dpi=300, facecolor=BEIGE)
plt.close()

# --- 7. Archival rate by top 10 TLDs ---
df_final["tld"] = df_final["domain"].str.extract(r"\.([a-z\.]{2,})$")
top10_tlds = df_final["tld"].value_counts().head(10).index
tld_rates = (
    df_final[df_final["tld"].isin(top10_tlds)]
    .groupby("tld")["found"]
    .mean()
    .sort_values(ascending=False) * 100
)

plt.figure(figsize=(8,6))
tld_rates.plot(kind="bar", color=MAROON, edgecolor=BROWN)
plt.title("Archival Rate by Top 10 TLDs", fontsize=TITLE_SIZE, fontweight="bold", color=BROWN)
plt.ylabel("Archived (%)", fontsize=LABEL_SIZE, color=BROWN)
plt.xticks(rotation=45, color=BROWN, fontsize=TICK_SIZE)
plt.yticks(color=BROWN, fontsize=TICK_SIZE)
plt.savefig("viz7_tld_archival_rate.png", dpi=300, facecolor=BEIGE)
plt.close()

print("All 7 standardized visualizations generated and saved as PNGs!")
