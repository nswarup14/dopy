from PyQt4 import QtCore, QtGui
import sys,os

class homeWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setupUi()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def setupUi(self):

        self.billButton = QtGui.QPushButton("Bill",self)
        self.billButton.setStyleSheet(self.parent.configurator.homeWidgetBillButtonStyleSheet)
        
        self.emailButton = QtGui.QPushButton("Email",self)
        self.emailButton.setStyleSheet(self.parent.configurator.homeWidgetEmailerButtonStyleSheet)

        self.unbillButton = QtGui.QPushButton("Review Billed",self)
        self.unbillButton.setStyleSheet(self.parent.configurator.homeWidgetReviewBilledButtonStyleSheet)

        self.merchButton = QtGui.QPushButton("Merch",self)
        self.merchButton.setStyleSheet(self.parent.configurator.homeWidgetMerchButtonStyleSheet)

        self.festLabel = QtGui.QLabel(self.parent.configurator.homeWidgetFestName,self)
        self.festLabel.setStyleSheet(self.parent.configurator.homeWidgetFestLabelFont)

        self.billButton.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.emailButton.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.unbillButton.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        self.merchButton.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)

        self.billButton.setFixedSize(300,300)
        self.emailButton.setFixedSize(300,300)
        self.unbillButton.setFixedSize(300,300)
        self.merchButton.setFixedSize(300,300)

        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.addWidget(self.billButton,0,0)
        self.gridLayout.addWidget(self.unbillButton,0,1)
        self.gridLayout.addWidget(self.emailButton,1,0)
        self.gridLayout.addWidget(self.merchButton,1,1)

        self.vertLayout = QtGui.QVBoxLayout()
        self.vertLayout.addStretch()
        self.vertLayout.addLayout(self.gridLayout)
        self.vertLayout.addStretch()

        self.leftvlayout = QtGui.QVBoxLayout()
        self.leftvlayout.addStretch()
        self.leftvlayout.addWidget(self.festLabel)

        self.widgetLayout = QtGui.QHBoxLayout()
        self.widgetLayout.addStretch()
        #hspacer1 = QtGui.QSpacerItem(100,100)
        self.widgetLayout.addLayout(self.vertLayout)
        self.widgetLayout.addStretch()
        self.widgetLayout.addLayout(self.leftvlayout)
        #hspacer2 = QtGui.QSpacerItem(100,100)
        
        self.setLayout(self.widgetLayout)

        #Connect Buttons#
        self.billButton.clicked.connect(lambda : self.parent.setupCentralWidget("billing"))
        self.unbillButton.clicked.connect(lambda : self.parent.setupCentralWidget("unbilling"))
        self.emailButton.clicked.connect(lambda : self.parent.setupCentralWidget("emailer"))
        self.merchButton.clicked.connect(lambda : self.parent.setupCentralWidget("merch"))

