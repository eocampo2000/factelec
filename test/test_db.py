
import logging

from common.loghdl    import getLogHandler
from datastore.dbutil import DBSQLLite, getDSConnStr


#from utils.generator import random_password
#from datastore.dbadmin import DBAdmin
#from datastore.initevaldb import * 

############################ TESTING TO BE REMOVED  
# md = cfg
#def test_spetest(cfg):
#       rs    = cfg.runQry(selSpeTestRegLkupQry,1)  #OT
#       rsLen = len(rs)
#       d = {}
#       if rsLen > 0 :   
#           rl = list(x[0] for x in rs)
#           #mdie.speTestRegLkup.append(rl)
#           print "RL is ",rl
#           for r in rl: d[r] = cfg.runQry(selSpeTestLkupQry,r) 
#           print "dict is %s " % d
#           print "keys are ", d.keys()
#       
#       else   : print("No Special Test Available")     
       
def test_sel_qry(qry,dsn):
    print "QUERY IS %s " % qry
    #log = Logger('C:\ptest\all\env\logs','C:\ptest') 
    log  = logging.getLogger(__name__)
    #cfg = DBOracle('infadev/infadev@infadev',log)
    cs = getDSConnStr('SQLLITE', 'ib.user', 'ib.pwd', dsn)
    cfg = DBSQLLite(cs,log)
    ret = cfg.connToDB()
    print "Connecting to DB : ret = %s " % ret
    rs = cfg.runQry(qry)
    for r in rs:
        print "r = ", r
#    D = {}
    #print "rs = ", rs
#    for (v,k) in rs: D[string.capitalize(k)]=v
#    print D
#    id = list(x[0] for x in rs)
#    print "id = ", id
#    sn = list(x[1] for x in rs)
#    print "sn = ", sn
    cfg.closeDBConn() 



    

def test_updSQLITE_qry():
    qrys =  """
                    UPDATE SERVER_CRED
                    SET STATUS = ?                      
                    WHERE ID   = ?                        
                    AND UNAME  = ?                         
                  """
    qry =   """  UPDATE SERVER_CRED
                          SET STATUS = :STATUS
                          WHERE ID   = :ID
                            AND UNAME = :UNAME """ 
                            
    db = "C:\\users\\eocampo\\workspace\\rydinfap\\src\\databases\\rydinfa.dbf"
    print " db is %s " % db  
    print "QUERY IS %s " % qry
   
    #log = Logger('C:\ptest\all\env\logs','C:\ptest') 
    log  = logging.getLogger(__name__)
    cfg = DBSQLLite(db,log) 
    ret = cfg.connToDB()
    print "Connecting to DB : ret = %s " % ret
    val =  ['5',  '1', 'infa']
    rs = cfg.exeQry(qry,val)
    print "rs = %s " % rs
    cfg.closeDBConn() 


def testMSrep():
    
    qry1 =   """ select  TASK
       ,ID
       ,Server
       ,Job_Name
       ,Severity
       ,Ack
       from tblSQLProcessStatus
       where ACK = 'N' 
       AND Server = 'INF'
       AND TASK like '%FAILED%' """ 
       

    qry =   """ select  TASK
       ,ID
       ,Server
       ,Job_Name
       ,Severity
       ,Ack
       from tblSQLProcessStatus
       where ACK = '%s'
       AND Server = '%s'
       AND TASK like '%%%s%%'
       """ % ('N','M3','FAILED')
      
    # cnxn = pyodbc.connect()                
    db = 'DRIVER={SQL Server};SERVER=maintserver3,1433;DATABASE=RepairHistory;UID=edwuser;;PWD=WiWLiC'
    print " db is %s " % db  
    print "QUERY IS %s " % qry
   
    log = Logger('C:\ptest\all\env\logs','C:\ptest') 
    cfg = ''
 #   cfg = DBPYODBC(db,log) 
    ret = cfg.connToDB()
    print "Connecting to DB : ret = %s " % ret
    val =  ['5',  '1', 'infa']
    rs = cfg.runQry(qry)
    for r in rs:
        print r
    print "rs = %s " % rs
    cfg.closeDBConn() 


def _getNZDS(sql,ib,log):
        r = []   
        print ('qry = %s' % sql)
        cs = getDSConnStr('NZODBC', ib.user, ib.pwd, ib.dbserver, ib.db)
        dbh = NZODBC(cs, log)
        if dbh.connToDB() != 0 : return r
        r = dbh.runQry(sql)
        dbh.closeDBConn()
        return r

# Empty Container   
class InfaBaseAppBean:
    pass

def test_wday(log):
    ib =  InfaBaseAppBean
    ib.user ='edwetl' ;ib.pwd='prodetl1203' ; ib.dbserver='rsnetezzap03' ; ib.db ='edw'
    sql = ds.workDay
    #sql =" SELECT Mon, Yr, Date_Day, Work_Day FROM EDW_WORK_DAY WHERE Date_Day =TO_DATE('19000101','yyyymmdd' )"
    rs = _getNZDS(sql,ib,log)
    if len(rs)    != 1 : return -1
    if len(rs[0]) != 4 : return -4
    return rs[0][03] 
    

    
def main():
    test_sel_qry()
    
   #log.setLogLevel("DEBUG")
   #cfg = DBSQLLite('C:\\mytest\\data\\evalgen.dbf',log)
    #cfg = DBSQLLite("C:\\eclipse\\workspace\\python\\test\\src\\data\\evalgen.dbf",log)
    #ret = cfg.connToDB()  
    #cfg.closeDBConn()



# def test_crypt():
#     enc = encrypt("welcome",'sscinfa2006') 
#     print "enc %s" % enc

