from typing import Dict, Optional
from up4w.service import UP4wServer
from up4w.request_manager import RequestManager
from up4w.core import Up4wCore, Up4wCoreInitReq
from up4w.message import Message
from up4w.social import Social
from up4w.swarm import Swarm
from up4w.persistent import Persistent
from up4w.types import SwarmNodes


class UP4W:
    def __init__(self, *, debug: bool = False, appdata: Optional[str] = None, endpoint_3rd: str = None, **kwargs):
        self.server: UP4wServer = UP4wServer(debug=debug, appdata=appdata)
        self.kwargs = kwargs or {}
        self.endpoint = ""
        self.endpoint_3rd = endpoint_3rd
        self.manager = None

        # If the 'endpoint_3rd' parameter is specified, the internal 'UP4W Service' process will not run anymore.
        if endpoint_3rd is not None:
            self.endpoint = endpoint_3rd
        else:
            self.__start_server()

        self.manager = RequestManager(endpoint=self.endpoint, kwargs=self.kwargs)
        self.core = Up4wCore(self.manager)
        self.message = Message(self.manager)
        self.social = Social(self.manager)
        self.swarm = Swarm(self.manager)
        self.persistent = Persistent(self.manager)

    def __start_server(self) -> str:
        resp = self.server.run()
        ws_endpoint = resp["available_endpoints"]["ws"]
        self.endpoint: str = ws_endpoint
        return self.endpoint

    def get_joined_swarm(self) -> Dict[str, SwarmNodes]:
        resp = self.core.status()
        return resp["ret"]["swarms"]

    def wait_for_initialize(self, params: Up4wCoreInitReq):
        status = self.core.status()
        if not status["ret"]["initialized"]:
            self.core.initialize(params)
        return True

    def stop_server(self):
        self.server.stop()

    def get_ver(self):
        return self.core.version()

    def shutdown(self):
        return self.core.shutdown()
