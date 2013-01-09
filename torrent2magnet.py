#! /usr/bin/python3

import sys
import hashlib
import urllib.parse
import bencode

for filename in sys.argv[1:]:
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

    # avoid duplicate urls
    seen_urls = []
    if "announce-list" in torrentdic:
        for urllist in torrentdic["announce-list"]:
            for url in urllist:
                if url not in seen_urls:
                    seen_urls.append(url)
                    quoted = urllib.parse.quote(url, safe="")
                    result.append("tr="+quoted)
    elif "announce" in torrentdic:
        url = torrentdic["announce"]
        if url not in seen_urls:
            seen_urls.append(url)
            quoted = urllib.parse.quote(url, safe="")
            result.append("tr="+quoted)

    print("magnet:?", "&".join(result), sep="")
