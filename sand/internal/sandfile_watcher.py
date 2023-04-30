import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SandfileHandler(FileSystemEventHandler):
    def __init__(self, function_to_run):
        super().__init__()
        self.function_to_run = function_to_run

    def on_modified(self, event):
        if event.is_directory:
            return

        if os.path.basename(event.src_path) == 'Sandfile':
            self.function_to_run()

def watch_for_sandfile_changes(function_to_run_on_change, path = '.'):
    event_handler = SandfileHandler(function_to_run_on_change)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
