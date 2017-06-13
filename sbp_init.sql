show databases;
create database kindlebookdb  character set utf8;
use kindlebookdb;
SET NAMES 'utf8'; 
create table booklist_tbl(
booklist_bookid INT NOT NULL AUTO_INCREMENT,
booklist_booktype varchar(120),
booklist_author varchar(120),
booklist_filename  varchar(240) NOT NULL,
booklist_filepath varchar(2048) NOT NULL ,
booklist_filesize  INT NOT NULL,
booklist_bookdate INT,
KEY bookname(booklist_filename),
PRIMARY KEY(booklist_bookid),
KEY author(booklist_author),
KEY booktype(booklist_booktype) 
) character set = utf8;
use mysql;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '7788414' WITH GRANT OPTION;
flush privileges;
commit;
