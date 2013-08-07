#! /usr/bin/python3

import sys
import binascii
import hashlib
import collections
import argparse
import bencode

def print_tree(tree, depth=0):
    ident = "  "
    if tree != None:
        if type(tree) in  [dict, collections.OrderedDict]:
            for key in tree:
                print(ident*depth, key, sep='')
                print_tree(tree[key], depth+1)
        elif type(tree) == list:
            for val in tree:
                print_tree(val, depth+1)
        elif type(tree) == bytes:
            for i in range(0, len(tree), 20):
                section = tree[i:i+20]
                print(ident*depth, bytes.decode(binascii.hexlify(section)), sep='')
        else:
            print(ident*depth, tree, sep='')

def print_key(tree, key):
    # 'hash' and 'info hash' aren't valid keys in neither the root or the info
    # trees, so we can use them to request a hash of the info tree
    if key in ['info hash', 'hash'] and 'info' in tree:
        info = bencode.bencode(tree['info'])
        print(hashlib.sha1(info).hexdigest())
        return True
    # root tree keys and info tree keys don't conflict, so we can just look for
    # the key in both trees and print what we find.
    elif key in tree:
        print_tree(tree[key])
        return True
    elif ('info' in tree) and (key in tree['info']):
        print_tree(tree['info'][key])
        return True
    return False

# main()

# a non comprehensive list of possible keys, meant only to be printed for the
# user (i.e. other keys are still allowed)
possible_keys = ['hash', 'info hash', 'announce', 'announce-list', 'info', 'name', 'piece length', 'pieces', 'length', 'files', 'root hash', 'private', 'nodes', 'httpseeds', 'created by', 'creation date', 'encoding', 'comment']

parser = argparse.ArgumentParser(description='Prints human readable '
                                             'representations of a torrent '
                                             'file\'s contents')
parser.add_argument('-f', '--file', dest='file', metavar='torrent_file',
                    help='read from file instead of stdin')
parser.add_argument('keys', nargs='*', metavar='key',
                    help='key from the torrent file\'s dictionary, whose '
                    'value is to be printed out; some of the possible keys '
                    'are: '+', '.join(possible_keys))
options = parser.parse_args()
filename = options.file
keys = options.keys

# read from torrent file or stdin
byte_stream = b''
if not filename:
    for line in sys.stdin.buffer:
        byte_stream += line
else:
    file = open(filename, 'br')
    byte_stream = file.read()
    file.close()
tree = bencode.bdecode(byte_stream)

# print requested keys, or whole tree; return non-zero status if a key isn't
# present
status = 0
if not keys:
    success = print_key(tree, 'info hash')
    if not success:
        status = 1
    print_tree(tree, depth=1)
else:
    for key in keys:
        success = print_key(tree, key)
        if not success:
            status += 1
exit(status)
