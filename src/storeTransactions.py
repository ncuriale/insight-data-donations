
### This script processes and stores each repeat donor transaction in python dictionary

import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

def storeTransaction(data,cmteRecord,percentile,outname):

    #Map important line data   
    cmte=data[0]
    zip=data[2]
    year=data[3][4:8]
    year_zip=year+'_'+zip
    amt=data[4]  
    cmteRecord=mapCMTE(cmte,year_zip,amt,cmteRecord)

    #Store transaction data in order 
    transactions=cmteRecord[cmte][year_zip][2:-1]
    transactions=orderTransaction(transactions,amt)
    cmteRecord[cmte][year_zip][2:]=transactions
    
    #Run nearest rank procedure
    rankValue=nearestRank(transactions,percentile)
    
    #Write to output file
    outList=[cmte,zip,year,rankValue,str(cmteRecord[cmte][year_zip][1]),str(cmteRecord[cmte][year_zip][0])]
    outLine="|".join(outList)
    oid=open(outname, 'a')
    oid.write(outLine + '\n')
    oid.close()
    
    return cmteRecord

def mapCMTE(cmte,year_zip,amt,cmteRecord):      
    
    #Creates list of all zip/amt combos for each year of all CMTE_IDs                   
    #First, check inCMTE_ID exits in record    
    if(not cmte in cmteRecord):
        yearzipRecord={ year_zip:[1,int(amt),amt] }
        cmteRecord.update({cmte: yearzipRecord }) 
    else:      
        #Check if the year/zip combo exists for this CMTE_ID   
        if(not year_zip in cmteRecord[cmte]):
            yearzipRecord={ year_zip:[1,int(amt),amt] }  
            cmteRecord[cmte].update( yearzipRecord )  
        else:
            cmteRecord[cmte][year_zip][0]+=1
            cmteRecord[cmte][year_zip][1]+=int(amt)
            cmteRecord[cmte][year_zip].append(amt)
   
    return cmteRecord
 
def orderTransaction(data,input):
    
    def calcMid(left,right):
        return np.int(np.floor((right+left)/2))
    
    #If no data yet
    if(len(data)==0):
        data=[input]
        return data
    
    #Initialize algorithm
    #Variation on quicksort
    #Use left and right indices to search ordered list
    #for location to insert value
    left=0
    right=len(data)-1
    mid=calcMid(left,right)
    while(1):
        
        #Check if converged on index
        if( mid == left ):                
            if (int(input)<int(data[mid])):   
                data=np.insert(data,mid,input)
            elif (int(data[mid])<int(input)):
                data=np.insert(data,mid+1,input)                
            break
        
        #Alter left/right indices depending on input value
        if (int(input)<=int(data[mid])):
            right=mid            
            mid=calcMid(left,right)
        elif (int(data[mid])<int(input)):
            left=mid            
            mid=calcMid(left,right)
    
    return data

def nearestRank(data,percentile):
    
    #Find nearest rank from formula
    n=np.int( np.ceil( (percentile/100)*len(data) ) )
    
    #Value in the array at calculated rank
    val=data[n-1]    

    #Round values to nearest dollar
    val=round( np.float(val) )
    val=str(val)
    
    return val 


     