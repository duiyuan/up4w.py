import time
from up4w.up4w import UP4W
from os.path import dirname,join

robot_address = "9S27676+Zx0Skrpr8hAEgPBS+9XgY0rt9jz2rHEZFeg="
robot_greeting_secret = "PJn3MTFwwXHZCSuYVFHO6OvOQoJSywpSATR1EZvj0Ho="
default_swarm = "5109e3b42b2f1d4724582cc69c219862448e30b1"
user_seed = "VRT0CH62TN9TP1NMAFGFSVXQ05GCXDRXANPVKG8JTBXY8DXGQDTV763EE0"


def process_message(message):
    print("client receive message:", message)


def main():
    up4w = UP4W()

    # Get UP4W Version by a simple request
    version = up4w.get_ver()
    print(f"current up4w version: {version['ret']}")

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
        "dvs": {},
        "hob": {}
    })
    print("wait_for_initialize", init_result)

    # Continuously receive message pushed by UP4W
    up4w.message.receive_message(process_message)

    # signin
    result = up4w.social.signin_with_seed(user_seed)
    print("signin_with_seed", result)

    result = up4w.social.add_user(robot_address, name="GPT4W(ROBOT)", greeting_secret=robot_greeting_secret)
    print("signin_with_seed", result)

    resp = up4w.message.send_text({
        "recipient": robot_address,
        "content": "1+2=?",
        "app": 1,
        "action": 4096,
    })
    print("message.send_text:", resp)


if __name__ == "__main__":
    main()
    time.sleep(1000)
