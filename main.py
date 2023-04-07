import argparse
from sand import Sand
from docker_image import DockerImage
import os


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    subprasers = parser.add_subparsers(dest="command")
    build_parser = subprasers.add_parser("build", help="Build the image")
    build_parser.add_argument("dir", type=str, nargs='?', help="Directory to build from", default=".")
    args = parser.parse_args()

    # Create Sandfile executor
    sand = Sand()

    if args.command == "build":
        image = sand.execute_sandfile(os.path.abspath(args.dir) + "/" + "Sandfile")
        print("Building image...")
        if image:
            image.save("Dockerfile")
        print("Image built successfully!")
    # elif args.command == "run":
    #     print(f'Running container "{image_name}"')