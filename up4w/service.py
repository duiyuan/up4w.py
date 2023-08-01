from ctypes import CDLL
import os
import shutil
from up4w.types import Up4wServiceRes
from multiprocessing import Process, Pipe, Event
from os.path import join, exists, abspath, dirname, expanduser
from sys import platform


def start_child_process(child_conn, apppath, dll_path):
    loader = CDLL(dll_path)
    start = loader.start(f"-data={apppath}")
    port = loader.get_api_port()

    child_conn.send({"port": port, "ret": start, "pid": os.getpid()})

    # do nothing when main process exist automatically, no message will receive
    # in this case, unexpected EOFError will occur
    try:
        signal = child_conn.recv()
        if signal:
            child_conn.close()
    except EOFError:
        pass


class UP4wServer:
    def __init__(self, *, debug=False, appdata=None):
        current_dir = dirname(__file__)

        self.debug = bool(debug)
        self.addons_path = abspath(join(current_dir, "addons"))
        self.nodes_path = abspath(join(current_dir, "nodes"))
        self.appdata = appdata
        self.child = None

        # windows -> dll
        if platform == "win32":
            self.file_path = join(self.addons_path, platform, "up4w.dll")
            self.default_appdata = os.getenv("APPDATA")
        # macOS -> dylib
        elif platform == "darwin":
            self.file_path = join(self.addons_path, platform, "up4w.dylib")
            self.default_appdata = expanduser('~/Library/Application Support')
        # linux -> linux
        elif platform == "linux":
            self.file_path = join(self.addons_path, platform, "up4w.so")
            self.default_appdata = expanduser('~/Library/Application Support')
        else:
            raise Exception("Unsupported platform")

        if appdata is None:
            self.appdata = self.default_appdata

        self.parent_conn, self.child_conn = Pipe()
        self.result_event = Event()

    def preset_nodes(self):
        nodes_path = self.nodes_path
        with os.scandir(nodes_path) as files:
            for file in files:
                file_type = file.name.split(".")[1]
                if file_type == "nodes":
                    shutil.copy2(file, self.appdata)

    def run(self) -> Up4wServiceRes:
        appdata = self.appdata
        if not exists(self.file_path):
            raise Exception("File does not exist :" + self.file_path)

        self.preset_nodes()
        self.child = Process(target=start_child_process, name="up4w_child_process",  args=(self.child_conn, appdata, self.file_path))
        self.child.start()

        data = self.parent_conn.recv()
        result = {
            "available_endpoints": {
                "http": f"http://127.0.0.1:{data['port']}/cmd",
                "ws": f"ws://127.0.0.1:{data['port']}/api",
            }
        }
        return result

    def stop(self):
        self.parent_conn.send(True)
        self.child.join()
        self.child = None


if __name__ == "__main__":
    server = UP4wServer()
    ep = server.run()
    print("ep:", ep)








