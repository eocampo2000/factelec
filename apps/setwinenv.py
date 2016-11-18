'''
Created on Oct 17, 2016

@author: tester

ADD IN MAIN :     
if __name__ == '__main__':   
    from setwinenv import setEnvVars  # Remove in UX 
    setEnvVars()        
    rc=  main(sys.argv)
'''

#mg.pmcmd      = r'C:\Informatica\9.1.0\clients\PowerCenterClient\CommandLineUtilities\PC\server\bin\pmcmd.exe'
#mg.pmrep      = r'C:\Informatica\9.1.0\clients\PowerCenterClient\CommandLineUtilities\PC\server\bin\pmrep.exe'
#mg.infacmd    = r'C:\Informatica\9.1.0\clients\PowerCenterClient\CommandLineUtilities\PC\server\bin\infacmd.bat'
#mg.infasrv    = r'C:\Informatica\9.1.0\clients\PowerCenterClient\CommandLineUtilities\PC\server\text_cmd'
### DEV 
#ib.rep_dbpwd  = 'infadev'


#ib.rep_dbuser = 'infadev'
#ib.IS         = 'IS_Development'
#ib.dom_dbport =  1521
#ib.dom_name   = 'Domain_Dev' 
#ib.dom_dbhost = 'SSCLTORA'
#ib.dom_dbuser = 'infadev'
#ib.dom_dbpwd  = 'infadev'
#ib.dom_dbservice = 'infadev''
#ib.dom_dbtype = 'oracle'

#ib.user       = 'eocampo'
#ib.pwd        = 'oceandev'
#### END DEV

###PROD
#ib.rep_dbuser = 'infa'
#ib.rep_dbpwd  = 'Infa4prod'
#ib.rep_dbname = 'infapd'
#ib.IS         = 'IS_Ryder'
#ib.dom_name   = 'Domain_Prod' 
#ib.dom_dbhost = 'sscbpinfapp01'
#ib.dom_dbuser = 'infa'
#ib.dom_dbpwd  = 'Infa4prod'
#ib.dom_dbservice = 'infapd'
#ib.dom_dbport =  1521
#ib.dom_dbtype = 'oracle'
#ib.rep_user       = 'eocampo'
#ib.rep_pwd        = 'oceanprod'


import os,sys
sysp=sys.platform
def setEnvVars(): 
    print " -- setwinenv SHOULD NOT SEE THIS MESSAGE IN UNIX /Setting Environment vars"
 
    if sysp != 'win32' : 
        print " ERROR -- Remove any reference to setwinenv !!!!!"
        
    #GRAL

#    os.environ['DTM'        ] = 'YYYYMMDD_HH_MM_SS'
#    os.environ['GP_NZ_HOME' ] = r'C:/apps/infa_share'  
#    os.environ['LOGFILE'    ] = r'C:/apps/logs/gp_nz_mig.log'       
#    #GP
#    os.environ['GP_DB_HOST' ] = 'sscgp01'
#    os.environ['GP_DB_USER' ] = 'infaetl'
#
#    os.environ['GP_DB_PORT' ] = '5432'
#    os.environ['GP_DB_ENV'  ] = 'dev'
#    os.environ['GP_DB_SCHE' ] = 'sdl'
#
#
#    #NZ                          
#    os.environ['NZ_DB_ENV'  ] = 'dev'
#    os.environ['NZ_DB_HOST' ] = 'sscptdnetezza2a'
#    os.environ['NZ_DB_USER' ] = 'admin'
#    os.environ['NZ_DB_PWD'  ] = 'password'
#    os.environ['NZ_DB_PORT' ] = '5480'
#    
#    #DATA
#    #os.environ['TBL_SAMP_PCT']  = '10'
#    os.environ['TBL_SAMP_ROW' ] = '100'  
#    return 0 
#    
#    return 0 

#     os.environ['INFA_DOMAINS_FILE'] = r'C:\Informatica\9.1.0\clients\PowerCenterClient\domains.infa' 
#     os.environ['PMCMD'        ] = r'C:/Informatica/9.1.0/clients/PowerCenterClient/CommandLineUtilities/PC/server/bin/pmcmd.exe'   
#     os.environ['PMREP'        ] = r'C:\Informatica\9.1.0\clients\PowerCenterClient\CommandLineUtilities\PC\server\bin\pmrep.exe' 
#     os.environ['INFACMD'      ] = r'C:\Informatica\9.1.0\clients\PowerCenterClient\CommandLineUtilities\PC\server\bin\infacmd.bat'
#     os.environ['INFA_BIN'   ] = r'C:/Informatica/9.1.0/clients/PowerCenterClient/CommandLineUtilities/PC/server/bin'
#     os.environ['INFASRV'      ] = r'C:\Informatica\9.1.0\clients\PowerCenterClient\CommandLineUtilities\PC\server\text_cmd'    
#     
    os.environ['INFA_SCRIPT'   ]   =  r'C:/fe/script'     
    os.environ['INFA_SHARE'    ]   =  r'C:/fe/data/20349663547'   # mks
    os.environ['INFA_PROV_DATA']   =  r'C:/fe/data/20349663547'    # mks
    os.environ['INFA_SRC'      ]   =  r'C:/fe/infa_share/SrcFiles'
    os.environ['INFA_APP'      ]   =  r'C:/fe' 
    os.environ['INFA_APP_CFG'  ]   =  r'C:/fe/config' 
    os.environ['INFA_APP_LCK'  ]   =  r'C:/fe/lck'     
    os.environ['INFA_APP_CTL'  ]   =  r'C:/fe/ctl'   
    os.environ['INFA_APP_REC'  ]   =  r'C:/fe/logs'   
    os.environ['CFG_FILE'      ]   =  r'C:/fe/config/20349663547/procelectbill.cfg'


