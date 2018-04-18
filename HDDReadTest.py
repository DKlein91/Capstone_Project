from io import BytesIO
import binascii
import struct
import datetime

OPDictionary = {
    0 : "No OP",
    1 : "Compensation Log Record",
    2 : "Initialize File Record Segment",
    3 : "Deallocate File Record Segment",
    4 : "Write EOF Record Segment",
    5 : "Create Attribute",
    6 : "Delete Attribute",
    7 : "Update Resident Value",
    8 : "Update Non-Resident Value",
    9 : "Update Mapping Pairs",
    10 : "Delete Dirty Clusters",
    11 : "Set New Attribute Sizes",
    12 : "Add Index Entry Root",
    13 : "Delete Index Entry Root",
    15 : "Add Index Entry Allocation",
    18 : "Set Index Entry Ven Allocation",
    19 : "Update File Name Root",
    20 : "Update File Name Allocation",
    21 : "Set Bits In Non-Resident Bit Map",
    22 : "Clear Bits In Non-Resident Bit Map",
    25 : "Prepare Transaction",
    26 : "Commit Transaction",
    27 : "Forget Transaction",
    28 : "Open Non-Resident Attribute",
    31 : "Dirty Page Table Dump",
    32 : "Transaction Table Dump",
    33 : "Update Record Data Root"
}

RecordTypeDictionary = {
    1 : "General",
    2 : "Checkpoint"
}

LogfileRecordFlagDictionary = {
    0 : "Doesn't Cross Current Page",
    1 : "Crosses Current Page"
}

def ParseLogfileMFTRecord(record):
    if(str(record[:4]) != "b'FILE'"):
        print("This is not a MFT Record!")
        return

    #MFT Record Header
    firstAttOffset = struct.unpack("<h",record[20:22])[0]

    attType = struct.unpack("<i",record[firstAttOffset:firstAttOffset+4])[0]
    attOffset = firstAttOffset

    #Find Data Attribute
    while(attType != 128):
        attOffset = attOffset + struct.unpack("<i",record[attOffset+4:attOffset+8])[0]
        attType = struct.unpack("<i",record[attOffset:attOffset+4])[0]

    attLength = struct.unpack("<i",record[attOffset+4:attOffset+8])[0]
    attResidentFlag = struct.unpack("<b",record[attOffset+8:attOffset+9])[0]

    logfileLoc,logfileSize = ParseDataAttribute(record[attOffset:attOffset+attLength], attLength)

    return logfileLoc,logfileSize

def ParseDataAttribute(attribute, attLength):
    runlistStartCluster = struct.unpack("<q",attribute[16:24])[0]
    runlistEndCluster = struct.unpack("<q",attribute[24:32])[0]
    runlistOffset = struct.unpack("<h",attribute[32:34])[0]
    compressionUnitSize = struct.unpack("<h",attribute[34:36])[0]
    allocatedContentSize = struct.unpack("<q",attribute[40:48])[0]
    actualContentSize = struct.unpack("<q",attribute[48:56])[0]
    initializedContentSize = struct.unpack("<q",attribute[56:64])[0]

    location,size = ParseDataRun(attribute[runlistOffset:attLength])
    return location,size


def ParseDataRun(content):
    dataRunHeader = str(binascii.hexlify(content[:1]))
    offsetBytes = int(dataRunHeader[2])
    lengthBytes = int(dataRunHeader[3])

    length = int(binascii.hexlify(content[lengthBytes:0:-1]),16)    
    offset = int(binascii.hexlify(content[lengthBytes+offsetBytes:lengthBytes:-1]),16)

    return offset,length

