# -*- coding: utf-8 -*-
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import mimetypes
import PIL.Image
import subprocess32 as subprocess
import datetime

def run(cmd):
    subprocess.run(cmd.split())

def log( *msg ):
    stamp = datetime.datetime.now().isoformat()
    print( '%s: %s' % (stamp, *msg))

def find_images_pil(dirname):
    """find_images
    Find images which can be displayed.

    :param dirname: Name of directory to search.
    """
    res = []
    for d, sd, fs in os.walk(dirname):
        for f in fs:
            fpath = os.path.join(d,f)
            mType = mimetypes.guess_type(fpath)[0]
            if not mType:
                continue
            appType = mType.split('/')[-1]
            try:
                im = PIL.Image.open(fpath)
                res.append(im)
            except Exception as e:
                pass
    return res


def test():
    find_images_pil( sys.argv[1] )

if __name__ == '__main__':
    test()
