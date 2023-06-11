from up4w.service import UP4wServer
import time


def main():
    server = UP4wServer()
    result = server.run()
    print("r:", result)
    time.sleep(5)
    # server.stop()


if __name__ == "__main__":
    main()
