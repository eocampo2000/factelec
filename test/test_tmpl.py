'''
Created on Oct 27, 2016

@author: tester
'''

import sys

def main():
    pass

if __name__ == "__main__":
    from apps.setwinenv import setEnvVars  # Remove in UX 
    setEnvVars()
    rc = main()
    print "rc = " , rc
    sys.exit(rc)