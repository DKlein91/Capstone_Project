import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
from win32api import GetSystemMetrics
import csv
from contextlib import suppress
import datetime

prefetchCSVFolder = os.getcwd() + "\Prefetch_Results"
LNKResultsFile = os.getcwd() + "\LNKData.csv"
jumpListCSVFolder = os.getcwd() + "\JumpList"
AppCompatCacheResultsFile = os.getcwd() + "\AppCompatCacheResults.csv"
windowsTrashResultsFile = os.getcwd() + "/trashData.csv"

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

#SEPARATE PARSER RUNNERS: GRAB CSV DATA AND OUTPUT IT INTO THE RESULTS TAB

def PrefetchRun():
    
    strfile = os.getcwd() + "\Prefetch_Results"
    outfile = os.getcwd() + "\PfOutput.csv"
    prefList = os.listdir(strfile)
    #data = []
    with open(outfile, 'w') as a:
        header = ['Executable Name','Last Executed','Run Count','Volume Name','Volume Creation Date','Volume Serial No','Directory Strings','Resources Loaded']
        pfOutputWriter = csv.DictWriter(a, fieldnames=header)
        pfOutputWriter.writeheader()
        pfOutputWriter = csv.writer(a)
        for file in prefList:
            p = open(strfile + "\\" + file, newline = '')
            PfFile = csv.reader(p)
            try:
                PfFile.__next__()
                pfOutputWriter.writerow(PfFile.__next__())
            except Exception as e:
                print(e)
        resultsSwitch(outfile)

def LNKRun():
    outfile = os.getcwd() + "\LNKData.csv"
    resultsSwitch(outfile)

def JumpListRun():
    jumpListFiles = os.listdir(os.getcwd() + "\JumpList")
    for file in jumpListFiles:
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
            row.append("")                                  #Skip creation date
            if(len(i[7]) > 0):                              #Confirm the accessed date cell is not blank
                row.append(i[7])                            #Add last accessed date
            else:
                row.append("")                              #If no date, add blank
            row.append("")                                  #Skip modified date
            row.append("")                                  #Skip deletion date
            row.append(i[3])                                #Add run count
            for j in range(0,11):                           #Skip the next 11 cells
                row.append("")
            if(i[9].find("Users")):                         #Confirm username is in file path
                user = CarveUserFromPath(i[9])
                row.append(user)                            #Add username
            else:
                row.append("")                              #If username is not in file path, skip username field
            sendToResults.writerow(row)                        #Write row to the aggregated results file
        readThisFile.close()                                #Close Jump List result file

def TrashRun():
    outfile = os.getcwd() + "\trashData.csv"
    resultsSwitch(outfile)

def AppCompatCacheRun():
    accFile = open(r"AppCompatCacheResults.csv","rb")
    data = accFile.read()
    accFile.close()
    newACCFile = open("ACCNoNull.csv", "wb")
    newACCFile.write(data.replace(b"\x00", b""))
    newACCFile.close()
    outfile = os.getcwd() + "\ACCNoNull.csv"
    resultsSwitch(outfile)

def GetACCData(sendToResults):
    accFile = open("AppCompatCacheResults.csv","rb")
    data = accFile.read()
    accFile.close()
    newACCFile = open("ACCNoNull.csv", "wb")
    newACCFile.write(data.replace(b"\x00", b""))
    newACCFile.close()

    readThisFile = open("ACCNoNull.csv","r")
    csv_accFile = csv.reader(readThisFile)
    count = 0
    for row in csv_accFile:
        if(count == 0):                                     #Confirm the row is not the header
            count += 1
            continue                                        #Skip row if header
        try:
            result = []
            csv_path = row[1]
            date = ConvertCSVDateToDateTime(row[0])
            name,path = CarveFilenameFromPath(csv_path)
            result.append(name)
            result.append(path)
            result.append(row[0])   #File creation date
            for i in range(0,16):
                result.append("")
            sendToResults.writerow(result)
        except:
            continue
    readThisFile.close()
    return

