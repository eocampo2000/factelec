'''
Created on Oct 17, 2016

@author: tester
'''
import logging

from common.loghdl     import getLogHandler
# create logger


import sys, os

# class Formatter(logging.Formatter):
# 
#     def formatTime(self, record, datefmt=None):
#         dt = self.converter(record.created)
#         t = dt.strftime(self.default_time_format)
#         s = self.default_msec_format % (t, record.msecs)
#         return s

logger  = logging.getLogger(__name__)

def func1():
    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    return 10

def main():
    logFile = getLogHandler('Test',logger,True)
    logger.info("Logfile is %s", logFile)
   
if __name__ == '__main__': 
    from apps.setwinenv import setEnvVars  # Remove in UX 
    setEnvVars()        
    main()
    rc= func1()
    sys.exit(rc)