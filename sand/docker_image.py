import docker
from io import BytesIO

class DockerImage:
    def __init__(self, name: str, dockerfile: str):
        self.name = name
        self.dockerfile = dockerfile

    def save(self, file_path: str):
        with open(file_path, "w") as f:
            f.write(self.dockerfile)

    def build(self):
        # Connect to Docker daemon
        client = docker.from_env()

        # Build Docker image
        with BytesIO(self.dockerfile.encode()) as f:
            client.images.build(
                fileobj=f,
                custom_context=True,
                tag=self.name
            )
        

    def __str__(self):
        return self.dockerfile
