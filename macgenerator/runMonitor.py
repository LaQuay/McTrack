from flask import Flask
import json
import time

import requests

app = Flask(__name__)
mac_list = []
data = []


def get_data():
    url = "https://mctrack-6a99b.firebaseio.com/customers.json" + \
          "?auth=XyGsxNV6kJdDSh4PxPKApPpwi6n051YqVao4uLfV"
    response = requests.get(url)
    return json.loads(response.content)


def cluster_probes():
    print("hellow")


@app.route('/next_advert/')
def next_advert():
    youtube_url = "https://www.youtube.com/watch?v=wOMKUihPNm4"  # desigual
    return youtube_url


def get_mac_types(mac):
    types = []
    url = "https://mctrack-6a99b.firebaseio.com/customers/" + \
          str(mac) + \
          "/probes.json" + \
          "?auth=XyGsxNV6kJdDSh4PxPKApPpwi6n051YqVao4uLfV"
    response = requests.get(url)
    probes = json.loads(response.content)
    for probe in probes:
        types += probes[probe]['types']

    return types


@app.route('/discover_relevant_types/')
def discover_relevant_types():
    types = ["establishment", "store", "shoe_store", "point_of_interest", "clothing_store", "clothing_store",
             "clothing_store", "clothing_store", "jewelry_store", "travel_agency", "lodging", "place_of_worship",
             "church", "real_estate_agency"]
    types = []
    near_macs = [
        "cd:e9:49:9b:df:2d",
        "e5:0b:10:00:20:c5",
        "85:49:5f:37:9d:ea",
        "f9:ec:85:76:8f:aa",
        "71:0c:07:37:07:ed",
        "cd:e9:49:9b:df:2d",
        "db:34:90:75:28:d4",
        "7b:d7:46:31:60:16",
        "89:4e:23:00:6f:82",
        "c3:f5:84:54:e9:04",
        "58:28:9e:72:52:95"
    ]
    for mac in near_macs:
        types += get_mac_types(mac)

    relevant_types = count_types(types)
    return relevant_types


def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist, wordfreq))


def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


def count_types(types):
    dictionary = wordListToFreqDict(types)
    sorted_dictionary = sortFreqDict(dictionary)

    for s in sorted_dictionary: print(str(s))
    return sorted_dictionary


def main():

    discover_relevant_types()
    # data = get_data()
    # cluster_probes()
    # while True:
    #    time.sleep(1)


if __name__ == "__main__":
    main()
