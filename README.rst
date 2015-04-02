PatrolTrigger
=============

Trigger custom commands from filesystem events.

Patrol uses libuv, which creates event driven hooks to filesystem events using epoll, kqueue or IOCP.

You can use it to selectively build your project when files change and run tests as soon as you hit the save button.


Use
===

To install::

    sudo pip install patroltrigger


Create a patrol.py file in your project's root directory:

.. code-block:: python

    #!/usr/bin/python
    from patroltrigger import runnable, run, trigger

    @trigger(["*.py", ], exclude=['venv/*',])
    def trigger1(filenames):
        print "trigger1"
        run("""echo first command triggered""")
        the_output_is_in_this_variable_though = run("echo this command is run, but the output is not displayed", silent=True)

    @trigger(["*.py", ], exclude=['venv/*',])
    def trigger2(filenames):
        print "trigger2 command triggered with filename: {}".format(', '.join(filenames))
        run("false", ignore_errors=True)    # If ignore_errors=False, nothing further will be executed.
        run("""echo if ignore_errors is False or not specified, you wont ever see this command *or* the results of trigger3.""")

    @trigger(["*.py", ], exclude=['venv/*',])
    def trigger3(filenames):
        print "trigger3 command triggered with filename: {}".format(', '.join(filenames))

    runnable(__name__)


Run like so::

    $ python patrol.py


Or get help::

    $ python patrol.py --help
    Usage: example.py [options]

    Options:
    -h, --help            show this help message and exit
    -r RUN, --run=RUN     Specify a method in example.py to run directly.
    -a, --all             Run all methods in example.py in priority order.
    -p POST, --post=POST  Command to run after a trigger (e.g. guake)
    -d DIRECTORY, --directory=DIRECTORY
                            Directory to run example.py in (default:
                            /home/user/yourproject).



Features
========

* Each time a set of methods are triggered, the total run time is timed.
* If a command fails (e.g. a unit test), the method is aborted by default at that point to shorten feedback time. Subsequent matching methods will not run.
* Run a custom command after each method is finished (e.g. guake, notify-send).
* If multiple methods are triggered by a changed file, they will run *in the order they appear* in patrol.py.
* Ability to run commands manually.
