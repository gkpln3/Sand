import argparse
import re
from typing import List

from sand.sand import AttributeDict

from .docker_image import DockerImage
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


def _add_config_command(subparsers):
    parser = subparsers.add_parser("config", help="config the image")
    parser.add_argument("dir", type=str, nargs='?', help="Directory to config from", default=".")
    parser.add_argument("-D", "--set", dest="config", type=str, action="append", help="Set config variable, these variables will be accessible by using the `config` variable in the Sandfile")
    return parser

def _add_ignore_command(subparsers):
    parser = subparsers.add_parser("ignore", help="Add all generated Dockerfiles to .gitignore")
    parser.add_argument("dir", type=str, nargs='?', help="Root directory of Sandfile", default=".")
    return parser

def _add_clean_command(subparsers):
    parser = subparsers.add_parser("clean", help="Remove all generated Dockerfiles")
    parser.add_argument("dir", type=str, nargs='?', help="Root directory of Sandfile", default=".")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Print Dockerfiles to be removed without removing them")
    return parser

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_config_command(subparsers)
    _add_ignore_command(subparsers)
    _add_clean_command(subparsers)
    args = parser.parse_args()

    # Create Sandfile executor
    root_sandfile_path = os.path.abspath(args.dir) + "/" + "Sandfile"

    config = _parse_config(args)
    env = {
        'config': AttributeDict(config)
    }
    executor = SandfileExecutor(root_sandfile_path, env)

    if args.command == "config":
        images = executor.execute()
        for image in images:
            image.save()
        print("Image built successfully!")
    if args.command == "build":
        images = executor.execute()
    if args.command == "ignore":
        images = executor.execute()
        _add_dockerfiles_to_gitignore(images)
    if args.command == "clean":
        images = executor.execute()
        _remove_dockerfiles(args, images)
        print("Cleaned successfully!")

def _remove_dockerfiles(args, images):
    for image in images:
        path_to_remove = image.path
        if not args.dry_run:
            if os.path.exists(path_to_remove):
                print(f"Removing {path_to_remove}")
                os.remove(path_to_remove)
            else:
                print(f"{path_to_remove} does not exist")
        else:
            print(f"Would remove {path_to_remove}")
        
    # elif args.command == "run":
    #     print(f'Running container "{image_name}"')


def _add_dockerfiles_to_gitignore(images: List[DockerImage]):
    for image in images:
        dockerfile_dir = os.path.dirname(image.path)
        gitignore_path = os.path.join(dockerfile_dir, ".gitignore")
        # Add the dockerfile to the gitignore if it's not already there
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                gitignore_contents = f.read()
            if not re.search(r"^Dockerfile$", gitignore_contents, re.MULTILINE):
                print(f"Appending Dockerfile to {gitignore_path}")
                with open(gitignore_path, "a") as f:
                    if not gitignore_contents.endswith("\n"):
                        f.write("\n")
                    f.write("Dockerfile\n")
        else:
            print(f"Creating {gitignore_path}")
            with open(gitignore_path, "w") as f:
                f.write("Dockerfile\n")

def _parse_config(args) -> dict:
    if args.config is None:
        return {}
    
    config = {}
    for arg in args.config:
        if "=" not in arg:
            config[arg] = True
        else:
            key, value = arg.split("=")
            config[key] = value
    return config

if __name__ == "__main__":
    main()