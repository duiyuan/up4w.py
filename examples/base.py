import asyncio
import time
from up4w.up4w import UP4W
from os import path
from os.path import dirname,join

robot_address = "9S27676+Zx0Skrpr8hAEgPBS+9XgY0rt9jz2rHEZFeg="
robot_greeting_secret = "PJn3MTFwwXHZCSuYVFHO6OvOQoJSywpSATR1EZvj0Ho="
default_swarm = "5109e3b42b2f1d4724582cc69c219862448e30b1"
userid = "VRT0CH62TN9TP1NMAFGFSVXQ05GCXDRXANPVKG8JTBXY8DXGQDTV763EE0"


def get_message_pushed(t):
    print("get_message_pushed", t)


def main():
    up4w = UP4W()

    # Get UP4W Version
    version = up4w.get_ver()
    # Output {'rsp': 'core.ver', 'ret': 'version 1.1, build Jul 5 2023 16:25:55'}
    print(version)

    # Continuously receive message pushed by UP4W
    up4w.message.receive_message(get_message_pushed)
    up4w.wait_for_initialize(**{
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
    up4w.social.signin_with_seed(userid)
    up4w.social.add_user(robot_address, name="GPT4W(ROBOT)", greeting_secret=robot_greeting_secret)
    resp = up4w.message.send_text({
        "recipient": robot_address,
        "content": "1+2=?",
        "app": 1,
        "action": 4096,
    })
    print("after send text:", resp)


if __name__ == "__main__":
    main()
    time.sleep(45)
