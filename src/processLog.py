import os
import pybloom_live

#import local files
from processLine import *
from storeTransactions import *
from repeatDonor import *

def main():
    
    #Start
    print("Initialize:")
    
    #Read percent data file
    percentname='input/percentile.txt'  
    pid = open(percentname, 'rb')   
    lines=pid.readlines()
    percentile=int(lines[0])
    print("Reading percentile:",percentile)  
    pid.close
        
    #Remove out file
    outname='output/repeat_donors.txt'
    try:
        os.remove(outname)
    except OSError:
        pass
    
    #Read data file
    print("Reading and processing data ...")
    filename='input/itcont.txt'  
    fid=open(filename, 'rb')
    lines=fid.readlines()
      
    #Initialize bloom filter for data search  
    UID=[]
    UIDfreq=[]
    bf = pybloom_live.pybloom.ScalableBloomFilter()
            
    #While loop to continuously look for data -- constant stream
    #This code will use a counter to index each new line in data file 
    #but can be altered to process new data once recognized
    i=0
    dateRecord={}
    cmteRecord={}
    while(1):

        ######## Process current data line #########
        #CMTE_ID, NAME, ZIP_CODE,
        #( MONTH, DAY, YEAR ) 
        #TRANSACTION_AMT, UID
        lineData,err=processLine(lines[i],i)
        if(err==1):
            i+=1      
            continue
          
        #Search data for repeat donors
        res,bf,UID,UIDfreq,dateRecord=repeatDonor(lineData,bf,UID,UIDfreq,dateRecord)  
        
        #If this is a repeat donor
        if(res):
            #Store and order transaction data
            cmteRecord=storeTransaction(lineData,cmteRecord,percentile,outname)
                
        #Increase counter and end loop if at end of data file
        i+=1        
        if(i==len(lines)):
            break
        
    fid.close()          
               
if __name__ == "__main__":
    main()