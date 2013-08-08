torrent2magnet
==============

Command line tool for printing magnet links from torrent files.

    usage: torrent2magnet.py [-h] [-a trackers_file] [-o output_file] [torrent [torrent ...]]

##Examples:##

To simply convert a torrent file into a magnet link, use:

    torrent2magnet.py file.torrent

or, alternatively, pipe it into stdin:

    torrent2magnet.py < file.torrent

To add trackers from a text file (separated by linebreaks), use the -a switch:

    torrent2magnet.py -a trackers.txt file.torrent

And to output into a new torrent file (for adding trackers), use the -o switch:

    torrent2magnet.py -a trackers.txt -o new_file.torrent file.torrent

Note that when using the -o switch, you can't specify more than one input file.

torrentinfo
===========

Command line tool for printing information from a torrent file.

    usage: torrentinfo.py [-h] [-f torrent_file] [key [key ...]]

The program will return a non-zero status if any of the specified keys is not present in the file.

##Examples:##

To print out the whole torrent's dictionary, don't specify any keys:

    torrentinfo.py -f file.torrent

Alternatively, you can pipe the torrent to stdin:

    torrentinfo.py < file.torrent

To print a (or more) specific key (or keys), just pass them as arguments:

    torrentinfo.py -f file.torrent 'info hash' 'name' 'announce-list'

The special keys 'info hash' or 'hash' will print out the torrent's info dict's hash. Any other key will print out the value to that key, if available in that torrent file.

A non-comprehensive list of possible keys is:

* hash
* info hash
* announce
* announce-list
* info
* name
* piece length
* pieces
* length
* files
* root hash
* private
* nodes
* httpseeds
* created by
* creation date
* encoding
* comment
