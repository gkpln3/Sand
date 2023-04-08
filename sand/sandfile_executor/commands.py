from abc import abstractmethod

class Command:
    @abstractmethod
    def serialize(self):
        pass

class FromCommand(Command):
    def __init__(self, image, tag):
        self.image = image
        self.tag = tag

    def serialize(self):
        return f"FROM {self.image}:{self.tag}"

class RunCommand(Command):
    def __init__(self, command):
        self.command = command

    def serialize(self):
        return f"RUN {self.command}"

class CopyCommand(Command):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def serialize(self):
        return f"COPY {self.src} {self.dst}"

class EntrypointCommand(Command):
    def __init__(self, command):
        self.command = command

    def serialize(self):
        return f"ENTRYPOINT {self.command}"

class ExposeCommand(Command):
    def __init__(self, ports):
        self.ports = ports

    def serialize(self):
        return f"EXPOSE {self.ports}"

class VolumeCommand(Command):
    def __init__(self, volumes):
        self.volumes = volumes

    def serialize(self):
        return f"VOLUME {self.volumes}"

