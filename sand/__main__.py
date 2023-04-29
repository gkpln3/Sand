from .internal.sandfile_executor import sandfile_executor as e
from .internal.sandfile_executor.commands import *
from .internal.sandfile_executor.sandfile_executor import SandfileExecutor
import os.path
    
if e._current_executor is None:
    raise Exception("Do not run this manually, use the `sand config` command to run Sandfile.")

def Sand(relative_path: str):
    # Determine absolute path to Sandfile
    abs_path = os.path.join(os.path.dirname(e._current_executor.path), relative_path, "Sandfile")

    # Execute Sandfile
    subsand = SandfileExecutor(abs_path, e._current_executor.env.copy())
    new_image = subsand.execute()

    # Add resulting images to current executor
    e._current_executor._images.extend(new_image)

def Run(command: str | list[str]):
    # If command is a list, add each command to the list of commands
    if isinstance(command, list):
        for cmd in command:
            e._current_executor._commands.append(RunCommand(cmd))
    # If command is a string, add it to the list of commands
    elif isinstance(command, str):
        e._current_executor._commands.append(RunCommand(command))
    else:
        raise Exception("Invalid type in run command")

def Copy(*args, **kwargs):
    e._current_executor._commands.append(CopyCommand(*args, **kwargs))

def Entrypoint(*args, **kwargs):
    e._current_executor._commands.append(EntrypointCommand(*args, **kwargs))

def From(*args, **kwargs):
    e._current_executor._commands.append(FromCommand(*args, **kwargs))

# _commands = {
#     "Run": Run,
#     "Copy": Copy,
#     "Entrypoint": Entrypoint,
#     "Sand": Sand,
#     "From": From,
#     # "config": type("Config", (object,), {"DEBUG": False}),
#     # "run_config": type("RunConfig", (object,), {"ports": "", "volumes": ""}),
# }