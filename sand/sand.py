from .internal.sandfile_executor import sandfile_executor as e
from .internal.sandfile_executor.commands import *
from .internal.sandfile_executor.sandfile_executor import SandfileExecutor
import os.path
    
def _assert_running_through_sand():
    if e._current_executor is None:
        raise Exception("Do not run this manually, use the `sand config` command to run Sandfile.")
    
def _SandAPI(f):
    def wrapper(*args, **kwargs):
        _assert_running_through_sand()
        return f(*args, **kwargs)
    return wrapper

@_SandAPI
def Sand(relative_path: str):
    # Determine absolute path to Sandfile
    abs_path = os.path.join(os.path.dirname(e._current_executor.path), relative_path, "Sandfile")

    # Execute Sandfile
    subsand = SandfileExecutor(abs_path, e._current_executor.env.copy())
    new_image = subsand.execute()

    # Add resulting images to current executor
    e._current_executor._images.extend(new_image)

@_SandAPI
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

@_SandAPI
def Copy(Src, Dst, From = None):
    e._current_executor._commands.append(CopyCommand(Src, Dst, From=From))

@_SandAPI
def Entrypoint(Command):
    e._current_executor._commands.append(EntrypointCommand(Command))

@_SandAPI
def From(Image, Tag=None, As=None):
    e._current_executor._commands.append(FromCommand(Image, Tag=Tag, As=As))


class AttributeDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        return None

    def __setattr__(self, attr, value):
        self[attr] = value

# _commands = {
#     "Run": Run,
#     "Copy": Copy,
#     "Entrypoint": Entrypoint,
#     "Sand": Sand,
#     "From": From,
#     # "config": type("Config", (object,), {"DEBUG": False}),
#     # "run_config": type("RunConfig", (object,), {"ports": "", "volumes": ""}),
# }

config: AttributeDict