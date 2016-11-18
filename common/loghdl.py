'''
Created on Oct 17, 2016

@author: tester
'''

import os 
import logging

# ln  log name
# st boolean to instantiate a sysout stream.
# logger logging instance 
# returns the logFile path/name

def getLogHandler(ln,logger,sh=False):
    
    logName   = os.environ['LOGNAME'] if os.environ.has_key('LOGNAME') else ln
    infaLogs  = os.environ['LOG_DIR'] if os.environ.has_key('LOG_DIR') else os.path.dirname(__file__)
    
    if os.environ.has_key('LOG_LEVEL'): ll = eval('logging.%s' % os.environ['LOG_LEVEL'])
    else                              : ll = logging.INFO
    
    logger.setLevel(ll)
    formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(module)s.%(funcName)s  -- %(message)s', 
                                   "%d.%m.%Y_%H:%M:%S")
    
    # Log Handler
    logFile = '%s/%s.log' % (infaLogs,logName)
    fhdl = logging.FileHandler(logFile)
    fhdl.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fhdl)
    
    if sh :
        shdl = logging.StreamHandler()
        shdl.setFormatter(formatter)
        logger.addHandler(shdl) 
    
    return logFile
    
