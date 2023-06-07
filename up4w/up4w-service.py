from ctypes import CDLL
import os
import time
from multiprocessing import Process, Pipe
from json import dumps, loads
from os.path import join, exists, dirname, abspath
from sys import platform


fd1, fd2 = Pipe()


def start_up4w(fd, apppath, dll_path):
    loader = CDLL(dll_path)
    start = loader.start(f"-data={apppath}")
    port = loader.get_api_port()
    fd.send(dumps({"port": port, "ret": start, "pid": os.getpid()}))
    # The dynamic link library will run a websocket service
    # Keep the process alive, prevent the gc from collecting it
    # time.sleep(3600 * 24 * 365 * 10)


class Up4wService:
    def __init__(self, *, debug=False, appdata=os.getenv("APPDATA")):
        self.debug = bool(debug)
        self.addons_path = abspath(join(os.curdir, "addons"))
        self.appdata = appdata

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

    @staticmethod
    def recv(fd):
        data = fd.recv()
        return data

    def start(self):
        appdata = self.appdata
        if not exists(self.file_path):
            raise Exception("File does not exist :" + self.file_path)
        print(self.file_path)

        child = Process(target=start_up4w, args=(fd1, appdata, self.file_path))
        # parent = Process(target=self.recv, args=(fd2,))
        child.start()
        # parent.start()
        child.join()
        # parent.join()
        return self.recv(fd2)


if __name__ == "__main__":
    server = Up4wService()
    ep = server.start()
    print(ep)






