#! /usr/bin/python3

import sys
import hashlib
import urllib.parse
import bencode
import argparse

parser = argparse.ArgumentParser(description='Convert torrent files to magnet '
                                             'links')
parser.add_argument('files', metavar='torrent', nargs='+',
                    help='a torrent file')
parser.add_argument('-a', '--append-trackers', dest='trackers_file',
                    metavar='trackers_file',
                    help='append tracker list to magnet')
args = parser.parse_args()

new_trackers = []
if args.trackers_file != None:
    f = open(args.trackers_file, 'r')
    for line in f:
        new_trackers.append(line.rstrip())
    f.close()

for filename in args.files:
    print(filename, ":", sep="", file=sys.stderr)
    result = []
    file = open(filename, "br")
    torrentdic = bencode.bdecode(file.read())
    file.close()

    if "info" not in torrentdic:
        raise ValueError("No info dict in torrent file")

    encodedInfo = bencode.bencode(torrentdic["info"])
    sha1 = hashlib.sha1(encodedInfo).hexdigest()
    result.append("xt=urn:btih:"+sha1)

    if "name" in torrentdic["info"]:
        quoted = urllib.parse.quote(torrentdic["info"]["name"], safe="")
        result.append("dn="+quoted)

    trackers = []
    if "announce-list" in torrentdic:
        for urllist in torrentdic["announce-list"]:
            trackers += urllist
    elif "announce" in torrentdic:
        trackers.append(torrentdic["announce"])
    trackers += new_trackers

    # eliminating duplicates without sorting
    seen_urls = []
    for url in trackers:
        if url not in seen_urls:
            seen_urls.append(url)
            quoted = urllib.parse.quote(url, safe="")
            result.append("tr="+quoted)
    print("magnet:?", "&".join(result), sep="")
