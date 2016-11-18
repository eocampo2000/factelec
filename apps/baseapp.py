'''
Created on Oct 19, 2016

@author: tester
'''
__version__ = '20161104'

import os      #, os.path
import sys
import socket
import time
import logging

import common.simpmail  as sm
import common.lockfile  as lck
import utils.fileutils  as fu
import utils.strutils   as su

from common.loghdl     import getLogHandler

RET_WARN = 101
RUN_DATE = su.getTodayDtStr(fmt='%Y%m%d')

# Empty Container   
class BaseAppBean:
    pass

class _BaseApp(object):
    hostname = socket.gethostname()
    
    def __init__(self):
        self.appName      = self.__class__.__name__.lower()
            
        self.log          = logging.getLogger(self.appName)     
        self.suf          = 'cfg'
        self.ib           = BaseAppBean
#       self.cmdStep    = {}                         # Empty for base class
        self.infaEnvVar   = {}                       # Empty for base class
        self.pLock        = None
        self.ib.fu        = 'eocampo@ryder.com'
        self.ib.touser    = None
        self.ib.pager     = None
        self.ib.pgOnErr   = 'False'                  # Need to be string by contract 
        self.ib.mailOnErr = 'False'                  # Need to be string by contract

              
        self.runSeq = None 
        


    # Create Lock File for processes that could not have more than one instances running concurrently.   
    # Command Step.
    def getLock(self):
        self.lockFn = '%s/%s.lck' % (self.ib.lckDir, self.appName) 
        self.pLock = lck.LockFile(self.lockFn, self.log)
        rc = self.pLock.getLock()
        self.log.debug('Creating Lock: %s\t:rc = %s ' % (self.lockFn, rc))
        if rc is True : return 0
        else          : return 1
    
    #---------------------- File Operations (high level)  --------------------------------------
    
    # Finds a list of file in dir.
    # values need to be in config file.
    # return a list of files to process. 
    # Use only for data files. For Trigger File(s) use chkTrigFiles
    # This method  will find  one or more files at a given time based on filename wildcards 
    # e.g.  Ap_scusrctl_*[0-9]_*[1-9].txt -> Ap_scusrctl_20120812_1.txt,Ap_scusrctl_20120812_2.txt, etc
    # This method will look for any file name in a pattern ( fu.getFileName ) and will capture 0 or more to process.
    def procIncFiles(self, dir, fn):
        filesInc = [] # Incoming file
        fl = fu.getFileName(dir, fn)        
        self.log.debug('dir=%s fn=%s File(s) found %s' % (dir,fn, ''.join(fl)))
        
        for f in fl: 
            filesInc.append(f) 
            self.log.info('File %s' , f)         
        return filesInc
    
    #---------------------- App Config File / Environment variables settings  --------------------------------------
    # Process App config file.
    # by convention file will be className with .cfg
    def _getConfigFile(self):
        #fn = '%s/%s.%s' % (self.ib.cfgDir, self.appName,self.suf)
        fn = '%s' % (self.ib.configFile)
        rc = fu.loadConfigFile(fn, self.ib, self.log)
        if rc == 0 : self.log.info('Loading config file:%s' % fn)
        else       : self.log.critical("Error Loading Config File %s" % fn)
     
        return rc 
    
    #  os.env ['INFA_SHARE'     ] --> self.ib.shareDir  == /apps/infa_shared/ruc
    #  os.env ['INFA_SCRIPT_DIR'] --> self.ib.scriptDir == /apps/script/ruc
    # 
    #  landDir  = self.ib.shareDir/srcfile    Files to process
    #  archDir  = self.ib.shareDir/archive    All archive
    #  workDir  = self.ib.shareDir/input      Trim files
    #  badDir   = self.ib.shareDir/bad        Bad files
    #  cdrOutDir= self.ib.shareDir/cdrout     CDR files for ERP consumption.
    #  procbill = self.ib.scriptDir           Provider returned ebill files (pdf/xml).
    #  proccdr  = self.ib.scriptDir           Provider returned CDR's
    
    def _setDataDir(self):
        self.ib.landDir   = '%s/%s' % (self.ib.shareDir, self.ib.landDirName)   # TXT files are placed.
        self.ib.archDir   = '%s/%s' % (self.ib.shareDir, self.ib.archDirName)   # Archive all files.
        self.ib.workDir   = '%s/%s' % (self.ib.shareDir, self.ib.workDirName)   # Working dir
        self.ib.badDir    = '%s/%s' % (self.ib.shareDir, self.ib.badDirName)    # Error Files
        self.ib.cdrOutDir = '%s/%s' % (self.ib.shareDir, self.ib.cdrOutDirName) # Landing for output Filr for ERP consumption.  
        self.ib.ebillDir  = '%s/%s' % (self.ib.shareDir, self.ib.ebillDirName)  # ebill palce for consulting.
        # Provider's directory
        self.ib.billDir   = '%s/%s' % (self.ib.provData, self.ib.billDirName)                           # processed ebill
        self.ib.cdrDir    = '%s/%s' % (self.ib.provData, self.ib.cdrDirName )                           # processed CDR
                         # processed CDR
        return 0
        
    def printEnvBean(self):
        ibr = vars(self.ib)
        for k, v in ibr.items():
            self.log.debug("k = %s\tv = %s" % (k, v))
            
    # Environment Variables that need to be set. Key is the ENV and ELE the name of var.
    # Below are global variables. Env variables should be set based on env settings.    
    def _getEnvVars(self):
        ret = 0   
        for ev, v in  self.infaEnvVar.items():
            self.log.debug("ev =%s v = %s" % (ev, v))
             
        try:     
            for ev, v in  self.infaEnvVar.items():
                x = os.environ[ev].strip()
                exec  "%s='%s'" % (v, x) 
                self.log.debug("%s='%s'" % (v, x))  
             
        except:
                ret = 2
                self.log.error("ENV var %s not set -- %s %s\n" % (ev,sys.exc_type, sys.exc_info()[1]))
                self.log.error("Need to set all env vars:\n %s" % self.infaEnvVar.keys())
     
        finally : return ret

    def _execSteps(self, runStep):
        
        self.log.debug('runStep = %s' % runStep)
        for s in runStep:
            if (not self.cmdStep.has_key(s)):
                self.log.error('Invalid step %s' % s)
                return 1
            
            rv = 1
            try:
                rv = self.cmdStep[s]()
                if rv != 0 and self.exitOnError : 
                    self.log.error('[%s]:%s()\trc\t= %d' % (s, self.cmdStep[s].__name__, rv))
                    return rv
                
                #self.log.debug('[%s]:%s()\trc\t= %s' % (s,self.cmdStep[s].__name__,rv))
                self.log.info('[%s]:%s()\trc\t= %d' % (s, self.cmdStep[s].__name__, rv))
            
            except AttributeError:
                self.log.error('[%s]:%s()' % (s, self.cmdStep[s].__name__))
                self.log.error(' %s ' % (sys.exc_info()[1]))
                if (self.exitOnError) : return rv
                
            except SyntaxError:
                self.log.error('[%s]:%s()' % (s, self.cmdStep[s].__name__))
                self.log.error(' %s ' % (sys.exc_info()[1]))
                if (self.exitOnError) : return rv
            
        return rv

    #Set Incoming arguments 
    def setArgs(self,Argv):
        
        if len(Argv) != 2 :
            self.log.critical("USAGE : <%s> fx [runSeq] Incorrect Number of arguments (%d)" % (Argv[0], len(Argv)))
            return 1  
        self.runSeq = Argv[1] 
        
        return 0
    # Argv is a list of runnable commands, defined per class basis
    # 'C:\\Users\\eocampo\\workspace\\rydinfap\\src\\apps\\infbaseapp.py'    
    def main(self, Argv):
        rc = 1  # Failed
        logFile = getLogHandler(self.appName, self.log,True)
        self.log.info('logFile= %s' % logFile)
        
        # should NEVER get this programmatic error !!!!
        if self.cmdStep is None or len(self.cmdStep) == 0 :
            self.log.critical("Program Error:self.cmdStep is ", self.cmdStep)
            return 1
        
        rc = self.setArgs(Argv)
        if rc != 0 : return rc
        
        rc = self._getEnvVars()
        if rc != 0 :return rc
        
        rc = self._getConfigFile()
        if rc != 0 :return rc
        
        self._setDataDir()
           
        if self.runSeq is not None and len(self.runSeq) > 0 : 
            rc = self._execSteps(self.runSeq)
            if rc == 0 : self.log.info ('Completed running execSteps rc = %s' % rc)
            else       : self.log.error('execSteps rc = %s' % rc)
        
        
        if rc != RET_WARN:
            text = 'Please see logFile %s' % logFile
            subj = "SUCCESS running %s on %s " % (self.appName, self.hostname) if rc == 0 else "ERROR running %s on %s" % (self.appName, self.hostname)
            #r, msg = sm.sendNotif(rc, self.log, subj, text, [logFile, ])
            r= -1 ; msg = "Need to enable notification"
            self.log.info('Sending Notification\t%s rc = %s' % (msg, r))    
        
        else:
            self.log.info('Notification Overrided. Not sending message (RET_WARN) rc = %s ' % rc)
            
        self.printEnvBean()
        return rc
    
    def __del___(self):
        self.log.debug('Base class cleaning')
# Use this for testing in windows env only. Should not use in UX
    
if __name__ == '__main__':
    from setwinenv import setEnvVars
    os.environ['LOG_LEVEL'] = 'DEBUG'
    setEnvVars()
    bd = r'C:/apps'
    a = _BaseApp(bd)
    rc = a.main(sys.argv)
    #rc = a.main(['cfg','ABCD'])
    #rc = a.main(['cfg', 'ABCD'])