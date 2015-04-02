import pyuv
import os
import signal


def watcher(directory, patrol_module):
    """Watch file system for changes in all subdirectories and loop."""
    subdirectories = [os.path.realpath(x[0]) for x in os.walk(directory)]
    loop = pyuv.Loop.default_loop()

    def close_handles():
        """Close all I/O handles prior to exit."""
        signal_h.close()
        for event_handle in event_handles:
            event_handle.close()

    def read_handle(handle, filename, events, error):
        """Callback every time something is modified in the repository."""
        fullpath = os.path.realpath(handle.path + os.sep + filename)
        if os.path.exists(fullpath):
            relative_path = fullpath.replace(os.path.realpath(directory) + os.sep, "")

            # Match the file to the trigger and run the method.
            patrol_module.match(relative_path)

    def signal_cb(handle, signum):
        """Handle ctrl-C"""
        close_handles()

    event_handles = []

    # Attach a handler for each subdirectory underneath
    for subdirectory in subdirectories:
        event_handle = pyuv.fs.FSEvent(loop)
        event_handle.start(subdirectory, 0, read_handle)
        event_handles.append(event_handle)

    signal_h = pyuv.Signal(loop)
    signal_h.start(signal_cb, signal.SIGINT)

    loop.run()
