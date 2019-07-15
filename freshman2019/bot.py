import slack
from typing import Callable
from .panel import Panel
from .camera import Camera
from .mode import Mode

ReplyType = Callable[[str], None]

MAX_TEMP = 30
MIN_TEMP = 18


class Bot(object):
    camera: Camera
    panel: Panel
    rtm: slack.RTMClient
    api: slack.WebClient

    command_list: dict

    mode: Mode

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

        self.mode = Mode.MANUAL

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
                reply("無効な命令です: {}".format(splited[0]))
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

        # 現在の電源状態確認
        is_power_on = self.camera.is_power_on()
        if is_power_on:
            if self.mode == Mode.AUTO:
                reply("現在、エアコンはオートモードで稼働しています。")
            else:
                reply("現在、エアコンはマニュアルモードで稼働しています。")
        else:
            reply("現在エアコンは稼働していません。")

    def auto(self, *args, reply: ReplyType) -> None:
        """
        オートモードコマンド
        """

        # 現在の電源状態確認
        is_power_on = self.camera.is_power_on()
        if is_power_on:
            if self.mode == Mode.AUTO:
                reply("現在、エアコンはオートモードで稼働しています。")
            else:
                # モード変更
                self.mode = Mode.AUTO
                reply("オートモードに変更しました。")
        else:
            reply("現在エアコンは稼働していません。")

    def manual(self, *args, reply: ReplyType) -> None:
        """
        マニュアルモードコマンド
        """

        # 現在の電源状態確認
        is_power_on = self.camera.is_power_on()
        if is_power_on:
            if self.mode == Mode.AUTO:
                # モード変更
                self.mode = Mode.MANUAL
                reply("マニュアルモードに変更しました。")
            else:
                reply("現在、エアコンはマニュアルモードで稼働しています。")
        else:
            reply("現在エアコンは稼働していません。")

    def temp(self, *args, reply: ReplyType) -> None:
        """
        温度設定コマンド
        """

        if len(args) != 1:
            reply("コマンドの引数の数が不正です。")
            return

        # 現在の設定温度確認
        current_temp = self.camera.get_temperature()
        delta = 0

        try:
            # 差分を計算
            t: str = args[0]
            if t.startswith("+"):
                delta = min(int(t.lstrip("+")) + current_temp, MAX_TEMP) - current_temp
            elif t.startswith("-"):
                delta = max(current_temp - int(t.lstrip("-")), MIN_TEMP) - current_temp
            else:
                delta = max(min(int(t), MAX_TEMP), MIN_TEMP) - current_temp
        except ValueError:
            reply("コマンドの引数が不正です。")
            return

        target_temp = current_temp + delta

        # 温度ボタンを押す
        self.panel.change_temperature(delta)

        # 温度設定確認
        current_temp = self.camera.get_temperature()
        if current_temp == target_temp:
            # 成功
            reply("設定温度を{}度にしました。".format(target_temp))
        else:
            # 失敗
            # TODO リトライ
            reply("温度設定に失敗しました。")

    def usage(self, *args, reply: ReplyType) -> None:
        """
        使い方コマンド
        """
        raise NotImplementedError()
