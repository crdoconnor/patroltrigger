import pyuv
import os
import signal


class Watcher(object):
    """Watches the filesystem and fires triggers using libuv."""

    def __init__(self, directory, patrol_module):
        self.directory = directory
        self.patrol_module = patrol_module
        self.change_queue = []
        self.event_handles = []
        self.signal_h = None

    def close_handles(self):
        """Close all I/O handles prior to exit."""
        self.signal_h.close()
        for event_handle in self.event_handles:
            event_handle.close()

    def read_handle(self, handle, filename, events, error):
        """Callback every time something is modified in the repository."""
        fullpath = os.path.realpath(handle.path + os.sep + filename)
        relative_path = fullpath.replace(os.path.realpath(self.directory) + os.sep, "")

        if os.path.exists(fullpath):
            self.change_queue.append(relative_path)

        if not os.path.exists(self.directory + os.sep + 'lock'):
            self.patrol_module.trigger(self.change_queue)
            self.change_queue = []

    def run(self):
        """Run the loop."""
        loop = pyuv.Loop.default_loop()

        # Attach a handler for each subdirectory underneath
        for subdirectory in [os.path.realpath(x[0]) for x in os.walk(self.directory)]:
            event_handle = pyuv.fs.FSEvent(loop)
            event_handle.start(subdirectory, 0, self.read_handle)
            self.event_handles.append(event_handle)

        # Attach a handler for CTRL-C
        self.signal_h = pyuv.Signal(loop)
        self.signal_h.start(lambda handle, signum: self.close_handles(), signal.SIGINT)

        loop.run()
