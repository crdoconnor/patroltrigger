import inspect
import fnmatch
import subprocess
import time
import sys


class PatrolModule(object):
    """Representation of a user's patrol.py file."""

    def __init__(self, actual_module, postcmd=None):
        """Intepret the code, list all non-private methods in order of appearance."""
        self.method_dict = {}
        self.all_methods = []
        self.postcmd = postcmd

        for method_name, actual_method in inspect.getmembers(actual_module, inspect.isfunction):
            if not method_name.startswith("_") and inspect.getmodule(actual_method) == actual_module:
                self.method_dict[method_name] = actual_method
                self.all_methods.append((method_name, actual_method, inspect.findsource(actual_method)[1]))

        sorted(self.all_methods, key=lambda method: method[2])  # Sort by line number

    def run_all_methods(self):
        """Cycle through all methods and run."""
        for _, method, _ in self.all_methods:
            try:
                method([])
            except subprocess.CalledProcessError:
                break

    def run_method(self, name, filenames=None):
        """Run a specific, named method."""
        try:
            self.method_dict[name](filenames)
        except subprocess.CalledProcessError:
            return

    def trigger(self, filenames):
        """Run methods which match the listed filenames."""
        def match(method, filenames):
            """Return True if method's trigger matches one of the specified filenames."""
            currently_matching = False

            for filename in filenames:
                for include in method.includes:
                    if fnmatch.fnmatch(filename, include):
                        currently_matching = True

                if method.excludes is not None:
                    for exclude in method.excludes:
                        if fnmatch.fnmatch(filename, exclude):
                            currently_matching = False
            return currently_matching

        start_time = time.time()
        command_ran = False
        for name, method, _ in self.all_methods:
            if match(method, filenames):
                command_ran = True

                try:
                    self.run_method(name, filenames=filenames)
                except subprocess.CalledProcessError:
                    break

        if self.postcmd is not None and command_ran:
            try:
                subprocess.check_call(self.postcmd, shell=True)
            except subprocess.CalledProcessError:
                sys.stderr.write("Error running postcmd.\n")
                sys.stderr.write("\n")
                sys.stderr.flush()
        if command_ran:
            sys.stdout.write("DURATION : {0:.1f} seconds\n".format(time.time() - start_time))
            sys.stdout.flush()
