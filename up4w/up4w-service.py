import ctypes
import os
from os.path import join
from sys import platform


class Up4wService:
    def __init__(self, *, debug=False, appdata=os.getenv("APPDATA")):
        self.debug = bool(debug)
        self.addons_path = join(os.curdir, "addons")
        self.appdata = appdata

        # windows -> dll
        if platform == "win32":
            self.file_path = join(self.addons_path, "up4w_core_shared.dll")
        # macOS -> dylib
        elif platform == "darwin":
            self.file_path = join(self.addons_path, "up4w_core_shared.dylib")
        # linux -> linux
        elif platform == "linux":
            self.file_path = join(self.addons_path, "up4w_core_shared.so")
        else:
            raise Exception("Unsupported platform")

    def start(self):
        appdata = self.appdata
        loader = ctypes.cdll.LibraryLoader(self.file_path)
        start = loader.start(f"-data={appdata}")
        print(start)


if __name__ == "__main__":
    server = Up4wService()
    server.start()






