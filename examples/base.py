import time
import typing
import asyncio
from up4w.request_manager import RequestManager
from up4w.up4w import UP4W


async def main():
    # up4w = UP4W(endpoint_3rd="ws://localhost:8765")
    up4w = UP4W()

    # Get UP4W Version
    version = up4w.get_ver()
    print(version)

    # receive message pushed by UP4W
    def get_message_pushed(t):
        print("get_message_pushed", t)

    up4w.message.receive_message(get_message_pushed)

if __name__ == "__main__":
    print(1)
    asyncio.run(main())
    print(2)
    time.sleep(15)
