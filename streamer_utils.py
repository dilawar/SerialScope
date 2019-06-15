"""streamer_utils.py: 
Utility for Table streamer. 
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import numpy as np
from collections import defaultdict

def bytes_to_np_arr(data):
    return np.frombuffer(data, float)

def np_array_to_string(arr):
    return np.uint8(arr).tostring()

def np_array_to_data(arr):
    # Make sure that first char of arr is 'H'
    n = 0
    res = defaultdict(list)
    leftOver = b''
    while n < len(arr):
        assert chr(int(arr[n])) == 'H', 'Expected H, Got %s'%arr[n]
        n += 1
        if n >= len(arr):
            return {}, arr.tobytes()
        hSize = int(arr[n])
        colName = np_array_to_string(arr[n+1:n+1+hSize])
        n += hSize + 1
        if n >= len(arr):
            return {}, arr.tobytes()
        assert chr(int(arr[n])) == 'V', 'Expected V'
        n += 1
        if n >= len(arr):
            return {}, arr.tobytes()
        dataSize = int(arr[n])
        n += 1
        if n >= len(arr) or n+dataSize >= len(arr): 
            return {}, arr.tobytes()
        res[colName].append(arr[n:n+dataSize])
        n += dataSize 
        leftOver += arr[n:].tobytes()
    return {k:np.concatenate(v) for k, v in res.items()}, leftOver

def decode_data(data):
    properSizeToDecode = 8*int(len(data)//8)
    data = data[:properSizeToDecode]
    leftOver = data[properSizeToDecode:]
    #  print( "[INFO ] Len of data %d bytes. %dx8 bytes" %(len(data), len(data)//8))
    try:
        arr = bytes_to_np_arr(data)
    except Exception as e:
        print("[WARN ] Error in decoding %s"%e)
        return {}, data+leftOver

    if not int(arr[0]) == ord('H'):
        print( "[WARN ] Not a valid stream. Missing header info." )
        return {}, data+leftOver
    res, rest = np_array_to_data(arr)
    return res, rest+leftOver

def test():
    with open(sys.argv[1], 'rb') as f:
        data = f.read()
    print( "[INFO ] Total bytes read %d" % len(data))
    s = decode_data(data)
    print(s)

if __name__ == '__main__':
    test()
