
###############################
#
#Name:      PrefetchTest1.py 
#Version:   1.0
#Date:      January 29, 2018
#Author(s): Joe Blanco, David Klein, Jessica Camilien, Justice Collier
#
#Functions(s):
#           Parse a single Prefetch File, showing the following information: Executable name, Last Execution Time, Volume Name(s), Creation Date(s), Serial Number(s), Directory String(s), and Resources Used.
#           Parse a single directory's Prefetch Files, showing the same information as is enumerated above.
#           Show Last Execution Times of all Prefetch Files, sorted from most recent to least recent.
#
#Source(s): 
#           PoorBillionaire's Windows-Prefetch-Parser: https://github.com/PoorBillionaire/Windows-Prefetch-Parser
#           StackOverflow, support for Python syntax and differences between Python 2 & 3
#           The Forensics Wiki, article on Prefetch Files: http://www.forensicswiki.org/wiki/Prefetch
#           
#
################################

from argparse import ArgumentParser
import binascii
import ctypes
from datetime import datetime,timedelta
import ntpath
import os
import struct
import sys
import tempfile
import math
import csv
import pathlib
import numpy


class Prefetch(object):
    def __init__(self, infile):
        self.pFileName = infile

        with open(infile, "rb") as f:
                d = DecompressWin10()
                decompressed = d.decompress(infile)

                t = tempfile.mkstemp()

                with open(t[1], "wb+") as f:
                    f.write(decompressed)
                    f.seek(0)

                    self.parseHeader(f)
                    self.fileInformation26(f)
                    self.metricsArray23(f)
                    self.traceChainsArray30(f)
                    self.volumeInformation30(f)
                    self.getTimeStamps(self.lastRunTime)
                    self.directoryStrings(f)
                    self.getFilenameStrings(f)
                    return

        with open(infile, "rb") as f:
            self.parseHeader(f)
            
            if self.version == 23:
                self.fileInformation23(f)
                self.metricsArray23(f)
                self.traceChainsArray17(f)
                self.volumeInformation23(f)
                self.getTimeStamps(self.lastRunTime)
                self.directoryStrings(f)

            elif self.version == 26:
                self.fileInformation26(f)
                self.metricsArray23(f)
                self.traceChainsArray17(f)
                self.volumeInformation23(f)
                self.getTimeStamps(self.lastRunTime)
                self.directoryStrings(f)

            self.getFilenameStrings(f)

    def parseHeader(self, infile):
        # Parse the file header
        # 84 bytes
        self.version = struct.unpack_from("I", infile.read(4))[0]
        self.signature = struct.unpack_from("I", infile.read(4))[0]
        unknown0 = struct.unpack_from("I", infile.read(4))[0]
        self.fileSize = struct.unpack_from("I", infile.read(4))[0]
        executableName = struct.unpack_from("60s", infile.read(60))[0]
        executableName = executableName.split(b"\x00\x00")[0]
        self.executableName = executableName.replace(b"\x00", b"")
        rawhash = hex(struct.unpack_from("I", infile.read(4))[0])
        self.hash = rawhash.lstrip("0x")
        unknown1 = infile.read(4)
    
    def fileInformation23(self, infile):
        # File Information
        # 156 bytes
        self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsCount = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
        self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
        unknown0 = infile.read(8)
        self.lastRunTime = infile.read(8)
        unknown1 = infile.read(16)
        self.runCount = struct.unpack_from("I", infile.read(4))[0]
        unknown2 = infile.read(84)

    def fileInformation26(self, infile):
        # File Information
        # 224 bytes
        self.metricsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.metricsCount = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.traceChainsCount = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameStringsSize = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationOffset = struct.unpack_from("I", infile.read(4))[0]
        self.volumesCount = struct.unpack_from("I", infile.read(4))[0]
        self.volumesInformationSize = struct.unpack_from("I", infile.read(4))[0]
        unknown0 = infile.read(8)
        self.lastRunTime = infile.read(64)
        unknown1 = infile.read(16)
        self.runCount = struct.unpack_from("I", infile.read(4))[0]
        unknown2 = infile.read(96)

    def metricsArray23(self, infile):
        # File Metrics Array
        # 32 bytes per array, not parsed in this script
        infile.seek(self.metricsOffset)
        unknown0 = infile.read(4)
        unknown1 = infile.read(4)
        unknown2 = infile.read(4)
        self.filenameOffset = struct.unpack_from("I", infile.read(4))[0]
        self.filenameLength = struct.unpack_from("I", infile.read(4))[0]
        unknown3 = infile.read(4)
        self.mftRecordNumber = self.convertFileReference(infile.read(6))
        self.mftSeqNumber = struct.unpack_from("H", infile.read(2))[0]

    def volumeInformation23(self, infile):
        # This function consumes the Volume Information array
        # 104 bytes per structure in the array
        # Returns a dictionary object which holds another dictionary
        # for each volume information array entry

        infile.seek(self.volumesInformationOffset)
        self.volumesInformationArray = []
        self.directoryStringsArray = []
        
        count = 0
        while count < self.volumesCount:
            self.volPathOffset = struct.unpack_from("I", infile.read(4))[0]
            self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
            self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
            volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
            self.volSerialNumber = volSerialNumber.rstrip("L").lstrip("0x")
            self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
            self.fileRefCount = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
            unknown0 = infile.read(68)

            self.directoryStringsArray.append(self.directoryStrings(infile))
            
            infile.seek(self.volumesInformationOffset + self.volPathOffset)
            volume = {}
            volume["Volume Name"] = infile.read(self.volPathLength * 2).replace("\x00", "")
            volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
            volume["Serial Number"] = self.volSerialNumber
            self.volumesInformationArray.append(volume)
            
            count += 1
            infile.seek(self.volumesInformationOffset + (104 * count))

    def traceChainsArray17(self, infile):
        # Read through the Trace Chains Array
        # Not being parsed for information
        # 12 bytes
        infile.read(12)

    def traceChainsArray30(self, infile):
        # Trace Chains Array
        # Read though, not being parsed for information
        # 8 bytes
        infile.read(8)



    def volumeInformation30(self, infile):
        # Volumes Information
        # 96 bytes

        infile.seek(self.volumesInformationOffset)
        self.volumesInformationArray = []
        self.directoryStringsArray = []

        count = 0
        while count < self.volumesCount:
            self.volPathOffset = struct.unpack_from("I", infile.read(4))[0] 
            self.volPathLength = struct.unpack_from("I", infile.read(4))[0]
            self.volCreationTime = struct.unpack_from("Q", infile.read(8))[0]
            self.volSerialNumber = hex(struct.unpack_from("I", infile.read(4))[0])
            self.volSerialNumber = self.volSerialNumber.rstrip("L").lstrip("0x")
            self.fileRefOffset = struct.unpack_from("I", infile.read(4))[0]
            self.fileRefCount = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsOffset = struct.unpack_from("I", infile.read(4))[0]
            self.dirStringsCount = struct.unpack_from("I", infile.read(4))[0]
            unknown0 = infile.read(60)

            self.directoryStringsArray.append(self.directoryStrings(infile))

            infile.seek(self.volumesInformationOffset + self.volPathOffset)
            volume = {}
            volume["Volume Name"] = infile.read(self.volPathLength * 2).replace(b"\x00", b"")
            volume["Creation Date"] = self.convertTimestamp(self.volCreationTime)
            volume["Serial Number"] = self.volSerialNumber
            self.volumesInformationArray.append(volume)
            
            count += 1
            infile.seek(self.volumesInformationOffset + (96 * count))

    def getFilenameStrings(self, infile):
        # Parses filename strings from the PF file
        self.resources = []
        infile.seek(self.filenameStringsOffset)
        self.filenames = infile.read(self.filenameStringsSize)

        for i in self.filenames.split(b"\x00\x00"):
            self.resources.append(i.replace(b"\x00", b""))

    def convertTimestamp(self, timestamp):
        # Timestamp is a Win32 FILETIME value
        # This function returns that value in a human-readable format
        return str(datetime(1601,1,1) + timedelta(microseconds=timestamp / 10.))


    def getTimeStamps(self, lastRunTime):
        self.timestamps = []

        start = 0
        end = 8
        while end <= len(lastRunTime):
            timestamp = struct.unpack_from("Q", lastRunTime[start:end])[0]

            if timestamp:
                self.timestamps.append(self.convertTimestamp(timestamp))
                start += 8
                end += 8
            else:
                break

    def directoryStrings(self, infile):
        infile.seek(self.volumesInformationOffset)
        infile.seek(self.dirStringsOffset, 1)

        directoryStrings = []

        count = 0
        while count < self.dirStringsCount:
            stringLength = struct.unpack_from("<H", infile.read(2))[0] * 2
            directoryString = infile.read(stringLength).replace(b"\x00", b"")
            infile.read(2) # Read through the end-of-string null byte
            directoryStrings.append(directoryString)
            count += 1

        return directoryStrings

    def convertFileReference(self, buf):
        byteArray = list(map(lambda x: '%02x' % x, buf))
            
        byteString = ""
        for i in byteArray[::-1]:
            byteString += i
        
        return int(byteString, 16)

    def csvPrintSingleFile(self, filepath):
        csvfilename = filepath + self.executableName[:-4].decode('utf-8', 'ignore') + '.csv'
        csvSingleRead = open(csvfilename, 'w+')
        csvSingleRead.close()
        csvSingleRead = open(csvfilename, 'r+')
        fieldNamesSingle = ['Executable Name', 'Last Executed', 'Run Count', 'Volume Name', 'Volume Creation Date', 'Volume Serial No', 'Directory Strings', 'Resources Loaded']
        if csvSingleRead.read(30) == '':
            csvSingleHeader = open(csvfilename, 'w')
            single_header = csv.DictWriter(csvSingleHeader, delimiter=',', lineterminator='\n',fieldnames=fieldNamesSingle)
            single_header.writeheader()
            csvSingleHeader.close()
        #masterlist = numpy.column_stack((self.executableName, self.timestamps, self.runCount, self.volumesInformationArray, self.directoryStringsArray, self.directoryStringsArray))
        csvSingleWrite = open(csvfilename, 'a')
        single_writer = csv.DictWriter(csvSingleWrite, delimiter=',', lineterminator='\n',fieldnames=fieldNamesSingle)
        longindex = 0

        argumentdict = dict.fromkeys([])
        if len(self.directoryStringsArray) > len(self.resources): 
            longindex = len(self.directoryStringsArray)
        else:
            longindex = len(self.resources)
                
        for row in range(0, longindex):
            if(row == 0):
                argumentdict['Run Count'] = self.runCount
                argumentdict['Executable Name'] = self.executableName
            if(len(self.timestamps) > row):
                argumentdict['Last Executed'] = self.timestamps[row]
            if(len(self.volumesInformationArray) > row):
                argumentdict['Volume Name'] = self.volumesInformationArray[row-1].get('Volume Name')
                argumentdict['Volume Creation Date'] = self.volumesInformationArray[row-1].get('Creation Date')
                argumentdict['Volume Serial No'] = self.volumesInformationArray[row-1].get('Serial Number')
            if(len(self.directoryStringsArray[0]) > row):
                argumentdict['Directory Strings'] = self.directoryStringsArray[0][row]
            if(len(self.resources) > row):
                argumentdict['Resources Loaded'] = self.resources[row]
            print(argumentdict)
            single_writer.writerow(argumentdict)
            argumentdict.clear()




    def prettyPrint(self):
        # Prints important Prefetch data in a structured format
        banner = "=" * (len(ntpath.basename(self.pFileName)) + 2)
        print ("\n{0}\n{1}\n{0}\n".format(banner, ntpath.basename(self.pFileName)))
        print ("Executable Name: {}\n".format(self.executableName.decode('UTF-8')))
        print ("Run count: {}".format(self.runCount))



        if len(self.timestamps) > 1:
            print ("Last Executed:")
            for i in self.timestamps:
                print ("    " + i)
        else:
            print ("Last Executed: {}".format(self.timestamps[0]))
        
        print ("\nVolume Information:")

        for i in self.volumesInformationArray:
            print ("    Volume Name: " + i["Volume Name"].decode('UTF-8'))
            print ("    Creation Date: " + str(i["Creation Date"]))
            print ("    Serial Number: " + str(i["Serial Number"]))
            print ("")

        print ("Directory Strings:")
        for volume in self.directoryStringsArray:
            for i in volume:
                print ("    " + i.decode('UTF-8'))
        print ("")

        print ("Resources loaded:\n")
        count = 1
        for i in self.resources:
            if i:
                if count > 999:
                    print ("{}: {}".format(count, i.decode('UTF-8')))
                if count > 99:
                    print ("{}:  {}".format(count, i.decode('UTF-8')))                          
                elif count > 9:
                    print ("{}:   {}".format(count, i.decode('UTF-8')))
                else:
                    print ("{}:    {}".format(count, i.decode('UTF-8')))
            count += 1

        print ("")
        