def GetPrefetchFiles(sendToResults):
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
                lastRunDates.append(i[1])                   #Add all run dates
            else:
                count += 1
                continue                                    #If cell is blank or the header, skip it
            if(count == 1):                                 #Confirm the reader is on the first row (where the run count is stored)
                runCount = i[2]
            count += 1                                      #Keep counting so runCount will not be overwritten with a blank cell
        row.append(file[:len(file)-4])                      #Add filename minus ".csv"
        row.append("")                                      #Skip file location
        row.append("")                                      #Skip creation date
        row.append(lastRunDates[0])                         #Add most recent accessed date
        row.append("")                                      #Skip modified date
        row.append("")                                      #Skip deletion date
        row.append(runCount)                                #Add number of times program was run
        row.append("")                                      #Skip vol location
        row.append("")                                      #Skip vol type
        row.append("")                                      #Skip vol serial
        
        count = 0
        for i in lastRunDates:
            if(count > 0): 
                row.append(i)                               #Add each date run
            count += 1
        for i in range(0, 11-len(lastRunDates)):            #If the last 7 dates were not pulled, skip the rest of the cells
            row.append("")   
        readThisFile.close()                                #Close the prefetch results file
        sendToResults.writerow(row)                         #Write the row to the aggregated results file
    return

def GetLNKFiles(sendToResults):
    #Extract info from the LNK results csv file
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
        if(len(i[1]) > 0):                                  #Confirm the creation date cell is not blank
            row.append(i[1])                                #Add file creation date
        else:
            row.append("")                                  #If no date, add blank                                    
        if(len(i[2]) > 0):                                  #Confirm accessed date cell is not blank
            row.append(i[2])                                #Add file accessed date
        else:
            row.append("")                                  #If no date, add blank
        if(len(i[3]) > 0):                                  #Confirm the modified date cell is not blank
            row.append(i[3])                                #Add file modified date
        else:
            row.append("")                                  #If no date, add blank
        row.append("")                                      #Skip deletion date
        row.append("")                                      #Skip run count
        row.append(i[5])                                    #Add volume location
        row.append(i[6])                                    #Add volume type
        row.append(i[7])                                    #Add volume serial number
        for j in range(0,7):
            row.append("")                                  #Skip the next 8 cells as LNK files only have one Accessed date and no Run Count
        row.append(i[4])                                    #Add file size

        #This code pulls the username from the file path
        if(i[0].find("Users") > -1):                        #Confirm username is in file path
            user = CarveUserFromPath(i[0])
            row.append(user)                                #Add username
        else:
            row.append("")                                  #If no username, add blank cell
        sendToResults.writerow(row)                            #Write row to the aggregated results file
    readThisFile.close()                                    #Close the LNK results file
    return

def GetJumpListFiles(sendToResults):
    #Extract info from the Jump List result files
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
            row.append("")                                  #Skip creation date
            if(len(i[7]) > 0):                              #Confirm the accessed date cell is not blank
                row.append(i[7])                            #Add last accessed date
            else:
                row.append("")                              #If no date, add blank
            row.append("")                                  #Skip modified date
            row.append("")                                  #Skip deletion date
            row.append(i[3])                                #Add run count
            for j in range(0,11):                           #Skip the next 11 cells
                row.append("")
            if(i[9].find("Users")):                         #Confirm username is in file path
                user = CarveUserFromPath(i[9])
                row.append(user)                            #Add username
            else:
                row.append("")                              #If username is not in file path, skip username field
            sendToResults.writerow(row)                        #Write row to the aggregated results file
        readThisFile.close()                                #Close Jump List result file
    return

