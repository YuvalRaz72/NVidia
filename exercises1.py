"""
Detect locally mounted disk (make sure it is local) with at least X MB free space,
create Z files of size Y,
run Z “dd” processes which where each process will fill the selected file with Data and print time took to complete the work.

"""

import psutil
from multiprocessing import Pool, TimeoutError
import os
from timeit import default_timer as timer
import threading
import asyncio

#Global vars
min_free_space = 0
file_size = 0
num_of_files  = 0

# Detect locally mounted disk (make sure it is local) with at least X MB free space
def Check_Free_Space():
    
    size=int(min_free_space)
    partitions = psutil.disk_partitions()
    for p in partitions:
        free_space = psutil.disk_usage(p.mountpoint).free / (1024.0)
        #check if free space is greater or equal from input
        if free_space >= size:
            print ("Free space available on drive ",p.mountpoint, ": ", free_space)
            #check if there is enough  space to run the test
            if file_size * num_of_files < free_space:
                run()
            else:
                print("Exit program, not enough free space!")

# create Z files of size Y
async def CreateFile(file_name):
    try:
        with open(str(file_name), 'w') as f:
            f.seek(file_size* 1024 * 1024) 
            f.write('0')
    except:
        print("fail to create file")
        # cmd = ("dd if=/dev/zero of="+ str(file_name) +".txt bs=1 count=0 seek="+str(file_size * 1024 * 1024))
        # os.system(cmd)
    
# run Z “dd” processes which where each process will fill the selected file with Data        
async def FillFile(file_name):
    
    try:
        cmd = ("dd if=/dev/zero of="+ str(file_name) +".txt bs=1,048,576 count=" + str(file_size * 1024 * 1024) +" conv=notrunc")
        os.system(cmd)
    except Exception as e: print(e)
    

    
def CreateFile_callback(file_name):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(CreateFile(file_name))
    loop.close()

def FillFile_callback(file_name):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(FillFile(file_name))
    loop.close()

def run():   
    start = timer()
    create_threads = []
    fill_threads = []
    #create async thread for each file to be created
    for item in range(1,num_of_files+1):       
        _thread = threading.Thread(target=CreateFile_callback, args=(str(item)),name= str(item))
        _thread.start()  
        #add the async thread to thread list      
        create_threads.append(_thread)

   #check when every async thread in the list is finished
    while len(create_threads):            
        for t in create_threads:
            if not t.is_alive():
                #create a new async thread to fill the specific file according to file name= thread name with data
                _thread = threading.Thread(target=FillFile_callback, args=(t.name))
                _thread.start()
                fill_threads.append(_thread)
                create_threads.remove(t)
   
    while len(fill_threads):            
        for t in fill_threads:
            if not t.is_alive():
                fill_threads.remove(t)

    end = timer()
    print(end - start)  


if __name__ == '__main__':
    #Get free space value
    try:
        min_free_space = int(input("Enter size for (in MB) free space:"))

        if min_free_space <= 0:
            print("Free space must be above 0.")
    except:
        print("Invalid value")
        exit()
    #get number of files value
    try:    
        num_of_files = int(input("Enter the number files to create:"))
        if num_of_files <= 0:
            print("Number of files must be above 0.")
        
    except:
        print("Invalid value")  
        exit() 

    #get files size value
    try:      
        file_size = int(input("Enter file size (in mb):"))
        if file_size < 0:
            print("file size must be above or equal to 0.")
    except:
        print("Invalid value")
        exit()
        
    Check_Free_Space()
   
    



