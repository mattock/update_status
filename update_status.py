#!/usr/bin/python
# -*- coding: utf-8 -*-

import apt, re

class Update_status():
    """Class that models that update status of a system"""

    def __init__(self, *args, **kwargs):

        # Update the cache before doing anything
        #self.update_apt_cache()
        self.kernel_regex=re.compile("^linux-image-.*$")

        self.upgradable_packages = self.get_upgradable_packages()
        self.kernel_upgradable = self.is_kernel_upgradable()
        self.reboot_required = False

    def update_apt_cache(self):
        """Update apt cache. This only affects the underlying system state, not the object state."""

        cache = apt.Cache()
        cache.open(None)
        cache.update()

    def get_upgradable_packages(self):
        """Get a list of upgradable package objects"""

        cache = apt.Cache()
        cache.open(None)

        upgradable_packages = []

        for key in cache.keys():
            package = cache[key]

            if package.is_upgradable:
                upgradable_packages.append(package)

        return upgradable_packages

    def is_kernel_upgradable(self):
        """Return a boolean value telling whether or not there are pending kernel updates"""

        kernel_upgradable = False

        for package in self.upgradable_packages:
            if self.kernel_regex.match(package.name):
                kernel_upgradable = True

        return kernel_upgradable

    def upgradable_packages_to_str(self):
        """Return a string presentation of all upgradable packages"""

        updates=""
        for package in self.upgradable_packages:
            updates = updates + package.name + "\n"

        return updates

    def update_count_to_str(self):
        """Return a string presentation of the upgradable package count"""
        return str(len(self.upgradable_packages))

    def kernel_upgradable_to_str(self):
        """Return a string telling whether kernel can be updated"""

        if self.kernel_upgradable:
            return "Yes"
        else:
            return "No"

    def oneline(self):
        """One-line representation of the system update status"""

        return "Kernel upgradable: "+self.kernel_upgradable_to_str()+"\tUpgradable packages: "+self.update_count_to_str()

    def csv(self):
        """CSV representation of the system update status"""
        return self.kernel_upgradable_to_str()+","+self.update_count_to_str()

    def __str__(self):
        """Detailed string representation of the system update status"""

        output = "Upgradable packages ("+self.update_count_to_str()+")\n"\
                  +self.upgradable_packages_to_str()+"\n"\
                  +"Kernel upgradable: "+self.kernel_upgradable_to_str()
        return output

def main():
    """The default action is to print a human-readable, one-line report system's update status"""
    update_status = Update_status()
    print update_status.oneline()

if __name__ == '__main__':
    main()
