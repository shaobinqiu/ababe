#!/usr/bin/env python

import sys
import os
import shutil
import pdb

def main():
    ndirs = sys.argv[1]
    files = sys.stdin.read().splitlines()
    working_path = os.getcwd()
    subdir_path = os.path.join(working_path, "subdirs")
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)
    else:
        shutil.rmtree(subdir_path)
        os.makedirs(subdir_path)

    for n, f in enumerate(files):
        f = os.path.join(working_path, f)
        d = "subdir_{0:}".format(n//int(ndirs))
        new_path = os.path.join(subdir_path, d)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        shutil.copy(f, new_path)


if __name__ == '__main__':
    main()
