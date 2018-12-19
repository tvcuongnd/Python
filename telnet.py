import getpass
import sys
import telnetlib
import ftplib
import os
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
HOST = "172.16.1.10"
user = "toolbwss"
password = "bkav@@)!*"
## path_save day la path
path_save= "/root/SCRIPT/ConfigSw_%s_%s.conf" % (timestr,HOST)
## file_save la object
file_save = open('%s' %path_save ,'wb+')

# FTP Server and account
ftp_server="10.2.32.220"
ftp_user="cuongtvb"
ftp_pass="123abc@A"

# Tao file backup
#copy_config(HOST,user,password,file_save)

# Day FTP
#ftp = ftplib.FTP("10.2.32.220")
#ftp.login("cuongtvb", "123abc@A")
#upload(ftp,path_save)

def copy_config(HOST,user,password,file_save):
    tn = telnetlib.Telnet(HOST)
    tn.read_until("Username: ")
    tn.write(user + "\n")
    if password:
       tn.read_until("Password: ")
       tn.write(password + "\n")
    tn.write("terminal length 0\n")
    tn.write("show running-config | include 0000.0000\n")
    tn.write("terminal length 24\n")
    tn.write("exit\n")
    file_save.write(tn.read_all())
    file_save.close() 


def upload(ftp_server,ftp_user,ftp_pass,path_save):
    ftp = ftplib.FTP(ftp_server)
    ftp.login(ftp_user,ftp_pass)
    ext = os.path.splitext(path_save)[1]
    print "%s,%s" %(file,ext)
    if ext in (".txt", ".htm", ".html", ".conf", ".log", ".txt"):
        ftp.storlines("STOR " + os.path.split(path_save)[1], open(path_save))
    else:
        ftp.storbinary("STOR " + os.path.split(path_save)[1], open(path_save, "rb"), 1024)


# Tao file backup
copy_config(HOST,user,password,file_save)
# Day FTP
upload(ftp_server,ftp_user,ftp_pass,path_save)


