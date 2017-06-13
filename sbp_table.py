#! /usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb
import os
import os.path
import configparse

kindlepParse = configparse.configparse()

rootdir = kindlepParse.getDir()['rootdir']
if rootdir == None:
    rootdir = "/home/pi/test/" 
mysqlInfo = kindlepParse.getMysql()
if mysqlInfo['host'] == '' or mysqlInfo['user'] == '' or mysqlInfo['passwd'] == '' or mysqlInfo['port'] == '' or mysqlInfo['table'] == '' or mysqlInfo['db'] == '':
    print 'kindle Parse fail'
    exit -1



db=MySQLdb.connect(host=mysqlInfo['host'], user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], port=mysqlInfo['port'])

cur=db.cursor()

sql = 'use ' + mysqlInfo['db'];
cur.execute(sql)
sql = 
sql = 'truncate table ' + mysqlInfo['table'];
cur.execute(sql)

#for t in range(0,100):

sql = 'insert into ' + mysqlInfo['table'] + ' (booklist_booktype,booklist_author,booklist_filename,booklist_filepath,booklist_filesize,booklist_bookdate) values'
count = 0
for parent,dirnames,filenames in os.walk(rootdir): 
    for filename in filenames:
    	
    	fullpath = os.path.join(parent,filename)
    	booktype = fullpath.split('/')[-2]
    	sql += ' (\"' + booktype +'\",\"unknown\",\"' + filename +'\",\"' + fullpath + '\",' + str(os.path.getsize(fullpath)) + ',' + '0)' 
    	count += 1
        if count == 10000:
            sql += ';'
            try:            	
                cur.execute(sql)
            except Exception,e:
                print sql
            finally:
                sql = 'insert into ' + mysqlInfo['table'] + ' (booklist_booktype,booklist_author,booklist_filename,booklist_filepath,booklist_filesize,booklist_bookdate) values'
                count = 0
            continue
        sql +=','
        
#sql += ' (test1,test,test,test,1,2)'
#for i in range(1,100000):
#        sql += ' ('+`t*100000+i`+', "tb5EXTRA"),'
#    sql +=p

if count != 0:
    cur.execute(sql[0:-1])

db.commit()

cur.close()

db.close()
