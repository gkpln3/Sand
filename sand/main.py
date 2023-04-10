import argparse
from .sand import Sand
import os

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    subprasers = parser.add_subparsers(dest="command", required=True)
    config_parser = subprasers.add_parser("config", help="config the image")
    config_parser.add_argument("dir", type=str, nargs='?', help="Directory to config from", default=".")
    args = parser.parse_args()

    # Create Sandfile executor
    sand = Sand()

    if args.command == "config":
        images = sand.execute_sandfile(os.path.abspath(args.dir) + "/" + "Sandfile")
        for image in images:
            image.save()
        print("Image built successfully!")
    if args.command == "build":
        image = sand.execute_sandfile(os.path.abspath(args.dir) + "/" + "Sandfile")
    # elif args.command == "run":
    #     print(f'Running container "{image_name}"')

if __name__ == "__main__":
    main()