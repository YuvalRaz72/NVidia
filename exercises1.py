import psutil
from multiprocessing import Pool, TimeoutError
import deepdish.io as dd
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


async def savefile(a,size):
    filesize = int(size) * 1024 * 1024
    with open(str(a), 'w') as f:
        f.seek(filesize) # One GB
        f.write('0')
   # dd.save(str(a),{'b':1,'t':2,'c':3,'g':4,'e':5,'d':6})
        
        

    
def between_callback(a, size):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(savefile(a,size))
    loop.close()


def run_many_calcs():
    num = input("Enter the number files to create:")
    size = input("Enter file size (in mb):")
    num_processes= int(num)
    
    pool = Pool(processes=num_processes)    
   
    start = timer()
    for a in range(1,num_processes+1):       
        _thread = threading.Thread(target=between_callback, args=(a, size))
        _thread.start()
      
    end = timer()
    print(end - start)  


if __name__ == '__main__':
    Check_Free_Space()
    run_many_calcs()
    



