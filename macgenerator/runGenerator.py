import json
import random
import threading
import time

import requests

type_list = [
    "sports", "coworking", "nike", "decathlon", "food", "technology", "real madrid", "coca-cola"
]
mac_list = []
token = "AIzaSyCWA2TGSeqZR2h_TPqOQfgHb_N0S-4geL0"


class ProbeGeneratorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        generate_probe()


def generate_nearby_to(location):
    lat = location['lat']
    lng = location['lng']
    new_location = location
    new_location['lat'] = lat + random.uniform(0.0001, 0.0009)
    new_location['lng'] = lng + random.uniform(0.0001, 0.0009)
    return new_location


def generate_random_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def generate_mac_list(list_size):
    print("MACs: ")
    for i in range(0, list_size):
        mac = generate_random_mac()
        mac_list.append(mac)
        print(mac)
    print("")


def pick_random_mac():
    return random.choice(mac_list)


def generate_probe_chunk_threaded(chunk_size):
    for i in range(0, chunk_size):
        new_thread = ProbeGeneratorThread()
        new_thread.start()


def generate_probe_chunk(chunk_size):
    for i in range(0, chunk_size):
        generate_probe()


def pick_random_types():
    num_types = random.randint(1, len(type_list))
    return random.sample(type_list, num_types)


def generate_nearby_location():
    location = {"lat": 50.088080, "lng": 14.420406}
    new_location = generate_nearby_to(location)
    return new_location


def get_types_from_gmaps(location):
    types = []
    lat = str(location['lat'])
    lng = str(location['lng'])
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + \
          "location=" + lat + ',' + lng + \
          "&radius=50&type=establishment&key=" + token
    response = requests.get(url)
    establishments = json.loads(response.content)['results']
    for element in establishments:
        # non repeated
        types += list(set(element['types']) - set(types))

    return types


def generate_probe():
    random_mac = pick_random_mac()
    timestamp = int(time.time())
    location = generate_nearby_location()
    types = get_types_from_gmaps(location)
    url = "https://mctrack-6a99b.firebaseio.com/customers/" + \
          str(random_mac) + \
          "/probes/" + \
          str(timestamp) + \
          ".json" + \
          "?auth=XyGsxNV6kJdDSh4PxPKApPpwi6n051YqVao4uLfV"
    payload = {
        "location": location,
        "timestamp": timestamp,
        "types": types
    }
    status = requests.put(url, json=payload)
    print(random_mac + " " + str(status.status_code))


def main():
    get_types_from_gmaps(generate_nearby_location())

    generate_mac_list(30)
    generate_probe_chunk_threaded(100)
    generate_probe_chunk(10)


if __name__ == "__main__":
    main()