def sortTimestamps(directory):
    timestamps = []

    for i in os.listdir(directory):
        if i.endswith(".pf"):
            if os.path.getsize(directory + i) > 0:
                try:
                    p = Prefetch(directory + i)
                except Exception as e:
                    print ("[ - ] {} could not be parsed".format(i))
                    continue
            else:
                continue
            
            start = 0
            end = 8
            while end <= len(p.lastRunTime):
                tstamp = struct.unpack_from("Q", p.lastRunTime[start:end])[0]

                if tstamp:
                    timestamps.append((tstamp, i[:-3]))
                    start += 8
                    end += 8
                else:
                    break
    
    return sorted(timestamps, key=lambda tup: tup[0], reverse=True)

def convertTimestamp(timestamp):
        # Timestamp is a Win32 FILETIME value
        # This function returns that value in a human-readable format
        return str(datetime(1601,1,1) + timedelta(microseconds=timestamp / 10.))
            
# The code in the class below was taken and then modified from Francesco 
# Picasso's w10pfdecomp.py script. This modification makes two simple changes:
#
#    - Wraps Francesco's logic in a Python class 
#    - Returns a bytearray of uncompressed data instead of writing it to a new 
#      file, like Francesco's original code did
#
# Author's name: Francesco "dfirfpi" Picasso
# Author's email: francesco.picasso@gmail.com
# Source: https://github.com/dfirfpi/hotoloti/blob/master/sas/w10pfdecomp.py
# License: http://www.apache.org/licenses/LICENSE-2.0

