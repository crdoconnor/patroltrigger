import inspect
import fnmatch
import os
import subprocess
import time
import sys


class PatrolModule(object):
    def __init__(self, actual_module, postcmd = None):
        """Create a representation of a patrol module that can be used."""
        self.method_dict = {}
        self.all_methods = []
        self.postcmd = postcmd

        for method_name, actual_method in inspect.getmembers(actual_module, inspect.isfunction):
            if not method_name.startswith("_") and inspect.getmodule(actual_method) == actual_module:
                self.method_dict[method_name] = actual_method
                self.all_methods.append((method_name, actual_method))

    def run_all_methods(self):
        """Cycle through all methods and run."""
        for name, method in self.all_methods:
            method()

    def run_method(self, name, filenames=None):
        """Run a specific, named method."""
        self.method_dict[name](filenames)

    def match(self, filename):
        """Match and run a filename to a method."""
        start_time = time.time()
        command_ran = False
        for name, method in self.all_methods:
            currently_matching = False

            for include in method.includes:
                if fnmatch.fnmatch(filename, include):
                    currently_matching = True

            if method.excludes is not None:
                for exclude in method.excludes:
                    if fnmatch.fnmatch(filename, exclude):
                        currently_matching = False

            if currently_matching:
                command_ran = True
                
                try:
                    self.run_method(name, filenames=[filename])
                except subprocess.CalledProcessError, error:
                    break
                except Exception, e:
                    sys.exit(1)
        if self.postcmd is not None and command_ran:
            try:
                os.system(self.postcmd)
            except Exception, e:
                sys.stderr.write("Error running postcmd:\n")
                sys.stderr.write(e)
                sys.stderr.write("\n")
                sys.stderr.flush()
        if command_ran:
            sys.stdout.write("DURATION : {0:.1f} seconds\n".format(time.time() - start_time))
            sys.stdout.flush()
