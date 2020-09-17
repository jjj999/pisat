#! python3
"""
Update local site-packages.

This script make your debug faster.

"""

from os.path import join, expanduser, abspath, exists
import shutil


path_pisat = abspath("pisat")           # TO EDIT as the pisat package's path in your environment
name_env = ""                           # TO EDIT as the virtual environment's name in your environment
version_python = "3.7"
path_site = join(expanduser("~"),
                 ".local",
                 "share",
                 "virtualenvs",
                 name_env,
                 "lib",
                 "python" + version_python, 
                 "site-packages", 
                 "pisat")


def main():
    if exists(path_site):
        shutil.rmtree(path_site)

    shutil.copytree(path_pisat, path_site)
    
if __name__ == "__main__":
    main()
