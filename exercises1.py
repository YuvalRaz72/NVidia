import psutil
from multiprocessing import Pool, TimeoutError
import os
from timeit import default_timer as timer
import threading
import asyncio

def Check_Free_Space():
    size_str = input("Enter size for (in MB) free space:")
    size=int(size_str)
    partitions = psutil.disk_partitions()
    for p in partitions:
        if psutil.disk_usage(p.mountpoint).free / (1024.0 ** 1) >= size:
            print (p.mountpoint, psutil.disk_usage(p.mountpoint).free / (1024.0))


async def CreateFile(a,size):
    filesize = int(size) * 1024 * 1024
    cmd = ("dd if=/dev/zero of="+ str(a) +".txt bs=1 count=0 seek="+str(filesize))
    os.system(cmd)

    # with open(str(a), 'w') as f:
    #     f.seek(filesize) # One GB
    #     f.write('0')
   
        
async def FillFile(a,size):
    filesize = int(size) * 1024 * 1024
 
    cmd = ("dd if=/dev/zero of="+ str(a) +".txt bs=1,048,576 count=" + str(size) +" conv=notrunc")
    os.system(cmd)

    

    
def CreateFile_callback(a, size):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(CreateFile(a,size))
    loop.close()

def FillFile_callback(a, size):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(FillFile(a,size))
    loop.close()

def run():
    num = input("Enter the number files to create:")
    size = input("Enter file size (in mb):")
    num_processes= int(num)
    
    pool = Pool(processes=num_processes)    
   
    start = timer()
    for a in range(1,num_processes+1):       
        _thread = threading.Thread(target=CreateFile_callback, args=(a, size))
        _thread.start()
    
    for a in range(1,num_processes+1):       
        _thread = threading.Thread(target=FillFile_callback, args=(a, size))
        _thread.start()

    end = timer()
    print(end - start)  


if __name__ == '__main__':
    Check_Free_Space()
    run()
    



