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
    def trigger2(filenameS):
        print "second command triggered with filename: {}".format(filenameS)
    
    runnable(__name__)

Run like so::

    $ python patrol.py


Features
========

* Each method is timed.
* If a command fails (e.g. a unit test), the entire method is aborted by default at that point to shorten feedback time.
* Run a custom command after each method is finished (e.g. guake, notify-send).
