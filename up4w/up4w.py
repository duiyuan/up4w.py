from typing import Dict, Optional, Callable
from up4w.service import UP4wServer
from up4w.request_manager import RequestManager
from up4w.core import Up4wCore

import asyncio


class UP4W:
    def __init__(self, *, debug: bool = False, appdata: Optional[str] = None, endpoint_3rd: str = None, **kwargs):
        self.server: UP4wServer = UP4wServer(debug=debug, appdata=appdata)
        self.kwargs = kwargs or {}
        self.endpoint = ""
        self.endpoint_3rd = endpoint_3rd
        self.manager = None

        if endpoint_3rd is not None:
            self.endpoint = endpoint_3rd
        else:
            self.__start_server()

        self.manager = RequestManager(endpoint=self.endpoint, kwargs=self.kwargs)
        self.core = Up4wCore(self.manager)

    def __start_server(self) -> str:
        resp = self.server.run()
        ws_endpoint = resp["available_endpoints"]["ws"]
        self.endpoint: str = ws_endpoint
        return self.endpoint

    def stop_server(self):
        self.server.stop()

    def get_ver(self):
        return self.core.version()

    def receive_message(self, callback: Callable):
        self.manager.receive_message(callback=callback)
        # try:
        #     loop = asyncio.get_running_loop()
        # except RuntimeError:
        #     loop = None
        # if loop and loop.is_running():
        #     task = loop.create_task(self.manager.receive_message())
        #     task.add_done_callback(callback)
        # else:
        #     asyncio.run(self.manager.receive_message(callback=callback))
