
from up4w.providers.ws import WSProvider
from up4w.service import UP4wServer

if __name__ == "__main__":
    server = UP4wServer()
    conf = server.run()
    print(conf)
