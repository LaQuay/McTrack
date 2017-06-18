import json
import random
import threading
import time

import requests

type_list = [
    "sports", "coworking", "nike", "decathlon", "food", "technology", "real madrid", "coca-cola"
]
mac_list = []


class ProbeGeneratorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        generate_probe()


class NearbyCoordinatesGenerator:

    def generate_nearby_to(self, location):
        #TODO: IMPLEMENT HERE LAQUAY
        lat = location['lat']
        lng = location['lng']
        radius = 200
        rangeX = (0, 2500)
        rangeY = (0, 2500)
        qty = 10  # or however many points you want

        # Generate a set of all points within 200 of the origin, to be used as offsets later
        # There's probably a more efficient way to do this.
        deltas = set()
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                if x * x + y * y <= radius * radius:
                    deltas.add((x, y))

        randPoints = []
        excluded = set()
        i = 0
        while i < qty:
            x = random.randrange(*rangeX)
            y = random.randrange(*rangeY)
            if (x, y) in excluded: continue
            randPoints.append((x, y))
            i += 1
            excluded.update((x + dx, y + dy) for (dx, dy) in deltas)

        print(randPoints)
        return randPoints


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
    return {"lat": 50.088080, "lng": 14.420406}


def get_types_from_gmaps(location):
    types = []
    lat = str(location['lat'])
    lng = str(location['lng'])
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + \
          "location=" + lat + ',' + lng + \
          "&radius=50&type=establishment&key=AIzaSyC0N7To1nSSIqAVHIvbs0FpLa3gIFfhP0k"
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
    gen = NearbyCoordinatesGenerator()
    gen.generate_nearby_to(generate_nearby_location())

    # generate_mac_list(50)
    # generate_probe_chunk_threaded(300)
    # generate_probe_chunk(1000)


if __name__ == "__main__":
    main()
