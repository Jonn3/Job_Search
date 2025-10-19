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

if __name__ == "__main__":
    main()