'''
Created on Oct 17, 2016

@author: tester

ScriptDir/ArchivoBatch.exe self.ib.landDir/F-100-00396465.TXT"

'''

__version__ = '20161104'

import sys

import proc.process     as p
import procdata.procxml as pxml
import utils.fileutils  as fu
import utils.strutils   as su

from baseapp import _BaseApp   

class ProcElectBill(_BaseApp):  
    exitOnError = True
    #exitOnError = False
    
    def __init__(self):
        #_InfaBaseApp.__init__(self)
        super(ProcElectBill,self).__init__()

        self.landDir   = 'SrcFiles'
        self.ebFilestoProc  = []                           # Ebill Text Files to Process. Send to provider.
        self.ebFilesRecv    = []                           # Ebill Files Received from provider (xml and pdf.
        self.cdrFilestoGet  = []                           # CDR Files to get from provider based on sent docs.
        self.cdrZipFiles    = []                           # CDR Zip Files to Process, Incoming from Sunat.
        self.cdrFilestoProc = []                           # CDR Uncompress Files to Process, Incoming from Sunat.
        self.ts             =  su.getTimeSTamp()
        
        # Allowable commands for this application
        self.cmdStep = { 'A' : self.getLock          ,
                         'B' : self.getBillsToProc   ,
                         'C' : self.trimBillBlank    , 
                         'D' : self.procBillFiles    ,
                         'E' : self.mvBillFiles      ,
                         'F' : self.getCDRToProc     ,
                         'G' : self.trimCDRBlank     ,
                         'H' : self.getCDRfromVendor ,
                         'I' : self.getZipCDRToProc  ,
                         'J' : self.unzipCDRFiles    ,
                         'K' : self.getXMLtoProcess  ,
                         'L' : self.procXMLFiles     ,
                       }

 
        # Infa Environmental variables/
        self.infaEnvVar   = {
                'CFG_FILE'        : 'self.ib.configFile' ,  
                'INFA_SHARE'      : 'self.ib.shareDir'   ,  
                'INFA_SCRIPT'     : 'self.ib.scriptDir'  ,
                'INFA_PROV_DATA'  : 'self.ib.provData'   ,
                'INFA_APP_CFG'    : 'self.ib.cfgDir'     ,   
                'INFA_APP_LCK'    : 'self.ib.lckDir'     ,   
               }
 
    def _trimLeftBlank(self, fileToProc):
        rc = 0; r = 1
        for ef in fileToProc:
            r = fu.trimRBlankFile(ef)
            self.log.debug('fu.trimRBlankFile r = %d fn = %s' % (r,ef))
            if r != 0:
                self.log.error('fu.trimRBlankFile r = %d fn = %s' % (r,ef))
                rc+=1
        return rc
                
    # Files Start Processing Files.
    # DFacture provider : 
    # moving files to bad or archive dir based on rc.
    def _procFiles(self,filestoProc):
        rc = 0; r = 1
        
        for ef in filestoProc:
            cmd = '%s/ArchivoBatch.exe %s' % (self.ib.scriptDir,ef)
            r,rmsg = p.runSync(cmd, self.log)
            ftn = fu.getFileBaseName(ef)
            self.log.debug('r = %s cmd = %s  ftn = %s' % (r,cmd,ftn))
            if r != 0 and r != 95:
                tgt = '%s/%s.%s' % (self.ib.badDir,ftn,self.ts) 
                self.log.error ('r = %s cmd = %s rmsg=%s' % (r,cmd,rmsg))
                rc+=r
            else :
                self.log.info ('r = %s cmd = %s rmsg=%s' % (r,cmd,rmsg))
                tgt = '%s/%s.%s' % (self.ib.archDir,ftn,self.ts)  
            
            r = fu.moveFile(ef, tgt)
            if r == 0 : self.log.info( 'mv %s to %s' % (ef,tgt))
            else      : self.log.error('mv %s to %s r = %s ' % (ef,tgt,r))
        return rc
    
    # Ebill operations
    # Get a list of files to process.
    # self.ib.erpfn         Source Bill Files to Process.
    # TXT Files that will be submitted to provider (DFacture)
    def getBillsToProc(self):
        rc = 0
        self.ebFilestoProc = self.procIncFiles(self.ib.landDir,self.ib.erpFileName)
        flen = len(self.ebFilestoProc)
        self.log.debug('%d Files to process %s  %s'  % (flen,self.ib.erpFileName,''.join(self.ebFilestoProc)))
        if flen < 1 :
            self.log.error('%d Files to process %s on dir %s' % (flen,self.ib.erpFileName,self.ib.landDir))
            rc = 1
        return rc
    
    def trimBillBlank(self) : return self._trimLeftBlank(self.ebFilestoProc)
    
    # Files Start Processing ebill Files.
    def procBillFiles(self): return self._procFiles(self.ebFilestoProc)
    
    # Move bills downloaded (pdf/xml) from provider (Dfacture) to data dir. 
    def mvBillFiles(self):
        rc = 0; r = 1;
        bf = self.procIncFiles(self.ib.billDir,self.ib.billFileName)
        
        flen = len(bf)
        self.log.debug(' %d Files to process %s  %s'  % (flen,self.ib.billFileName,''.join(bf)))
        for fsrc in bf:
            fn   = fu.getFileBaseName(fsrc)
            ftgt = '%s/%s' % (self.ib.ebillDir,fn)
            r = fu.moveFile(fsrc,ftgt)
            self.log.debug('r = %d mv %s %s' % (r,fsrc,ftgt))
            if r != 0:
                self.log.error ('r = %d mv %s %s' % (r,fsrc,ftgt))
                rc+=r
                     
        return rc

    #CDR Operations
    # Get a list of files to process.
    # self.ib.erpfn         Source Bill Files to Process.
    # self.ebFilestoProc    Full path for the files to process.
    # Will send request to Dfacture to download files.
    def getCDRToProc(self):
        rc = 0
        self.cdrFilestoGet = self.procIncFiles(self.ib.landDir,self.ib.cdrFileName)
        flen = len(self.cdrFilestoGet)
        self.log.debug('%d Files to process %s  %s'  % (flen,self.ib.cdrFileName,''.join(self.cdrFilestoGet)))
        if flen < 1 :
            self.log.error('%d Files to process %s on dir %s' % (flen,self.ib.cdrFileName,self.ib.landDir))
            rc = 1
        return rc
    
    def trimCDRBlank(self) : return self._trimLeftBlank(self.cdrFilestoGet)
    
    # Get CDR Files from vendor
    def getCDRfromVendor(self): return self._procFiles(self.cdrFilestoGet)
    
    
    # Zip CDR files downloaded to our server for processing.
    # List of received CDR Files to process. 
    def getZipCDRToProc(self):    
        rc = 0
        self.cdrZipFiles = self.procIncFiles(self.ib.cdrDir,self.ib.cdrZipArchName)
        flen = len(self.cdrZipFiles)
        self.log.debug('%d Files to process %s  %s on dir %s' % (flen,self.ib.cdrZipArchName,''.join(self.cdrZipFiles),self.ib.cdrDir))
        if flen < 1 :
            self.log.error('%d Files to process %s on dir %s' % (flen,self.ib.cdrZipArchName,self.ib.cdrDir))
            rc = 1
        return rc
    
    #Uncompress Incoming CDR files
    # fileutils.uncompressFile  -- ZipFile (fzp) = C:/fe/script/20349663547/20349663547\01-F100-00398201_cdr.zip  TgtDir = C:/fe/data/20349663547/input
    # procelecbill.unzipCDRFiles-- Uncompressed    C:/fe/script/20349663547/20349663547\01-F100-00398201_cdr.zip  to       C:/fe/data/20349663547/input
    def unzipCDRFiles(self): 
        rc = 0; r = 1
        path = '%s/%s' % (self.ib.shareDir,self.ib.workDirName)
        
        for fzp in self.cdrZipFiles:
            r = fu.uncompressFile(fzp, path ,self.log)
            if r != 0 :
                self.log.error('Error unziping %s ' % fzp)
                rc+=r
             
            else : 
                self.log.info('Uncompressed %s to %s' % (fzp,path))
                fn  = fu.getFileBaseName(fzp)
                tgt = '%s/%s%s' % (self.ib.archDir,fn,self.ts) 
                r   = fu.moveFile(fzp, tgt)
                if r == 0 : self.log.info( 'mv %s to %s' % (fzp,tgt))
                else      : 
                    self.log.error('mv %s to %s r = %s ' % (fzp,tgt,r))    
                    rc+=r      
        
        return rc
    
    # Files downloaded to our server for processing
    def getXMLtoProcess(self):   
        rc = 0
        self.cdrFilestoProc = self.procIncFiles(self.ib.workDir,self.ib.xmlFileName)
        flen = len(self.cdrFilestoProc)
        self.log.debug('%d Files to process %s  %s'  % (flen,self.ib.xmlFileName,''.join(self.cdrFilestoProc)))
        if flen < 1 :
            self.log.error('%d Files to process %s on dir %s' % (flen,self.ib.xmlFileName,self.ib.workDir))
            rc = 1
        return rc
         
    # Processing CDR/XML  Files...
    # x[0] ReferenceID  = F100-00398584
    # x[1] ResponseCode = 0
    # x[2] Description  = La Factura numero F100-00398584, ha sido aceptada
    
    def procXMLFiles(self): 
        rc = 0; r = False ; x = [] ; cdrRes = [] # List that contains all the responses.
        if len(self.cdrFilestoProc) < 1 :
            self.log.error('No incoming CDR files to process : cdrFilestoProc')
            return 1
        
        pxmlCDR = pxml.ProcXMLCDR(self.log)
        self.log.debug("Files to process %s"  % ''.join(self.cdrFilestoProc))
        for fn in self.cdrFilestoProc:
            self.log.debug("processing %s" % fn)
            r = pxmlCDR.isValidXML(fn)
            if r == False: rc+=1
            else:
                x = pxmlCDR.parseCDR(fn)
                ftn = fu.getFileBaseName(fn)
                if x is None or len(x) != 3:
                    self.log.error('Error Parsing %s ' % fn)
                    tgt = '%s/%s.%s' % (self.ib.badDir,ftn,self.ts) 
                    
                   
                else:
                    self.log.debug('fn=%s rfId=%s rCode=%s desc=%s' % (fn,x[0],x[1],x[2]))
                    r = su.toInt(x[1])
                    if r != 0 :
                        self.log.error('fn=%s rfId=%s rCode=%s desc=%s' % (fn,x[0],x[1],x[2]))
                        tgt = '%s/%s.%s' % (self.ib.badDir,ftn,self.ts) 
                        rc+=1
                    
                    else :
                        cdrRes.append('%s %s %s\n' % (x[0],self.ib.FS,x[1]))  
                        tgt = '%s/%s.%s' % (self.ib.archDir,ftn,self.ts)  
                        
                # Move files
                r  = fu.moveFile(fn, tgt)
                if r == 0 : self.log.info( 'mv %s to %s' % (fn,tgt))
                else      : self.log.error('mv %s to %s r = %s ' % (fn,tgt,r))  
         
        self.log.debug("cdrRes No of elements %d " % len(cdrRes))  
        
        if len(cdrRes) < 1:
            self.lo.error('cdrRes Did not find any valid element !')
            return 2

        fn = '%s/CDR_%s.txt' % (self.ib.cdrOutDir, self.ts)
        r = fu.createFile(fn,cdrRes)
        if r == 0: self.log.info('Created file %s with CDR responses' % fn)
        else     : 
            self.log.error('Could not create file %s with CDR responses' % fn)     
            rc=1
                 
        return rc
                    
def main(Args):
        a = ProcElectBill()
        rc = a.main(Args)
        return rc 

if __name__ == '__main__':   
#     import sys
#     from apps.setwinenv import setEnvVars  # Remove in UX 
#     setEnvVars()         # Remove in UX 
    rc=  main(sys.argv)
    sys.exit(rc)
