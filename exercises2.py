import paramiko
import threading
import asyncio


async def sshClient(host, port, user, password, command):
   
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Set policy to use when connecting to servers without a known host key
        ssh.connect(hostname=host, username=user, password=password, port=port)
        stdin, stdout, stderr = ssh.exec_command('sh ver')
        output = stdout.readlines()
        print(output)
    except:
        txt = "Unable to connect to server " , host
        print(txt)
    

def between_callback(host, port, user, password, command):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(sshClient(host, port, user, password, command))
    loop.close()



   

    
# If not exist create file serverlist.txt
# Add to file like this : IPAddress:User:password
serverList = []
try:
    with open("serverlist.txt") as fp:
        Lines = fp.readlines()
        for line in Lines:
            
            line = line.strip()    
            server=line.split(":")
            serverList.append([server[0],server[1],server[2]])
            
        fp.close()
except:
    print("File Error")


cmd = "echo 'hello world' > testing.txt"

for server in serverList:
    host = server[0]
    user = server[1]
    password = server[2]    
    port = '22'
    try: 
        
        _thread = threading.Thread(target=between_callback, args=(host, port, user, password, cmd))
        _thread.start()
    except:
        print("Thread return error")
      
    

    