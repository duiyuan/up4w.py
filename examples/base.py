import time
from up4w.up4w import UP4W
from os.path import dirname,join

robot_address = "9S27676+Zx0Skrpr8hAEgPBS+9XgY0rt9jz2rHEZFeg="
robot_greeting_secret = "PJn3MTFwwXHZCSuYVFHO6OvOQoJSywpSATR1EZvj0Ho="
default_swarm = "5109e3b42b2f1d4724582cc69c219862448e30b1"
user_seed = "JE+PEDZ4/2OOxdrCU3e6/SyWVjEKbucRzAdcAA=="


def process_message(message):
    print(f"◀◀ client receive message passively: {message}")


def main():
    # using local websocket webserver in examples/broadcast/server.py
    # up4w = UP4W(endpoint_3rd_party="ws://127.0.0.1:9801")

    # Using build-in UP4W dll if leave `endpoint_3rd_party` along
    up4w = UP4W()

    print(f"▶▶ current available endpoint: {up4w.available_endpoints}")

    # Get UP4W Version by a simple request
    version = up4w.get_ver()
    print(f"▶▶ current up4w version: {version['ret']}")

    # initialize up4w
    init_result = up4w.wait_for_initialize(**{
        "app_name": 'deso',
        "mrc": {
            "msgs_dir": join(dirname(__file__), ".data"),
            "default_swarm": default_swarm,
            "flags": ['delay00_load'],
        },
        "mlt": {},
        "gdp": {},
        "pbc": {},
        "lsm": {},
    })
    print("▶▶ wait_for_initialize: ", init_result)
    if init_result.get("err"):
        return

    # Continuously receive message pushed by UP4W
    up4w.message.receive_message(process_message)

    # signin
    result = up4w.social.signin_with_seed(user_seed)
    print("▶▶ signin_with_seed", result)
    if result.get("err"):
        return

    # add user
    result = up4w.social.add_user(robot_address, name="GPT4W(ROBOT)", greeting_secret=robot_greeting_secret)
    print("▶▶ add_user", result)
    if result.get("err"):
        return

    resp = up4w.message.send_text({
        "recipient": robot_address,
        "content": "51+5=?",
        "app": 1,
        "action": 4096,
    })
    print("▶▶ message.send_text:", resp)


if __name__ == "__main__":
    main()
    time.sleep(1000)
