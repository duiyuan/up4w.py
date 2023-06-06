from ctypes import CDLL
import os
import time
from os.path import join, exists, dirname, abspath
from sys import platform


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

    def start(self):
        appdata = self.appdata
        if not exists(self.file_path):
            raise Exception("File does not exist :" + self.file_path)
        print(self.file_path)
        loader = CDLL(self.file_path)
        start = loader.start(f"-data={appdata}")
        port = loader.get_api_port()
        print(start)
        print(port)


if __name__ == "__main__":
    server = Up4wService()
    server.start()
    time.sleep(1000)






