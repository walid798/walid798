from scholarly import scholarly
from pathlib import Path

SCHOLAR_ID = "2iwarAMAAAAJ"
MAX_PUBS = 8

readme_path = Path("README.md")
text = readme_path.read_text(encoding="utf-8")

start_marker = "<!-- GOOGLE-SCHOLAR:START -->"
end_marker = "<!-- GOOGLE-SCHOLAR:END -->"

author = scholarly.search_author_id(SCHOLAR_ID)
author = scholarly.fill(author, sections=["publications"])

publications = author.get("publications", [])
publications = sorted(
    publications,
    key=lambda p: p.get("bib", {}).get("pub_year", "0"),
    reverse=True
)[:MAX_PUBS]

lines = []
for pub in publications:
    filled = scholarly.fill(pub)
    bib = filled.get("bib", {})
    title = bib.get("title", "Untitled")
    year = bib.get("pub_year", "N/A")
    venue = (
        bib.get("journal")
        or bib.get("conference")
        or bib.get("publisher")
        or "Venue unavailable"
    )
    authors = bib.get("author", "Authors unavailable")
    citedby = filled.get("num_citations", 0)

    lines.append(
        f"- **{title}**  \n"
        f"  {authors}  \n"
        f"  *{venue}, {year}* · Citations: {citedby}"
    )

replacement = (
    f"{start_marker}\n"
    + ("\n\n".join(lines) if lines else "_No publications found._")
    + f"\n{end_marker}"
)

import re
new_text = re.sub(
    rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
    replacement,
    text,
    flags=re.DOTALL,
)

readme_path.write_text(new_text, encoding="utf-8")
print("README updated successfully.")
