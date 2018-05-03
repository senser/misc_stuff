#!/usr/bin/env python2

from __future__ import print_function
import os
import sys
import struct
import datetime
import zlib

if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]) or not sys.argv[1].endswith(('.tgz', '.gz')):
   print('Please provide correct tar.gz file')
   sys.exit(1)

FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT = 1, 2, 4, 8, 16

with open(sys.argv[1]) as f:
    # read and check gzip header
    print('magic header is ', end='')
    if f.read(2) == '\037\213':
        print('correct')
    else:
        print('not correct. exiting')
        sys.exit(0)
    print('compression method is ', end='')
    if ord(f.read(1)) == 8:
        print('correct')
    else:
        print('not correct')
    flag = ord(f.read(1))
    print('flag = %s' % flag)
    print('modification time is %s' % datetime.datetime.fromtimestamp(int(struct.unpack("<L", f.read(4))[0])).strftime('%d/%m/%Y %H:%M:%S'))
    print('extra flag = %s' % ord(f.read(1)))
    print('os type = %s' % ord(f.read(1)))
    if flag & FHCRC:
        print('skipping 16-bit header CRC')
        f.read(2)
    if flag & FEXTRA:
        print('skipping the extra field')
        xlen = ord(f.read(1)) 
        xlen += 256*ord(f.read(1)) 
        f.read(xlen) 
    if flag & FNAME:
        print('filename is ', end='')
        while True:
            s = f.read(1)
            if s == '\0':
                break
            print(s, end='')
        print('')
    if flag & FCOMMENT:
        print('comment is ', end='')
        while True:
            s = f.read(1)
            if s == '\0':
                break
            print(s, end='')
        print('')
    # read compressed data
    decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
    crcval = zlib.crc32("") & 0xffffffffL
    length = 0
    while True:
        data = f.read(1024)
        if data == '':
            break
        decompdata = decompressor.decompress(data)
        length += len(decompdata)
        crcval = zlib.crc32(decompdata, crcval)
    decompdata = decompressor.flush()
    length += len(decompdata)
    crcval = zlib.crc32(decompdata, crcval) & 0xffffffffL
    # reread last 8 bytes to get CRC and file size
    f.seek(-8, 2)
    crc32 = struct.unpack("<I", f.read(4))[0]
    isize = struct.unpack("<I", f.read(4))[0]
    print('CRC check ', end='')
    if crc32 == crcval:
        print('passed')
    else:
        print('failed (%s != %s)' % (crc32, crcval))
    print('file size is ', end='')
    if isize == length:
        print('correct')
    else:
        print('incorrect (%s != %s)' % (isize, length))
