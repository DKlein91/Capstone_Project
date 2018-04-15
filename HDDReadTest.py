import pycdlib
import sys
import io
import struct
import binascii
import zipfile
import os
from io import BytesIO
import datetime
from os import listdir

size = 65536

drive = open(r"\\.\C:","rb")
mypath = "D:\\"
os.chdir(mypath)
#drive = open(r"D:\testfile1.img", 'rb')

#print("Live System: ", cdrive.read(size))
#print("Dead System: ", drive.read(size))

bpb = drive.read(84)

bytesPerSector = struct.unpack("<h",bpb[11:13])[0]          #bytes per sector
print("Bytes Per Sector: " + str(bytesPerSector))
sectorsPerCluster = struct.unpack("<b",bpb[13:14])[0]       #sectors per cluster
print("Sectors Per Cluster: " + str(sectorsPerCluster))

mftClusterNumber = struct.unpack("<q",bpb[48:56])[0]        #logical MFT file cluster number
print("MFT Cluster Number: " + str(mftClusterNumber))
clustersPerMFTRecord = struct.unpack("<b",bpb[64:65])[0]    #clusters per MFT record
if(clustersPerMFTRecord < 0):
    clustersPerMFTRecord = 2 ** abs(clustersPerMFTRecord)

mftLocation = bytesPerSector * sectorsPerCluster * mftClusterNumber
print("MFT Location: " + str(mftLocation))
mftRecordSize = bytesPerSector * sectorsPerCluster * clustersPerMFTRecord

drive.seek(0)
drive.seek(mftLocation)

mftRecord = drive.read(1024)
mftMirror = drive.read(1024)
logfile = drive.read(1024)
drive.seek(8192)
extend = drive.read(1024)

mftFileSignature = extend[:4]
mftFixUpArrayPointer = struct.unpack("<h",extend[4:6])[0]
mftFixUpCount = struct.unpack("<h",extend[6:8])[0]
mftLogfileSequenceNumber = struct.unpack("<q",extend[8:16])[0]
mftSequenceNumber = struct.unpack("<h",extend[16:18])[0]
mftHardLinkCount = struct.unpack("<h",extend[18:20])[0]
firstAttOffset = struct.unpack("<h",extend[20:22])[0]
mftUsageFlags = extend[22:24]
mftRecordLogicalSize = struct.unpack("<i",extend[24:28])[0]
mftRecordPhysicalSize = struct.unpack("<i",extend[28:32])[0]
mftParentDirectoryRecordNumber = struct.unpack("<q",extend[32:40])[0]
mftNextAttributeID = struct.unpack("<h",extend[40:42])[0]
mftRecordNumber = struct.unpack("<i",extend[44:48])[0]
print()

print("\nMFT Record Header")
print("Signature: " + str(mftFileSignature))
print("Fix Up Array Pointer: " + str(mftFixUpArrayPointer))
print("Fix Up Count: " + str(mftFixUpCount))
print("Logfile Sequence Number: " + str(mftLogfileSequenceNumber))
print("Sequence Number: " + str(mftSequenceNumber))
print("Hard Link Count: " + str(mftHardLinkCount))
print("First Attribute Offset: " + str(firstAttOffset))
print("Usage Flags: " + str(mftUsageFlags))
print("Record Logical Size: " + str(mftRecordLogicalSize))
print("Record Physical Size: " + str(mftRecordPhysicalSize))
print("Parent Directory Record Number: " + str(mftParentDirectoryRecordNumber))
print("Next Attribute ID: " + str(mftNextAttributeID))
print("MFT Record Number: " + str(mftRecordNumber))

#$Standard_Information Header
attType = extend[firstAttOffset:firstAttOffset+4]
attLength = struct.unpack("<i",extend[firstAttOffset+4:firstAttOffset+8])[0]
attResidentFlag = struct.unpack("<b",extend[firstAttOffset+8:firstAttOffset+9])[0]
attNameLength = struct.unpack("<b",extend[firstAttOffset+9:firstAttOffset+10])[0]
attNameOffset = struct.unpack("<h",extend[firstAttOffset+10:firstAttOffset+12])[0]
attFlags = struct.unpack("<h",extend[firstAttOffset+12:firstAttOffset+14])[0]
attID = struct.unpack("<h",extend[firstAttOffset+14:firstAttOffset+16])[0]
contentLength = struct.unpack("<i",extend[firstAttOffset+16:firstAttOffset+20])[0]
contentOffset = struct.unpack("<h",extend[firstAttOffset+20:firstAttOffset+22])[0]

#$Standard_Information
createDateOffset = struct.unpack("<q",extend[firstAttOffset+24:firstAttOffset+32])[0]
modifiedDateOffset = struct.unpack("<q",extend[firstAttOffset+32:firstAttOffset+40])[0]
mftModifiedDateOffset = struct.unpack("<q",extend[firstAttOffset+40:firstAttOffset+48])[0]
accessedDateOffset = struct.unpack("<q",extend[firstAttOffset+48:firstAttOffset+56])[0]
flags = extend[firstAttOffset+56:firstAttOffset+60]
maxVersions = struct.unpack("<i",extend[firstAttOffset+60:firstAttOffset+64])[0]
classID = struct.unpack("<i",extend[firstAttOffset+64:firstAttOffset+68])[0]
ownerID = struct.unpack("<i",extend[firstAttOffset+68:firstAttOffset+72])[0]
securityID = struct.unpack("<i",extend[firstAttOffset+72:firstAttOffset+76])[0]
quotaCharged = struct.unpack("<q",extend[firstAttOffset+76:firstAttOffset+84])[0]
updateSequenceNumber = struct.unpack("<q",extend[firstAttOffset+84:firstAttOffset+92])[0]

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
print("Attribute Type: " + str(extend[firstAttOffset+96:firstAttOffset+100]))
print("Attribute Length: " + str(struct.unpack("<i",extend[firstAttOffset+100:firstAttOffset+104])[0]))
print("Attribute Resident: " + str(extend[firstAttOffset+104:firstAttOffset+105]))
print("Attribute Name Length: " + str(struct.unpack("<b",extend[firstAttOffset+105:firstAttOffset+106])[0]))
print("Attribute Name Offset: " + str(struct.unpack("<h",extend[firstAttOffset+106:firstAttOffset+108])[0]))
print("Attribute Flags: " + str(extend[firstAttOffset+108:firstAttOffset+110]))
print("Attribute ID: " + str(struct.unpack("<h",extend[firstAttOffset+110:firstAttOffset+112])[0]))
print("Content Length: " + str(struct.unpack("<i",extend[firstAttOffset+112:firstAttOffset+116])[0]))
print("Content Offset: " + str(struct.unpack("<h",extend[firstAttOffset+116:firstAttOffset+118])[0]))

