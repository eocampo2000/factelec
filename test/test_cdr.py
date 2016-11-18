'''
Created on Oct 17, 2016

@author: tester

Test CDR response.

-<cac:Response>
<cbc:ReferenceID>F001-00000065</cbc:ReferenceID>
<cbc:ResponseCode>0</cbc:ResponseCode>
<cbc:Description>La Factura numero F001-00000065, ha sido aceptada</cbc:Description>
</cac:Response>

'''
#from xml.etree import ElementTree
import sys
import xml.etree.ElementTree as ET
import utils.xmlutils  as xu
import procdata.procxml as pxml

# Logging
import logging 
from common.loghdl  import getLogHandler

logger  = logging.getLogger(__name__)

#import procdata.procxml as pxml
 

def readCDR():
    fn = r'C:\apps\infa_share\SrcFiles\CDR.xml'
#     f = fu.openFile(fn,'r')    
#     parser = xml.parsers.expat.ParserCreate() 
#     parser.ParseFile(open(fn, "r")) 
    rc = xu.chk_valid_xml(fn)
    print "----- u.chk_valid_xml(fn)" , rc

# fn = r'C:\apps\infa_share\SrcFiles\CDR.xml'
# with open(fn, 'rt') as f:
#     tree = ElementTree.parse(f)
# 
# for node in tree.findall('.//outline'):
#     url = node.attrib.get('xmlUrl')
#     if url:
#         print url

    
# namespaces = { 'ar':'urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2',
#                'ext':'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
#                'cbc':'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
#                'cac':'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
#                'ds' :'http://www.w3.org/2000/09/xmldsig#',
#               }

namespaces = {'ar':'urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2',
              'cac':'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
              'cbc':'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2', }


def  parseCDR():
    rootTag = '{urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2}ApplicationResponse'
    fn = r'C:\apps\infa_share\SrcFiles\CDR.xml'
    tree = ET.ElementTree(file=fn)
    root = tree.getroot()   
    print "root == " , root.tag, " type " , type(root.tag)
    
    if root.tag == rootTag: 
        print "Root is OK"
    else : print "Root is BAD"

    try:
        resp = root.findall('.//cac:Response', namespaces)
        print "//cac:Response Len resp = ", len(resp) 
        for r in resp:
            print r.tag, r.attrib, r.text
    
    except SyntaxError:
        print('Syntax Error  %s %s ' % (sys.exc_type,sys.exc_value))
       
    resp = root.findall('.//cbc:ReferenceID', namespaces)
    print "//cac:ReferenceID Len resp = ", len(resp) 
    print "LIST--",  resp[0].tag, resp[0].attrib, resp[0].text
    for r in resp:
        print r.tag, r.attrib, r.text
       
    resp = root.findall('.//cbc:ResponseCode', namespaces)
    print "//cac:ResponseCode Len resp = ", len(resp) 
    for r in resp:
        print r.tag, r.attrib, r.text
       
    resp = root.findall('.//cbc:Description', namespaces)
    print "//cac:Description Len resp = ", len(resp)
    for r in resp:
        print r.tag, r.attrib, r.text
#--p--------------------------------------------------------------------

#----------------------------------- Class -----------------------------#

def runC(logger):
    fn = r'C:\apps\infa_share\SrcFiles\CDR.xml'
    pxmlCDR = pxml.ProcXMLCDR(logger)
    rc = pxmlCDR.isValidXML(fn)
    if rc == False: return rc
    
    rc = pxmlCDR.parseCDR(fn)
    return rc
    

def main():
    logFile = getLogHandler('Test',logger,True)
    logger.info("Logfile is %s", logFile)
    #rc = parseCDR() 
    rc = runC(logger)
    return rc
 
        

if __name__ == "__main__":
   from apps.setwinenv import setEnvVars  # Remove in UX 
   setEnvVars()
   rc = main()
   print "rc = " , rc
   sys.exit(rc)
   #parseBookXML()