def main():
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

    data_dict = {}
    for tracker in trackers:
        location = tracker.find_all("div", {"class": "tracker-location"})
        if location not in data_dict.keys():
            data_dict[location] = []
        # strftime("%Y-%m-%d %H:%M:%S", gmtime())
        

if __name__ == "__main__":
    main()
else:
    raise ImportError()