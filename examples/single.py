from up4w.service import Up4wServer


def main():
    server = Up4wServer()
    result = server.run()
    ws_endpoint = result["availableEndpoint"]["ws"]
    print(ws_endpoint)


if __name__ == "__main__":
    main()
