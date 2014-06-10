#!/usr/bin/python
# -*- coding: utf-8 -*-

import apt, re, subprocess

class Update_status():
    """Class that models that update status of a system"""

    def __init__(self, *args, **kwargs):

        # Update the cache before doing anything
        #self.update_apt_cache()
        self.kernel_regex=re.compile("^linux-image-.*$")

        self.upgradable_packages = self.get_upgradable_packages()
        self.kernel_upgradable = self.is_kernel_upgradable()
        self.running_installed_kernel = self.is_running_installed_kernel()

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

    def is_running_installed_kernel(self):
        """Determine if the running kernel is different from the installed 
           kernel"""

        # Extract running kernel version, build and type from uname output
        uname_output = subprocess.check_output(['uname', '-r'], shell=False)
        r_version = uname_output.split('-')[0].rstrip('\n')
        r_build = uname_output.split('-')[1].rstrip('\n')
        type = uname_output.split('-')[2].rstrip('\n')

        # Construct the kernel package name for the running kernel
        kernel_package = 'linux-image-{type}'.format(type=type)

        # Convert uname-produced version info into format compatible with 
        # apt-show-versions output.
        r_full_version = r_version+"."+r_build

        # apt-show-versions can produce two types of output, both of which we 
        # need to be able to parse:
        #
        # linux-image-virtual/precise upgradeable from 3.2.0.63.75 to 3.2.0.64.76
        # linux-image-virtual/precise uptodate 3.2.0.64.76
        #
        asv_output = subprocess.check_output(['apt-show-versions', '-p', kernel_package], shell=False)

        if "upgradeable" in asv_output:
            i_full_version = asv_output.split(' ')[3]
        elif "uptodate" in asv_output:
            i_full_version = asv_output.split(' ')[2]

        # This only checks if the running kernel differs from the installed 
        # kernel, not whether it's older or newer.
        if not r_full_version in i_full_version:
            return False
        else:
            return True

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

    def running_installed_kernel_to_str(self):
        """Return a string telling if the running kernel is different from the 
           installed kernel."""

        if self.running_installed_kernel:
            return "Yes"
        else:
            return "No"

    def oneline(self):
        """One-line representation of the system update status"""

        return "Kernel upgradable: "+self.kernel_upgradable_to_str()+\
             "\tUpgradable packages: "+self.update_count_to_str()+\
             "\tRunning installed kernel: "+self.running_installed_kernel_to_str()

    def csv(self):
        """CSV representation of the system update status"""
        return self.kernel_upgradable_to_str()+","+self.update_count_to_str()+","+self.running_installed_kernel_to_str()

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
