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

    except Exception as e:
        print("❌ Error:", e)

    print("\nDone. (You can re-run and choose different options.)")


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()