import signal
import sys
import csv
import scraper
from time import sleep

def main():

    # do initial run
    scraper.grab_nick_data()
    scraper.grab_bakke_data()

    # every 15 minutes, check for new data
    while(True):
        sleep(20*60)
        scraper.grab_nick_data()
        scraper.grab_bakke_data()

if __name__ == "__main__":
    main()
else:
    raise ImportError()