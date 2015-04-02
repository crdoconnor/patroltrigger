import os
import sys
import optparse
import module
import watcher


def cli(actual_patrol_module):
    """Command line interpreter for a patrol file."""
    patrolpy_directory = os.path.dirname(os.path.realpath(sys.argv[0]))

    parser = optparse.OptionParser()
    parser.add_option("-r", "--run", type="str", dest="run", default=None,
                      help="Specify a method in {} to run directly.".format(actual_patrol_module.__file__))
    parser.add_option("-a", "--all", action="store_true", dest="all",
                      help="Run all methods in {} in priority order.".format(actual_patrol_module.__file__))
    parser.add_option("-p", "--post", type="str", dest="post",
                      help="Command to run after a trigger (e.g. guake)")
    parser.add_option("-d", "--directory", type="str", dest="directory",
                      help="Directory to run {} in (default: {}).".format(actual_patrol_module.__file__, patrolpy_directory))

    options, _ = parser.parse_args(sys.argv[1:])

    patrol_module = module.PatrolModule(actual_patrol_module, postcmd=options.post)

    # Use directory where patrol.py resides if no directory specified
    if options.directory:
        cwd = options.directory
    else:
        cwd = patrolpy_directory

    os.chdir(cwd)

    # Run all methods
    if options.all:
        patrol_module.run_all_methods()
        sys.exit()

    # Run specific method
    if options.run:
        if options.run in patrol_module.method_dict:
            patrol_module.run_method(options.run)
            sys.exit()
        else:
            sys.stderr.write("{} command not found.\n".format(options.run))
            sys.stderr.flush()
            sys.exit(1)

    watcher.watcher(cwd, patrol_module)
