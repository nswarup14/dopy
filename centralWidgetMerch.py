from PyQt4 import QtCore, QtGui
import sys, os

class itemComboBox(QtGui.QComboBox):

    def __init__(self, parent=None, clothes=False):

        QtGui.QComboBox.__init__(self)
        self.parent = parent
        self.model = QtGui.QStringListModel()
        if clothes:
            self.itemList = self.parent.parent.parent.configurator.clothesItemList
        else:
            self.itemList = self.parent.parent.parent.configurator.restItemList
        self.model.setStringList(self.itemList)
        self.addItems(self.itemList)

        self.setEditable(True)

        self.completer = CustomQCompleter(self)
        self.completer.setModel(self.model)


        self.setCompleter(self.completer)
        self.setEditText('')

        self.setGeometry(200, 100, 400, 300)

class quantityBox(QtGui.QLineEdit):

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self)
        self.parent = parent
        self.setText('')
        self.setGeometry(200, 100, 400, 300)

class sizeComboBox(QtGui.QComboBox):

    def __init__(self, parent=None):

        QtGui.QComboBox.__init__(self)
        self.parent = parent
        self.model = QtGui.QStringListModel()
        self.sizeList = ["S", "M", "L", "XL", "XXL"]

        self.model.setStringList(self.sizeList)
        self.addItems(self.sizeList)

        self.setEditable(True)

        self.completer = CustomQCompleter(self)
        self.completer.setModel(self.model)


        self.setCompleter(self.completer)
        self.setEditText('')

        self.setGeometry(200, 100, 400, 300)

class CustomQCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        super(CustomQCompleter, self).__init__(parent)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.setWrapAround(False)
        self.local_completion_prefix = ""
        self.source_model = None

    def setModel(self, model):
        self.source_model = model
        super(CustomQCompleter, self).setModel(self.source_model)

    def updateModel(self):
        local_completion_prefix = self.local_completion_prefix
        class InnerProxyModel(QtGui.QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
                searchStr = local_completion_prefix.lower()
                modelStr = str(self.sourceModel().data(index0,QtCore.Qt.DisplayRole)).lower()
                return searchStr in modelStr
        proxy_model = InnerProxyModel()
        proxy_model.setSourceModel(self.source_model)

        super(CustomQCompleter, self).setModel(proxy_model)
        cr=QtCore.QRect(QtCore.QPoint(1, 1), QtCore.QSize(1, 1))
        self.complete(cr)


    def splitPath(self, path):
        self.local_completion_prefix = str(path)
        self.updateModel()
        return ""

class centralWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.setupWidget()

    def setupWidget(self):

        self.database = self.parent.database
        # self.setFixedHeight(self.parent.parent.configurator.centralWidgetMerchHeight)
        self.setFixedHeight(440)
#############Gui Components
        self.syncButton = QtGui.QPushButton("Sync")

        self.idFieldLabel = QtGui.QLabel(r'ID Number (in format: 201XAXPSXXXX)')
        self.idFieldLabel.setWordWrap(True)
        self.idField = QtGui.QLineEdit("")

        self.isOutstiField = QtGui.QCheckBox("Outsti (Hover over text to view the checkbox)")

        self.clothesNameFields = []
        self.clothesSizeFields = []
        self.restNameFields = []
        self.quantityFields = []

        for entry in range(0, 5):        
            self.clothesNameFields.append(itemComboBox(self, True))
            self.clothesSizeFields.append(sizeComboBox(self))
            self.restNameFields.append(itemComboBox(self, False))
            self.quantityFields.append(quantityBox(self))

        self.doneButton = QtGui.QPushButton("Done")

        hboxSync = QtGui.QHBoxLayout()
        hboxSync.addStretch(True)
        hboxSync.addWidget(self.syncButton)

        hboxId = QtGui.QHBoxLayout()
        hboxId.addWidget(self.idFieldLabel)
        hboxId.addWidget(self.idField)

        hboxOutsti = QtGui.QHBoxLayout()
        hboxOutsti.addWidget(self.isOutstiField)

        hboxDone = QtGui.QHBoxLayout()
        hboxDone.addStretch(True)
        hboxDone.addWidget(self.doneButton)

        widgetLayout = QtGui.QVBoxLayout()
        widgetLayout.addLayout(hboxSync)
        widgetLayout.addLayout(hboxId)
        widgetLayout.addLayout(hboxOutsti)

        clothesVbox = QtGui.QVBoxLayout()
        restVbox = QtGui.QVBoxLayout()

        for entry in range(0, 5):
            hbox = QtGui.QHBoxLayout()
            hbox.addStretch(True)
            label = QtGui.QLabel('Item-'+str(entry + 1))
            hbox.addWidget(label)
            hbox.addWidget(self.clothesNameFields[entry])
            hbox.addWidget(self.clothesSizeFields[entry])
            clothesVbox.addLayout(hbox)

            hbox = QtGui.QHBoxLayout()
            hbox.addStretch(True)
            label = QtGui.QLabel('Item-'+str(entry + 1))
            hbox.addWidget(label)
            hbox.addWidget(self.restNameFields[entry])
            hbox.addWidget(self.quantityFields[entry])
            restVbox.addLayout(hbox)

        itemsHbox = QtGui.QHBoxLayout()
        itemsHbox.addLayout(clothesVbox)
        itemsHbox.addLayout(restVbox)

        widgetLayout.addLayout(itemsHbox)
        widgetLayout.addLayout(hboxDone)
        self.setLayout(widgetLayout)

    def refresh(self):
        self.idField.setText("")
        self.isOutstiField.setChecked(False)
        for entry in range(0, 5):
            self.clothesNameFields[entry].setEditText('')
            self.clothesSizeFields[entry].setEditText('')
            self.restNameFields[entry].setEditText('')
            self.quantityFields[entry].setText('')