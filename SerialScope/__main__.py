__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

from SerialScope import scope
import argparse

def main(args=None):
    description = '''Arduino NeuroScope.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--port', '-p', type=str
            , required = False, default= ''
            , help = 'Serial port.'
            )
    parser.add_argument('--baudrate', '-B'
            , required = False
            , default = 115200
            , help = 'Baudrate of Arduino board.'
            )
    parser.add_argument( '--debug', '-d', action='store_true')
    class Args: pass
    args = Args()
    parser.parse_args(namespace=args)
    scope.main(args)

if __name__ == '__main__':
    main()
