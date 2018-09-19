"""Module for handling GLGA qa files.

Defines classes and methods for manipulating GLGA qa files.
GLGA qa files are flat text files with 39 keyword/values 
pairs, one per line, separated by '=' in column 17 and may
or may not be followed by a comment which begins with a '#'
after the value.

"""

__version__ = "$Id: qa.py,v 1.2 2011/06/30 00:17:27 neill Exp $"
# $Source: /users/neill/cvshome/pylib/pydon/glga/qa.py,v $

class GLGAQa:

    """GLGAQa class definition.

    Attributes:
    dict - dictionary containing qa keyword/value pairs
    coms - dictionary containing qa keyword/comment pairs
    good_count - correct number of entries in qa file (39)

    Methods:
    read - read a qa file
    write - write a qa file
    set - set a qa value associated with a key
    prt - print qa dictionary to screen
    
    """

    def __init__(self):
        """Initialize GLGAQa class."""

        self.dict = {}
        self.coms = {}
        self.good_count = 39


    def read(self,filename, verbose=False):
        """Read GLGA qa file into self.dict.

        Inputs:
        filename - GLGA qa filename (string)

        Optional Keyword:
        verbose - set to True to print bad file warnings

        Returns number of key/value pairs read.

        Usage: nk = self.read(<filename>, verbose=True)

        """

        # check if file exists
        try:
            with open(filename,"r") as fh:
                lines = fh.readlines()
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)

        # lines successfuly read in
        else:
            for line in lines:

                # check proper format
                try:
                    key = line.split("=")[0].strip().lower()
                    val = line.split("=")[1].split("#")[0].strip()
                    try:
                        com = line.split("#")[1].strip()
                    except IndexError:
                        com = ""
                    if val.isdigit(): val = int(val)
                    self.dict[key] = val
                    self.coms[key] = com

                # escape if improper, len will signal error
                except IndexError:
                    break

        if len(self.dict) != self.good_count and verbose:
            print "Warning - incomplete or invalid qa file: ", filename

        return len(self.dict)


    def set(self, key, val):
        """Set qa value associated with key in self.dict.

        Inputs:
        key - qa keyword (string)
        val - value to assign in qa dictionary
        
        Returns True if value successfuly set, False if not.

        Usage: if not self.set('key', <value>): print "Error - value not set"

        """
        
        ret = False

        if key in self.dict:
            self.dict[key] = val
            ret = True

        return ret


    def prt(self, *keys):
        """Print qa dictionary to screen.

        Optional Inputs:
        keys: a list of keywords to print.  If not present print all.

        Does nothing if self.dict not initialized (read).

        Usage: self.prt(*[list of keys])

        """

        # are we not empty?
        if len(self.dict) > 0:

            # were specific keys requested?
            if len(keys) > 0:

                for k in sorted(keys):

                    # check for invalid keys
                    try:
                        print k.ljust(16),
                        print str(self.dict[k]).rjust(15),
                        if len(str(self.coms[k])) > 0: print "  # ",
                        print str(self.coms[k])
                    except KeyError:
                        print "NOT FOUND".rjust(15)

            # just print all the keys
            else:
                for k in sorted(self.dict.keys()):
                    print k.ljust(16),
                    print str(self.dict[k]).rjust(15),
                    if len(str(self.coms[k])) > 0: print "  # ",
                    print str(self.coms[k])


if __name__ == "__main__":
    import sys
    gqa = GLGAQa()
    if gqa.read(sys.argv[1]) != gqa.good_count:
        print "Error - invalid qa file: ",sys.argv[1]
        sys.exit()

    gqa.prt()

