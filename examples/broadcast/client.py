import time
from up4w.up4w import UP4W


def process_message(message):
    print("client receive message:", message)


def main():
    # Create UP4W Instance, with connection to endpoint_3rd_party
    # instead of connection to build-in UP4W.dll
    up4w = UP4W(endpoint_3rd_party="ws://localhost:9801")
    # up4w = UP4W()

    resp = up4w.manager.make_request("method_0")
    print("0st:", resp)

    # Invoke process_message when every message coming
    up4w.manager.receive_message(process_message)

    resp = up4w.manager.make_request("method_1")
    print("1st:", resp)

    resp = up4w.manager.make_request("method_2")
    print("2nd:", resp)


if __name__ == "__main__":
    main()
    time.sleep(1000)
