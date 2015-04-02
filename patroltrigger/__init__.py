import cmd
import cli
import sys
import trigger

run = cmd.run
trigger = trigger.trigger
cli = cli.cli

def runnable(name):
    """Makes a patrol file runnable directly."""
    if name == '__main__':
        cli(sys.modules[name])