#def test_ins():
#    
#    qry = DBMain.insServCredQry
#    qry = """ INSERT INTO SERVER_CRED(
#                           SERV_ID,                       
#                           UNAME,                        
#                           PWD,                           
#                           DESCR           
#                           )
#                    VALUES(
#                      :SERV_ID,
#                      :UNAME,
#                      :PWD,  
#                      :DESCR 
#                 ) """
#    #dic = { 'SERV_ID':1, 'UNAME':'NAME','PWD':'PASWWORD','DESCR':'DESCR'}
#    enc = encrypt("HELLO WORLD",'EOR') 
#    bindVar = ('SERV_ID','UNAME','PWD','DESCR')
#    val     =  (3,'NAME',enc,'DESCR')
#    dic     =dict(zip( bindVar,val))
#    
#    print "START TEST_INS QRy = %s " % qry
#    log = Logger('C:\ptest\all\env\logs','C:\ptest') 
#    cfg = DBOracle('tdbu03/tdbu03@IMMDWD',log)
#    ret = cfg.connToDB()
#    print "Connecting to DB : ret = %s " % ret
#    lst = [1,'USER','PWD','THIS IS THE DESCR',]
#    #ret = cfg.runQry(qry,lst)
#    ret = cfg.exeQry(qry,dic)
#    print " Query returned ", ret 
#    cfg.closeDBConn() 
#  
#
#def test_upd():
#    qry = DBMain.updCredQry % 'SERVER_CRED'
#    print "Qry is %s " % qry
#    bindVar = ('ID','UNAME','PWD','DESCR')
#    val     =  (3,'NAME','PWD','DESCR3')
#    dic     =dict(zip( bindVar,val))
#    log = Logger('C:\ptest\all\env\logs','C:\ptest') 
#    cfg = DBOracle('tdbu03/tdbu03@IMMDWD',log)
#    ret = cfg.connToDB()
#    print "Connecting to DB : ret = %s " % ret
#    ret = cfg.exeQry(qry,dic)
#    print " Query returned ", ret 
#    cfg.closeDBConn() 
#  
#    
#def test_ins_frfile():
#    
#    qry = DBMain.insCredQry % 'SERVER_CRED'
#
#    #dic = { 'SERV_ID':1, 'UNAME':'NAME','PWD':'PASWWORD','DESCR':'DESCR'}
#    enc = encrypt("HELLO WORLD",'EOR') 
#    bindVar = ('SERV_ID','UNAME','PWD','DESCR')
#    val     =  (3,'NAME',enc,'DESCR')
#    dic     =dict(zip( bindVar,val))
#    
#    print "START TEST_INS QRy = %s " % qry
#    log = Logger('C:\ptest\all\env\logs','C:\ptest') 
#    cfg = DBOracle('tdbu03/tdbu03@IMMDWD',log)
#    ret = cfg.connToDB()
#    print "Connecting to DB : ret = %s " % ret
#    lst = [1,'USER','PWD','THIS IS THE DESCR',]
#    #ret = cfg.runQry(qry,lst)
#    ret = cfg.exeQry(qry,dic)
#    print " Query returned ", ret 
#    cfg.closeDBConn() 
#  
#
#
#
#def _printLst(lst):
#    
#    if(len(lst) > 0):
#        for r in lst:
#            print "Records ", r
#            print "r2 = %s, decrypt = %s " % ( r[2],decrypt(r[2],'EOR'))
#
#
#def test_sel():
#    
#    qry =  "SELECT SERV_ID, UNAME, PWD, DESCR FROM  SERVER_CRED"
#    log = Logger('C:\ptest\all\env\logs','C:\ptest') 
#    cfg = DBOracle('tdbu03/tdbu03@IMMDWD',log)
#    ret = cfg.connToDB()
#    print "Connecting to DB : ret = %s " % ret
#    ret = cfg.runQry(qry)
#    print " Query returned ", ret 
#    _printLst(ret)
#    cfg.closeDBConn() 
#
#def test_new(prod_id):
#    qry = """SELECT e.name,
#       e.BU,
#       s.name,
#       s.alias,
#       s.os,
#       s.ver,
#       s.patch, 
#       e.license ,
#       e.ver ,
#       e.patch ,
#       e.build ,
#       e.inst_path
#FROM  environment e, server s
#WHERE e.prod_id = %s
#AND      e.serv_id = s.id
#order by BU, e.name"""  
#    log = Logger('C:\ptest\all\env\logs','C:\ptest') 
#    cfg = DBSQLLite('C:\infaapp\soft_inv.sqlite',log)
#    ret = cfg.connToDB()
#    print "Connecting to DB : ret = %s " % ret
#    ret = cfg.runQry(qry % prod_id)
#    print " Query returned ", ret 
#    cfg.closeDBConn() 
#
#    return 0
#
#def get_pwd():
#    qry = 'select NAME,OS  from server'
#    pwd_qry(qry)
#
#
#def uptime():
#    qry = DBAdmin.selDomQry
#    log = Logger('C:\ptest\all\env\logs','C:\ptest') 
#    cfg = DBOracle('tdbu03/tdbu03@IMMDWD',log)
#    ret = cfg.connToDB()
#    print "Connecting to DB : ret = %s " % ret
#    ret = cfg.runQry(qry)
#    print " Query returned ", ret 
#    cfg.closeDBConn() 

if __name__ == '__main__':
    #testMSrep() 
    #rc = main()
    rc = 0
    #test_crypt()
    print "RC = ", rc
    #test_new(3)
    #test_qry(3)
    #test_ins()
    #test_upd()
    #test_sel() # selSubjArea selInfSchedQry)
    #test_sel_qry(DBInfaRepo.selRepWfl)
    #test_updSQLITE_qry()
    #get_pwd()
    #uptime()

