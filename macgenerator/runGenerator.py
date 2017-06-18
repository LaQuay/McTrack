import random
import time

import requests

topic_list = [
    "sports", "coworking", "nike", "decathlon", "food", "technology", "real madrid", "coca-cola"
]
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


def pick_topics():
    num_topics = random.randint(1, len(topic_list))
    return random.sample(topic_list, num_topics)


def generate_probe():
    random_mac = pick_random_mac()
    timestamp = int(time.time())
    topics = pick_topics()
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
        "topics": topics
    }
    status = requests.put(url, json=payload)
    print(random_mac + " " + str(status.status_code))


def main():
    generate_mac_list(50)
    generate_probe_chunk(1000)


if __name__ == "__main__":
    main()
