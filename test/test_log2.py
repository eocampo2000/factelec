'''
Created on Oct 17, 2016

@author: tester
'''
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create file handler which logs even debug messages
fhdl = logging.FileHandler('spam.log')
fhdl.setLevel(logging.DEBUG)
fhdl.setFormatter(formatter)
logger.addHandler(fhdl)
# create console handler with a higher log level
chdl = logging.StreamHandler()
chdl.setLevel(logging.DEBUG)
chdl.setFormatter(formatter)
logger.addHandler(chdl)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')