#simpleBookPush
This is used for push books to kindle mail automatically , You can used the tools by simply filling in the config files and setting up the environment in server. I used a raspberry Pi as the server.
#Environment Set up
###Server Software Configure
######set up the environment in raspberry or Debian/Ubuntu system with following commands:
```
apt-get update
sudo apt-get upgrade
sudo apt-get install libev-dev mysql-server python-mysqldb
sudo pip install bjoern 
sudo apt-get install smbclient samba samba-common-bin
```
###Mysql Configure 
######Set mysql configure so that we can connect the mysql from network and set default character code as utf8
add following configs in  /etc/mysql/my.cnf 
```
[client]
default-character-set=utf8
[mysqld]
default-storage-engine=INNODB
character-set-server=utf8
collation-server=utf8_general_ci
```
comment  following in /etc/mysql/my.cnf 
```
bind-address           = 127.0.0.1 
```

######Create tables, set utf8 and enable remote access.
```
mysql -u root -p
source sbp_init.sql
```
###samba Configure (optional)
```
sudo mkdir /home/pi/samba
sudo mount -t cifs //192.168.123.183/移动磁盘-C /home/pi/samba
```
###Fill the Correct info in sbp.ini
```
{  
    "mysql":  
    {     
        "host":"192.168.1.123",  
        "port":3306,
        "user":"root",  
        "passwd":"root",
        "table":"test",
        "db":"test"
    },  
    "dir":  
    {  
        "rootdir":"/home/pi/test/"  
    },  
    "mailto":  
    {  
        "mailTo":["test@kindle.cn" ]
    },  
    "mailhost":
    {
        "mail_host" : "smtp.163.com",  
        "mail_user" : "test",                           
        "mail_pass" : "test",                             
        "mail_postfix" : "163.com",                    
        "fromHost" : "test@163.com"
    }
}  

```
###Run Create book list table
```
python sbp_table.py
```
###Run Server
```
python sbp_server.py
```
