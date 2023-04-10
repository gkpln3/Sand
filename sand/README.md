# Sand 🏝
Sand is a Dockerfile generator.

It allows you to write cleaner, shorter and more configurable dockerfiles.

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