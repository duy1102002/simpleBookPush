#! /usr/bin/env python
# -*- coding:utf-8 -*-
from time import time
import bjoern
import json
from urllib import unquote
import os
import glob
import sys 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import MySQLdb
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

#db.set_character_set('utf8')
mailtoInfo = kindlepParse.getMailto()
mailHostInfo = kindlepParse.getMailHost() 

reload(sys)  
#sys.setdefaultencoding('utf8')


mailtoList=mailtoInfo['mailtoList']

#收件人(列表)
mail_host = mailHostInfo['mail_host']            #使用的邮箱的smtp服务器地址
mail_user = mailHostInfo['mail_user']                            #用户名
mail_pass = mailHostInfo['mail_pass']                            #密码
mail_postfix = mailHostInfo['mail_postfix']                     #邮箱的后缀
fromHost = mailHostInfo['fromHost'] 


#{"search":""}

# 127.0.0.1:8081/find?{"search":"test"}   查找请求    返回 {"result": ["./search_test.py", "./sendmail_test.py", "./test.txt"]}
# 127.0.0.1:8081/sendmail?{"bookName":"test.txt"}   发送邮件请求  返回 {"result":"success"}
def start():
    def return_hello(environ, start_response):
        start_response('200 OK', [('Content-Type','text/plain')])
        return '{"result":"success"}'
    
    def return_404(environ, start_response):
        start_response('404 Not Found', [('Content-Type','text/plain'),])
        return "URL %s not found" % environ.get('PATH_INFO', 'UNKNOWN')
    
    def return_find(environ, start_response):
        start_response('200 OK', [('Content-Type','text/plain')])
        query_string = unquote(environ.get('QUERY_STRING'))
        print query_string
        #print unquote(query_string)
        
        json_parse = json.loads(query_string)
        if json_parse == None:
            return ('Error')
        bookName = json_parse.get('search')
        if bookName == None:
            return ('Please input you want search')
        bookList = scan_files(contains=bookName)
        strBookList = ",".join(bookList)
        bookListResponse = {'result':bookList}
        bookListResponseJson = json.dumps(bookListResponse)
        print bookListResponseJson
        return (bookListResponseJson)
    
    def return_sendmail(environ, start_response):
        start_response('200 OK', [('Content-Type','text/plain')])

        query_string = unquote(environ.get('QUERY_STRING'))
        json_parse = json.loads(query_string)
        if json_parse == None:
            return ('Error')
        bookName = json_parse.get('bookName')
        #print bookName
        if bookName == None:
            return ('Please input you want search')
        #bookList = scan_files(scanPath,contains=bookName)
        #strBookList = "".join(bookList)
        #print strBookList

        #print fromHost,mailtoList,bookName
        
        if send_mail(fromHost,mailtoList,bookName) == True:
            return '{"result":"success"}'
        else:
            return '{"result":"failure"}'
    
    dispatch = {
        '/': return_hello,
        '/find': return_find,
        '/sendmail' : return_sendmail,
    }
    
    def choose(environ, start_response):
        print environ
        return dispatch.get(environ.get('PATH_INFO'), return_404)(environ, start_response)


#private logic
    def scan_files(contains=None):
        files_list=[]
        
        if contains:
            contains = contains.encode('utf8')
            #contains = contains.decode('utf8')
            cur=db.cursor()
            #cur.execute('SET NAMES utf8;')
            #cur.execute('SET CHARACTER SET utf8;')
            #cur.execute('SET character_set_connection=utf8;')
            sql = 'use ' + mysqlInfo['db'];
            cur.execute(sql)
            sql = "select * from " + mysqlInfo['table'] + " where booklist_filename like \"%" + contains + "%\" ; "
            count=cur.execute(sql)
            if count > 0:
                info = cur.fetchmany(count)
                #count = 0
                for ii in info:
                    #print ii
                    (booklist_index,booklist_booktype,booklist_author,booklist_filename,booklist_filepath,booklist_filesize,booklist_bookdate) = ii;
                    print booklist_filename

                    files_list.append(booklist_filename)
            else:
                print 'no such book contains: ',contains
            cur.close()

        return files_list

    def send_mail(fromHost,toList,bookName):
        #me= sub +"<"+mail_user+"@"+mail_postfix+">"
        # 如名字所示： Multipart就是多个部分
        bookName = bookName.encode('utf8')
        msg = MIMEMultipart()
        
        msg['Subject'] = bookName
        msg['From'] = fromHost
        msg['To'] = ";".join(toList)                #将收件人列表以‘；’分隔
        
        pureText = MIMEText('Only for kindle book transmission');
        msg.attach(pureText);
        cur=db.cursor()
        #cur.execute('SET NAMES utf8;')
        #cur.execute('SET CHARACTER SET utf8;')
        #cur.execute('SET character_set_connection=utf8;')
        sql = 'use ' + mysqlInfo['db'];
        cur.execute(sql)
        sql = "select * from " + mysqlInfo['table'] + " where booklist_filename =\"" + bookName + "\"; "
        count=cur.execute(sql)
        print count
        bookPath = ''
        if count > 0:
            info = cur.fetchmany(count)
            
            for ii in info:
                #print ii
                (booklist_index,booklist_booktype,booklist_author,booklist_filename,booklist_filepath,booklist_filesize,booklist_bookdate) = ii;
                print booklist_filename
            

            bookPath = booklist_filepath
            cur.close()
        else:
            print 'no such book: ',bookName
            cur.close()
            return False
        
        #附件，每次只能加一个附件
        kindleBook = MIMEApplication(open(bookPath,'rb').read())
        kindleBook.add_header('Content-Disposition', 'attachment', filename=bookName)
        msg.attach(kindleBook)
        try:
            server = smtplib.SMTP()
            server.connect(mail_host)                            #连接服务器
            server.login(mail_user,mail_pass)               #登录操作
            server.sendmail(fromHost, toList, msg.as_string())
            server.close()
            return True
        except smtplib.SMTPRecipientsRefused:
            print 'Recipient refused'
            return False
        except smtplib.SMTPAuthenticationError:
            print 'Auth error'
            return False
        except smtplib.SMTPSenderRefused:
            print 'Sender refused'
            return False
        except smtplib.SMTPException,e:
            print e.message
            return False

    bjoern.run(choose, '0.0.0.0', 8081)

if __name__ == "__main__":
    start()
