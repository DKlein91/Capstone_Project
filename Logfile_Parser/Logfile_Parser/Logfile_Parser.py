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

    ParseLogfileRecord(page[64:])
    

def ParseLogfileRecord(record):
    #Record Header
    currentLSN = struct.unpack("<q",record[:8])[0]
    previousLSN = struct.unpack("<q",record[8:16])[0]
    clientDataLength = struct.unpack("<i",record[24:28])[0]
    if struct.unpack("<i",record[32:36])[0] in RecordTypeDictionary:
        recordType = RecordTypeDictionary[struct.unpack("<i",record[32:36])[0]]
    else:
        recordType = struct.unpack("<i",record[32:36])[0]
    if struct.unpack("<H",record[40:42])[0] in LogfileRecordFlagDictionary:
        flags = LogfileRecordFlagDictionary[struct.unpack("<h",record[40:42])[0]]
    else:
        flags = struct.unpack("<H",record[40:42])[0]
    if struct.unpack("<H",record[48:50])[0] in OPDictionary:
        redoOP = OPDictionary[struct.unpack("<H",record[48:50])[0]]
    else:
        redoOP = struct.unpack("<H",record[48:50])[0]
    if struct.unpack("<H",record[50:52])[0] in OPDictionary:
        undoOP = OPDictionary[struct.unpack("<H",record[50:52])[0]]
    else:
        undoOP = struct.unpack("<H",record[50:52])[0]
    redoOffset = struct.unpack("<H",record[52:54])[0]
    redoLength = struct.unpack("<H",record[54:56])[0]
    undoOffset = struct.unpack("<H",record[56:58])[0]
    undoLength = struct.unpack("<H",record[58:60])[0]
    targetAttribute = struct.unpack("<h",record[60:62])[0]
    lcnToFollow = struct.unpack("<h",record[62:64])[0]
    recordOffset = struct.unpack("<H",record[64:66])[0]
    attributeOffset = struct.unpack("<H",record[66:68])[0]
    mftClusterIndex = struct.unpack("<h",record[68:70])[0]
    targetVCN = struct.unpack("<i",record[72:76])[0]
    targetLCN = struct.unpack("<i",record[80:84])[0]
    
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

if __name__ == "__main__":
    drive = open(r"\\.\C:","rb")

    bpb = drive.read(84)

    bytesPerSector = struct.unpack("<h",bpb[11:13])[0]
    sectorsPerCluster = struct.unpack("<b",bpb[13:14])[0]
    mftClusterNumber = struct.unpack("<q",bpb[48:56])[0]        #logical MFT file cluster number
    clustersPerMFTRecord = struct.unpack("<b",bpb[64:65])[0]    #clusters per MFT record
    if(clustersPerMFTRecord < 0):
        clustersPerMFTRecord = 2 ** abs(clustersPerMFTRecord)

    mftLocation = bytesPerSector * sectorsPerCluster * mftClusterNumber
    mftRecordSize = 1024

    drive.seek(0)
    drive.seek(mftLocation + mftRecordSize*2)

    logfileMFTRecord = drive.read(mftRecordSize)

    logfileLocation,logfileSize = ParseLogfileMFTRecord(logfileMFTRecord)

    drive.seek(0)
    drive.seek(bytesPerSector * sectorsPerCluster * logfileLocation)
    logfile = drive.read(bytesPerSector * sectorsPerCluster * logfileSize)

    logfilePageSize = struct.unpack("<i",logfile[20:24])[0]

    ParseLogfile(logfile, logfilePageSize)
#    ParseLogfileRestartArea(logfile[:logfilePageSize])
    print()
#    ParseLogfileRestartArea(logfile[logfilePageSize:logfilePageSize*2])
    print()
#    ParseLogfilePage(logfile[logfilePageSize*4:logfilePageSize*5])
#    print(struct.unpack("<q",logfile[:8]))