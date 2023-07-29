import time
import typing
import asyncio
from up4w.request_manager import RequestManager
from up4w.up4w import UP4W


async def main():
    up4w = UP4W(endpoint_3rd="ws://localhost:8765")
    version = up4w.get_ver()

    print(version)

    def get_result(t):
        print("get_result", t)

    up4w.receive_message(get_result)

if __name__ == "__main__":
    asyncio.run(main())
    time.sleep(15)
