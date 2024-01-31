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


def write_csv(sig, frame):
    # upon exit, write data to a csv file

    with open('out.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(scraper.data_out)
    
    sys.exit(0)

# catch when ctrl+c is pressed and save the csv file
signal.signal(signal.SIGINT, write_csv)


if __name__ == "__main__":
    main()
else:
    raise ImportError()