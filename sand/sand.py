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
def Run(Command: str | list[str], Mount: str | list[str] = None):
    if isinstance(Mount, str):
        Mount = [Mount]

    # If command is a list, add each command to the list of commands
    if isinstance(Command, list):
        for cmd in Command:
            e._current_executor._commands.append(RunCommand(cmd, Mounts=Mount))
    # If command is a string, add it to the list of commands
    elif isinstance(Command, str):
        e._current_executor._commands.append(RunCommand(Command, Mounts=Mount))
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
    if ":" in Image:
        if Tag is not None:
            raise Exception("Cannot specify tag twice")
        Image, Tag = Image.split(":")
    e._current_executor._commands.append(FromCommand(Image, Tag=Tag, As=As))

@_SandAPI
def Env(Name, Value=None):
    if "=" in Name:
        if Value is not None:
            raise Exception("Cannot specify value twice")
        Name, Value = Name.split("=")
    elif Value is None:
        raise Exception("Must specify value")
    e._current_executor._commands.append(EnvCommand(Name, Value))


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