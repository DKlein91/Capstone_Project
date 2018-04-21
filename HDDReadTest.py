from io import BytesIO
import binascii
import struct
import datetime
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

def ParseStandardInformationHeader(record):
    attribType = record[:4]
    lengthFile = struct.unpack("<i", record[4:8])[0]
    if b"\x00" in record[8:9]:
        lenStandardAttrib = struct.unpack("<i", record[16:20])[0]
        offsetStandardAttrib = struct.unpack("<h", record[20:22])[0]

    return attribType, lengthFile, lenStandardAttrib, offsetStandardAttrib
 
def ParseFileRecord(record):
    signature = record[:4]
    if signature != b"FILE":
        return
    print("FILE raw: " + str(record[:48]))
    offsetToUpdateSequence = struct.unpack("<h", record[4:6])[0]
    sizeUpdateSequence = struct.unpack("<h", record[6:8])[0]
    offsetFirstAtt = struct.unpack("<h", record[20:22])[0]
    flags = struct.unpack("<h", record[22:24])[0]
    realSizeFILERecord = struct.unpack("<i", record[24:28])[0]
    allocatedSizeFILERecord = struct.unpack("<i", record[28:32])[0]
    referenceBaseFILERecord = struct.unpack("<q", record[32:40])[0]
    numMFTRecord = struct.unpack("<i", record[44:48])[0]

    print("Offset to UpdSeq: " + str(offsetToUpdateSequence))
    print("Size UpdSeq: " + str(sizeUpdateSequence))

    print("offset to the first att: " + str(offsetFirstAtt))
    print("Flags: " + str(flags))
    print("Real size of the FILE Record: " + str(realSizeFILERecord))
    print("Allocated size of FILE record: " + str(allocatedSizeFILERecord))
    print("Reference to the base FILE Record: " + str(referenceBaseFILERecord))
    print("MFT Record Number: " + str(numMFTRecord))
    print("Eof: " + str(record[offsetFirstAtt:]))

    attribType, lengthFile, lenStandardAttrib, offsetStandardAttrib = ParseStandardInformationHeader(record[offsetFirstAtt:])

    print("Attrib Type: " + str(attribType))
    print("Length of File: " + str(lengthFile))
    print("Length of Standard Attribute: " + str(lenStandardAttrib))
    print("Offset of Standard Attribute: " + str(offsetStandardAttrib))

    print("EOF: " + str(record[offsetFirstAtt + lengthFile:]))   
    
def fileNameGrabber(record):
    try:
        if b"\x10\x00\x00\x00" in record:
            record = record[record.index(b"\x10\x00\x00\x00"):]
            standardLength = struct.unpack("<i", record[4:8])[0]
            nameAttrOffset = struct.unpack("<h", record[standardLength+20:standardLength+22])[0]
            nameLength = struct.unpack("<B", record[(standardLength+nameAttrOffset+64):(standardLength+nameAttrOffset+65)])[0]
            name = record[standardLength + nameAttrOffset+66:standardLength+nameAttrOffset+66+(nameLength*2)].decode('utf-16')
            if ".PF" in name:
                print(name)
                print(str(record))
    except Exception as e: 
        return

if __name__ == "__main__":
    drive = open(r"\\.\C:","rb")

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
    testLength = struct.unpack("<i",MFTRecord[firstAttOffset+100:firstAttOffset+104])[0]
    print("Attribute Length: " + str(testLength))
    print("Attribute Resident: " + str(MFTRecord[firstAttOffset+104:firstAttOffset+105]))
    print("Attribute Name Length: " + str(struct.unpack("<b",MFTRecord[firstAttOffset+105:firstAttOffset+106])[0]))
    print("Attribute Name Offset: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+106:firstAttOffset+108])[0]))
    print("Attribute Flags: " + str(MFTRecord[firstAttOffset+108:firstAttOffset+110]))
    print("Attribute ID: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+110:firstAttOffset+112])[0]))
    print("Content Length: " + str(struct.unpack("<i",MFTRecord[firstAttOffset+112:firstAttOffset+116])[0]))
    print("Content Offset: " + str(struct.unpack("<h",MFTRecord[firstAttOffset+116:firstAttOffset+118])[0]))

    print("\n$File_Name")

    print("MFT Parent Directory: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+120:firstAttOffset+128])[0]))
    print("Logical File Size: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+160:firstAttOffset+168])[0]))
    print("Physical File Size: " + str(struct.unpack("<q",MFTRecord[firstAttOffset+168:firstAttOffset+176])[0]))
    print("Flags: " + str(MFTRecord[firstAttOffset+176:firstAttOffset+180]))
    print("Extended Attributes: " + str(MFTRecord[firstAttOffset+180:firstAttOffset+184]))
    print("Filename Length: " + str(struct.unpack("<b",MFTRecord[firstAttOffset+184:firstAttOffset+185])[0]))
    print("Filename Namespace: " + str(MFTRecord[firstAttOffset+185:firstAttOffset+186]))
    print("Filename: " + str(MFTRecord[firstAttOffset+testLength+80:firstAttOffset+testLength+96].decode('utf-16')))

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
        signCheck = '0x7FF'
        signNeg = '0x10000'
        for i in range(0, lengthBytes):
            signCheck += 'FF'
            signNeg += '00'
        y = int(binascii.hexlify(content[lengthBytes+offsetBytes:lengthBytes:-1]), 16)
        if x > int(signCheck, 16):
            x -= int(signNeg, 16)

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
    lastThing = b""
    for i in range( 0, len(datarun)):
        temp = drive.read(datarun[i][0]*bytesPerSector*sectorsPerCluster)
        testdatarun = lastThing + temp
        drive.seek(0)
        drive.seek(driveLCNLocation*bytesPerSector*sectorsPerCluster)
        driveLCNLocation += (datarun[i][1] * bytesPerSector * sectorsPerCluster)
        while b"\xff\xff\xff\xff" in testdatarun and len(testdatarun) > bytesPerSector:
            fileNameGrabber(testdatarun[testdatarun.index(b"FILE"):testdatarun.index(b"\xff\xff\xff\xff")+4])
            testdatarun = testdatarun[4:]
            testdatarun = (testdatarun[testdatarun.index(b"FILE"):])
        lastThing = testdatarun
    
