import subprocess
import sys


def run(command, silent=True, ignore_errors=False):
    """Run command and fail the whole build if it fails, unless errors are suppressed."""
    try:
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError, error:
        if ignore_errors == False:
            sys.stderr.write("""- "{}" returned non-zero exit code {}.\n""".format(command, error.returncode))
            sys.stderr.write("""- Use ignore_errors=True to suppress and continue.\n""")
            if error.output is not None:
                sys.stderr.write(str(error.output))
                sys.stderr.write("\n")
            sys.stderr.flush()
            raise