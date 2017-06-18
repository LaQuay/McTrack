import random
import time

import requests

mac_list = []


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


def generate_probe_chunk(chunk_size):
    for i in range(0, chunk_size):
        generate_probe()


def generate_probe():
    random_mac = pick_random_mac()
    timestamp = int(time.time())
    url = "https://mctrack-6a99b.firebaseio.com/customers/" + \
          str(random_mac) + \
          "/probes/" + \
          str(timestamp) + \
          ".json" + \
          "?auth=XyGsxNV6kJdDSh4PxPKApPpwi6n051YqVao4uLfV"
    payload = {
        "location": {
            "features": [
                {
                    "geometry": {
                        "coordinates": [
                            14.442162830382586,
                            50.07002479852162
                        ],
                        "type": "Point"
                    },
                    "type": "Feature"
                }
            ],
            "type": "FeatureCollection"
        },
        "timestamp": timestamp,
        "topics": [
            {"name": "sports"},
            {"name": "coworking"},
            {"name": "technology"}
        ]
    }
    status = requests.put(url, json=payload)
    print(random_mac + " " + str(status.status_code))


def main():
    generate_mac_list(10)
    generate_probe_chunk(100)


if __name__ == "__main__":
    main()