# 
#     # DEV Env
#     os.environ['INFA_USER'     ] = 'eocampo'
#     #os.environ['INFA_PWD'     ] =  'oceandev'
#     #os.environ['INFA_XPWD'     ] = 'Q05VMTcccOOm9jZWFuZGV2'   #BAD
#     os.environ['INFA_XPWD'     ] = 'Q05VMTQ1MldOVzpvY2VhbmRldg==' #GOOD
#     os.environ['DOMAIN'        ] = 'Domain_Dev'
#     os.environ['INT_SERV'      ] = 'IS_Development'    
#     os.environ['REP_DB_USER'   ] = 'infadev'   
#     os.environ['REP_DB_NAME'   ] = 'infadev'      
#     os.environ['INT_SERV'      ] = 'IS_Development'     
#     os.environ['DOM_DBPORT'    ] = '1521'                        
#     os.environ['DOM_NAME'      ] = 'Domain_Dev'          
#     os.environ['DOM_DBUSER'    ] = 'infadev'         
#     os.environ['DOM_DBXPWD'    ] = 'infadev'            
#     os.environ['DOM_DBSERVICE' ] = 'infadev'            
#     os.environ['DOM_DBTYPE'    ] = 'oracle' 
#     
#     
#     # Dummy sets.
#     
#     os.environ['DOM_BKUP'   ] =  'x '                          
#     os.environ['DOM_DBPORT' ] =  'x '             
#     os.environ['DOM_DBHOST' ] =  'x '
#     os.environ['DOM_HOST'   ] =  ' x'
#     os.environ['INFASETUP'  ] =  'x '
#     os.environ['INFA_BIN'   ] =  'x '
#     os.environ['INFA_DOM'   ] =  'x '
#     os.environ['INFA_HOME'  ] =  'x '
#     os.environ['INFA_HOST'  ] =  'x '
#     os.environ['INFA_SERVER'] =  'x '
#     os.environ['NODE'       ] =  'x '
#     os.environ['INFA_NODE'  ] =  'x '
#     os.environ['PMREP'      ] =  'x '    
#     os.environ['INFA_PORT'  ] =  '6005'    
#     os.environ['REPO_BKUP'  ] =  ' x'
#     os.environ['REPO_SERV'  ] =  'x '
#     os.environ['REP_DB_NAME'] =  'x '
#     os.environ['REP_DB_USER'] =  'x '
#     os.environ['REP_DB_XPWD'] =  'x '    
#    
#     # FTP Stuff
#     #FTP Related variables
#     os.environ['REMOTE_HOST' ] = 'sscltinf'
#     os.environ['USER'     ]    = 'infa'   
#     os.environ['PWD'      ]    = 'tone4all'
#     #os.environ['REMOTE_DIR'  ] =  '/home/infa/Interfaces/EDWHierarchy'
#     
#     #os.environ['REMOTE_DIR'  ] =  r'/home/infa/talentmap/Reports/APS'
#     os.environ['REMOTE_DIR'  ] =  r'/home/infa/vehicle'
#     #os.environ['RXFILE'   ]    =  r'*_[0-9]*.TXT'
#     #os.environ['LOC_DIR'  ] =  r'C:\\apps\\infa_share\\SrcFiles\\lease_credit'
#     os.environ['LOC_DIR'  ] =  r'C:\\apps\\infa_share\\SrcFiles\\vehicle'               # Where file is pulled from 
#     #os.environ['LOC_DIR'  ] =  r'C:\\apps\\infa_share\\TgtFiles\\finance\\output'   
#     #os.environ['LOC_DIR'  ] =  r'C:\\apps\\infa_share\\SrcFiles\\talentmap'  
#     #os.environ['LOC_DIR'  ] =  r'C:\\apps\\infa_share\\SrcFiles\\employee'  
#     # os.environ['FILE'     ] =  (r"\'P.PO225D15.UMPK(0)\',\'P.PO875D30.WHOUSE.CURR.STD\'")    # MainFrame 
#     #os.environ['FILE'     ] =  r'Cortera_Trx_Extract.txt,CTRL_BUREGION.txt,CTRL_CORTERA.txt,Bu_region.csv,'
#     #os.environ['RXFILE'   ] =  r'Cortera_Trx_Extract_[0-9]*.txt'
#     
#     os.environ['FTP_PORT' ]     =  '21'
#     os.environ['FTP_VERB' ]     =  '2'     
#     os.environ['FTP_PORT' ]     =  '21'
#     os.environ['FTP_TIMEOUT' ]  =  '1000'
#     

    # Logger related
    os.environ['LOG_DIR']   = r'C:/fe/logs/20349663547' 
    os.environ['LOGNAME']   = 'test'
    os.environ['LOG_LEVEL'] = 'DEBUG'

