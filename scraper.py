def collect():
    import requests
    import re
    import json
    from bs4 import BeautifulSoup
    from time import gmtime, strftime
    
    url = "https://recwell.wisc.edu/liveusage/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html5lib')

    trackers = soup.find_all("div", {"class": "live-tracker"})
    # print(trackers)

    data_dict = {"location" : [], "time" : [], "count" : [], "maximum" : []}
    for tracker in trackers:
        location = tracker.find_all("div", {"class": "tracker-location"})
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        count = tracker.find_all("span", {"class": "tracker-current-count pending"})
        maximum = tracker.find_all("span", {"class": "tracker-max-count"})
        if len(data_dict["location"]) == 0:
            # if we're doing the first run, just collect it
            data_dict["location"].append(location)
            data_dict["time"].append(time)
            data_dict["count"].append(count)
            data_dict["maximum"].append(maximum)
        else:
            # compare the last run as to not collect redundant data
            # TODO: finish
            pass