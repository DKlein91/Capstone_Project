from io import BytesIO
import binascii
import struct
import datetime

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

    ParseLogfilePage(logfile[loggingAreaStart:])

def ParseLogfilePage(page):
    if(str(page[:4]) != "b'RCRD'"):
        print("This is not a $Logfile page!")
        return
    
    #Page Header
    lastLSN = struct.unpack("<q",page[8:16])[0]
    nextRecordOffset = struct.unpack("<h", page[24:26])[0]
    lastEndLSN = struct.unpack("<q", page[32:40])[0]

    print("$Logfile Page Header:")
    print("Last LSN: " + str(lastLSN))
    print("Next Record Offset: " + str(nextRecordOffset))
    print("Last End LSN: " + str(lastEndLSN))

    ParseLogfileRecord(page[nextRecordOffset:])
    

def ParseLogfileRecord(record):
    #Record Header
    currentLSN = struct.unpack("<q",record[:8])[0]
    previousLSN = struct.unpack("<q",record[8:16])[0]
    clientDataLength = struct.unpack("<i",record[24:28])[0]
    recordType = record[32:36]
    flags = record[40:42]
    redoOP = struct.unpack("<h",record[48:50])[0]
    undoOP = struct.unpack("<h",record[50:52])[0]
    redoOffset = struct.unpack("<h",record[52:54])[0]
    redoLength = struct.unpack("<h",record[54:56])[0]
    undoOffset = struct.unpack("<h",record[56:58])[0]
    undoLength = struct.unpack("<h",record[58:60])[0]
    targetAttribute = struct.unpack("<h",record[60:62])[0]
    lcnToFollow = struct.unpack("<h",record[62:64])[0]
    recordOffset = struct.unpack("<h",record[64:66])[0]
    attributeOffset = struct.unpack("<h",record[66:68])[0]
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