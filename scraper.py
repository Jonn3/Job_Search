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



if __name__ == "__main__":
    main()