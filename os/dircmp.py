#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import re
import argparse as ap
import time
import filecmp
import difflib
from os.path import abspath, isdir, isfile, basename
from os.path import join as pathjoin


AUTHOR = 'luyl@biomarker.com.cn'
VERSION = '1.0'
DATE = 'March 28, 2017'
SCRIPTDIR, SCRIPTNAME = os.path.split(abspath(sys.argv[0]))


DESCRIPTION = """
DESCRIPTION
  %s verison %s (%s)
  Compare two directories and find the differences.

  AUTHORS: %s

""" %(SCRIPTNAME, VERSION, DATE, AUTHOR)

USAGE = """
python %s 
""" %tuple([SCRIPTNAME]*1)

EPILOG = """
epilog.
"""

def arg_parse():
    parser = ap.ArgumentParser(description = DESCRIPTION, usage = USAGE, epilog = EPILOG,
          formatter_class=ap.RawTextHelpFormatter)
    arg = parser.add_argument
    arg("dir1", help="the first directory")
    arg("dir2", help="the second directory")
    arg("-redundant", help="to show detail different information", action="store_true")
    arg("-v", dest="version", action="version", version=SCRIPTNAME+" "+VERSION)
    args = parser.parse_args()
    return vars(args)


def mkdir(*paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
    return paths


def tprint(str):
    time_user = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    print "[%s] %s" %(time_user,str)


class Dircmp():
    def __init__(self):
        self.common = []
        self.common_files = []
        self.common_dirs = []
        self.common_funny = []
        self.common_diff_files = []
        self.left_list = []
        self.left_files = []
        self.left_dirs = []
        self.right_list = []
        self.right_files = []
        self.right_dirs = []
    def dircmp(self, dir1, dir2):
        cmps = filecmp.dircmp(dir1, dir2)
        self.common += [pathjoin(dir1, i) for i in cmps.common]
        self.common_files += [pathjoin(dir1, i) for i in cmps.common_files]
        self.common_dirs += [pathjoin(dir1, i) for i in cmps.common_dirs]
        self.common_funny += [pathjoin(dir1, i) for i in cmps.common_funny]
        self.common_diff_files += [(pathjoin(dir1, i), pathjoin(dir2, i)) for \
                                   i in filecmp.cmpfiles(dir1, dir2, cmps.common_files)[1]]
        left_list = [pathjoin(dir1, i) for i in cmps.left_only]
        self.left_list += left_list
        self.left_files += [i for i in left_list if isfile(i)]
        self.left_dirs += [i for i in left_list if isdir(i)]
        right_list = [pathjoin(dir2, i) for i in cmps.right_only]
        self.right_list += right_list
        self.right_files += [i for i in right_list if isfile(i)]
        self.right_dirs += [i for i in right_list if isdir(i)]
        subdirs = sorted(cmps.subdirs.keys())
        for sd in subdirs:
            left_subdir = pathjoin(dir1, sd)
            right_subdir = pathjoin(dir2, sd)
            self.dircmp(left_subdir, right_subdir)


def filediff(file1, file2):
    f1 = file(file1).readlines()
    f2 = file(file2).readlines()
    cmps = ''.join(difflib.unified_diff(f1, f2))
    return 'FILE1: [%s]\nFILE2: [%s]\n%s\n' %(file1, file2, cmps)


def main():
    args = arg_parse()
    dir1 = abspath(args['dir1'])
    dir2 = abspath(args['dir2'])
    redundant = args['redundant']

    d = Dircmp()
    d.dircmp(dir1, dir2)

    # filter file
    filter_pat = r'((^\..*)|(.*\.bak\.*[0-9]*$)|(.*\.pyc$))'
    d.left_list = [i for i in d.left_list if not re.match(filter_pat, basename(i))]
    d.right_list = [i for i in d.right_list if not re.match(filter_pat, basename(i))]
    d.common_diff_files = [(i, j) for (i, j) in d.common_diff_files if \
                           not re.match(filter_pat, basename(i)) or \
                           not re.match(filter_pat, basename(j))]

    print "## THE TWO FILES AS FOLLOWS:\n\t%s\n\t%s" %(dir1, dir2)
    if d.left_list:
        print "\n## THE ONLY FILES EXIET IN %s:" %dir1
        print '\t%s' %('\n\t'.join(d.left_list))
    if d.right_list:
        print "\n## THE ONLY FILES EXIET IN %s:" %dir2
        print '\t%s' %('\n\t'.join(d.right_list))
    if d.common_diff_files:
        print "\n## THE DIFF:"
        results = ['\t- %s\n\t+ %s\n' %(x,y) for x,y in d.common_diff_files]
        print ''.join(results)
        if redundant:
            print "\n## THE DIFF [DETIAL]:"
            results = map(lambda x: filediff(*x), d.common_diff_files)
            print ''.join(results)


if __name__ == '__main__':
    main()