def ParseLogfile(logfile, pageSize):
    #Skip Restart Area of Logfile
    loggingAreaStart = pageSize * 2

    if(str(logfile[loggingAreaStart:loggingAreaStart + 4]) != "b'RCRD'"):
        print("This is not a $Logfile page!")
        return
    
    i = 0
    while True:
        try:
            print("Page: " + str(i))
            ParseLogfilePage(logfile[loggingAreaStart + pageSize*i:loggingAreaStart + pageSize*(i+1)])
            print()
            i += 1
        except:
            ParseLogfilePage(logfile[loggingAreaStart + pageSize*i:])
            break

    #Page Header
    updateSequenceOffset = struct.unpack("<h",logfile[loggingAreaStart+4:loggingAreaStart+6])[0]
    updateSequenceCount = struct.unpack("<h",logfile[loggingAreaStart+6:loggingAreaStart+8])[0]
    lastLSN = struct.unpack("<q",logfile[loggingAreaStart+8:loggingAreaStart+16])[0]
    pageCount = struct.unpack("<h",logfile[loggingAreaStart+20:loggingAreaStart+22])[0]
    pagePosition = struct.unpack("<h",logfile[loggingAreaStart+22:loggingAreaStart+24])[0]
    nextRecordOffset = struct.unpack("<h", logfile[loggingAreaStart+24:loggingAreaStart+26])[0]
    lastEndLSN = struct.unpack("<q", logfile[loggingAreaStart+32:loggingAreaStart+40])[0]
    updateSequenceValue = struct.unpack("<h",logfile[loggingAreaStart+48:loggingAreaStart+50])[0]

    print("$Logfile Page Header:")
    print("Update Sequence Offset: " + str(updateSequenceOffset))
    print("Update Sequence Count: " + str(updateSequenceCount))
    print("Last LSN: " + str(lastLSN))
    print("Page Count: " + str(pageCount))
    print("Page Position: " + str(pagePosition))
    print("Next Record Offset: " + str(nextRecordOffset))
    print("Last End LSN: " + str(lastEndLSN))
#    print("Update Sequence Value: " + str(updateSequenceValue))

#    print(page)

#    ParseLogfileRecord(logfile[nextRecordOffset:])

#    ParseLogfilePage(logfile[len(logfile)-pageSize*7:])

def ParseLogfilePage(page):
    if(str(page[:4]) != "b'RCRD'"):
        print("This is not a $Logfile page!")
        return
    
    #Page Header
    updateSequenceOffset = struct.unpack("<h",page[4:6])[0]
    updateSequenceCount = struct.unpack("<h",page[6:8])[0]
    lastLSN = struct.unpack("<q",page[8:16])[0]
    pageCount = struct.unpack("<h",page[20:22])[0]
    pagePosition = struct.unpack("<h",page[22:24])[0]
    nextRecordOffset = struct.unpack("<h", page[24:26])[0]
    lastEndLSN = struct.unpack("<q", page[32:40])[0]
    updateSequenceValue = struct.unpack("<h",page[48:50])[0]

    print("$Logfile Page Header:")
    print("Update Sequence Offset: " + str(updateSequenceOffset))
    print("Update Sequence Count: " + str(updateSequenceCount))
    print("Last LSN: " + str(lastLSN))
    print("Page Count: " + str(pageCount))
    print("Page Position: " + str(pagePosition))
    print("Next Record Offset: " + str(nextRecordOffset))
    print("Last End LSN: " + str(lastEndLSN))
#    print("Update Sequence Value: " + str(updateSequenceValue))

#    print(page)

    ParseLogfileRecord(page[64:], nextRecordOffset)
    

def ParseLogfileRecord(record, offset):
    #Record Header
    print(struct.unpack("<h",record[offset+30:offset+32])[0])
    
    currentLSN = struct.unpack("<q",record[offset:offset+8])[0]
    previousLSN = struct.unpack("<q",record[offset+8:offset+16])[0]
    clientDataLength = struct.unpack("<i",record[offset+24:offset+28])[0]
    if struct.unpack("<i",record[offset+32:offset+36])[0] in RecordTypeDictionary:
        recordType = RecordTypeDictionary[struct.unpack("<i",record[offset+32:offset+36])[0]]
    else:
        recordType = struct.unpack("<i",record[offset+32:offset+36])[0]
    if struct.unpack("<H",record[offset+40:offset+42])[0] in LogfileRecordFlagDictionary:
        flags = LogfileRecordFlagDictionary[struct.unpack("<h",record[offset+40:offset+42])[0]]
    else:
        flags = struct.unpack("<H",record[offset+40:offset+42])[0]
    if struct.unpack("<H",record[offset+48:offset+50])[0] in OPDictionary:
        redoOP = OPDictionary[struct.unpack("<H",record[offset+48:offset+50])[0]]
    else:
        redoOP = struct.unpack("<H",record[offset+48:offset+50])[0]
    if struct.unpack("<H",record[offset+50:offset+52])[0] in OPDictionary:
        undoOP = OPDictionary[struct.unpack("<H",record[offset+50:offset+52])[0]]
    else:
        undoOP = struct.unpack("<H",record[offset+50:offset+52])[0]
    redoOffset = struct.unpack("<H",record[offset+52:offset+54])[0]
    redoLength = struct.unpack("<H",record[offset+54:offset+56])[0]
    undoOffset = struct.unpack("<H",record[offset+56:offset+58])[0]
    undoLength = struct.unpack("<H",record[offset+58:offset+60])[0]
    targetAttribute = struct.unpack("<h",record[offset+60:offset+62])[0]
    lcnToFollow = struct.unpack("<h",record[offset+62:offset+64])[0]
    recordOffset = struct.unpack("<H",record[offset+64:offset+66])[0]
    attributeOffset = struct.unpack("<H",record[offset+66:offset+68])[0]
    mftClusterIndex = struct.unpack("<h",record[offset+68:offset+70])[0]
    targetVCN = struct.unpack("<i",record[offset+72:offset+76])[0]
    targetLCN = struct.unpack("<i",record[offset+80:offset+84])[0]
    
    print("\nRecord Header:")
    print("Current LSN: " + str(currentLSN))
    print("Previous LSN: " + str(previousLSN))
    print("Client Data Length: " + str(clientDataLength))
    print("Record Type: " + str(recordType))
    print("Flags: " + str(flags))
    print("Redo OP: " + str(redoOP))
    print("Undo OP: " + str(undoOP))
    print("Redo Offset: " + str(redoOffset))
    print("Redo Length: " + str(redoLength))
    print("Undo Offset: " + str(undoOffset))
    print("Undo Length: " + str(undoLength))
    print("Target Attribute: " + str(targetAttribute))
    print("LCN To Follow?: " + str(lcnToFollow))
    print("Record Offset: " + str(recordOffset))
    print("Attribute Offset: " + str(attributeOffset))
    print("MFT Cluster Index: " + str(mftClusterIndex))
    print("Target VCN: " + str(targetVCN))
    print("Target LCN: " + str(targetLCN))

    i = offset
    findThisLSN = previousLSN
    while(findThisLSN != struct.unpack("<q",record[i-8:i])[0]):
        print(struct.unpack("<q",record[i-8:i])[0])
        i -= 1
    
    return i
    

