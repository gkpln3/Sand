from abc import abstractmethod

class Command:
    @abstractmethod
    def serialize(self):
        pass

class FromCommand(Command):
    def __init__(self, Image, Tag=None, As=None):
        self.image = Image
        self.tag = Tag
        self._as = As

    def serialize(self):
        ret = f"FROM {self.image}"
        if self.tag is not None:
            ret += f":{self.tag}"
        if self._as is not None:
            ret += f" AS {self._as}"
        return ret

class RunCommand(Command):
    def __init__(self, Command):
        self.command = Command

    def serialize(self):
        return f"RUN {self.command}"

class CopyCommand(Command):
    def __init__(self, Src, Dst, From = None):
        self.src = Src
        self.dst = Dst
        self._from = From

    def serialize(self):
        cmd = "COPY "
        if self._from:
            cmd += f"--from={self._from} "
        return f"{cmd}{self.src} {self.dst}"

class EntrypointCommand(Command):
    def __init__(self, Command):
        self.command = Command

    def serialize(self):
        return f"ENTRYPOINT {self.command}"

class ExposeCommand(Command):
    def __init__(self, Ports):
        self.ports = Ports

    def serialize(self):
        return f"EXPOSE {self.ports}"

class VolumeCommand(Command):
    def __init__(self, Volumes):
        self.volumes = Volumes

    def serialize(self):
        return f"VOLUME {self.volumes}"