#Windows-only utility to decompress MAM compressed files
class DecompressWin10(object):
    def __init__(self):
        pass

    def tohex(self, val, nbits):
        """Utility to convert (signed) integer to hex."""
        return hex((val + (1 << nbits)) % (1 << nbits))

    def decompress(self, infile):
        """Utility core."""

        NULL = ctypes.POINTER(ctypes.c_uint)()
        SIZE_T = ctypes.c_uint
        DWORD = ctypes.c_uint32
        USHORT = ctypes.c_uint16
        UCHAR  = ctypes.c_ubyte
        ULONG = ctypes.c_uint32

        # You must have at least Windows 8, or it should fail.
        try:
            RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
        except AttributeError as e:
            sys.exit("[ - ] {}".format(e) + \
            "\n[ - ] Windows 8+ required for this script to decompress Win10 Prefetch files")

        RtlGetCompressionWorkSpaceSize = \
            ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize

        with open(infile, 'rb') as fin:
            header = fin.read(8)
            compressed = fin.read()

            signature, decompressed_size = struct.unpack('<LL', header)
            calgo = (signature & 0x0F000000) >> 24
            crcck = (signature & 0xF0000000) >> 28
            magic = signature & 0x00FFFFFF
            if magic != 0x004d414d :
                sys.exit('Wrong signature... wrong file?')

            if crcck:
                # I could have used RtlComputeCrc32.
                file_crc = struct.unpack('<L', compressed[:4])[0]
                crc = binascii.crc32(header)
                crc = binascii.crc32(struct.pack('<L',0), crc)
                compressed = compressed[4:]
                crc = binascii.crc32(compressed, crc)          
                if crc != file_crc:
                    sys.exit('{} Wrong file CRC {0:x} - {1:x}!'.format(infile, crc, file_crc))

            compressed_size = len(compressed)

            ntCompressBufferWorkSpaceSize = ULONG()
            ntCompressFragmentWorkSpaceSize = ULONG()

            ntstatus = RtlGetCompressionWorkSpaceSize(USHORT(calgo),
                ctypes.byref(ntCompressBufferWorkSpaceSize),
                ctypes.byref(ntCompressFragmentWorkSpaceSize))

            if ntstatus:
                sys.exit('Cannot get workspace size, err: {}'.format(
                    self.tohex(ntstatus, 32)))
                    
            ntCompressed = (UCHAR * compressed_size).from_buffer_copy(compressed)
            ntDecompressed = (UCHAR * decompressed_size)()
            ntFinalUncompressedSize = ULONG()
            ntWorkspace = (UCHAR * ntCompressFragmentWorkSpaceSize.value)()
            
            ntstatus = RtlDecompressBufferEx(
                USHORT(calgo),
                ctypes.byref(ntDecompressed),
                ULONG(decompressed_size),
                ctypes.byref(ntCompressed),
                ULONG(compressed_size),
                ctypes.byref(ntFinalUncompressedSize),
                ctypes.byref(ntWorkspace))

            if ntstatus:
                sys.exit('Decompression failed, err: {}'.format(
                    tohex(ntstatus, 32)))

            if ntFinalUncompressedSize.value != decompressed_size:
                sys.exit('Decompressed with a different size than original!')

        return bytearray(ntDecompressed)



