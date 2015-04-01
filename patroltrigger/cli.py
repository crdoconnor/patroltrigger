import os
import sys
import optparse
import inspect
import pyuv
import signal
import module
import subprocess


def cli(actual_patrol_module):
    """Command line interpreter for a patrol file."""
    parser = optparse.OptionParser()
    parser.add_option("-r", "--run", type="str", dest="run", default=None,
                      help="Specify a method in {} to run directly.".format(actual_patrol_module.__file__))
    parser.add_option("-a", "--all", action="store_true", dest="all",
                      help="Run all methods in {} in priority order.".format(actual_patrol_module.__file__))
    parser.add_option("-p", "--post", type="str", dest="post",
                      help="Command to run after a trigger (e.g. guake)")
    parser.add_option("-d", "--directory", type="str", dest="directory",
                      help="Directory to run {} in (default: {}).".format(actual_patrol_module.__file__, sys.argv[0]))

    options, _ = parser.parse_args(sys.argv[1:])

    pm = module.PatrolModule(actual_patrol_module, postcmd=options.post)

    if options.all:
        pm.run_all_methods()
        sys.exit()

    if options.run:
        if options.run in pm.method_dict:
            pm.run_method(options.run)
            sys.exit()
        else:
            sys.stderr.write("{} command not found.\n".format(options.run))
            sys.stderr.flush()
            sys.exit(1)

    if options.directory:
        cwd = options.directory
    else:
        cwd = os.path.dirname(os.path.realpath(sys.argv[0]))

    os.chdir(cwd)
    subdirectories = [os.path.realpath(x[0]) for x in os.walk(cwd)]
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
            relpath = fullpath.replace(os.path.realpath(cwd) + os.sep, "")

            pm.match(relpath)

    def signal_cb(handle, signum):
        """Handle ctrl-C"""
        close_handles()

    event_handles = []

    for subdirectory in subdirectories:
        event_handle = pyuv.fs.FSEvent(loop)
        event_handle.start(subdirectory, 0, read_handle)
        event_handles.append(event_handle)

    signal_h = pyuv.Signal(loop)
    signal_h.start(signal_cb, signal.SIGINT)

    loop.run()



