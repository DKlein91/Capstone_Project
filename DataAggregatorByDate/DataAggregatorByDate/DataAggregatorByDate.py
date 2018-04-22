import datetime
import csv
import os
import codecs

#Global variables
epoch = datetime.datetime(1601,1,1)
currentDate = datetime.datetime.now()
prefetchCSVFolder = "C:\\Users\\dmk16\\Documents\\Prefetch_Results"
LNKResultsFile = "C:\\Users\\dmk16\\Documents\\GitHub\\Capstone_Project\\LNK_Inspector\\PythonApplication2\\LNKData.csv"
jumpListCSVFolder = "C:\\Users\\dmk16\\Documents\\JumpList"
AppCompatCacheResultsFile = "C:\\Users\\dmk16\\Documents\\AppCompatCacheResults.csv"
windowsTrashResultsFile = "C:\\Users\\dmk16\\Desktop\\trashData.csv"
#shellbagsResultsFile
#usnJrnlResultsFile
#logfileResultsFile
#indexDatResultsFile

    #Accepts four booleans representing the types of dates selected by user and optional start dates and end dates. Outputs all results into a csv file
def SearchByDateRange(created, accessed, modified, deleted, startDate = epoch, endDate = currentDate):
    #Set up the results output file
    resultsFile = open("SearchByDateRangeResults.csv","w",newline="")
    output = csv.writer(resultsFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers = ["File","Location"]   #These headers will be on every result

    #Define unique headers for each date type selected
    createdHeaders = ["First Run", "User", "Local/Network"]
    accessedHeaders = ["Last Run 1", "Last Run 2", "Last Run 3", "Last Run 4", "Last Run 5", "Last Run 6", "Last Run 7", "Last Run 8", "Run Count", "Volume Type", "Volume Serial", "User", "MAC Address"]
    modifiedHeaders = ["Last Modified"]
    deletedHeaders = ["File Size", "Deleted"]

    #Begin checking which types of dates were selected
    #Only created dates
    if(created == True and accessed == False and modified == False and deleted == False):
        headers += createdHeaders
        output.writerow(headers)
        GatherCreationDateInfo()

    #Only accessed dates
    elif(created == False and accessed == True and modified == False and deleted == False):
        headers += accessedHeaders
        output.writerow(headers)
        GatherAccessedDateInfo(startDate,endDate,output)

    #Only modified dates
    elif(created == False and accessed == False and modified == True and deleted == False):
        headers += modifiedHeaders
        output.writerow(headers)
        GatherModifiedDateInfo()

    #Only deleted dates
    elif(created == False and accessed == False and modified == False and deleted == True):
        headers += deletedHeaders
        output.writerow(headers)
        GatherDeletedDateInfo()

    #Only created and accessed dates
    elif(created == True and accessed == True and modified == False and deleted == False):
        headers += createdHeaders
        headers += accessedHeaders
        output.writerow(headers)
        GatherCreationAccessedDateInfo()

    #Only created and modified dates
    elif(created == True and accessed == False and modified == True and deleted == False):
        headers += createdHeaders
        headers += modifiedHeaders
        output.writerow(headers)
        GatherCreationModifiedDateInfo()

    #Only created and deleted dates
    elif(created == True and accessed == False and modified == False and deleted == True):
        headers += createdHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherCreationDeletedDateInfo()

    #Only accessed and modified dates
    elif(created == False and accessed == True and modified == True and deleted == False):
        headers += accessedHeaders
        headers += modifiedHeaders
        output.writerow(headers)
        GatherAccessedModifiedDateInfo()

    #Only accessed and deleted dates
    elif(created == False and accessed == True and modified == False and deleted == True):
        headers += accessedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherAccessedDeletedDateInfo()

    #Only modified and deleted dates
    elif(created == False and accessed == False and modified == True and deleted == True):
        headers += modifiedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherModifiedDeletedDateInfo()

    #Only created and accessed and modified dates
    elif(created == True and accessed == True and modified == True and deleted == False):
        headers += createdHeaders
        headers += accessedHeaders
        headers += modifiedHeaders
        output.writerow(headers)
        GatherCreationAccessedModifiedDateInfo()

    #Only created and accessed and deleted dates
    elif(created == True and accessed == True and modified == False and deleted == True):
        headers += createdHeaders
        headers += accessedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherCreationAccessedDeletedDateInfo()

    #Only created and modified and deleted dates
    elif(created == True and accessed == False and modified == True and deleted == True):
        headers += createdHeaders
        headers += modifiedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherCreationModifiedDeletedDateInfo()

    #Only accessed and modified and deleted dates
    elif(created == False and accessed == True and modified == True and deleted == True):
        headers += accessedHeaders
        headers += modifiedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherAccessedModifiedDeletedDateInfo()

    #ALL types of dates
    elif(created == True and accessed == True and modified == True and deleted == True):
        headers += createdHeaders
        headers += accessedHeaders
        headers += modifiedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GetALLDateInfo()

    #Return no dates selected message if no date types were selected
    else:
        message = "No date types selected!"
        return message                    

def GatherCreationDateInfo(startDate, endDate, outputFile):
#    for file in os.listdir(prefetchCSVFolder):
#        row.append(file)
#        location = os.path.join(prefetchCSVFolder, file)
#        row.append(location)
#        readThisFile = open(location, "r")
#        csv_readThisFile = csv.reader(readThisFile)
#        for i in csv_readThisFile:
#            try:
    return

def GatherAccessedDateInfo(startDate, endDate, outputFile):
    #Extract info from prefetch files first
    for file in os.listdir(prefetchCSVFolder):
        if(file == "indexPrefetch.csv"): #This file is different from the others so I elected to skip it
            continue
        
        row = []
        
        #Open prefetch csv result file
        location = os.path.join(prefetchCSVFolder, file)
        readThisFile = open(location, "r")
        csv_readThisFile = csv.reader(readThisFile)

        #Check if any of the last run dates are within the date range
        lastRunDates = []
        runCount = 0
        count = 0
        for i in csv_readThisFile:
            if(len(i[1]) > 0 and count > 0):                #Confirm the cell is not blank and is not the header
                date = ConvertCSVDateToDateTime(i[1])
                if(date > startDate and date < endDate):
                    lastRunDates.append(i[1])               #If date is between the given dates, pull it to be displayed
            else:
                count += 1
                continue                                    #If cell is blank or the header, skip it
            if(count == 1):                                 #Confirm the reader is on the first row (where the run count is stored)
                runCount = i[2]
            count += 1                                      #Keep counting so runCount will not be overwritten with a blank cell
        if(len(lastRunDates) <= 0):                         #Dates are only stored if within the range. If no dates were in the range, skip this file.
            continue
        row.append(file[:len(file)-4])                      #Add filename minus ".csv"
        row.append(location)                                #Add file location
        for i in lastRunDates:  
            row.append(i)                                   #Add each date run
        for i in range(0, 8-len(lastRunDates)):             #If 8 dates were not pulled, skip the rest of the date cells
            row.append("")
        row.append(runCount)                                #Add number of times program was run
        readThisFile.close()                                #Close the prefetch results file
        outputFile.writerow(row)                            #Write the row to the aggregated results file

    #Extract info from the LNK results csv file second
    readThisFile = open(LNKResultsFile,"r")                 #Open LNK results file
    csv_readThisFile = csv.reader(readThisFile)             #Set up csv reader

    count = 0
    for i in csv_readThisFile:
        if(count == 0):                                     #Confirm the row is not the header
            count += 1
            continue                                        #Skip row if header
        
        row = []

        filename,filepath = CarveFilenameFromPath(i[9])
        row.append(filename)                                #Add filename
        row.append(filepath)                                #Add file path
        if(len(i[2]) > 0):                                  #Confirm the date cell is not blank
            date = ConvertCSVDateToDateTime(i[2])
            if(date >= startDate and date <= endDate):
                row.append(i[2])
            else:
                continue                                    #If date is not within range, skip record
        else:
            continue                                        #If no date, skip record
        for j in range(0,8):
            row.append("")                                  #Skip the next 8 cells as LNK files only have one Accessed date and no Run Count
        row.append(i[6])                                    #Add volume type
        row.append(i[7])                                    #Add volume serial number

        #This code pulls the username from the file path
        if(i[0].find("Users")):                             #Confirm username is in file path
            user = CarveUserFromPath(i[0])
            row.append(user)                                #Add username
        else:
            row.append("")                                  #If no username, add blank cell
        outputFile.writerow(row)                            #Write row to the aggregated results file
    readThisFile.close()                                    #Close the LNK results file

    #Extract info from the Jump List result files third
    for file in os.listdir(jumpListCSVFolder):
        if(file[16:24] != "DestList"):                      #The folder has two types of files: -LinkFiles.csv and DestList.csv. The -LinkFiles are blank. We only want the DestList files.
            continue                                        #If not a DestList file, skip it

        #Open Jump List result file
        readThisFile = open(os.path.join(jumpListCSVFolder, file), "r")
        csv_readThisFile = csv.reader(x.replace('\0', '') for x in readThisFile)

        count = 0
        for i in csv_readThisFile:
            if(count == 0):                                 #Confirm the row is not the header
                count += 1
                continue                                    #Skip row if header

            row = []
        
            name,path = CarveFilenameFromPath(i[9])
            row.append(name)                                #Add filename
            row.append(path)                                #Add file path
            if(len(i[7]) > 0):                              #Confirm the date cell is not blank
                date = ConvertCSVDateToDateTime(i[7])
                if(date >= startDate and date <= endDate):
                    row.append(i[7])                        #Add last accessed date
                else:
                    continue                                #If date is not within range, skip record
            else:
                continue                                    #If no date, skip record
            for j in range(0,7):                            #Skip the next 7 cells as Jump List files only have one Accessed date
                row.append("")
            row.append(i[3])                                #Add run count
            row.append("")                                  #Skip volume type
            row.append("")                                  #Skip volume serial
            if(i[9].find("Users")):                         #Confirm username is in file path
                user = CarveUserFromPath(i[9])
                row.append(user)                            #Add username
            else:
                row.append("")                              #If username is not in file path, skip username field
            row.append(i[8])                                #Add MAC Address
            outputFile.writerow(row)                        #Write row to the aggregated results file
        readThisFile.close()                                #Close Jump List result file
    return

def GatherModifiedDateInfo(startDate, endDate, outputFile):
    return

def GatherDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationAccessedDateInfo(startDate, endDate, outputFile):
    GatherAccessedDateInfo(startDate, endDate, outputFile)
    return

def GatherCreationModifiedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherAccessedModifiedDateInfo(startDate, endDate, outputFile):
    GatherAccessedDateInfo(startDate, endDate, outputFile)
    return

def GatherAccessedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherModifiedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationAccessedModifiedDateInfo(startDate, endDate, outputFile):
    GatherAccessedDateInfo(startDate, endDate, outputFile)
    return

def GatherCreationAccessedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationModifiedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherAccessedModifiedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GetALLDateInfo(startDate, endDate, outputFile):
    return
    
    #Accepts a date string and returns a datetime object
def ConvertCSVDateToDateTime(stringDate):
    try:
        datetimeObject = datetime.datetime.strptime(stringDate[:19], "%Y-%m-%d %H:%M:%S")   #Converts datetime from a specific format in the csv file 
    except:
        datetimeObject = datetime.datetime.strptime(stringDate[:19], "%d %b %Y %H:%M:%S")   #Converts datetime from another specific format in the csv file
    return datetimeObject

    #Accepts a complete file path string and separates and returns the name and location of the file
def CarveFilenameFromPath(pathString):
    filenameStart = pathString.rfind("\\")              #Starts from the end of the file path string and navigates backwards to the character indicated, which in this case is \
    name = pathString[filenameStart+1:]                 #Carves the name from the file path, minus the \
    path = pathString[:filenameStart]                   #Gets the file path minus the name
    return name,path

    #Accepts a file path string and returns the username carved from it
def CarveUserFromPath(pathString):
    userStart = pathString.find("Users\\")              #Finds the where the username begins
    user = pathString[userStart+6:]                     #Carves from beginning of username (+6 is to skip the "Users\\") to the end of the file path
    userEnd = user.find("\\")                           #Finds the next \ which is where the username ends
    user = user[:userEnd]                               #Carves username from remaining path
    return user

if __name__ == "__main__":
#    start = datetime.datetime(2018,4,1)        
#    end = datetime.datetime(2018,4,7)
    SearchByDateRange(False, True, False, False)