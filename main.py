import argparse
from sand import Sand
from docker_image import DockerImage


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["build", "run", "config"])
    args = parser.parse_args()

    # Create Sandfile executor
    sand = Sand()

    # Execute the relevant action
    if args.command == "config":
        image: DockerImage
        image = sand.execute_sandfile("Sandfile")
        print(f'Building image "{image.name}"...')
        image.save("Dockerfile")
        print(f'Image "{image.name}" built!')
    elif args.command == "build":
        image = sand.execute_sandfile("Sandfile")
        print("Building image...")
        image.build()
        print("Image built!")
    # elif args.command == "run":
    #     print(f'Running container "{image_name}"')