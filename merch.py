from PyQt4 import QtGui, QtCore
import sys, os, re, json
import chorePlay, niggerFiles, centralWidgetMerch, leftWidget, displayWidget
from operator import itemgetter

class Entry:
    pass

class Batch:
    pass

class merchWidget(QtGui.QWidget):

    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.batch = Batch()
        self.database = parent.database
        self.setupWidget()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setupWidget(self):

###########GUI components
        self.centralWidget = centralWidgetMerch.centralWidget(self)

        widgetLayout = QtGui.QHBoxLayout()

        widgetLayout.addWidget(self.centralWidget)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.centralWidget)
        widgetLayout.addLayout(vbox)
        widgetLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(widgetLayout)

        self.centralWidget.doneButton.clicked.connect(self.doneButtonHandler)

    def doneButtonHandler(self):
        result = self.updateEntries()
        if result == 0:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Information)
            msg.setText("Entry added! Press OK to continue to the next.")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.buttonClicked.connect(self.closeDialog)
            msg.exec_()
            self.centralWidget.refresh()
        else:
            # Show error popup.
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Critical)
            msg.setText("ID Number not in database!")
            msg.setStandardButtons(QtGui.QMessageBox.Ok)
            msg.buttonClicked.connect(self.closeDialog)
            msg.exec_()
            pass

    def updateEntries(self):
        idNum = self.centralWidget.idField.text()
        if not self.database.idValid(idNum):
            return 1

        tempDict = {
            "ID": idNum,
            idNum: []
        }

        if self.itemOneExists():
            item = self.centralWidget.itemField1.currentText()
            size = self.centralWidget.sizeField1.currentText()
            fullItem = self.appendSizeToItem(item, size)
            tempDict[idNum].append(fullItem)

        if self.itemTwoExists():
            item = self.centralWidget.itemField2.currentText()
            size = self.centralWidget.sizeField2.currentText()
            fullItem = self.appendSizeToItem(item, size)
            tempDict[idNum].append(fullItem)

        if self.itemThreeExists():
            item = self.centralWidget.itemField3.currentText()
            size = self.centralWidget.sizeField3.currentText()
            fullItem = self.appendSizeToItem(item, size)
            tempDict[idNum].append(fullItem)

        if self.itemFourExists():
            item = self.centralWidget.itemField4.currentText()
            size = self.centralWidget.sizeField4.currentText()
            fullItem = self.appendSizeToItem(item, size)
            tempDict[idNum].append(fullItem)

        if self.itemFiveExists():
            item = self.centralWidget.itemField5.currentText()
            size = self.centralWidget.sizeField5.currentText()
            fullItem = self.appendSizeToItem(item, size)
            tempDict[idNum].append(fullItem)
        self.appendToFile(tempDict)
        return 0

    def appendToFile(self, tempDict):
        file_path = 'data-entries.txt'
        with open(file_path, "a") as file:
            file.write(json.dumps(tempDict))

    def closeDialog(self):
        return

    def itemOneExists(self):
        itemOne = self.centralWidget.itemField1.currentText()
        sizeOne = self.centralWidget.sizeField1.currentText()

        if itemOne and sizeOne:
            return True
        else:
            return False

    def itemTwoExists(self):
        itemTwo = self.centralWidget.itemField2.currentText()
        sizeTwo = self.centralWidget.sizeField2.currentText()

        if itemTwo and sizeTwo:
            return True
        else:
            return False

    def itemThreeExists(self):
        itemThree = self.centralWidget.itemField3.currentText()
        sizeThree = self.centralWidget.sizeField3.currentText()

        if itemThree and sizeThree:
            return True
        else:
            return False

    def itemFourExists(self):
        itemFour = self.centralWidget.itemField4.currentText()
        sizeFour = self.centralWidget.sizeField4.currentText()

        if itemFour and sizeFour:
            return True
        else:
            return False

    def itemFiveExists(self):
        itemFive = self.centralWidget.itemField5.currentText()
        sizeFive = self.centralWidget.sizeField5.currentText()

        if itemFive and sizeFive:
            return True
        else:
            return False

    def appendSizeToItem(self, item, size):
        itemSplit = item.split('-')
        itemSplit.insert(1, size)
        return '-'.join(itemSplit)
