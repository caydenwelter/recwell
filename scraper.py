from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import json
from time import gmtime, strftime, sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import csv
from pytz import timezone
from datetime import datetime

# init globals
data_out = [["Location", "Count", "Max", "Timestamp"]]
sleep_time = 10
url = "https://recwell.wisc.edu/liveusage/"

options = Options()
options.add_argument("--headless")

if os.name == "nt":
    path_to_chromedriver = "chromedriver.exe"
elif os.name == "posix":
    path_to_chromedriver = os.path.join(os.getcwd(), "chromedriver_linux")
    os.environ['PATH'] += path_to_chromedriver
    os.system("sudo chmod a+x chromedriver_linux")

service = Service(executable_path=path_to_chromedriver)

nick_locations = ["Nick Level 1 Fitness", "Nick Level 2 Fitness", "Nick Level 3 Fitness", "Nick Power House", "Nick Track", "Soderholm Family Aquatic Center", "Nick Courts 1 & 2", "Nick Courts 3-6", "Nick Courts 7 & 8"]
bakke_locations = ["Level 1 Fitness", "Level 2 Fitness", "Level 3 Fitness", "Level 4 Fitness", "Bakke Track", "Courts 1&2", "Courts 3&4", "Courts 5-8", "Orbit", "Willow Room", "Cove Pool", "Mount Mendota", "Skybox Suites", "SubZero Ice Center"]

delimiter = "|"

def grab_nick_data():
    # load driver
    driver = webdriver.Chrome(options=options, service=service)

    # collect the nick data, put it into an array of strings temporarily, split by |
    nick_data_temp = []

    # load data and timestamp it
    driver.get(url)
    time = datetime.now(timezone('America/Chicago')).strftime("%Y-%m-%d %H:%M:%S")

    # add a bit of delay to let the counts load
    sleep(sleep_time)

    # grab all the trackers
    trackers = driver.find_elements(By.CLASS_NAME, "live-tracker")

    # parse data and load into nick_data
    for tracker in trackers:
        location = tracker.find_element(By.CLASS_NAME, "tracker-location").text
        count = tracker.find_element(By.CLASS_NAME, "tracker-current-count.pending").text
        maximum = tracker.find_element(By.CLASS_NAME, "tracker-max-count").text
        tracker_time = time
        if location not in nick_locations:
            continue
        else:
            nick_data_temp.append((location + delimiter + count + delimiter + maximum + delimiter + tracker_time))
    
    # process data
    add_data_to_data_lists(nick_data_temp)

    # quit the driver
    driver.quit()

def grab_bakke_data():
    driver = webdriver.Chrome(options=options, service=service)

    # collect the bakke data, put it into an array of strings temporarily, split by |
    bakke_data_temp = []

    # load data and timestamp it
    driver.get(url)
    time = datetime.now(timezone('America/Chicago')).strftime("%Y-%m-%d %H:%M:%S")

    # add a bit of delay to let the counts load
    sleep(sleep_time)

    # grab all the trackers
    trackers = driver.find_elements(By.CLASS_NAME, "live-tracker")

    # parse data and load into nick_data
    for tracker in trackers:
        location = tracker.find_element(By.CLASS_NAME, "tracker-location").text
        count = tracker.find_element(By.CLASS_NAME, "tracker-current-count.pending").text
        maximum = tracker.find_element(By.CLASS_NAME, "tracker-max-count").text
        tracker_time = time
        if location not in bakke_locations:
            continue
        else:
            bakke_data_temp.append((location + delimiter + count + delimiter + maximum + delimiter + tracker_time))
    
    # process data
    add_data_to_data_lists(bakke_data_temp)

    # quit the driver
    driver.quit()

def add_data_to_data_lists(data):

    # loop through each string
    for raw_value in data:

        # split based on delimiter
        elements = raw_value.split(delimiter)

        # add to data
        data_out.append([elements[0], elements[1], elements[2], elements[3]])

    with open('out.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data_out)
    
    # push the data file to remote
    try:
        print("Attempting file push")
        os.system("git add out.csv")
        print("Staged out.csv")
        os.system("git commit -m 'update out.csv'")
        print("Commited changes")
        os.system("git push")
        time = datetime.now(timezone('America/Chicago')).strftime("%Y-%m-%d %H:%M:%S")
        print("Pushed file to remote at " + time)
    except:
        time = datetime.now(timezone('America/Chicago')).strftime("%Y-%m-%d %H:%M:%S")
        print("Update failed at " + time + ". Exiting.")
        exit(0)