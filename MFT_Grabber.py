import os
import sys
from io import BytesIO
import struct
import binascii
import ctypes

def decodeAttributeHeader(record):
    decodingList = {}
    decodingList['type'] = struct.unpack("<L", record[:4])[0]
    #print(decodingList['type'])
    if decodingList['type'] == 0xffffffff:
        return record
    decodingList['len'] = struct.unpack("<L",record[4:8])[0]
    #print(decodingList['len'])
    #print(struct.unpack("B", record[8]))
    decodingList['resident'] = struct.unpack("B", bytes([record[8]]))[0]
    decodingList['nameLen'] = struct.unpack("B", bytes([record[9]]))[0]
    decodingList['nameOffset'] = struct.unpack("<H",record[10:12])[0]
    decodingList['flags'] = struct.unpack("<H",record[12:14])[0]
    decodingList['attID'] = struct.unpack("<H",record[14:16])[0]
    if decodingList['resident'] == 0:
        decodingList['ssize'] = struct.unpack("<L",record[16:20])[0]
        decodingList['soff'] = struct.unpack("<H",record[20:22])[0]
        #decodingList['idxflag'] = struct.unpack("<H",record[22:24])[0]
    else:
        decodingList['start_vcn'] = struct.unpack("<d",record[16:24])[0]
        decodingList['last_vcn'] = struct.unpack("<d",record[24:32])[0]
        decodingList['run_off'] = struct.unpack("<H",record[32:34])[0]
        decodingList['compusize'] = struct.unpack("<H",record[34:36])[0]
        decodingList['f1'] = struct.unpack("<I",record[36:40])[0]
        decodingList['alen'] = struct.unpack("<d",record[40:48])[0]
        decodingList['ssize'] = struct.unpack("<d",record[48:56])[0]
        decodingList['initsize'] = struct.unpack("<d",record[56:64])[0]

    return decodingList

def decodeDataRuns(run):
    decodingPosition = 0
    recordHeader = run[decodingPosition]
    while recordHeader !='\x00':
        #print('HEADER\n' + hexdump(recordHeader))
        offset = int(binascii.hexlify(recordHeader)[0])
        runlength = int(binascii.hexlify(recordHeader)[1])
        #print('OFFSET %d LENGTH %d' %(offset, runlength))
        
        #move into the length data for the run
        decodingPosition += 1

        #print(decodePos, runlength)
        length = run[decodingPosition:decodingPosition + int(runlength)][::-1]
        #print('LENGTH\n'+hexdump(length))
        length = int(binascii.hexlify(length), 16)
            
        hexoffset = run[decodingPosition + runlength:decodingPosition + offset + runlength][::-1]
        #print('HEXOFFSET\n' + hexdump(hexoffset))
        cluster = twos_comp(int(binascii.hexlify(hexoffset), 16), offset * 8)
        
        yield(length, cluster)
        decodingPosition = decodingPosition + offset + runlength
        header = run[decodingPosition]
        #break

if __name__ == "__main__":
    ntfsDriveBytes = open(r"\\.\C:", "rb")
    firstFiveTwelveBytes = ntfsDriveBytes.read(512)
    #print(firstFiveTwelveBytes)
    firstFiveTwelveString = BytesIO(firstFiveTwelveBytes)

    firstFiveTwelveString.seek(0x0b)
    sectorBytes = firstFiveTwelveString.read(2)
    #print(sectorBytes)
    sectorBytes = struct.unpack("<h", binascii.unhexlify(binascii.hexlify(sectorBytes)))[0]

    firstFiveTwelveString.seek(0x0d)
    clusterSectors = firstFiveTwelveString.read(ctypes.sizeof(ctypes.c_byte))
    clusterSectors = struct.unpack("<b", binascii.unhexlify(binascii.hexlify(clusterSectors)))[0]

    firstFiveTwelveString.seek(0x30)
    clusterNumber = firstFiveTwelveString.read(ctypes.sizeof(ctypes.c_longlong))
    mftCluster = struct.unpack("<q", binascii.unhexlify(binascii.hexlify(clusterNumber)))[0]
    
    mftLocation = sectorBytes * clusterSectors * mftCluster

    ntfsDriveBytes.seek(0)
    ntfsDriveBytes.seek(mftLocation)
    rawMFTBytes = ntfsDriveBytes.read(1024)
    #print(rawMFTBytes)

    readPointer = 0
    mft = []
    mftDictionary = {}
    mftDictionary['attributeOffset'] = struct.unpack("<H", rawMFTBytes[20:22])[0]
    
    readPointer = mftDictionary['attributeOffset']
    while readPointer < len(rawMFTBytes):
        activeRecord = decodeAttributeHeader(rawMFTBytes[readPointer:])
        print(activeRecord)
        #if activeRecord['type'] == 0x80:
        #    dataRuns = rawMFTBytes[readPointer + activeRecord['run_off']:readPointer + activeRecord['len']]
        #    previousCluster = None
        #    previousSeek = 0          
            #for length, cluster in decodeDataRuns(dataruns):                
            #    if previousCluster==None:    
            #        ntfsDriveBytes.seek(cluster * sectorBytes * clusterSectors)
            #        previousSeek = ntfsDriveBytes.tell()
            #        #sock.send(ntfsdrive.read(length*bytesPerSector*sectorsPerCluster))
            #        previousCluster = cluster
            #    else:
            #        ntfsDriveBytes.seek(previousSeek)
            #        newPosition = previousSeek + (cluster * sectorBytes * clusterSectors)
            #        ntfsDriveBytes.seek(newPosition)
            #        previousSeek = ntfsDriveBytes.tell()                    
            #        #sock.send(ntfsdrive.read(length*bytesPerSector*sectorsPerCluster))
            #        previousCluster = cluster                   
            #break
        try:
            print(activeRecord['type'])
        except:
            print("End of File")

        try:
            if activeRecord['len'] > 0:
                readPointer = readPointer + activeRecord['len']
                mft.append(activeRecord)
        except:
            readPointer = readPointer + len(activeRecord)
