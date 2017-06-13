# -*- coding:utf-8 -*-  
  
import json  
import sys  
import argparse  
  
 
class configparse:
    def  __init__(self,configFile='sbp.ini'): 
        configfile = open(configFile)  
        self.jsonconfig = json.load(configfile)  
        configfile.close() 
    def getMysql(self):
        mysql =  self.jsonconfig['mysql'];
    def getDir(self):
        return self.jsonconfig['dir'];
    def getMailto(self):
        return self.jsonconfig['mailto'];
    def getMailHost(self):
        return self.jsonconfig['mailhost'];
 
if __name__ == '__main__':  
#    main(sys.argv)  
    parse = configparse();
    print parse.getMysql()
    print parse.getDir(); 
    print parse.getMailto();
    print parse.getMailHost(); 
