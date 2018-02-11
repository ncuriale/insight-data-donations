
### This script computes if a transaction is from a repeat donor or not

import pybloom_live
from datetime import datetime
from dateutil.relativedelta import relativedelta

def repeatDonor(data,bf,UID,UIDfreq,dateRecord):       
    
    #Bloom filter check on UID  
    indx,bf,UID,UIDfreq=bloomFilterUID(data[-1],bf,UID,UIDfreq)
    
    #Check dates to see if repeat donor
    res=checkDates(data[3],UID[indx],UIDfreq[indx],dateRecord)
    
    #Map data to UID in dictionary
    dateRecord=mapUID(data,UID[indx],UIDfreq[indx],dateRecord)
    
    return res,bf,UID,UIDfreq,dateRecord
    
def bloomFilterUID(data,bf,UID,UIDfreq): 
    #check if CMTE_ID is in bfilter
    #count cmte_id,zip,year    
    #list of transactions
    #sum transactions
    #percentile transactions      
        
    if(not UID):#add first entry to type 
        indx=0
        UID.append(data)
        UIDfreq.append(1) 
        
        #initialize bloom filter
        bf = pybloom_live.pybloom.ScalableBloomFilter()
        bf.add(data)
        
    else:                            
        if(data in bf):                
            try:#test to see if BF gives result
                indx=UID.index(data)
                UIDfreq[indx]+=1

            except:#if false-positive,add entry to type  
                indx=len(UID)        
                UID.append(data)
                UIDfreq.append(1) 
                bf.add(data)
            
        else:#add entry to type  
            indx=len(UID)      
            UID.append(data)
            UIDfreq.append(1) 
            bf.add(data)   
         
    return indx,bf,UID,UIDfreq
            
def mapUID(data,UID,UIDfreq,dateRecord):      
    
    date=data[3]
                    
    if(UIDfreq==1):
        repeat=0
        dateRecord.update({UID: [date] })  
    else:                      
        temp=dateRecord[UID] + [date] 
        dateRecord.update({UID: temp})  
    
    return dateRecord

def checkDates(date,UID,UIDfreq,dateRecord):           
    
    #This checks dates within the UID record
    #Reports if this UID is a repeat donor (1) or not (0)
    
    #Start res as zero
    res=False    
    if(not UIDfreq==1):
        #Go through all records for this UID
        thisdateRecord=dateRecord[UID]        
        for i in range(len(thisdateRecord)):
            out=dateCompare(date,thisdateRecord[i])
        
            #If one date shows at least one year difference
            #Set res=1 at break loop
            if(out==True):
                res=True
                break                
                
    return res
    
def dateCompare(date1,date2):
    
    #Output False, if at least one year difference between dates    
    #Start output as zero
    out=False 

    #Create two datetime objects
    date1=date1[0:2]+'/'+date1[2:4]+'/'+date1[4:8]
    date2=date2[0:2]+'/'+date2[2:4]+'/'+date2[4:8]
    dateTime1= datetime.strptime(date1, '%m/%d/%Y')
    dateTime2= datetime.strptime(date2, '%m/%d/%Y')
    
    #Compare dates and output if at least one calendar year difference
    if(dateTime1>dateTime2):
        if( (dateTime1+relativedelta(years=-1))>=dateTime2 ):
            out=True            
    elif(dateTime2>dateTime1):
        if( (dateTime2+relativedelta(years=-1))>=dateTime1 ):
            out=True

    return out
         
     
     
        
    