def GetTrashData(sendToResults):
    #Extract info from the trash results csv file
    readThisFile = open(windowsTrashResultsFile,"r")        #Open trash results file
    csv_readThisFile = csv.reader(readThisFile)             #Set up csv reader

    count = 0
    for i in csv_readThisFile:
        if(count == 0):                                     #Confirm the row is not the header
            count += 1
            continue                                        #Skip row if header
        
        row = []

        row.append(i[0])                                    #Add filename
        row.append(i[1])                                    #Add file path
        row.append("")                                      #Skip creation date                                   
        row.append("")                                      #Skip accessed date
        row.append("")                                      #Skip modified date
        row.append(i[3])                                    #Skip deletion date
        row.append("")                                      #Skip run count
        for j in range(0,11):
            row.append("")                                  #Skip the next 11 cells
        row.append(i[2])                                    #Add file size
        row.append("")                                      #Skip username
        sendToResults.writerow(row)                         #Write row to the aggregated results file
    readThisFile.close()                                    #Close the LNK results file
    return

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

def ConsolidateData():
    #Set up the results output file
    resultsFile = open("AllData.csv","w",newline="")
    output = csv.writer(resultsFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #These headers will be on every result
    headers = ["File","Location","Created","Accessed (Run)","Modified","Deleted","Run Count","Vol Location","Vol Type","Vol Serial","Last Run 2","Last Run 3","Last Run 4","Last Run 5","Last Run 6","Last Run 7","Last Run 8","Size (bytes)","User"]  

    output.writerow(headers)
    GetACCData(output)
    GetPrefetchFiles(output)
    GetLNKFiles(output)
    GetJumpListFiles(output)
    GetTrashData(output)
#    GetLogfileData(output)
#    GetShellBagData(output)
#    GetUsnJrnlData(output)
#    GetIndexDatData(output)
    resultsFile.close()

epoch = datetime.datetime(1601,1,1)
currentDate = datetime.datetime.now()
dataFilePath = "AllData.csv"

def Search(filename, username, created, accessed, modified, deleted, startDate = epoch, endDate = currentDate):
    writeThisFile = open("Search_Results.csv","w",newline="")
    csv_writeThisFile = csv.writer(writeThisFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    headers = ["Filename", "Location", "Created Date", "Accessed Date", "Modified Date", "Deleted Date", "Run Count", "Volume Location", "Volume Type", "Volume Serial", "Size", "Username"]
    headerWriter = csv.DictWriter(writeThisFile, delimiter=",",fieldnames=headers)
    headerWriter.writeheader()
    searchThisFile = open(dataFilePath, "r")
    csv_searchThisFile = csv.reader(searchThisFile)
    count = 0
    for row in csv_searchThisFile:
        if(count < 1):
            count += 1
            continue
        output = []
        hasCreated = False
        hasAccessed = False
        hasModified = False
        hasDeleted = False
        accessedCellNum = 3
        if(len(filename) > 0):
            if(row[0].find(filename) <= -1):
                continue
        if(len(username) > 0):
            if(row[18].find(username) <= -1):
                continue
        if(created == True and len(row[2]) > 0):
            date = ConvertCSVDateToDateTime(row[2])
            if(date >= startDate and date <= endDate):
                hasCreated = True
        if(accessed == True and len(row[3]) > 0):
            date = ConvertCSVDateToDateTime(row[3])
            if(date >= startDate and date <= endDate):
                hasAccessed = True
            if(len(row[10]) > 0):
                date = ConvertCSVDateToDateTime(row[10])
                if(date >= startDate and date <= endDate and hasAccessed == False):
                    hasAccessed = True
                    accessedCellNum = 10
            if(len(row[11]) > 0):
                date = ConvertCSVDateToDateTime(row[11])
                if(date >= startDate and date <= endDate and hasAccessed == False):
                    hasAccessed = True
                    accessedCellNum = 11
            if(len(row[12]) > 0):
                date = ConvertCSVDateToDateTime(row[12])
                if(date >= startDate and date <= endDate and hasAccessed == False):
                    hasAccessed = True
                    accessedCellNum = 12
            if(len(row[13]) > 0):
                date = ConvertCSVDateToDateTime(row[13])
                if(date >= startDate and date <= endDate and hasAccessed == False):
                    hasAccessed = True
                    accessedCellNum = 13
            if(len(row[14]) > 0):
                date = ConvertCSVDateToDateTime(row[14])
                if(date >= startDate and date <= endDate and hasAccessed == False):
                    hasAccessed = True
                    accessedCellNum = 14
            if(len(row[15]) > 0):
                date = ConvertCSVDateToDateTime(row[15])
                if(date >= startDate and date <= endDate and hasAccessed == False):
                    hasAccessed = True
                    accessedCellNum = 15
            if(len(row[16]) > 0):
                date = ConvertCSVDateToDateTime(row[16])
                if(date >= startDate and date <= endDate and hasAccessed == False):
                    hasAccessed = True
                    accessedCellNum = 16
        if(modified == True and len(row[4]) > 0):
            date = ConvertCSVDateToDateTime(row[4])
            if(date >= startDate and date <= endDate):
                hasModified = True
        if(deleted == True and len(row[5]) > 0):
            date = ConvertCSVDateToDateTime(row[5])
            if(date >= startDate and date <= endDate):
                hasDeleted = True
        if(created == True or accessed == True or modified == True or deleted == True):
            if(hasCreated == False and hasAccessed == False and hasModified == False and hasDeleted == False):
                continue
        output.append(row[0])                   #Filename
        output.append(row[1])                   #Location
        output.append(row[2])                   #Created Date
        output.append(row[accessedCellNum])     #Accessed Date
        output.append(row[4])                   #Modified Date
        output.append(row[5])                   #Deleted Date
        output.append(row[6])                   #Run Count
        output.append(row[7])                   #Volume Location
        output.append(row[8])                   #Volume Type
        output.append(row[9])                   #Volume Serial
        output.append(row[17])                  #Size
        output.append(row[18])                  #Username
        csv_writeThisFile.writerow(output)

    return

def MajorSearch():
    #Get all the data ino a single csv file to parse for output
    ConsolidateData()
    #scrape applicable info for the search functions
    if ui.fileNameLineEdit.text():
        fileNameSearch = ui.fileNameLineEdit.text()
    else: 
        fileNameSearch = ""
    if ui.userNameLineEdit.text():
        userNameSearch = ui.userNameLineEdit.text()
    else: 
        userNameSearch = ""
    #Check Button fields
    createdSearch =  ui.createdCheckBox.isChecked()
    accessedSearch = ui.accessedCheckBox.isChecked()
    modifiedSearch = ui.modifiedCheckBox.isChecked()
    deletedSearch = ui.deletedCheckBox.isChecked()
    if ui.allTypesCheckBox.isChecked():
        createdSearch = True
        accessedSearch = True
        modifiedSearch = True
        deletedSearch = True
    
    startDateSearch = datetime.datetime.strptime(ui.startDateEdit.text(), '%m/%d/%Y')
    endDateSearch = datetime.datetime.strptime(ui.endDateEdit.text(), '%m/%d/%Y')

    Search(fileNameSearch, userNameSearch, createdSearch, accessedSearch, modifiedSearch, deletedSearch, startDateSearch, endDateSearch)
    resultsSwitch("Search_Results.csv")

def resultsSwitch(incsv):
    resui = Results_Dialog()
    resultsDialog = QtWidgets.QDialog()
    Dialog.accept()
    resui.setupUi(resultsDialog)
    with open(incsv, "r") as a:
        b = csv.reader(a, delimiter=",")
        c = list(b)
        rowcount = len(c)
        print(rowcount)
        a.seek(0)
        header = next(b)
        resui.resultsTableBox.setColumnCount(len(header))
        """for i in range(0, resui.resultsTableBox.columnCount()+1):
            resui.resultsTableBox.setColumnWidth(i, 150)"""    
        resui.resultsTableBox.setHorizontalHeaderLabels(header)
        resui.resultsTableBox.setRowCount(rowcount)
        currentRowCount = resui.resultsTableBox.rowCount()
        for row in b:
            with suppress(Exception):
                for col in range(0, resui.resultsTableBox.columnCount()):
                    if row[col]:
                        qtwi = QtWidgets.QTableWidgetItem(row[col], 0)
                    else:
                        qtwi = QtWidgets.QTableWidgetItem(" ", 0)
                    resui.resultsTableBox.setItem(currentRowCount, col, qtwi)
                currentRowCount += 1
    #resui.resultsTableBox.
    resultsDialog.show()
    resultsDialog.activateWindow()
    resultsDialog.setWindowState(resultsDialog.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
    app.setActiveWindow = resultsDialog

def mainSwitch():
    mainUI = Ui_Dialog()
    mainDialog = QtWidgets.QDialog()
    Dialog.accept()
    mainUI.setupUi(mainDialog)
    mainDialog.show()
    mainDialog.activateWindow()
    mainDialog.setWindowState(mainDialog.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
    app.setActiveWindow = mainDialog

class Results_Dialog(object):
    def setupUi(self, ResultsDialog):
        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(270, 10, 741, 71))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("font: 75 48pt \"Trebuchet MS\";")
        self.titleLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        ResultsDialog.setObjectName("ResultsDialog")
        ResultsDialog.resize(1280,720)
        self.resultsTableBox = QtWidgets.QTableWidget(ResultsDialog)
        self.resultsTableBox.setGeometry(QtCore.QRect(10, 100, 1000, 500))
        self.resultsTableBox.setObjectName("resultsTableBox")
        self.returnToMainButton = QtWidgets.QPushButton(ResultsDialog)
        self.returnToMainButton.setGeometry(QtCore.QRect(10, 650, 100, 40))
        self.returnToMainButton.setStyleSheet("background-color: white;\n"
                                        "    border-style: outset;\n"
                                        "    border-width: 2px;\n"
                                        "    border-radius: 10px;\n"
                                        "    border-color: black;\n"
                                        "    font: bold 14px;\n"
                                        "    min-width: 10em;\n"
                                        "    padding: 6px;")
        self.returnToMainButton.setObjectName("returnToMainButton")
        self.returnToMainButton.clicked.connect(lambda: mainSwitch())
        self.widget = QtWidgets.QWidget(ResultsDialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1281, 721))
        self.widget.setMinimumSize(ResultsDialog.frameSize())
        self.widget.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.409091 rgba(248, 0, 0, 255), stop:1 rgba(168, 0, 0, 255))")
        self.widget.setObjectName("widget")

        self.retranslateUi(ResultsDialog)
        self.widget.raise_()
        self.titleLabel.raise_()
        self.returnToMainButton.raise_()
        self.resultsTableBox.raise_()

        QtCore.QMetaObject.connectSlotsByName(ResultsDialog)

    def retranslateUi(self, ResultsDialog):
        _translate = QtCore.QCoreApplication.translate
        ResultsDialog.setWindowTitle(_translate("ResultsDialog", "Dialog"))
        self.returnToMainButton.setText(_translate("ResultsDialog", "Return To Main"))


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1280, 720)

        Dialog.setStyleSheet("")
        self.titleLabel = QtWidgets.QLabel(Dialog)
        self.titleLabel.setGeometry(QtCore.QRect(270, 10, 741, 71))
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("font: 75 48pt \"Trebuchet MS\";")
        self.titleLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 320, 581, 231))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(13)
        self.gridLayout.setVerticalSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.fileNameLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.fileNameLineEdit.setFont(font)
        self.fileNameLineEdit.setStyleSheet("padding: 3px;\n"
                                        "border-style: solid;\n"
                                        "border: 2px black;\n"
                                        "border-radius: 8px;")
        self.fileNameLineEdit.setObjectName("fileNameLineEdit")
        self.gridLayout.addWidget(self.fileNameLineEdit, 5, 1, 1, 1)
        self.fileNameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.fileNameLabel.setFont(font)
        self.fileNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.gridLayout.addWidget(self.fileNameLabel, 5, 0, 1, 1)
        self.startDateEdit = QtWidgets.QDateEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startDateEdit.sizePolicy().hasHeightForWidth())
        self.startDateEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.startDateEdit.setFont(font)
        self.startDateEdit.setStyleSheet("padding: 3px;\n"
                                    "border-style: solid;\n"
                                    "border: 2px black;\n"
                                    "border-radius: 8px;")
        self.startDateEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.startDateEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.startDateEdit.setProperty("showGroupSeparator", False)
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setDate(QtCore.QDate(2018, 1, 1))
        self.startDateEdit.setObjectName("startDateEdit")
        self.gridLayout.addWidget(self.startDateEdit, 7, 1, 1, 1)
        self.endDateEdit = QtWidgets.QDateEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.endDateEdit.setFont(font)
        self.endDateEdit.setStyleSheet("padding: 3px;\n"
                                        "border-style: solid;\n"
                                        "border: 2px black;\n"
                                        "border-radius: 8px;")
        self.endDateEdit.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.setDate(QtCore.QDate.currentDate())
        self.endDateEdit.setObjectName("endDateEdit")
        self.gridLayout.addWidget(self.endDateEdit, 10, 1, 1, 1)
        self.fileActionLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.fileActionLabel.setFont(font)
        self.fileActionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.fileActionLabel.setObjectName("fileActionLabel")
        self.gridLayout.addWidget(self.fileActionLabel, 11, 0, 1, 1)
        self.userNameLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.userNameLabel.setFont(font)
        self.userNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.userNameLabel.setObjectName("userNameLabel")
        self.gridLayout.addWidget(self.userNameLabel, 4, 0, 1, 1)
        self.endDateLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.endDateLabel.setFont(font)
        self.endDateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.endDateLabel.setObjectName("endDateLabel")
        self.gridLayout.addWidget(self.endDateLabel, 10, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.dateSortRadioButton = QtWidgets.QRadioButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.dateSortRadioButton.setFont(font)
        self.dateSortRadioButton.setObjectName("dateSortRadioButton")
        self.horizontalLayout_4.addWidget(self.dateSortRadioButton)
        self.userNameRadioButton = QtWidgets.QRadioButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.userNameRadioButton.setFont(font)
        self.userNameRadioButton.setObjectName("userNameRadioButton")
        self.horizontalLayout_4.addWidget(self.userNameRadioButton)
        self.fileNameRadioButton = QtWidgets.QRadioButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.fileNameRadioButton.setFont(font)
        self.fileNameRadioButton.setObjectName("fileNameRadioButton")
        self.horizontalLayout_4.addWidget(self.fileNameRadioButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 12, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setVerticalSpacing(6)
#        self.gridLayout_2.setRowMinimumHeight(50,100)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.createdCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.createdCheckBox.setFont(font)
        self.createdCheckBox.setObjectName("createdCheckBox")
        self.gridLayout_2.addWidget(self.createdCheckBox, 0, 0, 1, 1)
        self.modifiedCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.modifiedCheckBox.setFont(font)
        self.modifiedCheckBox.setObjectName("modifiedCheckBox")
        self.gridLayout_2.addWidget(self.modifiedCheckBox, 0, 1, 1, 1)
        self.deletedCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.deletedCheckBox.setFont(font)
        self.deletedCheckBox.setObjectName("deletedCheckBox")
        self.gridLayout_2.addWidget(self.deletedCheckBox, 0, 2, 1, 1)
        self.accessedCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.accessedCheckBox.setFont(font)
        self.accessedCheckBox.setObjectName("accessedCheckBox")
        self.gridLayout_2.addWidget(self.accessedCheckBox, 0, 3, 1, 1)
        self.allTypesCheckBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.allTypesCheckBox.setFont(font)
        self.allTypesCheckBox.setObjectName("allTypesCheckBox")
        self.gridLayout_2.addWidget(self.allTypesCheckBox, 0, 4, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 11, 1, 1, 1)
        self.sortByLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.sortByLabel.setFont(font)
        self.sortByLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.sortByLabel.setObjectName("sortByLabel")
        self.gridLayout.addWidget(self.sortByLabel, 12, 0, 1, 1)
        self.startDateLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.startDateLabel.setFont(font)
        self.startDateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.startDateLabel.setObjectName("startDateLabel")
        self.gridLayout.addWidget(self.startDateLabel, 7, 0, 1, 1)
        self.userNameLineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.userNameLineEdit.setFont(font)
        self.userNameLineEdit.setStyleSheet("padding: 3px;\n"
                                    "border-style: solid;\n"
                                    "border: 2px black;\n"
                                    "border-radius: 8px;")
        self.userNameLineEdit.setObjectName("userNameLineEdit")
        self.gridLayout.addWidget(self.userNameLineEdit, 4, 1, 1, 1)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(80, 130, 1051, 125))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.searchEverythingLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.searchEverythingLabel.setFont(font)
        self.searchEverythingLabel.setObjectName("searchEverythingLabel")
        self.verticalLayout.addWidget(self.searchEverythingLabel)
        self.allInputExplanationLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.allInputExplanationLabel.setFont(font)
        self.allInputExplanationLabel.setObjectName("allInputExplanationLabel")
        self.verticalLayout.addWidget(self.allInputExplanationLabel)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.searchButton = QtWidgets.QPushButton(Dialog)
        self.searchButton.setGeometry(QtCore.QRect(235, 560, 60, 40))
        self.searchButton.setStyleSheet("background-color: white;\n"
                                        "    border-style: outset;\n"
                                        "    border-width: 2px;\n"
                                        "    border-radius: 10px;\n"
                                        "    border-color: black;\n"
                                        "    font: bold 14px;\n"
                                        "    min-width: 10em;\n"
                                        "    padding: 6px;")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(MajorSearch)
        #self.searchButton.clicked.connect(Dialog.accept)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1281, 721))
        self.widget.setMinimumSize(Dialog.frameSize())
        self.widget.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.409091 rgba(248, 0, 0, 255), stop:1 rgba(168, 0, 0, 255))")
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(700, 290, 461, 221))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_7.setSpacing(17)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.prefetchButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.prefetchButton.setFont(font)
        self.prefetchButton.setStyleSheet("background-color: white;\n"
                                        "    border-style: outset;\n"
                                        "    border-width: 2px;\n"
                                        "    border-radius: 10px;\n"
                                        "    border-color: black;\n"
                                        "    font: bold 14px;\n"
                                        "    min-width: 10em;\n"
                                        "    padding: 6px;")
        self.prefetchButton.setObjectName("prefetchButton")
        self.prefetchButton.clicked.connect(PrefetchRun)

        self.horizontalLayout_7.addWidget(self.prefetchButton)
        self.LNKButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.LNKButton.setFont(font)
        self.LNKButton.setStyleSheet("background-color: white;\n"
                                    "    border-style: outset;\n"
                                    "    border-width: 2px;\n"
                                    "    border-radius: 10px;\n"
                                    "    border-color: black;\n"
                                    "    font: bold 14px;\n"
                                    "    min-width: 10em;\n"
                                    "    padding: 6px;")
        self.LNKButton.setObjectName("LNKButton")
        self.LNKButton.clicked.connect(LNKRun)
        self.horizontalLayout_7.addWidget(self.LNKButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 30)
        self.horizontalLayout_6.setSpacing(17)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.jumpListButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.jumpListButton.setFont(font)
        self.jumpListButton.setStyleSheet("background-color: white;\n"
                                            "    border-style: outset;\n"
                                            "    border-width: 2px;\n"
                                            "    border-radius: 10px;\n"
                                            "    border-color: black;\n"
                                            "    font: bold 14px;\n"
                                            "    min-width: 10em;\n"
                                            "    padding: 6px;")
        self.jumpListButton.setObjectName("jumpListButton")
        self.horizontalLayout_6.addWidget(self.jumpListButton)
        self.appCompatCacheButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.appCompatCacheButton.setFont(font)
        self.appCompatCacheButton.setStyleSheet("background-color: white;\n"
                                                "    border-style: outset;\n"
                                                "    border-width: 2px;\n"
                                                "    border-radius: 10px;\n"
                                                "    border-color: black;\n"
                                                "    font: bold 14px;\n"
                                                "    min-width: 10em;\n"
                                                "    padding: 6px;")
        self.appCompatCacheButton.setObjectName("appCompatCacheButton")
        self.horizontalLayout_6.addWidget(self.appCompatCacheButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.trashButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.trashButton.setFont(font)
        self.trashButton.setStyleSheet("background-color: white;\n"
                                    "    border-style: outset;\n"
                                    "    border-width: 2px;\n"
                                    "    border-radius: 10px;\n"
                                    "    border-color: black;\n"
                                    "    font: bold 14px;\n"
                                    "    min-width: 10em;\n"
                                    "    padding: 6px;")
        self.trashButton.setObjectName("trashButton")
        self.verticalLayout_3.addWidget(self.trashButton)
        self.widget.raise_()
        self.titleLabel.raise_()
        self.gridLayoutWidget.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.searchButton.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.titleLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600; color:#ffffff;\">Windows Forensics Suite</span></p></body></html>"))
        self.fileNameLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">File Name:</span></p></body></html>"))
        self.startDateEdit.setDisplayFormat(_translate("Dialog", "d/M/yyyy"))
        self.fileActionLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">File Action:</span></p></body></html>"))
        self.userNameLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">User Name:</span></p></body></html>"))
        self.endDateLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">End Date:</span></p></body></html>"))
        self.dateSortRadioButton.setText(_translate("Dialog", "Date"))
        self.userNameRadioButton.setText(_translate("Dialog", "User name"))
        self.fileNameRadioButton.setText(_translate("Dialog", "File Name"))
        self.createdCheckBox.setText(_translate("Dialog", "Created"))
        self.modifiedCheckBox.setText(_translate("Dialog", "Modified"))
        self.deletedCheckBox.setText(_translate("Dialog", "Deleted"))
        self.accessedCheckBox.setText(_translate("Dialog", "Accessed"))
        self.allTypesCheckBox.setText(_translate("Dialog", "All Types"))
        self.sortByLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Sort By:</span></p></body></html>"))
        self.startDateLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Start Date:</span></p></body></html>"))
        self.searchEverythingLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Search Everything:</span></p></body></html>"))
        self.allInputExplanationLabel.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Input any filters (or no filters)</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Search a Single Inspector:</span></p></body></html>"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#ffffff;\">Select an Inspector to run </span></p></body></html>"))
        self.searchButton.setText(_translate("Dialog", "Search"))
        self.prefetchButton.setText(_translate("Dialog", "Prefetch Files"))
        self.LNKButton.setText(_translate("Dialog", ".LNK Files"))
        self.jumpListButton.setText(_translate("Dialog", "Jump List Files"))
        self.appCompatCacheButton.setText(_translate("Dialog", "AppCompatCache"))
        self.trashButton.setText(_translate("Dialog", "Windows Trash ($Recycle Bin)"))

    def destroyUi(self, Dialog):
        self.titleLabel.destroy()
        self.fileNameLabel.destroy()
        self.startDateEdit.destroy()
        self.fileActionLabel.destroy()
        self.userNameLabel.destroy()
        self.endDateLabel.destroy()
        self.dateSortRadioButton.destroy()
        self.userNameRadioButton.destroy()
        self.fileNameRadioButton.destroy()
        self.createdCheckBox.destroy()
        self.modifiedCheckBox.destroy()
        self.deletedCheckBox.destroy()
        self.accessedCheckBox.destroy()
        self.allTypesCheckBox.destroy()
        self.sortByLabel.destroy()
        self.startDateLabel.destroy()
        self.searchEverythingLabel.destroy()
        self.allInputExplanationLabel.destroy()
        self.label_2.destroy()
        self.label.destroy()
        self.searchButton.destroy()
        self.prefetchButton.destroy()
        self.LNKButton.destroy()
        self.jumpListButton.destroy()
        self.appCompatCacheButton.destroy()
        self.trashButton.destroy()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    Dialog.setModal(True)
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


