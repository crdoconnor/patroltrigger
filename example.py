#!/usr/bin/python
from patrol import runnable, run, watcher
import time

@watcher(["*.py", ], exclude=['venv/*',])
def trigger1(filename):
    print "trigger1... waiting 10 seconds"
    run("false", ignore_errors=True)
    time.sleep(10)
    run("echo first finished")
    run("false")
    print "this message should never print"

@watcher(["*.rst", ], exclude=['venv/*',])
def trigger2(filename):
    print "second command triggered with filename: {}".format(filename)

runnable(__name__)