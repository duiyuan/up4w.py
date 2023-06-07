from ctypes import CDLL
import os
import time
from multiprocessing import Process, Pipe
from json import dumps, loads
from os.path import join, exists, dirname, abspath
from sys import platform


def start_up4w(child_conn, apppath, dll_path):
    loader = CDLL(dll_path)
    start = loader.start(f"-data={apppath}")
    port = loader.get_api_port()
    child_conn.send(dumps({"port": port, "ret": start, "pid": os.getpid()}))

    while True:
        signal = child_conn.poll()
        if signal:
            data = child_conn.recv()
            if data:
                child_conn.close()
                break


class Up4wService:
    def __init__(self, *, debug=False, appdata=os.getenv("APPDATA")):
        self.debug = bool(debug)
        self.addons_path = abspath(join(os.curdir, "addons"))
        self.appdata = appdata
        self.child = None

        self.parent_conn, self.child_conn = Pipe()

        # windows -> dll
        if platform == "win32":
            self.file_path = join(self.addons_path, platform, "up4w_core_shared.dll")
        # macOS -> dylib
        elif platform == "darwin":
            self.file_path = join(self.addons_path, platform, "up4w_core_shared.dylib")
        # linux -> linux
        elif platform == "linux":
            self.file_path = join(self.addons_path, platform, "up4w_core_shared.so")
        else:
            raise Exception("Unsupported platform")

    def start(self):
        appdata = self.appdata
        if not exists(self.file_path):
            raise Exception("File does not exist :" + self.file_path)

        self.child = Process(target=start_up4w, args=(self.child_conn, appdata, self.file_path))
        self.child.start()

        data = self.parent_conn.recv()
        return data

    def stop(self):
        self.parent_conn.send(True)
        self.child.join()
        self.child = None


if __name__ == "__main__":
    server = Up4wService()

    ep = server.start()
    print("ep.", ep)

    # time.sleep(3)
    # server.stop()







