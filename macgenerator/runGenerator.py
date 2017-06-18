import random


def rand_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def main():
    print("hello world")
    for i in range(0, 20):
        print(rand_mac())


if __name__ == "__main__":
    main()
