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
Write your Dockerfile in a Python-like syntax.
```python
# Sandfile
from sand import *

From("ubuntu", Tag="20.04")
Run("apt-get update")
Run("apt-get install ffmpeg python3")

# Install python debugger on debug images.
if config.DEBUG:
    Run("pip3 install pdb")

Copy("app", "/app")
Entrypoint("python3 /app/app.py")
```
⬇️
```dockerfile
# Auto-generated by Sand, do not edit!
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install ffmpeg python3
COPY app /app
ENTRYPOINT python3 /app/app.py
```

### Share Code
Sandfiles are just Python files, and are being evaluated in an hierarchical manner by using the `Sand` directive, so you can easily share code between them.
```python
# ./Sandfile
from sand import *

def MyService(name):
    From("ubuntu", "20.04")
    Run(f"apt-get install python3")
    Copy(Src="app", Dst="/app")
    Entrypoint(f"python3 /app/{name}.py")

Sand("tweet_service")
Sand("home_timeline")
```
```python
# ./tweet_service/Sandfile
from sand import *

MyService("tweet_service") # Defined in ../Sandfile
```

```python
# ./home_timeline/Sandfile
from sand import *

MyService("home_timeline") # Defined in ../Sandfile
```


## Running
Running Sand is as simple as running `sand` in your terminal.
This will generate Dockerfiles for all Sandfiles in the current directory.
```bash
$ sand config
Saving Dockerfile to backend/service1/Dockerfile
Saving Dockerfile to backend/service2/Dockerfile
Built successfully!
```
You can also watch for changes and automatically rebuild your Dockerfiles.
```bash
$ sand config -w
Watching for changes...
```

### Configuring
You can pass configuration values to Sand using the `-D` or `--set` flag.
```bash
$ sand config -DDEBUG=True
```
Or use a YAML file. (not implemented yet)
```yaml
# sand.yaml
DEBUG: True
```
```bash
$ sand config --values sand.yaml
```

