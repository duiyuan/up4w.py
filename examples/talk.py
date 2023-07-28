
import typing
import asyncio
from up4w.request_manager import RequestManager
from up4w.up4w import UP4W


async def main():
    up4w = UP4W()
    version = up4w.get_ver()

    print(version)

if __name__ == "__main__":
    asyncio.run(main())
