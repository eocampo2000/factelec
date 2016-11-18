'''
Created on Oct 27, 2016

@author: tester
'''

import sys
import utils.fileutils as fu


def trimFile():
    fn = r"C:\apps\infa_share\SrcFiles\F-100-00397704.TXT"
    tgt = r"C:\apps\infa_share\SrcFiles\F-100-00397704.trim"
    #rc = fu.remBlankLineFile(fn,tgt)
    rc = fu.trimRBlankFile(fn)
    return rc


def main():
    return trimFile()

if __name__ == "__main__":
    from apps.setwinenv import setEnvVars  # Remove in UX 
    setEnvVars()
    rc = main()
    print "rc = " , rc
    sys.exit(rc)