#!/usr/bin/python
# -*- coding: utf-8 -*-

import apt, re, subprocess, os

class Update_status():
    """Class that models that update status of a system"""

    def __init__(self, *args, **kwargs):

        # Executable locations
        self.un_dir = '/usr/lib/update-notifier'
        self.apt_check = os.path.join(self.un_dir, 'apt-check')
        self.reboot_required_file = '/var/run/reboot-required'

        # Update the cache before doing anything
        #self.update_apt_cache()
        self.kernel_regex=re.compile("^linux-image-.*$")

        # Data derived using the Python apt module
        self.pending_updates = self.get_pending_updates()
        self.kernel_upgradable = self.is_kernel_upgradable()

        # Data derived from update-notifier
        self.pending_update_count = None
        self.pending_security_update_count = None
        self.set_update_counts()
        self.need_restart = self.does_need_restart()

    def update_apt_cache(self):
        """Update apt cache. This only affects the underlying system state, not the object state."""

        cache = apt.Cache()
        cache.open(None)
        cache.update()

    def set_update_counts(self):
        """Set update counts"""
        aco = subprocess.check_output(self.apt_check, shell=False, stderr=subprocess.STDOUT)
        self.pending_update_count = aco.split(';')[0]
        self.pending_security_update_count = aco.split(';')[1]

    def get_pending_updates(self):
        """Get a list of upgradable package objects"""

        cache = apt.Cache()
        cache.open(None)

        pending_updates = []

        for key in cache.keys():
            package = cache[key]

            if package.is_upgradable:
                pending_updates.append(package)

        return pending_updates

    def is_kernel_upgradable(self):
        """Return a boolean value telling whether or not there are pending kernel updates"""

        kernel_upgradable = False

        for package in self.pending_updates:
            if self.kernel_regex.match(package.name):
                kernel_upgradable = True

        return kernel_upgradable

    def get_pending_update_count(self):
        """Return the number of pending updates"""
        return self.pending_update_count

    def get_pending_security_update_count(self):
        """Return the number of pending security updates"""
        return self.pending_update_count

    def does_need_restart(self):
        """Determine if a restart is required. This will only work properly after a kernel has been installed after update-notifier-common installation"""
        if os.path.isfile(self.reboot_required_file):
            return True

    def pending_updates_to_str(self):
        """Return a string presentation of all upgradable packages"""

        updates=""
        for package in self.pending_updates:
            updates = updates + package.name + "\n"

        return updates

    def pending_update_count_to_str(self):
        """Return a string presentation of the upgradable package count"""
        return str(self.pending_update_count)

    def pending_security_update_count_to_str(self):
        """Return a string presentation of the upgradable package count"""
        return str(self.pending_security_update_count)

    def kernel_upgradable_to_str(self):
        """Return a string telling whether kernel can be updated"""

        if self.kernel_upgradable:
            return "Yes"
        else:
            return "No"

    def need_restart_to_str(self):
        """Return a string telling if a restart is required"""

        if self.need_restart:
            return "Yes"
        else:
            return "No"

    def __str__(self):
        """Detailed string representation of the system update status"""

        return "Kernel upgradable: "+self.kernel_upgradable_to_str() +\
             "\tPending updates: "+self.pending_update_count_to_str() +\
             "\tPending security updates: "+self.pending_security_update_count_to_str() +\
             "\tNeeds restart: "+self.need_restart_to_str()

def main():
    """The default action is to print a human-readable, one-line report system's update status"""
    update_status = Update_status()
    print update_status

if __name__ == '__main__':
    main()
