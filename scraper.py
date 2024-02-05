from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import json
from time import gmtime, strftime, sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

# init globals
data_out = [["Location", "Count", "Max", "Timestamp"]]
url = "https://recwell.wisc.edu/liveusage/"
options = Options()
options.add_argument("--headless")
if os.name == "nt":
    path_to_chromedriver = "chromedriver.exe"
elif os.name == "posix":
    path_to_chromedriver = os.path.join(os.getcwd(), "chromedriver_linux")
    os.environ['PATH'] += path_to_chromedriver
service = Service(executable_path=path_to_chromedriver)

nick_locations = ["Nick Level 1 Fitness", "Nick Level 2 Fitness", "Nick Level 3 Fitness", "Nick Power House", "Nick Track", "Soderholm Family Aquatic Center", "Nick Courts 1 & 2", "Nick Courts 3-6", "Nick Courts 7 & 8"]
bakke_locations = ["Level 1 Fitness", "Level 2 Fitness", "Level 3 Fitness", "Level 4 Fitness", "Bakke Track", "Courts 1&2", "Courts 3&4", "Courts 5-8", "Orbit", "Willow Room", "Cove Pool", "Mount Mendota", "Skybox Suites", "SubZero Ice Center"]

last_run_nick = ""
last_run_bakke = ""

delimiter = "|"

def update_nick_if_new_data():
    # load driver
    driver = webdriver.Chrome(options=options, service=service)

    # collect the nick data, put it into an array of strings temporarily, split by |
    nick_data_temp = []

    # load data and timestamp it
    driver.get(url)
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # add a bit of delay to let the counts load
    sleep(2)

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
    
    # sort the data to standardize it
    nick_data_temp.sort()

    # initialize
    this_run = get_last_run_nick()

    # set value
    for string in nick_data_temp:
        this_run += string
    
    # if the data has changed since the last run
    if this_run != get_last_run_nick():
        #collect it
        add_data_to_data_lists(nick_data_temp)

        #set the string for next time so we don't have duplicate data
        set_last_run_nick(this_run)

    # quit the driver
    driver.quit()

def update_bakke_if_new_data():
    driver = webdriver.Chrome(options=options, service=service)

    # collect the bakke data, put it into an array of strings temporarily, split by |
    bakke_data_temp = []

    # load data and timestamp it
    driver.get(url)
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # add a bit of delay to let the counts load
    sleep(2)

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
    
    # sort the data to standardize it
    bakke_data_temp.sort()

    # initialize
    this_run = get_last_run_bakke()

    # set value
    for string in bakke_data_temp:
        this_run += string
    
    # if the data has changed since the last run
    if this_run != get_last_run_bakke():
        #collect it
        add_data_to_data_lists(bakke_data_temp)

        #set the string for next time so we don't have duplicate data
        set_last_run_bakke(this_run)

    # quit the driver
    driver.quit()

def add_data_to_data_lists(data):
    # loop through each string
    for raw_value in data:

        # split based on delimiter
        elements = raw_value.split(delimiter)

        # add to data
        data_out.append([elements[0], elements[1], elements[2], elements[3]])

### getters and setters

def set_last_run_nick(nick):
    global last_run_nick
    last_run_nick = nick

def get_last_run_nick():
    global last_run_nick
    return last_run_nick

def set_last_run_bakke(bakke):
    global last_run_bakke
    last_run_bakke = bakke

def get_last_run_bakke():
    global last_run_bakke
    return last_run_bakke