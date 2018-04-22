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
    if(created == True):
        headers += createdHeaders
        output.writerow(headers)
        GatherCreationDateInfo()

    #Only accessed dates
    elif(accessed == True):
        headers += accessedHeaders
        output.writerow(headers)
        GatherAccessedDateInfo(startDate,endDate,output)

    #Only modified dates
    elif(modified == True):
        headers += modifiedHeaders
        output.writerow(headers)
        GatherModifiedDateInfo()

    #Only deleted dates
    elif(deleted == True):
        headers += deletedHeaders
        output.writerow(headers)
        GatherDeletedDateInfo()

    #Only created and accessed dates
    elif(created == True and accessed == True):
        headers += createdHeaders
        headers += accessedHeaders
        output.writerow(headers)
        GatherCreationAccessedDateInfo()

    #Only created and modified dates
    elif(created == True and modified == True):
        headers += createdHeaders
        headers += modifiedHeaders
        output.writerow(headers)
        GatherCreationModifiedDateInfo()

    #Only created and deleted dates
    elif(created == True and deleted == True):
        headers += createdHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherCreationDeletedDateInfo()

    #Only accessed and modified dates
    elif(accessed == True and modified == True):
        headers += accessedHeaders
        headers += modifiedHeaders
        output.writerow(headers)
        GatherAccessedModifiedDateInfo()

    #Only accessed and deleted dates
    elif(accessed == True and deleted == True):
        headers += accessedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherAccessedDeletedDateInfo()

    #Only modified and deleted dates
    elif(modified == True and deleted == True):
        headers += modifiedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherModifiedDeletedDateInfo()

    #Only created and accessed and modified dates
    elif(created == True and accessed == True and modified == True):
        headers += createdHeaders
        headers += accessedHeaders
        headers += modifiedHeaders
        output.writerow(headers)
        GatherCreationAccessedModifiedDateInfo()

    #Only created and accessed and deleted dates
    elif(created == True and accessed == True and deleted == True):
        headers += createdHeaders
        headers += accessedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherCreationAccessedDeletedDateInfo()

    #Only created and modified and deleted dates
    elif(created == True and modified == True and deleted == True):
        headers += createdHeaders
        headers += modifiedHeaders
        headers += deletedHeaders
        output.writerow(headers)
        GatherCreationModifiedDeletedDateInfo()

    #Only accessed and modified and deleted dates
    elif(accessed == True and modified == True and deleted == True):
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
    for file in os.listdir(prefetchCSVFolder):
        if(file == "indexPrefetch.csv"):
            continue
        row = []
        location = os.path.join(prefetchCSVFolder, file)
        readThisFile = open(location, "r")
        csv_readThisFile = csv.reader(readThisFile)

        #Check if any of the last run dates are within the date range
        lastRunDates = []
        runCount = 0
        count = 0
        for i in csv_readThisFile:
            if(len(i[1]) > 0 and count > 0):
                date = ConvertCSVDateToDateTime(i[1])
                if(date > startDate and date < endDate):
                    lastRunDates.append(i[1])
            else:
                count += 1
                continue
#            if(count == 1):
#                runCount = int(i[2])
        if(len(lastRunDates) <= 0):
            continue
        row.append(file[:len(file)-4])
        row.append(location)
        for i in lastRunDates:
            row.append(i)
        for i in range(0, 8-len(lastRunDates)):
            row.append("")
        row.append(runCount)
        readThisFile.close()
        outputFile.writerow(row)

    readThisFile = open(LNKResultsFile,"r")
    csv_readThisFile = csv.reader(readThisFile)
    count = 0
    for i in csv_readThisFile:
        if(count == 0):
            count += 1
            continue
        row = []
        filename,filepath = CarveFilenameFromPath(i[9])
        row.append(filename)
        row.append(filepath)
        if(count > 0 and len(i[2]) > 0):
            date = ConvertCSVDateToDateTime(i[2])
            if(date >= startDate and date <= endDate):
                row.append(i[2])
            else:
                continue
        else:
            continue
        for j in range(0,8):
            row.append("")
        row.append(i[6])
        row.append(i[7])
        if(i[0].find("Users")):
            user = CarveUserFromPath(i[0])
            row.append(user)
        else:
            row.append("")
        outputFile.writerow(row)
    readThisFile.close()

    for file in os.listdir(jumpListCSVFolder):
        if(file[16:24] != "DestList"):
            continue
        readThisFile = open(os.path.join(jumpListCSVFolder, file), "r")
        csv_readThisFile = csv.reader(x.replace('\0', '') for x in readThisFile)

        count = 0
        for i in csv_readThisFile:
            if(count == 0):
                count += 1
                continue
            row = []
            name,path = CarveFilenameFromPath(i[9])
            row.append(name)
            row.append(path)
            if(len(i[7]) > 0):
                date = ConvertCSVDateToDateTime(i[7])
                if(date >= startDate and date <= endDate):
                    row.append(i[7])
                else:
                    row.append("")
                    continue
            else:
                continue
            for j in range(0,7):
                row.append("")
            row.append(i[3])
            row.append("")
            row.append("")
            if(i[9].find("Users")):
                user = CarveUserFromPath(i[9])
                row.append(user)
            else:
                row.append("")
            row.append(i[8])
            outputFile.writerow(row)
        readThisFile.close()
    return

def GatherModifiedDateInfo(startDate, endDate, outputFile):
    return

def GatherDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationAccessedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationModifiedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherAccessedModifiedDateInfo(startDate, endDate, outputFile):
    return

def GatherAccessedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherModifiedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationAccessedModifiedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationAccessedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherCreationModifiedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GatherAccessedModifiedDeletedDateInfo(startDate, endDate, outputFile):
    return

def GetALLDateInfo(startDate, endDate, outputFile):
    return

def ConvertCSVDateToDateTime(stringDate):
    try:
        datetimeObject = datetime.datetime.strptime(stringDate[:19], "%Y-%m-%d %H:%M:%S")
    except:
        datetimeObject = datetime.datetime.strptime(stringDate[:19], "%d %b %Y %H:%M:%S")
    return datetimeObject

def CarveFilenameFromPath(pathString):
    filenameStart = pathString.rfind("\\")
    name = pathString[filenameStart+1:]
    path = pathString[:filenameStart]
    return name,path

def CarveUserFromPath(pathString):
    if(pathString.find("Users\\") > 0):
        userStart = pathString.find("Users\\")
        user = pathString[userStart+6:]
        userEnd = user.find("\\")
        user = user[:userEnd]
    else:
        user = ""
    return user

if __name__ == "__main__":
    SearchByDateRange(False, True, False, True)