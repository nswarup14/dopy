import os
class configurator:

    def __init__(self):
        self.configFilePath = os.getcwd() + os.sep + "resources" + os.sep + "config"
        try:
            with open(self.configFilePath) as f:
                self.lines = f.readlines()
        except:
            pass
        self.getAttributes()

    def getAttributes(self):
        print(self.lines)
        #Properties Widget Height
        try:
            index = self.lines.index("Properties Widget Height:\n")
            self.propertiesWidgetHeight = int(self.lines[index+1])
        except Exception as e:
            print("Error configuring propertiesWidgetHeight: ",str(e))
            self.propertiesWidgetHeight = 440

        #Properties Widget Num Fields:
        try:
            index = self.lines.index("Properties Widget Num Fields:\n")
            self.propertiesWidgetNumFields = int(self.lines[index+1])
        except Exception as e:
            print("Error configuring propertiesWidgetNumFields: ",str(e))
            self.propertiesWidgetNumFields = 500

        #Application Window SyleSheet
        try:
            index = self.lines.index("Application SyleSheet:\n")
            tag = self.lines[index+1]
            index+=2
            self.applicationStyleSheet = ""
            while(self.lines[index] != tag):
                #print(self.lines[index])
                self.applicationStyleSheet += self.lines[index]
                index+=1
        except Exception as e:
            print("Error configuring applicationStyleSheet: ",str(e))
            self.applicationStyleSheet = """
QWidget{background-color:#000400;color:#62BECB;}
QMenuBar::item{padding:3px;}
QMenuBar::item:selected{background-color:#62BECB;color:white;border-radius:2px;padding:3px;}
QMenu::item{padding:3px;}
QMenu::item:selected{background-color:#62BECB;color:white;border-radius:2px;padding:3px;}
QFileDialog{background-color:#000400;color:#62BECB;}
"""

        #Home Window SyleSheet
        try:
            index = self.lines.index("Home Widget SyleSheet:\n")
            tag = self.lines[index+1]
            index+=2
            self.homeWidgetStyleSheet = ""
            while(self.lines[index] != tag):
                #print(2)
                self.homeWidgetStyleSheet += self.lines[index]
                index+=1
        except Exception as e:
            print("Error configuring homeWidgetStyleSheet: ",str(e))
            self.homeWidgetStyleSheet = """
QPushButton:hover{background-color:#62BECB;color:white;}
QPushButton:pressed{background-color:#0E4E5A;color:white;}
"""

        #Other Widgets Style Sheet:
        try:
            index = self.lines.index("Other Widgets Style Sheet:\n")
            tag = self.lines[index+1]
            index+=2
            self.otherWidgetsStyleSheet = ""
            while(self.lines[index] != tag):
                #print(2)
                self.otherWidgetsStyleSheet += self.lines[index]
                index+=1
        except Exception as e:
            print("Error configuring otherWidgetsStyleSheet: ",str(e))
            self.otherWidgetsStyleSheet = """
QPushButton{border-radius:3px;border-width:1px;border-color:#0E4E5A;border-style:outset;padding:5px}
QPushButton:hover{background-color:#62BECB;color:white;border-radius:3px;border-color:#0E4E5A;border-width:1px;border-style:outset;}
QPushButton:pressed{background-color:#0E4E5A;color:white;}
QLineEdit{background-color:#3F4038;color:white;border-radius:3px;padding:2px}
QSpinBox{background-color:#3F4038;color:white;border-radius:2px;padding:2px}
QComboBox{background-color:#3F4038;color:white;border-radius:2px;padding:2px}
"""

        #displayWidgetViewerWidth
        try:
            index = self.lines.index("Display Widget Viewer Width:\n")
            self.displayWidgetViewerWidth = int(self.lines[index+1])
        except Exception as e:
            print("Error configuring displayWidgetViewerWidth: ",str(e))
            self.displayWidgetViewerWidth = 715

        #displayWidgetViewerHeight
        try:
            index = self.lines.index("Display Widget Viewer Height:\n")
            self.displayWidgetViewerHeight = int(self.lines[index+1])
        except Exception as e:
            print("Error configuring displayWidgetViewerHeight: ",str(e))
            self.displayWidgetViewerWidth = 580

        #displayWidgetBackgroundTexture
        try:
            index = self.lines.index("Display Widget Background Texture:\n")
            self.displayWidgetBackgroundTexture = (self.lines[index+1])
        except Exception as e:
            print("Error configuring displayWidgetBackgroundTexture: ",str(e))
            self.displayWidgetBackgroundTexture = "resources\Textures\Satin_Black_Texture.jpg"

        #homeWidgetBillButtonStyleSheet
        try:
            index = self.lines.index("Home Widget Bill Button StyleSheet:\n")
            self.homeWidgetBillButtonStyleSheet = (self.lines[index+1])
        except Exception as e:
            print("Error configuring homeWidgetBillButtonStyleSheet: ",str(e))
            self.homeWidgetBillButtonStyleSheet = "background-image:url(bill.png);background-repeat:no-repeat;background-position:center;font-size:14pt;padding-top:200px"

        #homeWidgetReviewBilledButtonStyleSheet
        try:
            index = self.lines.index("Home Widget Review Billed Button StyleSheet:\n")
            self.homeWidgetReviewBilledButtonStyleSheet = (self.lines[index+1])
        except Exception as e:
            print("Error configuring homeWidgetReviewBilledButtonStyleSheet: ",str(e))
            self.homeWidgetReviewBilledButtonStyleSheet = "background-image:url(review.png);background-repeat:no-repeat;background-position:center;font-size:14pt;padding-top:200px"

        #homeWidgetEmailerButtonStyleSheet
        try:
            index = self.lines.index("Home Widget Emailer Button StyleSheet:\n")
            self.homeWidgetEmailerButtonStyleSheet = (self.lines[index+1])
        except Exception as e:
            print("Error configuring homeWidgetEmailerButtonStyleSheet: ",str(e))
            self.homeWidgetEmailerButtonStyleSheet = "background-image:url(email.png);background-repeat:no-repeat;background-position:center;font-size:14pt;padding-top:200px"

        #homeWidgetMerchButtonStyleSheet
        try:
            index = self.lines.index("Home Widget Merch Button StyleSheet:\n")
            self.homeWidgetMerchButtonStyleSheet = (self.lines[index+1])
        except Exception as e:
            print("Error configuring homeWidgetMerchButtonStyleSheet: ",str(e))
            self.homeWidgetMerchButtonStyleSheet = "background-image:url(merch.png);background-repeat:no-repeat;background-position:center;font-size:14pt;padding-top:200px"

        #homeWidgetFestName
        try:
            index = self.lines.index("Home Widget Fest Name:\n")
            self.homeWidgetFestName = (self.lines[index+1])
        except Exception as e:
            print("Error configuring homeWidgetFestName: ",str(e))
            self.homeWidgetFestName = "BOSM 2013"

        #homeWidgetFestLabelFont = "font: bold;font-size:20pt"
        try:
            index = self.lines.index("Home Widget Fest Label Font:\n")
            self.homeWidgetFestLabelFont = (self.lines[index+1])
        except Exception as e:
            print("Error configuring homeWidgetFestLabelFont: ",str(e))
            self.homeWidgetFestLabelFont = "font: bold;font-size:20pt"

        #leftWidgetSnapViewerSize
        try:
            index = self.lines.index("Left Widget Snap Viewer Dimension:\n")
            self.leftWidgetSnapViewerSize = int(self.lines[index+1])
        except Exception as e:
            print("Error configuring leftWidgetSnapViewerSize: ",str(e))
            self.leftWidgetSnapViewerSize = 150

        #searchWidgetHeight
        try:
            index = self.lines.index("Search Widget Height:\n")
            self.searchWidgetHeight = int(self.lines[index+1])
        except Exception as e:
            print("Error configuring searchWidgetHeight: ",str(e))
            self.searchWidgetHeight = 210

        #unbillingTableHeight
        try:
            index = self.lines.index("Unbilling Table Height:\n")
            self.unbillingTableHeight = int(self.lines[index+1])
        except Exception as e:
            print("Error configuring unbillingTableHeight: ",str(e))
            self.unbillingTableHeight = 500



    def loadTheme(self):
        pass
