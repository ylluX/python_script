#!/usr/bin/env python
#coding:utf-8

# show colors at pixels


from __future__ import division

import sys
import os
import argparse as ap
from math import sqrt, ceil
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


AUTHOR = 'luyulinvip@qq.com'
VERSION = 'v0.1'
DATE = '2017.9.11'
SCRIPTDIR, SCRIPTNAME = os.path.split(os.path.abspath(sys.argv[0]))

DESCRIPTION = """
  DESCRIPTION:
    show colors at pixels
    %s version %s (%s)

    AUTHOR: %s

""" %(SCRIPTNAME, VERSION, DATE, AUTHOR)

USAGE = """
python %s color.txt color.svg
python %s --maatrix color.txt color.png

color.txt
  o---------------------------------------------------------------------------------+
  | #E64B35 #4DBBD5 #00A087 #3C5488 #F39B7F #8491B4 #91D1C2 #DC0000 #7E6148 #B09C85 |
  | #3B4992 #EE0000 #008B45 #631879 #008280 #BB0021 #5F559B #A20056 #808180 #1B1919 |
  | #BC3C29 #0072B5 #E18727 #20854E #7876B1 #6F99AD #FFDC91 #EE4C97                 |
  | #00468B #ED0000 #42B540 #0099B4 #925E9F #FDAF91 #AD002A #ADB6B6 #1B1919         |
  | #374E55 #DF8F44 #00A1D5 #B24745 #79AF97 #6A6599 #80796B                         |
  +---------------------------------------------------------------------------------+

"""
USAGE = USAGE %tuple([SCRIPTNAME] * USAGE.count('%s'))

EPILOG = """
USAGE: %s
""" %USAGE


def arg_parse():
    parser = ap.ArgumentParser(description=DESCRIPTION, epilog=EPILOG,
                               formatter_class=ap.RawTextHelpFormatter)
    arg = parser.add_argument
    arg("color", help="color file")
    arg("figure", help="figure")
    arg("--matrix", help="show color at N*N matrix", action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = arg_parse()

    if args.matrix:
        colors_list = matrix_data(args.color)
    else:
        colors_list = line_data(args.color)

    fig = show_colors(colors_list)

    fig.savefig(args.figure)


def line_data(colors_file):
    """
    show colors by primitive input style
    """

    with open(colors_file, 'r') as f:
        colors_list = [i.strip().split() for i in f.readlines() if i.strip()]

    return colors_list


def matrix_data(colors_file):
    """
    show colors by rearrangement colors as matrix style
    """

    with open(colors_file, 'r') as f:
        colors = [j for i in f.readlines() if i.strip() for j in i.strip().split()]
    ncols = int(ceil(sqrt(len(colors))))
    nrows = int(ceil(len(colors) / ncols))
    colors_list = []

    for i in range(nrows):
        colors_list.append(colors[i*ncols:(i+1)*ncols])

    return colors_list


def show_colors(colors_list):

    cnum = sum(map(len, colors_list))
    colors = [j for i in colors_list for j in i]

    ncols = max(map(len, colors_list))
    nrows = len(colors_list)

    fig_width = 8
    fig_height = 8 / ncols * nrows

    fig, ax = plt.subplots(figsize=(fig_width,fig_height))

    X, Y = fig.get_dpi() * fig.get_size_inches()
    h = Y / nrows
    w = X / ncols

    patches = []
    
    for i, x in enumerate(colors_list):
        for j, y in enumerate(x):
            rect = mpatches.Rectangle([j*w, Y-(i+1)*h], w, h)
            patches.append(rect)

    collection = PatchCollection(patches, color=colors)
    ax.add_collection(collection)

    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_axis_off()
    
    fig.subplots_adjust(left=0, right=1,
                        top=1, bottom=0,
                        hspace=0, wspace=0)

    return fig


if __name__ == '__main__':
    main()
