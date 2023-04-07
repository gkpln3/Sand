# Sand 🏝
Sand is a Dockerfile generator.

It allows you to write cleaner, shorter and more configurable dockerfiles.

# Example

```python
# Sandfile
image("my_app", from_image="ubuntu", tag="20.04")
run("apt-get update")
run("apt-get install ffmpeg python3")

# Install python debugger on debug images.
if config.DEBUG:
    run("pip3 install pdb")

copy("app", "/app")
entrypoint("python3 /app/app.py")

run_config.ports += "8080"
run_config.volumes += "db_files:/db_files"
```

```bash
$ sand build
Building image "my_app"...
Image "my_app" built!
```

```bash
$ sand run
Running container "my_app"
```

```bash
$ sand config build
# Builds the dockerfile and outputs it to stdout
```

```bash
$ sand config run
# Builds a `docker run` command and outputs it to stdout
```

```bash
$ sand config run --set DEBUG=True
```

```bash
$ sand config run --values sand.yaml
```