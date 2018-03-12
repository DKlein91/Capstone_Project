#   This script is intended to scan the C:\$Recycle.Bin folder of a system and return any
#   metadata regarding files that were deleted from the system.

import os
import binascii
import struct
import datetime
import csv
import argparse

def parseTrash(fileName, sizeOfFile, isWin10):
    fileSize = fileName.read(8)
    deleted = fileName.read(8)
    if isWin10 == True:
        unknownOffset = fileName.read(4)
        filePath = fileName.read(sizeOfFile - 30)
    else:
        filePath = fileName.read(sizeOfFile - 26)

    fileSizeNum = int.from_bytes(fileSize, byteorder="little")
    deleteDateTimeStamp = int.from_bytes(deleted, byteorder="little")    

    result = filePath.decode('utf-16', errors = 'ignore')
    
    fileNameStart = result.rfind("\\")+1

    originalFileName = result[fileNameStart:]
    originalFilePath = result[:fileNameStart]

    print("Name:    " + originalFileName)
    print("Path:    " + originalFilePath)
    print("Size:    " + str(fileSizeNum) + " bytes")
    print("Deleted: " + convertDateTime(deleteDateTimeStamp))
    print()

    return [originalFileName, originalFilePath, str(fileSizeNum) + " bytes", convertDateTime(deleteDateTimeStamp)]

def parseWin8Trash(fileName):
    fileSize = fileName.read(8)
    deleted = fileName.read(8)
    unknownOffset = fileName.read(4)
    filePath = fileName.read(520)

    fileSizeNum = int.from_bytes(fileSize, byteorder="little")
    deleteDateTimeStamp = int.from_bytes(deleted, byteorder="little")    

    result = filePath.decode('utf-16', errors = 'ignore')
    
    fileNameStart = result.rfind("\\")+1

    originalFileName = result[fileNameStart:]
    originalFilePath = result[:fileNameStart]

    print("Name:    " + originalFileName)
    print("Path:    " + originalFilePath)
    print("Size:    " + str(fileSizeNum) + " bytes")
    print("Deleted: " + convertDateTime(deleteDateTimeStamp))
    print()
    
    return [originalFileName, originalFilePath, str(fileSizeNum) + " bytes", convertDateTime(deleteDateTimeStamp)]

def convertDateTime(offset):
    deleteDateOffset = offset / 10000000
    startDate = datetime.datetime(1601, 1, 1)
    returnDate = startDate + datetime.timedelta(0, int(round(deleteDateOffset)))
    return str(returnDate)

def main():
    print("\nWelcome to the Windows Trash Inspector for Windows 8 and 10!")
    print()

    parser = argparse.ArgumentParser(description='Input and output')
    parser.add_argument('-i', '--input', metavar='[iP]', type=str, nargs=1, help='A string containing the file or directory to parse. Default is C:\\$Recycle.Bin\\')
    parser.add_argument('-o', '--output', metavar='[oP]', type=str, nargs=1, help='A string containing the location to place the CSV file. Default is the folder containing this script.')
    
    args = parser.parse_args()
    
    try:
        dirName = args.input[0]
    except:
        dirName = "C:\\$Recycle.Bin\\"

    try:
        outputFile = os.path.join(args.output[0], "trashData.csv")
    except:
        outputFile = "trashData.csv"

    filename = open(outputFile, "w", newline='')
    writer = csv.writer(filename, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Name", "Path", "Size", "Deleted"])

    unopenedFiles = 0
    
    print("Inspecting Directory: " + dirName)
    print("Output File Location: " + outputFile + "\n")

    if os.path.isfile(dirName):
        openThisFile = open(dirName,"rb")
        osVersionTest = openThisFile.read(8)
        if osVersionTest == b'\x02\x00\x00\x00\x00\x00\x00\x00':
            csvrow = parseTrash(openThisFile, size, True)
            writer.writerow(csvrow)
        elif osVersionTest == b'\x01\x00\x00\x00\x00\x00\x00\x00':
            if size == 544:
                parseWin8Trash(openThisFile)
            else:
                parseTrash(openThisFile, size, False)
    else:
        for dirs, sdirs, files in os.walk(dirName):
            for name in files:
                if os.path.isfile(os.path.join(dirs,name)):
                    try:
                        openThisFile = open(os.path.join(dirs,name), "rb")
                        osVersionTest = openThisFile.read(8)
                        size = os.path.getsize(os.path.join(dirs,name))
                        if osVersionTest == b'\x02\x00\x00\x00\x00\x00\x00\x00':
                            csvrow = parseTrash(openThisFile, size, True)
                            writer.writerow(csvrow)
                        elif osVersionTest == b'\x01\x00\x00\x00\x00\x00\x00\x00':
                            if size == 544:
                                parseWin8Trash(openThisFile)
                            else:
                                parseTrash(openThisFile, size, False)
                    except:
                        unopenedFiles = unopenedFiles + 1
    if unopenedFiles > 0:    
        print("\n" + str(unopenedFiles) + " files were not opened.")
    
    filename.close()

if __name__ == "__main__":
    main()
