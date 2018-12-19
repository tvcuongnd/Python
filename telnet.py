import getpass
import sys
import telnetlib
import ftplib
import os
import time
import paramiko


host_list_telnet=open("/root/SCRIPT/CISCO_TELNET.list")
host_list_ssh=open("/root/SCRIPT/CISCO_SSH.list")
mk_list=open("/root/SCRIPT/mk.list")
timestr = time.strftime("%Y%m%d-%H%M%S")
#host = "172.16.1.10"

# account telnet
#user = "toolbwss"
#password = "bkav@@)!*"
with mk_list as j:
    acc = j.read().splitlines()
    user = acc[0]
    password = acc[1]
# FTP Server and account
ftp_server="10.2.32.220"
ftp_user="cuongtvb"
ftp_pass="123abc@A"

def copy_config_telnet(host,user,password,file_save):
    tn = telnetlib.Telnet(host)
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
    #print "%s,%s" %(file,ext)
    if ext in (".txt", ".htm", ".html", ".conf", ".log", ".txt"):
        ftp.storlines("STOR " + os.path.split(path_save)[1], open(path_save))
    else:
        ftp.storbinary("STOR " + os.path.split(path_save)[1], open(path_save, "rb"), 1024)

with host_list_telnet as f:
    content = f.read().splitlines()
for host_telnet in content:
    ## path_save day la path
    #print host
    path_save= "/root/SCRIPT/ConfigSw_%s_%s.conf" % (timestr,host_telnet)
    #path_save= "/root/SCRIPT/ConfigSw_%s.conf" % (timestr)
    ## file_save la object
    file_save = open('%s' %path_save ,'wb+')
    # Tao file backup
    copy_config_telnet(host_telnet,user,password,file_save)
    # Day FTP
    #upload(ftp_server,ftp_user,ftp_pass,path_save)
###############################################SSH####################################################3

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''
    remote_conn.send("terminal length 0\n")
    time.sleep(1)
    # Clear the buffer on the screen
    output = remote_conn.recv(1000)
    return output


for ip in host_list_ssh:

        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()

        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #initiate SSH connection
        remote_conn_pre.connect(ip, username=user, password=password)
        print '#################################################'
        print "SSH connection established to %s" % ip

        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        # print "Interactive SSH session established"

        # Strip the initial router prompt
        output = remote_conn.recv(1000)

        # See what we have
        #print output

        # Turn off paging
        disable_paging(remote_conn)
        remote_conn.send("\n")
        output = remote_conn.recv(0)
        remote_conn.send("show run | include 0000.0000\n")
        time.sleep(10)
        output = remote_conn.recv(500000000)


        ##################
        #OUTPUT GENERATED FOR FILES
        ###########################
        mytime = time.strftime('%Y-%m-%d-%H-%M-%S')
        ip = ip.strip(' \t\n\r')
        print
        print ip + ' config backup in place'
        print
        path_save= "/root/SCRIPT/ConfigSw_%s_%s.conf" % (timestr,ip)
        file_save = open('%s' %path_save ,'wb+')
        file_save.write(output)
        file_save.close()
        remote_conn.send("exit\n")

        print "SSH connection closed to %s" % ip
        print '#################################################'

       