#!/usr/bin/python
from __future__ import print_function
from patroltrigger import runnable, run, trigger

@trigger(["*.py", ], exclude=['venv/*',])
def trigger1(filenames):
    print("trigger1")
    run("""echo first command triggered""")
    the_output_is_in_this_variable_though = run("echo this command is run, but the output is not displayed", silent=True)

@trigger(["*.py", ], exclude=['venv/*',])
def trigger2(filenames):
    print("trigger2 command triggered with filename: {}".format(', '.join(filenames)))
    run("false", ignore_errors=True)    # Abort here on non-zero return code
    run("""echo if ignore_errors is False or not specified, you wont ever see this command *or* subsequent methods that are also triggered.""")

@trigger(["*.py", ], exclude=['venv/*',])
def trigger3(filenames):
    print("trigger3 command triggered with filename: {}".format(', '.join(filenames)))

runnable(__name__)