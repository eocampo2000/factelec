#------------------------------------------------------------
# Version 0.1 20101105
#
# dbutils.py
#
# Creation Date:     2012/01/03
# Modification Date:
# Description: This module contains all DB database related classes/methods.

#-------------------------------------------------------------
__version__ = '20161119'

import sys
import string as ST


#===============================================================================
# ConnectString
#===============================================================================
# t DS type currently 'oracle', 'SQLLite'. Mandatory by Contract (not nullor blank)
# u username
# p password
# dsn data source name or server name
# db database
# Entries defined on the odbcinst.ini for UX
#[ODBC Drivers]
#NetezzaSQL = Installed
#[NetezzaSQL]
#Driver           = /infa/Informatica/ODBC6.1/Netezza/lib64/libnzodbc.so
#Setup            = /infa/Informatica/ODBC6.1/Netezza/lib64/libnzodbc.so
#
#SQL Server = Installed
#[SQL Server]
#Driver=/infa/Informatica/ODBC6.1/lib/DWsqls25.so

def getDSConnStr(t,u,p,dsn,db=None):
    
    if  ST.upper(t) == 'SQLLITE' and dsn is not None                : 
        return _getSQLITEStr(dsn)
#     if  ST.upper(t) == 'ORADB'  and u is not None and p is not None: 
#         return _getOracleOCIStr(u,p,dsn)
#     if  ST.upper(t) == 'NZODBC'  and u is not None and p is not None and dsn and db is not None: 
#         return _getNetODBCStr(u,p,dsn,db)
#     if  ST.upper(t) == 'MSSQLODBC'  and u is not None and p is not None and dsn and db is not None: 
#         return _getMSSQLODBCStr(u,p,dsn,db)   
#     if  ST.upper(t) == 'MSSQLNAT'  and u is not None and p is not None and dsn and db is not None: 
#         return _getMSSQLNatStr(u,p,dsn,db)   
    return None

def _getSQLITEStr(dsn)           : return dsn
# def _getOracleOCIStr(u,p,dsn)    : return '%s/%s@%s' % (u,p,dsn)
# def _getNetODBCStr(u,p,srv,db)   : return "DRIVER={NetezzaSQL};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (srv,db,u,p)
# def _getMSSQLODBCStr(u,p,srv,db) : return "DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (srv,db,u,p)
# def _getMSSQLNatStr(u,p,srv,db)  : return "DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (srv,db,u,p)

#===============================================================================
# Enumeration
#===============================================================================
# This class does not trim for blanks (performance) , make sure the names parameter
# is properly trim !
class Enumerate(object):
    def __init__(self, names, sep):
        for number, name in enumerate(names.split(sep)):
            setattr(self, name, number)

def getIDX(idxStr, sep = ','):
    en = Enumerate(idxStr,sep)
    return (en)

