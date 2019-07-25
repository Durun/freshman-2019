#!/usr/bin/env python
import os
from .camera import Camera
from .panel import Panel
from .bot import Bot


def main():
    # TODO カメラモジュール初期化
    camera = Camera()

    # TODO パネルモジュール初期化
    panel = Panel()

    bot = Bot(
        camera=camera,
        panel=panel,
        slack_token=os.environ['SLACK_BOT_TOKEN'],
        post_channel=os.environ['SLACK_BOT_POST_CHANNEL']
    )

    bot.start()


if __name__ == '__main__':
    main()