print("\n$File_Name")

fnCreateDateOffset = struct.unpack("<q",extend[firstAttOffset+128:firstAttOffset+136])[0]
fnModifiedDateOffset = struct.unpack("<q",extend[firstAttOffset+136:firstAttOffset+144])[0]
fnMFTModifiedDateOffset = struct.unpack("<q",extend[firstAttOffset+144:firstAttOffset+152])[0]
fnAccessedDateOffset = struct.unpack("<q",extend[firstAttOffset+152:firstAttOffset+160])[0]

fnDateCreated = startDate + datetime.timedelta(microseconds=fnCreateDateOffset/10)
fnDateModified = startDate + datetime.timedelta(microseconds=fnModifiedDateOffset/10)
fnDateMFTModified = startDate + datetime.timedelta(microseconds=fnMFTModifiedDateOffset/10)
fnDateAccessed = startDate + datetime.timedelta(microseconds=fnAccessedDateOffset/10)

print("MFT Parent Directory: " + str(struct.unpack("<q",extend[firstAttOffset+120:firstAttOffset+128])[0]))
print("File Created: " + str(fnDateCreated))
print("File Modified: " + str(fnDateModified))
print("File MFT Modified: " + str(fnDateMFTModified))
print("File Accessed: " + str(fnDateAccessed))
print("Logical File Size: " + str(struct.unpack("<q",extend[firstAttOffset+160:firstAttOffset+168])[0]))
print("Physical File Size: " + str(struct.unpack("<q",extend[firstAttOffset+168:firstAttOffset+176])[0]))
print("Flags: " + str(extend[firstAttOffset+176:firstAttOffset+180]))
print("Extended Attributes: " + str(extend[firstAttOffset+180:firstAttOffset+184]))
print("Filename Length: " + str(struct.unpack("<b",extend[firstAttOffset+184:firstAttOffset+185])[0]))
print("Filename Namespace: " + str(extend[firstAttOffset+185:firstAttOffset+186]))
print("Filename: " + str(extend[firstAttOffset+186:firstAttOffset+208].decode('utf-16', 'ignore')))

print("\nStandard IndexRoot Header")
print("Attribute Type: " + str(extend[firstAttOffset+208:firstAttOffset+212]))
print("Length: " + str(struct.unpack("<i",extend[firstAttOffset+212:firstAttOffset+216])[0]))
print("Resident? : " + str(struct.unpack("<b",extend[firstAttOffset+216:firstAttOffset+217])[0]))
print("Name Length: " + str(struct.unpack("<b", extend[firstAttOffset+217:firstAttOffset+218])[0]))
print("Name Offset: " + str(struct.unpack("<h", extend[firstAttOffset+218:firstAttOffset+220])[0]))
print("Index Entry?: " + str(struct.unpack("<h",extend[firstAttOffset+220:firstAttOffset+222])[0]))
print("Attribute Id: " + str(struct.unpack("<h", extend[firstAttOffset+222:firstAttOffset+224])[0]))
print("Atribute Length: " + str(struct.unpack("<L", extend[firstAttOffset+224:firstAttOffset+228])[0]))
"""
print("Attribute ID: " + str(struct.unpack("<h",extend[firstAttOffset+222:firstAttOffset+224])[0]))
print("Start Cluster of RunList: " + str(struct.unpack("<q",extend[firstAttOffset+224:firstAttOffset+232])[0]))
print("End Cluster of Runlist: " + str(struct.unpack("<q",extend[firstAttOffset+232:firstAttOffset+240])[0]))
print("Offset To Runlist: " + str(struct.unpack("<h",extend[firstAttOffset+240:firstAttOffset+242])[0]))
print("Compression Unit Size: " + str(struct.unpack("<h",extend[firstAttOffset+242:firstAttOffset+244])[0]))
print("Allocated Size of Content: " + str(struct.unpack("<q",extend[firstAttOffset+248:firstAttOffset+256])[0]))
print("Actual Size of Content: " + str(struct.unpack("<q",extend[firstAttOffset+256:firstAttOffset+264])[0]))
print("Initialized Size of Content: " + str(struct.unpack("<q",extend[firstAttOffset+264:firstAttOffset+272])[0]))
"""
print("\n$Data")
print(struct.unpack("<q",extend[firstAttOffset+272:firstAttOffset+280])[0])

print("\n$EOF")
print(extend[firstAttOffset+280:firstAttOffset+284])

print("\nTrailing...")
print(extend[284:344])
#targetpath = "C/Windows/"
#count = 0

        #print(zipdirectory.namelist())
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



#drive = open(r"D:\\DESKTOP-4JBOM9R\\MediaID.bin","rb")
#drive.seek(262144*8)
#print(drive.read(100000))


