#!/usr/bin/env python
import sys
#from .gress_lib import Gress
from gress_lib import Gress


def main():
    target = sys.argv[1]
    filename = sys.argv[2]

    gress = Gress(target, filename)
    gress.run()


if __name__ == "__main__":
    main()
