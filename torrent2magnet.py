#! /usr/bin/python3

import sys
import os.path
import hashlib
import urllib.parse
import bencode
import argparse

def print_magnet(torrentdic, output=sys.stdout, new_trackers=None):
    result = []

    # add hash info
    if "info" not in torrentdic:
        raise ValueError("No info dict in torrent file")
    encodedInfo = bencode.bencode(torrentdic["info"])
    sha1 = hashlib.sha1(encodedInfo).hexdigest()
    result.append("xt=urn:btih:"+sha1)

    # add display name
    if "name" in torrentdic["info"]:
        quoted = urllib.parse.quote(torrentdic["info"]["name"], safe="")
        result.append("dn="+quoted)

    # add trackers list
    trackers = []
    if "announce-list" in torrentdic:
        for urllist in torrentdic["announce-list"]:
            trackers += urllist
    elif "announce" in torrentdic:
        trackers.append(torrentdic["announce"])
    if new_trackers:
        trackers += new_trackers

    # eliminate duplicates without sorting
    seen_urls = []
    for url in trackers:
        if [url] not in seen_urls:
            seen_urls.append([url])
            quoted = urllib.parse.quote(url, safe="")
            result.append("tr="+quoted)
    torrentdic["announce-list"] = seen_urls

    # output magnet or torrent file
    if output == sys.stdout:
        print("magnet:?", "&".join(result), sep="")
    else:
        out = open(output, 'bw')
        out.write(bencode.bencode(torrentdic))
        out.close()

# main ()
parser = argparse.ArgumentParser(description='Convert torrent files to magnet '
                                             'links')
parser.add_argument('files', metavar='torrent', nargs='*',
                    help='read from file instead of stdin; if outputting to a '
                         'torrent file, only one input file is allowed')
parser.add_argument('-a', '--append-trackers', dest='trackers_file',
                    metavar='trackers_file',
                    help='append tracker list to magnet')
parser.add_argument('-o', '--output-torrent', dest='output_file',
                    metavar='output_file',
                    help="output to torrent file instead of magnet (for adding "
                    "trackers, otherwise useless)")
args = parser.parse_args()

# select output
output = sys.stdout
if args.output_file:
    if os.path.exists(args.output_file):
        print('File exists, aborting:', args.output_file, file=sys.stderr)
        exit(1)
    else:
        output = args.output_file
        if len(args.files) > 1:
            raise ValueError('Can\'t output multiple input files into a torrent '
                             'file')

# read trackers file
new_trackers = []
if args.trackers_file != None:
    f = open(args.trackers_file, 'r')
    for line in f:
        new_trackers.append(line.rstrip())
    f.close()

# read from torrent files or stdin and print magnets
if args.files:
    for filename in args.files:
        print(filename, ":", sep="", file=sys.stderr)
        file = open(filename, "br")
        byte_stream = file.read()
        file.close()

        torrentdic = bencode.bdecode(byte_stream)
        print_magnet(torrentdic, output, new_trackers)
else:
    byte_stream = b''
    for line in sys.stdin.buffer:
        byte_stream += line

    torrentdic = bencode.bdecode(byte_stream)
    print_magnet(torrentdic, output, new_trackers)
