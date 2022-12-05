# Define Sandfile environment
class Config:
    DEBUG = False

class RunConfig:
    ports = ""
    volumes = ""

image_result = None
run_results = []
copy_result = None
entrypoint_result = None

def image(name, from_image, tag):
    global image_result
    image_result = (name, from_image, tag)

def run(command):
    run_results.append(command)

def copy(src, dst):
    global copy_result
    copy_result = (src, dst)

def entrypoint(command):
    global entrypoint_result
    entrypoint_result = command

config = Config()
run_config = RunConfig()

# Run Sandfile in environment
with open("Sandfile", "r") as f:
    exec(f.read(), globals())

# Extract values from environment
image_name, image_from, image_tag = image_result
install_commands = run_results
copy_src, copy_dst = copy_result
entrypoint = entrypoint_result
run_config_ports = run_config.ports
run_config_volumes = run_config.volumes

# Generate Dockerfile
dockerfile_template = """
FROM {image_from}:{image_tag}

# Install dependencies
RUN {install_commands}

# Copy app source code
COPY {copy_src} {copy_dst}

# Set the entrypoint
ENTRYPOINT {entrypoint}

# Expose ports and mount volumes
EXPOSE {run_config_ports}
VOLUME {run_config_volumes}
"""

dockerfile = dockerfile_template.format(
    image_name=image_name,
    image_from=image_from,
    image_tag=image_tag,
    install_commands=" \\\n    && ".join(install_commands),
    copy_src=copy_src,
    copy_dst=copy_dst,
    entrypoint=entrypoint,
    run_config_ports=run_config_ports,
    run_config_volumes=run_config_volumes
)

# Save Dockerfile to disk
with open("Dockerfile", "w") as f:
    f.write(dockerfile)