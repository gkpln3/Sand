import argparse

from .sandfile_executor.sandfile_executor import SandfileExecutor
import os
import docker

# Connect to Docker daemon
try:
    _docker_client = docker.from_env()
except Exception as e:
    _docker_client = None

# def build_container(dockerfile_path, image_name):
#     # Read Dockerfile from disk
#     with open(dockerfile_path, "r") as f:
#         dockerfile = f.read()

#     # Build Docker image
#     return _docker_client.images.build(
#         fileobj=BytesIO(dockerfile.encode()),
#         custom_context=True,
#         tag=image_name
#     )

# def run_container(image_name):
#     # Run Docker container
#     _docker_client.containers.run(image_name)

def execute_sandfile(sandfile_path):
    # Create Sandfile executor
    executor = SandfileExecutor(sandfile_path)

    # Execute Sandfile and generate Dockerfile
    image_name = executor.execute()

    # Return image name
    return image_name


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    subprasers = parser.add_subparsers(dest="command", required=True)
    config_parser = subprasers.add_parser("config", help="config the image")
    config_parser.add_argument("dir", type=str, nargs='?', help="Directory to config from", default=".")
    args = parser.parse_args()

    if args.command == "config":
        images = execute_sandfile(os.path.abspath(args.dir) + "/" + "Sandfile")
        for image in images:
            image.save()
        print("Image built successfully!")
    if args.command == "build":
        image = execute_sandfile(os.path.abspath(args.dir) + "/" + "Sandfile")
    # elif args.command == "run":
    #     print(f'Running container "{image_name}"')

if __name__ == "__main__":
    main()