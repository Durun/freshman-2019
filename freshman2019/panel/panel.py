class Panel(object):

    def push_power_button(self) -> None:
        raise NotImplementedError()

    def change_temperature(self, dtemp: int) -> None:
        raise NotImplementedError()
