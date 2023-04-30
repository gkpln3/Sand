# Sand 🏝
Sand is a Dockerfile generator.

It allows you to write cleaner, shorter and more configurable Dockerfiles.

## Developers ❤️ Sand
Sand is built by developers, for developers. It's built to be as simple as possible, while still being super useful.

## Features
✅ Simple, easy to learn syntax based on python.
✅ Configurable Dockerfiles. 
✅ Build and run your Dockerfiles with a single command.

# Example

```python
# Sandfile
From("my_app", "ubuntu", Tag="20.04")
Run("apt-get update")
Run("apt-get install ffmpeg python3")

# Install python debugger on debug images.
if config.DEBUG:
    Run("pip3 install pdb")

Copy("app", "/app")
Entrypoint("python3 /app/app.py")
```

```bash
$ sand config run --values sand.yaml
```