class Camera(object):
    def __init__(self, camera_num: int):
        pass

    def get_temperature(self) -> int:
        raise NotImplementedError

    def is_power_on(self) -> bool:
        raise NotImplementedError
