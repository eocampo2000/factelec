'''
Created on Oct 19, 2016

@author: tester
'''
__version__ = '20161019'

import sys
import xml.parsers.expat 

def chk_valid_xml(fn): 
    rc = (False,'')
    try: 
        parser = xml.parsers.expat.ParserCreate() 
        parser.ParseFile(open(fn, "r")) 
        rc = (True, '%s is well-formed' % fn )
    
    except IOError:
        rc = (False, '%s : %s' % (sys.exc_type,sys.exc_value))
    
    except xml.parsers.expat.ExpatError:
        rc = (False, '%s : %s' % (sys.exc_type,sys.exc_value))
    
    except Exception: 
        rc = (False, "%s :%s"  % (sys.exc_type,sys.exc_value))
    
    finally : return rc 
    
# This method reads and xml element root recursively and places the result in a dictionary.
# Child attributes will have the @
# Use the following  to invoke:
#    tree = ElementTree.parse(f)
#    root = tree.getroot()
#    d    = xml_to_dict(root)
#   
def xml_to_dict(el):
    d={}
    if el.text:
        d[el.tag] = el.text
    else:
        d[el.tag] = {}
    children = el.getchildren()
    if children:
        d[el.tag] = map(xml_to_dict, children)

    d.update(('@' + k, v) for k, v in el.attrib.iteritems())

    return d     