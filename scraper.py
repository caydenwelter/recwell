from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import json
from time import gmtime, strftime, sleep

data_dict = {"location" : [], "time" : [], "count" : [], "maximum" : []}
url = "https://recwell.wisc.edu/liveusage/"

nick_locations = ["Nick Level 1 Fitness", "Nick Level 2 Fitness", "Nick Level 3 Fitness", "Nick Power House", "Nick Track", "Soderholm Family Aquatic Center", "Nick Courts 1 & 2", "Nick Courts 3-6", "Nick Courts 7 & 8"]
bakke_locations = ["Level 1 Fitness", "Level 2 Fitness", "Level 3 Fitness", "Level 4 Fitness", "Bakke Track", "Courts 1&2", "Courts 3&4", "Courts 5-8", "Orbit", "Willow Room", "Cove Pool", "Mount Mendota", "Skybox Suites", "SubZero Ice Center"]

last_run_nick = ""
last_run_bakke = ""

def update_nick_if_new_data():
    # load driver
    driver = webdriver.Firefox()

    # collect the nick data, put it into an array of strings temporarily, split by |
    nick_data = []

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
            nick_data.append((location + "|" + count + "|" + maximum + "|" + tracker_time))
    
    # sort the data to standardize it
    nick_data.sort()

    # initialize
    this_run = ""

    # set value
    for string in nick_data:
        this_run += string
    
    # if the data has changed since the last run
    if this_run != get_last_run_nick():
        #collect it
        add_data_to_data_dict(nick_data)

        #set the string for next time so we don't have duplicate data
        set_last_run_nick(this_run)

    # quit the driver
    driver.quit()

def update_bakke_if_new_data(last_run=""):
    bakke_data = []
    pass

def add_data_to_data_dict(data):

    pass

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

def collect():
    url = "https://recwell.wisc.edu/liveusage/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html5lib')

    trackers = soup.find_all("div", {"class": "live-tracker"})
    # print(trackers)

    data_dict = {"location" : [], "time" : [], "count" : [], "maximum" : []}
    for tracker in trackers:
        location = tracker.find("p", {"class": "tracker-location"}).get_text()
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        count = tracker.find("span", {"class": "tracker-current-count pending"}).get_text()
        maximum = tracker.find("span", {"class": "tracker-max-count"}).get_text()
        # if len(data_dict["location"]) == 0:
        #     # if we're doing the first run, just collect it
        #     data_dict["location"].append(location)
        #     data_dict["time"].append(time)
        #     data_dict["count"].append(count)
        #     data_dict["maximum"].append(maximum)
        # else:
        #     # compare the last run as to not collect redundant data
        #     # TODO: finish
        #     pass
        print(location, count, maximum)