#===============================================================================
# SQLLITE Driver 
#===============================================================================
import sqlite3  
class DBSQLLite(object): 

    QRY = 0     # Query objects
    IDX = 1     # Column idx objects
   
    def __init__(self, cs, logger,encode=str):
        self.connStr  = cs
        self.dbConn   = None
        self.logger   = logger
        self.encode   = encode
        self.sep      = ','
    
    def connToDB(self):
        retVal = 0
        try:
            #self.dbConn = sqlite3.connect(self.connStr,isolation_level=None)
            self.dbConn = sqlite3.connect(self.connStr)
            self.dbConn.text_factory = self.encode
            self.logger.debug("Connecting to %s" % self.connStr)
            
        except:

            self.logger.error("==EXCEP Connect String << %s >>"   % self.connStr )
            self.logger.error("==EXCEP %s %s "  % (sys.exc_type, sys.exc_info()[1]))
            retVal = -101
        
        finally:  return retVal

    # Use this query for select options
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine
#    def runQry(self,qryStr,s=[]):
#
#        if(type(s) != list) : 
#            s = [s,]
#
#        resLst =[]
#        if (self.dbConn == None):
#            self.logger.error("self.dbConn has not been set")
#            return resLst
#       
#        try:   
#            cursor = self.dbConn.cursor()      
#            res = cursor.execute(qryStr,s)
#            for row in res:
#                   resLst.append(row)
#        except sqlite3.OperationalError, msg:
#        #except:
#            print("==>> EO OPEr EXCEP IN RUNQRY %s " % msg)
#            raise sqlite3.OperationalError, msg
#            
#        
#        finally:return resLst
#        

    # Use this query for select options
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine
    def runQry(self,qryStr,s=[]):
        print "qryStr + %s " % qryStr  
        if(type(s) != list) : 
            s = [s,]

        resLst = None
        if (self.dbConn == None):
            self.logger.error("self.dbConn has not been set")
            return resLst
       
        try:   
            tmp = []
            cursor = self.dbConn.cursor()      
            res = cursor.execute(qryStr,s)
            for row in res:
                tmp.append(row)
                          
        except sqlite3.OperationalError, msg:
            self.logger.error("==>> sqlite3.OperationalError : %s " % msg)
            #raise sqlite3.OperationalError, msg
                
        else    : resLst = tmp
        finally : return resLst

#   DEBUG ONLY            
#    def runQry(self,qryStr,s=[]):
#
#        if(type(s) != list) : 
#            s = [s,]
#
#        resLst =[]
#        if (self.dbConn == None):
#            self.logger.error("self.dbConn has not been set")
#            return resLst
#        cursor = self.dbConn.cursor()      
#        res = cursor.execute(qryStr,s)
#        for row in res:
#            resLst.append(row)
#            
#        return resLst


    # Use this method for DML insert, update, delete
    # qryStr: SQL command to execute
    # s     : list of BINDING VARIABLES, that need to be passed to the SQL Engine

    def exeQry(self,qryStr,s = []) :
        #print "qryStr + %s " % qryStr                #EO Remove after test
        rc = -1

        if(type(s) != list or type(s) != tuple) : 
            s = list(s)

        if (self.dbConn == None):
            self.logger.error("self.dbConn has not been set")
            return -102
        
        try:    
            cursor = self.dbConn.cursor()                
            cursor.execute(qryStr,s)
            rc = cursor.rowcount
            self.dbConn.commit()
            self.logger.debug("rc is %s " % rc) 
            return rc
        
        # IntegrityError columns fac_name, addr1 are not unique
        # ProgrammingError: Incorrect number of bindings supplied
        except sqlite3.OperationalError, msg:  
            #self.dbConn.rollback()
            #raise sqlite3.OperationalError, msg
            self.logger.error("==>> sqlite3.OperationalError : %s " % msg)
            
        except sqlite3.IntegrityError, msg:  
            #self.dbConn.rollback()              # EO might help in DB lock issue.
            #raise sqlite3.IntegrityError, msg
            self.logger.error("==>> sqlite3.IntegrityError : %s " % msg)
                   
        except:
            self.logger.error("Gral Excp  %s %s\n" % (sys.exc_type,sys.exc_info()[1]))
                  
        finally:  
            self.dbConn.rollback()         # WIll get in here only 
            return rc
                 
##   DEBUG ONLY     
#    def exeQry(self,qryStr,s = []) :
#            print "\n\n==============Qry = %s " % qryStr
#            rc = -1
#            cursor = self.dbConn.cursor()                
#            cursor.execute(qryStr,s)
#            rc = cursor.rowcount
#            self.dbConn.commit()
#            self.logger.debug("exeQry: rc is %s " % rc) 
#            return rc

    def getIDX(self,idxStr):
        self.logger.debug("%s " % idxStr)
        en = Enumerate(idxStr, self.sep)
        return (en)
    
    def closeDBConn(self):
        if(self.dbConn != None):
            self.dbConn.commit()
            self.logger.debug( "Closing Conn %s " % self.connStr)
            self.dbConn.close()

