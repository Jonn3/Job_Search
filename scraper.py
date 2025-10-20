import argparse, csv, sys
from datetime import datetime

def main():
   
    print(r"""
  _____       _                _             
 |  __ \     | |              | |            
 | |__) |___ | |__   ___  _ __| | _____ _ __ 
 |  _  // _ \| '_ \ / _ \| '__| |/ / _ \ '__|
 | | \ \ (_) | |_) | (_) | |  |   <  __/ |   
 |_|  \_\___/|_.__/ \___/|_|  |_|\_\___|_|   
    """)
    print("==============================================")
    print("         Welcome to the Job Search App        ")
    print("==============================================\n")

    print("This app is designed to help automate parts of your job search.\n")
    print("Here’s what it does:")
    print(" - Scrapes university mission statements (like XULA and Dillard).")
    print(" - Gathers fake job postings for testing data scraping skills.")
    print(" - Saves job listings neatly into a CSV file for easy viewing.")
    print("\nYou'll later add web scraping and data storage features as you complete more TODOs.\n")

    print("Let's get started! 🚀")


    def require_libs():
        try:
            import requests
            from bs4 import BeautifulSoup
            return requests, BeautifulSoup
        except Exception:
            print("⚠️  Missing deps. Run: pip install -r requirements.txt")
            raise

    def scrape_xula_mission():
        """TODO 6: Scrape XULA mission from the div.editorarea, look for 'founded by Saint'."""
        requests, BeautifulSoup = require_libs()
        url = "https://www.xula.edu/about/mission-values.html"
        print(f"\n[Scraping XULA mission] {url}")
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

    def scrape_harvard_mission():
        """Scrape Harvard University's mission statement from its About page."""
        requests, BeautifulSoup = require_libs()
        url = "https://www.harvard.edu/about/mission-vision-values/"
        print(f"\n[Scraping Harvard Mission] {url}")
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        block = soup.find("div", class_="rte") or soup.find("div", class_="field-item")
        text = block.get_text(" ", strip=True) if block else soup.get_text(" ", strip=True)

        print("\n--- Harvard Mission (first 800 chars) ---")
        print(text[:800] + ("..." if len(text) > 800 else ""))

    def scrape_fake_jobs_to_csv():
        """TODO 9: Scrape fake jobs and store into fake_jobs.csv with required headers."""
        import csv, os
        requests, BeautifulSoup = require_libs()
        url = "https://realpython.github.io/fake-jobs/"
        print(f"\n[Scraping fake jobs] {url}")
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        rows = []
        for card in soup.select("div.card-content"):
            title = card.select_one("h2.title")
            company = card.select_one("h3.subtitle")
            location = card.select_one("p.location")
            date = card.select_one("time")
            rows.append({
                "Job Title": title.get_text(strip=True) if title else "",
                "Company": company.get_text(strip=True) if company else "",
                "Location": location.get_text(strip=True) if location else "",
                "Date Posted": date.get_text(strip=True) if date else "",
            })

        out = "fake_jobs.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Job Title","Company","Location","Date Posted"])
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ Saved {len(rows)} rows to {os.path.abspath(out)}")

    def _parse_date(s):
        from datetime import datetime
        s = (s or "").strip()
        for fmt in ("%Y-%m-%d", "%b %d, %Y", "%B %d, %Y"):
            try:
                return datetime.strptime(s, fmt)
            except Exception:
                pass
        return None

    def clean_jobs_csv(source="fake_jobs.csv", dest="fake_jobs_clean.csv", drop_older_than_days=None):
        """De-duplicate, optionally drop older-than-N-days, and sort newest→oldest."""
        import csv
        from datetime import datetime, timedelta

        try:
            with open(source, newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
        except FileNotFoundError:
            print(f"⚠️  '{source}' not found. Run the fake jobs scrape first.")
            return

        seen = set()
        deduped = []
        for r in rows:
            key = (
                (r.get("Job Title") or "").strip().lower(),
                (r.get("Company") or "").strip().lower(),
                (r.get("Location") or "").strip().lower(),
                (r.get("Date Posted") or "").strip().lower(),
            )
            if key not in seen:
                seen.add(key)
                deduped.append(r)

        if drop_older_than_days is not None:
            cutoff = datetime.now() - timedelta(days=drop_older_than_days)
            tmp = []
            for r in deduped:
                d = _parse_date(r.get("Date Posted"))
                if d is None or d >= cutoff:
                    tmp.append(r)
            deduped = tmp

        deduped.sort(key=lambda r: _parse_date(r.get("Date Posted")) or _parse_date("1900-01-01"), reverse=True)

        with open(dest, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Job Title","Company","Location","Date Posted"])
            writer.writeheader()
            writer.writerows(deduped)

        print(f"✅ Cleaned {len(deduped)} rows → {dest}")


    try:
        do_xula = input("\nRun TODO 6 (XULA mission scrape)? [y/N]: ").strip().lower() == "y"
        if do_xula:
            scrape_xula_mission()

        do_harvard = input("\nRun Harvard University scrape? [y/N]: ").strip().lower() == "y"
        if do_harvard:
            scrape_harvard_mission()


        do_jobs = input("\nRun TODO 9 (Fake jobs → CSV)? [y/N]: ").strip().lower() == "y"
        if do_jobs:
            scrape_fake_jobs_to_csv()

        do_clean = input("\nBONUS: Clean CSV (de-dup, drop old, sort)? [y/N]: ").strip().lower() == "y"
        if do_clean:
            try:
                days = input("Drop listings older than how many days? (blank = keep all): ").strip()
                days_int = int(days) if days else None
            except ValueError:
                days_int = None
            clean_jobs_csv(drop_older_than_days=days_int)


    except Exception as e:
        print("❌ Error:", e)

    print("\nDone. (You can re-run and choose different options.)")

    

if __name__ == "__main__":
    main()