import subprocess
import sys


def run(command, silent=False, ignore_errors=False):
    """Run command and fail the whole build if it fails, unless errors are suppressed."""
    try:
        if silent:
            return subprocess.check_output(command, shell=True)
        else:
            return subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError:
        if ignore_errors == False:
            _, error = sys.exc_info()[:2]
            sys.stderr.write("""- "{}" returned non-zero exit code {}. """.format(command, error.returncode))
            sys.stderr.write("""Use ignore_errors=True to suppress and continue in future.\n""")
            if error.output is not None:
                sys.stderr.write(str(error.output))
                sys.stderr.write("\n")
            sys.stderr.flush()
            raise
