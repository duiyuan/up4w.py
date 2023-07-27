
import typing
import asyncio
from up4w.providers.ws import WSProvider
from up4w.service import UP4wServer


async def main():
    server = UP4wServer()
    conf = server.run()

    ws = conf["available_endpoints"]["ws"]
    socket = WSProvider(endpoint=ws, kwargs={})
    data = await socket.make_request({
        "req": "",
        "arg": {},
        "inc": None
    })

    print(data)

if __name__ == "__main__":
    asyncio.run(main())
