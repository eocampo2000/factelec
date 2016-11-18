'''
Created on Oct 17, 2016

@author: tester

 XML files parser. Please specify the main LAYOUT.
 TODO encapsulate it into a class

'''

__version__ = '20161017'

import sys
                  
import utils.xmlutils        as xutil
import xml.etree.ElementTree as ET

class ProcXMLBean:
    pass

class _ProcXML(object):
    
    def __init__(self,log):
        self.appName = self.__class__.__name__.lower()
        self.log  = log          # namespace to parse XML (compound)
        self.tree = None
        self.root = None
  
    # Check XML validity.
    def isValidXML(self,fn):
        rc = xutil.chk_valid_xml(fn)
        self.log.debug("fn = %s  rc = %s msg = %s" % (fn,rc[0],rc[1]))
        if rc[0] is False:
            self.log.error("fn = ",fn,"rc = ", rc)
            return False
        return True
    
    # Method that can process file 
    def _getFileTree(self,fn):
        self.tree = ET.ElementTree(file=fn)
    
    # Method that can process a stream
    def _getStrTree(self,st):
        self.tree = ET.ElementTree()
            
    def _getRoot(self):
        self.root = self.tree.getroot() 
            
    # Root tag for a particular XML
    def _isRootTag(self,rt):
        self.log.debug('root.tag %s === rt %s' % (self.root.tag,rt))
        if self.root.tag == rt: return True
        else :
            self.log.error('root.tag %s <> to rt %s' % (self.root.tag,rt))      
            return False

    # Needs to set tree and root on child class. 
    def parseXML(self):
        return ()

    # lkps : Element to look for (wild)
    # ns   : namespace
    def findAllElem(self,lkps,ns): 
        rc = None
        self.log.debug("lkps = %s " % (lkps))
        try:
            resp = self.root.findall(lkps,ns)
            if len(resp) == 1:
                rc = resp[0].text
                self.log.debug("tag = %s  attrib = %s text = %s" % (resp[0].tag, resp[0].attrib, resp[0].text)) 
            else:
                self.log.error('No of Element(s) found %s = %d  Need to be 1' % (lkps,len(resp)))
                
        except SyntaxError:
            self.log.error('Syntax Error  %s %s ' % (sys.exc_type,sys.exc_value))
        
        finally:
            return rc
    
class ProcXMLCDR(_ProcXML):
     
    def __init__(self,log):
        super(ProcXMLCDR,self).__init__(log)
                    
    # returns a tuple 
    def parseCDR(self,fn):
        rootTag    = '{urn:oasis:names:specification:ubl:schema:xsd:ApplicationResponse-2}ApplicationResponse'
        namespaces = {'cac':'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                      'cbc':'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2', 
                     }
        
        self._getFileTree(fn)
        self._getRoot() 
        #self.log.debug()
        if not self._isRootTag(rootTag) : return None

        rfId  = self.findAllElem('.//cbc:ReferenceID',  namespaces)
        rCode = self.findAllElem('.//cbc:ResponseCode', namespaces) 
        desc  = self.findAllElem('.//cbc:Description',  namespaces)

        return (rfId,rCode,desc) 

       
if __name__ == "__main__" : 
    fn = r'C:\apps\infa_share\SrcFiles\CDR.xml'
#     from setwinenv import setEnvVars
#     os.environ['LOG_LEVEL'] = 'DEBUG'
#     setEnvVars()
#     bd = r'C:/apps'
#     a = _InfaBaseApp(bd)
#     rc = a.main(sys.argv)