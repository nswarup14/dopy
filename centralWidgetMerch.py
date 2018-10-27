from PyQt4 import QtCore, QtGui
import sys, os

class itemComboBox(QtGui.QComboBox):

    def __init__(self, parent=None):

        QtGui.QComboBox.__init__(self)
        self.parent = parent
        self.model = QtGui.QStringListModel()
        self.itemList = self.parent.parent.parent.configurator.merchItemList

        self.model.setStringList(self.itemList)
        self.addItems(self.itemList)

        self.setEditable(True)

        self.completer = CustomQCompleter(self)
        self.completer.setModel(self.model)


        self.setCompleter(self.completer)
        self.setEditText('')

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

        self.itemLabel1 = QtGui.QLabel(r'Item')
        self.itemField1 = itemComboBox(self)
        self.sizeField1 = sizeComboBox(self)

        self.itemLabel2 = QtGui.QLabel(r'Item')
        self.itemField2 = itemComboBox(self)
        self.sizeField2 = sizeComboBox(self)

        self.itemLabel3 = QtGui.QLabel(r'Item')
        self.itemField3 = itemComboBox(self)
        self.sizeField3 = sizeComboBox(self)

        self.itemLabel4 = QtGui.QLabel(r'Item')
        self.itemField4 = itemComboBox(self)
        self.sizeField4 = sizeComboBox(self)

        self.itemLabel5 = QtGui.QLabel(r'Item')
        self.itemField5 = itemComboBox(self)
        self.sizeField5 = sizeComboBox(self)

        self.doneButton = QtGui.QPushButton("Done")

        hboxSync = QtGui.QHBoxLayout()
        hboxSync.addStretch(True)
        hboxSync.addWidget(self.syncButton)

        hboxId = QtGui.QHBoxLayout()
        hboxId.addWidget(self.idFieldLabel)
        hboxId.addWidget(self.idField)

        hboxOutsti = QtGui.QHBoxLayout()
        hboxOutsti.addWidget(self.isOutstiField)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.itemLabel1)
        hbox1.addWidget(self.itemField1)
        hbox1.addWidget(self.sizeField1)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.itemLabel2)
        hbox2.addWidget(self.itemField2)
        hbox2.addWidget(self.sizeField2)

        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(self.itemLabel3)
        hbox3.addWidget(self.itemField3)
        hbox3.addWidget(self.sizeField3)

        hbox4 = QtGui.QHBoxLayout()
        hbox4.addWidget(self.itemLabel4)
        hbox4.addWidget(self.itemField4)
        hbox4.addWidget(self.sizeField4)

        hbox5 = QtGui.QHBoxLayout()
        hbox5.addWidget(self.itemLabel5)
        hbox5.addWidget(self.itemField5)
        hbox5.addWidget(self.sizeField5)

        hboxDone = QtGui.QHBoxLayout()
        hboxDone.addStretch(True)
        hboxDone.addWidget(self.doneButton)

        widgetLayout = QtGui.QVBoxLayout()
        widgetLayout.addLayout(hboxSync)
        widgetLayout.addLayout(hboxId)
        widgetLayout.addLayout(hboxOutsti)

        widgetLayout.addLayout(hbox1)
        widgetLayout.addLayout(hbox2)
        widgetLayout.addLayout(hbox3)
        widgetLayout.addLayout(hbox4)
        widgetLayout.addLayout(hbox5)

        widgetLayout.addLayout(hboxDone)

        self.setLayout(widgetLayout)

    def refresh(self):
        self.idField.setText("")
        self.isOutstiField.setChecked(False)
        self.itemField1.setEditText("")
        self.sizeField1.setEditText("")
        self.itemField2.setEditText("")
        self.sizeField2.setEditText("")
        self.itemField3.setEditText("")
        self.sizeField3.setEditText("")
        self.itemField4.setEditText("")
        self.sizeField4.setEditText("")
        self.itemField5.setEditText("")
        self.sizeField5.setEditText("")
