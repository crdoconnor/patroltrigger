PatrolTrigger
=============

Trigger custom commands from filesystem events.

Patrol uses libuv, which creates event driven hooks to filesystem events using epoll, kqueue or IOCP.

You can use it to selectively build your project when files change and run tests as soon as you hit the save button.


Use
===

To install::

    sudo pip install patroltrigger


Create a patrol.py file in your project's root directory::

    #!/usr/bin/python
    from patroltrigger import runnable, run, trigger
    
    @trigger(["*.py", ], exclude=['venv/*',])
    def trigger1(filenames):
        run("echo first command triggered")
        run("false")    # non-zero return code):
        run("echo you won't ever see this command")
    
    @trigger(["*.py", ], exclude=['venv/*',])
    def trigger2(filenames):
        print "second command triggered with filename: {}".format(', '.join(filenames))
    
    runnable(__name__)


Run like so::

    $ python patrol.py


Or get help::

    $ python patrol.py --help
    Usage: patrol.py [options]

    Options:
      -h, --help            show this help message and exit
      -r RUN, --run=RUN     Specify a method in patrol.py to run directly.
      -a, --all             Run all methods in patrol.py in priority order.
      -p POST, --post=POST  Command to run after a trigger (e.g. guake)
      -d DIRECTORY, --directory=DIRECTORY
                            Directory to run patrol.py in (default: /directory/patrolpy/is/in/).



Features
========

* Each method is timed.
* If a command fails (e.g. a unit test), the entire method is aborted by default at that point to shorten feedback time.
* Run a custom command after each method is finished (e.g. guake, notify-send).
* Run commands manually.
