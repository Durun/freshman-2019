import slack
from .panel import Panel
from .camera import Camera


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

    def state(self, *args, reply) -> None:
        """
        エアコン状態確認コマンド
        """
        raise NotImplementedError()

    def switch(self, on: bool, reply) -> None:
        """
        エアコン電源操作コマンド
        """
        raise NotImplementedError()

    def mode(self, *args, reply) -> None:
        """
        モード確認コマンド
        """
        raise NotImplementedError()

    def auto(self, *args, reply) -> None:
        """
        オートモードコマンド
        """
        raise NotImplementedError()

    def manual(self, *args, reply) -> None:
        """
        マニュアルモードコマンド
        """
        raise NotImplementedError()

    def temp(self, *args, reply) -> None:
        """
        温度設定コマンド
        """
        raise NotImplementedError()

    def usage(self, *args, reply) -> None:
        """
        使い方コマンド
        """
        raise NotImplementedError()
