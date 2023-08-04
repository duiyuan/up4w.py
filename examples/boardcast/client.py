import time
from up4w.up4w import UP4W


def process_message(message):
    print("client receive message:", message)


def main():
    up4w = UP4W(endpoint_3rd="ws://localhost:9801")
    # up4w = UP4W()

    resp = up4w.manager.make_request({
        "req": "method_0"
    })
    print("0st:", resp)

    # 每次广播消息到达，都会回调 receive 方法
    up4w.manager.receive_message(process_message)

    resp = up4w.manager.make_request({
        "req": "method_1"
    })
    print("1st:", resp)

    resp = up4w.manager.make_request({
        "req": "method_2"
    })
    print("2nd:", resp)


if __name__ == "__main__":
    main()
    time.sleep(1000)
