import asyncio
import time
from up4w.up4w import UP4W


def main():
    up4w = UP4W()

    # Get UP4W Version
    version = up4w.get_ver()
    # Output {'rsp': 'core.ver', 'ret': 'version 1.1, build Jul 5 2023 16:25:55'}
    print(version)

    # Continuously receive message pushed by UP4W
    def get_message_pushed(t):
        print("get_message_pushed", t)

    up4w.message.receive_message(get_message_pushed)


if __name__ == "__main__":
    main()
    time.sleep(15)
