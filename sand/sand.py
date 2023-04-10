
from io import BytesIO
import docker
from .sandfile_executor.sandfile_executor import SandfileExecutor

class Sand:
    def __init__(self):
        # Connect to Docker daemon
        self.client = docker.from_env()

    def build_container(self, dockerfile_path, image_name):
        # Read Dockerfile from disk
        with open(dockerfile_path, "r") as f:
            dockerfile = f.read()

        # Build Docker image
        return self.client.images.build(
            fileobj=BytesIO(dockerfile.encode()),
            custom_context=True,
            tag=image_name
        )

    def run_container(self, image_name):
        # Run Docker container
        self.client.containers.run(image_name)

    def execute_sandfile(self, sandfile_path):
        # Create Sandfile executor
        executor = SandfileExecutor()

        # Execute Sandfile and generate Dockerfile
        image_name = executor.execute(sandfile_path)

        # Return image name
        return image_name
