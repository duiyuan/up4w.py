
from typing import Dict, Optional
from up4w.service import UP4wServer, AvailableEndpoint
from up4w.request_manager import RequestManager
from up4w.core import Up4wCore, MRCConfig, DVSConfig
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
        self.available_endpoints: AvailableEndpoint = {
            "http": "",
            "ws": ""
        }

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
        available_endpoints = resp["available_endpoints"]
        ws_endpoint = available_endpoints["ws"]
        self.endpoint: str = ws_endpoint
        self.available_endpoints = available_endpoints
        return self.endpoint

    def get_joined_swarm(self) -> Dict[str, SwarmNodes]:
        resp = self.core.status()
        return resp["ret"]["swarms"]

    def wait_for_initialize(self, *, app_name: str = None, mrc: MRCConfig = None, dvs: DVSConfig = None,
                            hob: Dict = None, lsm: Dict = None, mlt: Dict = None, gdp: Dict = None, pbc: Dict = None):
        status = self.core.status()
        params = {
            "app_name": app_name,
            "mrc": mrc,
            "dvs": dvs,
            "hob": hob,
            "lsm": lsm,
            "mlt": mlt,
            "gdp": gdp,
            "pbc": pbc,
        }
        if not status["ret"]["initialized"]:
            self.core.initialize(params)
        return True

    def stop_server(self):
        self.server.stop()

    def get_ver(self):
        return self.core.version()

    def shutdown(self):
        return self.core.shutdown()
