
### This script processes each independent line

def processLine(line,i):
    
    #------------------------------------------------------------------------------
    #
    # Purpose: This function filters the data line to required data
    #
    #------------------------------------------------------------------------------
    
    try: 
        err=0
        line=line.decode('ascii')
                                      
        #call sort function and add to array
        lineData,errlvl=sortLine(line) 
                
        if (not errlvl==0):
            raise ValueError('A very specific bad thing happened')
                
        #Good data gets a UID
        #Unique ID generator and add to data
        lineData=lineData + [getUID(lineData[1],lineData[2])] 
            
    except UnicodeDecodeError:
        print (i,"-- entry was not an ascii-encoded unicode string")
        err=1
        
    except ValueError:
        print (i,"-- entry did not comply with data formatting ")
        err=1
          
    return lineData,err

def sortLine(line):
    
    #------------------------------------------------------------------------------
    #
    # Purpose: Split data into respective values and check validity
    #
    #------------------------------------------------------------------------------
    
    #Split line based on '|'
    line=line.split('|')     
    CMTE_ID,NAME,ZIP_CODE,TRANSACTION_DT,TRANSACTION_AMT,OTHER_ID=line[0],line[7],line[10][0:5],line[13],line[14],line[15]
            
    #Check all conditions
    errlvl=checkID(CMTE_ID)
    errlvl+=checkNAME(NAME)
    errlvl+=checkDATE(TRANSACTION_DT)
    errlvl+=checkAMOUNT(TRANSACTION_AMT)
    errlvl+=checkZIP(ZIP_CODE)
    errlvl+=checkOTHER(OTHER_ID)
      
    #Combine required data for further calculations
    lineData=[CMTE_ID,NAME.upper(),ZIP_CODE,TRANSACTION_DT,TRANSACTION_AMT]    
    
    #lineData=[CMTE_ID,NAME.upper(),ZIP_CODE,TRANSACTION_DT[0:2],TRANSACTION_DT[2:4],TRANSACTION_DT[4:8],TRANSACTION_AMT]    
    
    return lineData, errlvl

def checkID(CMTE_ID):
    
    #Initialize errlvl to zero
    errlvl=0
        
    #Check CMTE_ID value
    if ( CMTE_ID == '' ):
        errlvl=1
                     
    return errlvl 

def checkNAME(NAME):
    
    #Initialize errlvl to zero
    errlvl=0
    
    #Invalid name check
    #Assuming a valid name requires at least first name and last name   
    #Must be in format (lastname, firstname mid_initial) 
    #Lastname and firstname/mid_init must not be empty
    n_split=NAME.split(',')
    
    #First, check at least two names and lastname is all alphabetical
    if ( not len(n_split)==2 or not n_split[0].isalpha() ):
        errlvl=1
    
    #Second, check if firstname is present & alphabetical
    #Ensure first split actually worked as well
    if ( len(n_split)>1 ):
        fn_split=n_split[1].split()
        
        #Check second split works
        if ( len(fn_split)>0 and len(fn_split)<3 ):
            
            #Ensure firstname is alphabetical
            if ( not fn_split[0].isalpha() ):
                errlvl=1
                
            #Check middle initial as well, if present
            if ( len(fn_split)==2 ):
                if ( not fn_split[1].isalpha() ):
                    errlvl=1
                            
        else:
            errlvl=1          
            
    return errlvl

def checkDATE(TRANSACTION_DT):
    
    #Initialize errlvl to zero
    errlvl=0
    
    #Check invalid transaction date
    #Must be MMDDYYYY format
    #All digits
    #Length of 8
    #Month not higher than 12
    #Days not more than 31
    if ( not TRANSACTION_DT.isdigit() or not len(TRANSACTION_DT)==8 or int(TRANSACTION_DT[0:2])>12 or int(TRANSACTION_DT[2:4])>31):
        errlvl=1
    
    return errlvl
 
def checkAMOUNT(TRANSACTION_AMT):
           
    #Initialize errlvl to zero
    errlvl=0
        
    #Check TRANSACTION_AMT value
    if ( TRANSACTION_AMT == '' ):
        errlvl=1
        
    return errlvl  

def checkZIP(ZIP_CODE):
    
    #Initialize errlvl to zero
    errlvl=0
    
    #Check ZIP_CODE proper length --- extra digits already removed
    if ( len(ZIP_CODE) < 5 ):
        errlvl=1
        
    return errlvl  

def checkOTHER(OTHER_ID): 
    
    #Initialize errlvl to zero
    errlvl=0
      
    #Check OTHER_ID value
    if ( OTHER_ID != '' ):
        errlvl=1

    return errlvl  
  
def getUID(NAME,ZIP):
    
    #Split first and last
    n_split=NAME.split(',')
    #Split first with middle name or initial
    fn_split=n_split[1].split()
    
    #If middle name or initial present
    if (len(fn_split)==2):
        UID = ZIP + n_split[0] + fn_split[0] + fn_split[1]
    else:
        UID = ZIP + n_split[0] + fn_split[0] 
        
    return UID
    