def main():
    """p = ArgumentParser()
    p.add_argument("-d", "--directory", help="Parse all PF files in a given directory")
    p.add_argument("-e", "--executed", help="Sort PF files by ALL execution times")
    p.add_argument("-f", "--file", help="Parse a given Prefetch file")
    p.add_argument("-c", "--csv", help="Parse all Prefetch files and output to a csv file in the directory")
    args = p.parse_args()"""
    if len(sys.argv) > 1:
        action1 = sys.argv[1]
        if action1 in ['-f', 'file']:
            action2 = sys.argv[2]
            if sys.argv[2].endswith(".pf"):
                if os.path.getsize(action2) > 0:
                    try:
                        p = Prefetch(action2)
                    except Exception as e:
                        print ("[ - ] {}".format(e))
                        sys.exit("[ - ] {} could not be parsed".format(action2))

                    p.prettyPrint()
                else:
                    print ("[ - ] {}: Zero byte Prefetch file".format(action2))

        elif action1 in ['-d', 'directory']:
            action2 = sys.argv[2]
            if not (action2.endswith("/") or action2.endswith("\\")):
                sys.exit("\n[ - ] When enumerating a directory, add a trailing slash\n")

            directoryPath = sys.argv[2]
            if os.path.isdir(directoryPath):
                for i in os.listdir(directoryPath):
                    if i.endswith(".pf"):
                        if os.path.getsize(directoryPath + i):
                            try:
                                p = Prefetch(directoryPath + i)
                                # p.csvPrintSingleFile()
                                p.prettyPrint()
                            except Exception as e:
                                print ("[ - ] {} could not be parsed".format(i))
                        else:
                            print ("[ - ] Zero-byte Prefetch file")
        elif action1 in ['-e', 'executed']:
            if not (argv[2].endswith("/") or argv[2].endswith("\\")):
                sys.exit("\n[ - ] When enumerating a directory, add a trailing slash\n")
            csvfile = open('indexPrefetch.csv', 'w')
            fieldNamesIndex = ['Executable Name', 'Last Executed']
            fieldNamesSingle = ['Executable Name', 'Last Executed', 'Run Count', 'Volume Name', 'Creation Date', 'Serial Number']
            lnk_writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=fieldNamesIndex)
            lnk_writer.writeheader()
            print ("Execution Time, File Executed")
            for i in  sortTimestamps(argv[2]):
                singlefile = open('C:/Test/' + str(i[1])[:-13] + ".csv", 'w' )
                single_writer = csv.DictWriter(singlefile, delimiter=',', lineterminator='\n',fieldnames=fieldNamesSingle)
                single_writer.writerow({'Executable Name':str(i[1])[:-13], 'Last Executed':convertTimestamp(i[0])})
                lnk_writer.writerow({'Executable Name':str(i[1])[:-13], 'Last Executed':convertTimestamp(i[0])})
                print ("{}, {}".format(convertTimestamp(i[0]), i[1]))
 
        elif action1 in ['-c', 'csv']:
            #fieldNamesSingle = ['Executable Name', 'Last Executed', 'Run Count', 'Volume Name', 'Creation Date', 'Serial Number']
            if not os.path.exists(sys.argv[3]):
                os.makedirs(sys.argv[3])
            os.chdir(sys.argv[3])
            print(os.getcwd())
            prefPath = sys.argv[2]
            if os.path.isdir(prefPath):
                for i in os.listdir(prefPath):
                    if i.endswith(".pf"):
                        if os.path.getsize(prefPath + i):
                            try:
                                p = Prefetch(prefPath + i)
                                p.csvPrintSingleFile(sys.argv[3])
                            except Exception as e:
                                print ("[ - ] {} could not be parsed".format(i))
                        else:
                            print ("[ - ] Zero-byte Prefetch file")

            csvfile = open('indexPrefetch.csv', 'w')
            fieldNamesIndex = ['Executable Name', 'Last Executed']
            lnk_writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=fieldNamesIndex)
            lnk_writer.writeheader()

            for i in  sortTimestamps(sys.argv[2]):
                dt = p.convertTimestamp(i[0])
                lnk_writer.writerow({'Executable Name':i[1].encode('utf-8', 'ignore'), 'Last Executed':dt})
        else:
            print("Incorrect Argument; Accepted Arguments: " + "\n-l \"[Absolute Location of File]\" \n-d \"[Absolute Directory Location]\"\n-e \n-c \"[Absolute Location of File]\" \"[Absolute Output Folder]\"  ")

    else:
        print(" Please Input an argument; Accepted Arguments: " + "\n-l \"[Absolute Location of File]\" \n-d \"[Absolute Directory Location]\"\n-e \n-c \"[Absolute Location of File]\" \"[Absolute Output Folder]\"  ")

if __name__ == '__main__':
    main()