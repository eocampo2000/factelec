'''
Created on Oct 19, 2016

@author: eocampo

Loading config file:C:/apps/config/testbaseapp.cfg

'''

from apps.baseapp import _BaseApp   

class testBaseApp(_BaseApp):  
    exitOnError = True
    
    def __init__(self):
        #_InfaBaseApp.__init__(self)
        super(testBaseApp,self).__init__()
        self.dSrcLoad  = ''
        self.drunID    = []   # Run Id's 
        self.dupdEdID  = []   # Update Editions.
        self.drunIdCnt = {}
        self.landDir   = 'SrcFiles/finance'
        # Allowable commands for this application
        self.cmdStep = { 'A' : self.getLock      ,
                         #'B' : self.isLastWorkDayWarn  ,
                         #'B'  : self._getUpdEdition
                         #'B' : self._testWrkDay  ,  
                         #'B' : self._testWkfDep ,
                         'B'  : self.isWkfPredReady,                         
                       }
       
        # Infa Environmental variables/
        self.infaEnvVar   = {
                'INFA_SHARE'       : 'self.ib.shareDir'   ,  
                'INFA_APP_CFG'     : 'self.ib.cfgDir'     ,   
                'INFA_APP_LCK'     : 'self.ib.lckDir'     ,   
                'CONFIG_FILE'      : 'self.ib.configFile' , 
               }
 
    def _setDataDir(self) : return  0


    def _testWrkDay(self):
        rc = self.isWorkDay()
        print "rc = %s self.isWorkDay()" % rc
        rc = self.isWorkDayWarn()
        print "rc = %s self.isWorkDayWarn()" % rc
        return 0
    
    
    def isWkfPredReady(self):
        #rc = self._chkWkfPred(self.ib.infadlypred,'Mthly') 
        rc = " ----- Dummy Method -----"
        print "rc = %s" % rc
        return 0
    
def main(Args):
        a = testBaseApp()
        rc = a.main(Args)
        return rc 

if __name__ == '__main__':   
    import sys
    from apps.setwinenv import setEnvVars  # Remove in UX 
    setEnvVars()         # Remove in UX 
    rc=  main(sys.argv)