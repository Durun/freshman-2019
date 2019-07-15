import slack
from typing import Callable
from .panel import Panel
from .camera import Camera

ReplyType = Callable[[str], None]


class Bot(object):
    camera: Camera
    panel: Panel
    rtm: slack.RTMClient
    api: slack.WebClient

    command_list: dict

    def __init__(self, camera: Camera, panel: Panel, slack_token: str):
        self.camera = camera
        self.panel = panel
        self.rtm = slack.RTMClient(token=slack_token)
        self.api = slack.WebClient(token=slack_token)

        self.command_list = {
            'state': self.state,
            'on': lambda *args, reply: self.switch(on=True, reply=reply),
            'off': lambda *args, reply: self.switch(on=False, reply=reply),
            'mode': self.mode,
            'auto': self.auto,
            'manual': self.manual,
            'temp': self.temp,
            'help': self.usage,
            'usage': self.usage,
        }

        self.rtm.on(event='message', callback=lambda **payload: self.__on_message_received(**payload))
        self.rtm.start()

    def __on_message_received(self, **payload):
        data = payload['data']

        # 返信用関数
        def reply(message: str):
            self.api.chat_postMessage(
                channel=data['channel'],
                text=message,
            )

        if 'subtype' not in data:  # 純粋なメッセージイベントだけ処理
            text: str = data['text']
            splited = text.split()

            command = self.command_list.get(splited[0])
            if command is not None:
                # コマンドを実行
                command(*splited[1:], reply=reply)
            else:
                # 不明なコマンド
                self.usage(*splited[1:], reply=reply)

    def state(self, *args, reply: ReplyType) -> None:
        """
        エアコン状態確認コマンド
        """

        # 現在の電源状態確認
        is_power_on = self.camera.is_power_on()
        if is_power_on:
            # 現在の設定温度確認
            temp = self.camera.get_temperature()
            reply("現在エアコンはオンで、設定温度は{}度です。".format(temp))
        else:
            reply("現在エアコンはオフです。")

    def switch(self, on: bool, reply: ReplyType) -> None:
        """
        エアコン電源操作コマンド
        """

        # 現在の電源状態確認
        current_power = self.camera.is_power_on()
        if current_power != on:
            # 電源ボタンを押す
            self.panel.push_power_button()

            # 成功しているかどうか確認
            current_power = self.camera.is_power_on()
            if current_power == on:
                # 成功
                if on:
                    temp = self.camera.get_temperature()
                    reply("エアコンの電源をつけました。設定温度は{}度です。".format(temp))
                else:
                    reply("エアコンの電源を切りました。")
            else:
                # 失敗
                # TODO リトライ
                reply("エアコンボタンの操作に失敗しました。")
        else:
            # 既に指定の電源状態になってる
            if on:
                reply("既にエアコンの電源はついています。")
            else:
                reply("既にエアコンの電源は切れています。")

    def mode(self, *args, reply: ReplyType) -> None:
        """
        モード確認コマンド
        """
        raise NotImplementedError()

    def auto(self, *args, reply: ReplyType) -> None:
        """
        オートモードコマンド
        """
        raise NotImplementedError()

    def manual(self, *args, reply: ReplyType) -> None:
        """
        マニュアルモードコマンド
        """
        raise NotImplementedError()

    def temp(self, *args, reply: ReplyType) -> None:
        """
        温度設定コマンド
        """
        raise NotImplementedError()

    def usage(self, *args, reply: ReplyType) -> None:
        """
        使い方コマンド
        """
        raise NotImplementedError()
