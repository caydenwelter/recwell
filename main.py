import signal
import sys
import csv
import scraper
from time import sleep

def main():

    # do initial run
    scraper.update_nick_if_new_data()
    scraper.update_bakke_if_new_data()

    # every 15 minutes, check for new data
    while(True):
        sleep(15*60)
        scraper.update_nick_if_new_data()
        scraper.update_bakke_if_new_data()

if __name__ == "__main__":
    main()
else:
    raise ImportError()