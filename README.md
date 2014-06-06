update_status
=============

A python application for viewing system's update status.

This application gathers and displays information about the system's update
status such as:

- How many packages can be updated?
- Are the any pending kernel updates?
- Does the system need to be rebooted?

While this application can be run manually from the command-line on the node in
question, it's probably most useful when it's used with a remote monitoring
application plugin, or with remote management tools such as Fabric
(http://www.fabfile.org).

For example, the following Fabric task can be used to print the update status of
several hosts in parallel:

    @task
    @parallel
    def show_update_status():
        with settings(hide("everything"), hide("status")):
            output = run("/path/to/update_status.py")
            print "%-30s: %s" % (env.host, output)

This Fabric task would produce output similar to this:

    server1.domain.com            : Kernel upgradable: Yes  Upgradable packages: 4
    server2.domain.com            : Kernel upgradable: Yes  Upgradable packages: 4
    server3.domain.com            : Kernel upgradable: No   Upgradable packages: 0

The Fabric task could be easily extended to upload the update_status.py script
to the target host before running it.

TODO
====

- Add an option parser
