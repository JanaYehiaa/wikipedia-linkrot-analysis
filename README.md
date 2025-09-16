# wikipedia-linkrot-analysis

## Overview
This project collects and analyzes citation links from Wikipedia using the **MediaWiki API** and checks whether those links are archived in the **Internet Archive (Wayback Machine API)**.  
The pipeline generates cleaned datasets and visualizations to better understand the preservation of web resources cited on Wikipedia.

## Features
- Uses the **Wikipedia API** to fetch article titles and extract citation links across multiple categories.  
- Cleans and standardizes citation data (removes duplicates, fixes formatting, flags archive links).  
- Queries the **Wayback Machine Availability API** to check whether citations are already archived.  
- Produces multiple CSV outputs at different stages:
  - `wikipedia_citations.csv` → raw dataset  
  - `wikipedia_citations_clean.csv` → cleaned citations  
  - `wikipedia_citations_with_archive_status.csv` → archive check results  
  - `wikipedia_citations_final.csv` → final processed dataset  
- Includes **data visualization scripts** for analysis.  
- Order of scripts:
  1. `getting citations.py`  
  2. `data cleaning.py`  
  3. `analysis.py`  
  4. `output data cleaning.py`  
  5. `data vis.py`  

## Resources
- [Wayback Machine API Documentation](https://archive.org/help/wayback_api.php)  
- [MediaWiki API: Categorymembers](https://www.mediawiki.org/wiki/API:Categorymembers)  
- [Wikipedia Categories](https://en.wikipedia.org/wiki/Wikipedia:Contents/Categories)  
- [MediaWiki API: Parse](https://en.wikipedia.org/w/api.php?action=help&modules=parse)  
- [StackOverflow: Get all pages in category](https://stackoverflow.com/questions/5771745/how-to-get-all-article-pages-under-a-wikipedia-category-and-its-sub-categories)  
- [YouTube Tutorial 1](https://youtu.be/hpc5jyVpUpw?si=QEKoaAXZdk9Qqd0J)  
- [YouTube Tutorial 2](https://youtu.be/fklHBWow8vE?si=FooDcRQNSdM5BE0c)  

## AI Transparency
AI assistance was used to:
- Debug runtime errors in the scripts.  
- Improve styling of Seaborn-generated visualizations.  
- Ensure consistent code formatting and clarity.  