if __name__ == "__main__":
    drive = open(r"D:\testfile1.img","rb")

    bpb = drive.read(84)

    bytesPerSector = struct.unpack("<h",bpb[11:13])[0]
    sectorsPerCluster = struct.unpack("<b",bpb[13:14])[0]
    mftClusterNumber = struct.unpack("<q",bpb[48:56])[0]        #logical MFT file cluster number
    clustersPerMFTRecord = struct.unpack("<b",bpb[64:65])[0]    #clusters per MFT record
    if(clustersPerMFTRecord < 0):
        clustersPerMFTRecord = 2 ** abs(clustersPerMFTRecord)

    print("Bytes Per Sector: " + str(bytesPerSector))
    print("Sectors Per Cluster: " + str(sectorsPerCluster))

    mftLocation = bytesPerSector * sectorsPerCluster * mftClusterNumber
    mftRecordSize = clustersPerMFTRecord

    drive.seek(0)
    drive.seek(mftLocation)

    MFTRecord = drive.read(1024)
    MFTMirror = drive.read(1024)
    logfile = drive.read(1024)

    mftLogfileSequenceNumber = struct.unpack("<q",MFTRecord[8:16])[0]
    mftSequenceNumber = struct.unpack("<h",MFTRecord[16:18])[0]
    mftHardLinkCount = struct.unpack("<h",MFTRecord[18:20])[0]
    firstAttOffset = struct.unpack("<h",MFTRecord[20:22])[0]
    mftRecordNumber = struct.unpack("<i",MFTRecord[44:48])[0]

    print("Logfile Sequence Number: " + str(mftLogfileSequenceNumber))
    print("Sequence Number: " + str(mftSequenceNumber))
    print("Hard Link Count: " + str(mftHardLinkCount))
    print("First Attribute Offset: " + str(firstAttOffset))
    print("MFT Record Number: " + str(mftRecordNumber))

   
    #$Standard_Information Header
    attType = MFTRecord[firstAttOffset:firstAttOffset+4]
    attLength = struct.unpack("<i",MFTRecord[firstAttOffset+4:firstAttOffset+8])[0]
    attResidentFlag = struct.unpack("<b",MFTRecord[firstAttOffset+8:firstAttOffset+9])[0]
    attNameLength = struct.unpack("<b",MFTRecord[firstAttOffset+9:firstAttOffset+10])[0]
    attNameOffset = struct.unpack("<h",MFTRecord[firstAttOffset+10:firstAttOffset+12])[0]
    attFlags = struct.unpack("<h",MFTRecord[firstAttOffset+12:firstAttOffset+14])[0]
    attID = struct.unpack("<h",MFTRecord[firstAttOffset+14:firstAttOffset+16])[0]
    contentLength = struct.unpack("<i",MFTRecord[firstAttOffset+16:firstAttOffset+20])[0]
    contentOffset = struct.unpack("<h",MFTRecord[firstAttOffset+20:firstAttOffset+22])[0]

    #$Standard_Information
    createDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+24:firstAttOffset+32])[0]
    modifiedDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+32:firstAttOffset+40])[0]
    mftModifiedDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+40:firstAttOffset+48])[0]
    accessedDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+48:firstAttOffset+56])[0]
    flags = MFTRecord[firstAttOffset+56:firstAttOffset+60]
    maxVersions = struct.unpack("<i",MFTRecord[firstAttOffset+60:firstAttOffset+64])[0]
    classID = struct.unpack("<i",MFTRecord[firstAttOffset+64:firstAttOffset+68])[0]
    ownerID = struct.unpack("<i",MFTRecord[firstAttOffset+68:firstAttOffset+72])[0]
    securityID = struct.unpack("<i",MFTRecord[firstAttOffset+72:firstAttOffset+76])[0]
    quotaCharged = struct.unpack("<q",MFTRecord[firstAttOffset+76:firstAttOffset+84])[0]
    updateSequenceNumber = struct.unpack("<q",MFTRecord[firstAttOffset+84:firstAttOffset+92])[0]

    print("\n$Standard_Information Header")
    print("Attribute Type: " + str(attType))
    print("Attribute Length: " + str(attLength))
    print("Attribute Resident: " + str(attResidentFlag))
    print("Attribute Name Length: " + str(attNameLength))
    print("Attribute Name Offset: " + str(attNameOffset))
    print("Attribute Flags: " + str(attFlags))
    print("Attribute ID: " + str(attID))
    print("Content Length: " + str(contentLength))
    print("Content Offset: " + str(contentOffset))

    print("\n$Standard_Information")

    startDate = datetime.datetime(1601,1,1)

    dateCreated = startDate + datetime.timedelta(microseconds=createDateOffset/10)
    dateModified = startDate + datetime.timedelta(microseconds=modifiedDateOffset/10)
    dateMFTModified = startDate + datetime.timedelta(microseconds=mftModifiedDateOffset/10)
    dateAccessed = startDate + datetime.timedelta(microseconds=accessedDateOffset/10)

    print("Date Created: " + str(dateCreated))
    print("Date Modified: " + str(dateModified))
    print("Date MFT Modified: " + str(dateMFTModified))
    print("Date Accessed: " + str(dateAccessed))
    print("Flags: " + str(flags))
    print("Max Versions: " + str(maxVersions))
    print("Class ID: " + str(classID))
    print("Owner ID: " + str(ownerID))
    print("Security ID: " + str(securityID))
    print("Quota Charged: " + str(quotaCharged))
    print("Update Sequence Number: " + str(updateSequenceNumber))

    #$File_Name Header
    print("\n$File_Name Header")
    print("Attribute Type: " + str(MFTRecord[firstAttOffset+96:firstAttOffset+100]))
    print("Attribute Length: " + str(struct.unpack("<i",MFTRecord[firstAttOffset+100:firstAttOffset+104])[0]))
    print("Attribute Resident: " + str(MFTRecord[firstAttOffset+104:firstAttOffset+105]))
    print("Attribute Name Length: " + str(struct.unpack("<b",MFTRecord[firstAttOffset+105:firstAttOffset+106])[0]))
    print("Attribute Name Offset: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+106:firstAttOffset+108])[0]))
    print("Attribute Flags: " + str(MFTRecord[firstAttOffset+108:firstAttOffset+110]))
    print("Attribute ID: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+110:firstAttOffset+112])[0]))
    print("Content Length: " + str(struct.unpack("<i",MFTRecord[firstAttOffset+112:firstAttOffset+116])[0]))
    print("Content Offset: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+116:firstAttOffset+118])[0]))

    print("\n$File_Name")

    fnCreateDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+128:firstAttOffset+136])[0]
    fnModifiedDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+136:firstAttOffset+144])[0]
    fnMFTModifiedDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+144:firstAttOffset+152])[0]
    fnAccessedDateOffset = struct.unpack("<q",MFTRecord[firstAttOffset+152:firstAttOffset+160])[0]

    fnDateCreated = startDate + datetime.timedelta(microseconds=fnCreateDateOffset/10)
    fnDateModified = startDate + datetime.timedelta(microseconds=fnModifiedDateOffset/10)
    fnDateMFTModified = startDate + datetime.timedelta(microseconds=fnMFTModifiedDateOffset/10)
    fnDateAccessed = startDate + datetime.timedelta(microseconds=fnAccessedDateOffset/10)

    print("MFT Parent Directory: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+120:firstAttOffset+128])[0]))
    print("File Created: " + str(fnDateCreated))
    print("File Modified: " + str(fnDateModified))
    print("File MFT Modified: " + str(fnDateMFTModified))
    print("File Accessed: " + str(fnDateAccessed))
    print("Logical File Size: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+160:firstAttOffset+168])[0]))
    print("Physical File Size: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+168:firstAttOffset+176])[0]))
    print("Flags: " + str(MFTRecord[firstAttOffset+176:firstAttOffset+180]))
    print("Extended Attributes: " + str(MFTRecord[firstAttOffset+180:firstAttOffset+184]))
    print("Filename Length: " + str(struct.unpack("<b",MFTRecord[firstAttOffset+184:firstAttOffset+185])[0]))
    print("Filename Namespace: " + str(MFTRecord[firstAttOffset+185:firstAttOffset+186]))
    print("Filename: " + str(MFTRecord[firstAttOffset+186:firstAttOffset+200].decode('utf-16')))

    offsetDataRuns = (struct.unpack("<h",MFTRecord[firstAttOffset+232:firstAttOffset+234])[0])
    attLength = struct.unpack("<i",MFTRecord[firstAttOffset+204:firstAttOffset+208])[0]
    print("\n$Data Header")
    print("Attribute Type: " + str(MFTRecord[firstAttOffset+200:firstAttOffset+204]))
    print("Attribute Length: " + str(struct.unpack("<i",MFTRecord[firstAttOffset+204:firstAttOffset+208])[0]))
    print("Attribute Resident: " + str(MFTRecord[firstAttOffset+208:firstAttOffset+209]))
    print("Attribute Name Length: " + str(MFTRecord[firstAttOffset+209:firstAttOffset+210]))
    print("Attribute Name Offset: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+210:firstAttOffset+212])[0]))
    print("Attribute Flags: " + str(MFTRecord[firstAttOffset+212:firstAttOffset+214]))
    print("Attribute ID: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+214:firstAttOffset+216])[0]))
    print("Starting VCN: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+216:firstAttOffset+224])[0]))
    print("Last VCN: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+224:firstAttOffset+232])[0]))
    print("Offset To Data Runs: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+232:firstAttOffset+234])[0]))
    print("Compression Unit Size: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+234:firstAttOffset+236])[0]))
    print("Allocated Size of Content: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+240:firstAttOffset+248])[0]))
    print("Actual Size of Content: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+248:firstAttOffset+256])[0]))
    print("Initialized Size of Content: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+256:firstAttOffset+264])[0]))
    print("Data Run: " + str(MFTRecord[firstAttOffset+264:firstAttOffset+200+attLength]))

    
    content = MFTRecord[firstAttOffset+264:firstAttOffset+200+attLength]

    datarun = list()

    while content[:1] != b'\x00':

        dataRunHeader = str(binascii.hexlify(content[:1]))
        offsetBytes = int(dataRunHeader[2])
        lengthBytes = int(dataRunHeader[3])

        x = int(binascii.hexlify(content[lengthBytes+offsetBytes:lengthBytes:-1]),16)
        signCheck = '0x7F'
        signNeg = '0x10'
        for i in range(0, lengthBytes):
            signCheck += 'FF'
            signNeg += '00'
        y = int(binascii.hexlify(content[lengthBytes+offsetBytes:lengthBytes:-1]), 16)
        if x > int(signCheck, 16):
            x -= int(signNeg, 16)

        print(x)

        length = int(binascii.hexlify(content[lengthBytes:0:-1]),16)    
        offset = int(binascii.hexlify(content[lengthBytes+offsetBytes:lengthBytes:-1]),16)

        print("Length: " + str(length) + ", " + str(content[lengthBytes:0:-1]))
        print("Offset: " + str(offset)+ ", " + str(content[lengthBytes+offsetBytes:lengthBytes:-1]))
        datarun.append((length, offset))
        content = content[1 + offsetBytes + lengthBytes:]

    drive.seek(0)
    driveLCNLocation = bytesPerSector * sectorsPerCluster * datarun[0][1]
    drive.seek(driveLCNLocation)
    n = 51232
    for i in range( 0, len(datarun)):
        testdatarun = drive.read(n)
        driveLCNLocation += datarun[i][0]
        drive.seek(0)
        drive.seek(driveLCNLocation - n)
        while b"\xff\xff\xff\xff" in testdatarun and len(testdatarun) > 1000:
            print(testdatarun[:testdatarun.index(b"\xff\xff\xff\xff")+4])
            testdatarun = (testdatarun[:testdatarun.index(b"\xff\xff\xff\xff")+4])
    