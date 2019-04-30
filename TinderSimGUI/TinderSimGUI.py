from PyQt5 import Qt

from PyQt5 import QtCore, QtGui                                                 #PyQt4
from PyQt5.QtCore import QObject
'''
from PyQt5.QtGui import *                                                       #PyQt4
from PyQt5.QtCore import *                                                      #PyQt4
'''

import pymysql
pymysql.install_as_MySQLdb()

from subprocess import *
import sys, os

cwd = ""
tempDir = ""

testers = "donald alwyn daniel luis eli tristan zane darren stephen"
userList = testers.split()
currentUser = ""
candidateUserID = 0
candidateName = ""
candidateImagePath = ""
selectionValue = -1

#############################
##   Main Window                (nothing displayed for now)
#############################

# Declare class mainStart, inherits from QtGui.QWidget
class progStart(Qt.QWidget):                                                 #QtGui.QWidget)

    # Define __init__() method calling two constructors first for mainStart class and second for inherited class
    def __init__(self):
        super(progStart, self).__init__()
        self.counter = 0
        self.initUI()

    # GUI window created in this method where I add widgets and specify their layout
    def initUI(self):
        global currentUser, candidateUserID, candidateName, candidateImagePath, selectionValue, cwd, tempDir

        pipecwd = Popen(('pwd'), shell=True,stdout=PIPE).stdout
        cwd = pipecwd.read().rstrip().decode("utf-8")
        profileDir = cwd + "/Profiles"
        currentUser = self.showLoginDialog()

        db = pymysql.connect('localhost', 'root', 'password', 'TinderSimDB')
        cursor = db.cursor()
        currentUserIDQuery = "SELECT USER_ID, GENDER_PREF FROM USER WHERE NAME LIKE '%s'" % (currentUser)
        cursor.execute(currentUserIDQuery)
        recordCUID = cursor.fetchone()
        cUID = recordCUID[0]
        createUserDirPath = profileDir + "/%s" % (cUID)
        pipecheckDir = Popen(('if [ ! -d %s ]; then echo \"not exists\"; fi' % createUserDirPath), shell=True, stdout=PIPE).stdout
        dirCheck = pipecheckDir.read().rstrip().decode("utf-8")
        print(dirCheck)
        if dirCheck == "not exists":
            makeUserDirCommand = Popen(('mkdir %s' % createUserDirPath), shell=True)
            makeUserDirCommand.wait()
            cGP = recordCUID[1]
            cGPDir = cGP + "s"
            genderDir = createUserDirPath + "/%s" % (cGPDir)
            makeGenderDirCommand = Popen(('mkdir %s' % genderDir), shell=True)
            makeGenderDirCommand.wait()
            hotDir = genderDir + "/Hot"
            makeHotDirCommand = Popen(('mkdir %s' % hotDir), shell=True)
            makeHotDirCommand.wait()
            notDir = genderDir + "/Not"
            makeNotDirCommand = Popen(('mkdir %s' % notDir), shell=True)
            makeNotDirCommand.wait()
            currentUserRateQuery = "SELECT USER_ID, NAME, IMAGE_FILE_PATH FROM USER WHERE GENDER LIKE '%s'" % (cGP)
            cursor.execute(currentUserRateQuery)
            curRecords = cursor.fetchall()

            print(curRecords)

            if len(curRecords) != 0:
                for row in curRecords:
                    candidateUserID = row[0]
                    candidateName = row[1]
                    candidateImagePath = row[2]
                    imageName = candidateImagePath.split('/')[-1]
                    #print(imageName)
                    showImage()
                    if selectionValue == 0:
                        copyDestPath = notDir + "/%s" % imageName
                        copyImageCommand = Popen(('cp %s %s' % (candidateImagePath, copyDestPath)), shell=True)
                        copyImageCommand.wait()
                    elif selectionValue == 1:
                        copyDestPath = hotDir + "/%s" % imageName
                        copyImageCommand = Popen(('cp %s %s' % (candidateImagePath, copyDestPath)), shell=True)
                        copyImageCommand.wait()
                    insertQuery = "INSERT INTO USER_SELECTION(USER_USER_ID, OTHER_USER_ID, USER_SELECTION_VALUE) " \
                                  "VALUES " \
                                  "('%s', '%s', '%s')" % \
                                  (int(cUID), int(candidateUserID), int(selectionValue))
                    try:
                        cursor.execute(insertQuery)
                        db.commit()
                    except:
                        db.rollback()
            else:
                print("No images for user to rate.")
                self.center()
                self.resize(800, 600)
                completeLabel = QtGui.QLabel('No images for user to rate.')
                completeLabel.setAlignment(QtCore.Qt.AlignCenter)

                hbox = Qt.QHBoxLayout(self)
                #QtGui.QHBoxLayout(self)
                hbox.addWidget(completeLabel)

                self.setLayout(hbox)
                #sys.exit()

            print("All images rated.")
            self.center()
            self.resize(800, 600)
            completeLabel = Qt.QLabel('All images rated.')
            #QtGui.QLabel('All images rated.')
            completeLabel.setAlignment(QtCore.Qt.AlignCenter)

            hbox = Qt.QHBoxLayout(self)
            #QtGui.QHBoxLayout(self)
            hbox.addWidget(completeLabel)

            self.setLayout(hbox)
            #sys.exit()
        else:
            print("User already rated all images.")
            self.center()
            self.resize(800, 600)
            completeLabel = Qt.QLabel('User already rated all images.')
            #QtGui.QLabel('User already rated all images.')
            completeLabel.setAlignment(QtCore.Qt.AlignCenter)

            hbox = Qt.QHBoxLayout(self)
            #QtGui.QHBoxLayout(self)
            hbox.addWidget(completeLabel)

            self.setLayout(hbox)
            #sys.exit()

    def center(self):
        qr = self.frameGeometry()
        cp = Qt.QDesktopWidget().availableGeometry().center()
        #QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showLoginDialog(self):
        global userList, currentUser
        userName, ok = Qt.QInputDialog.getItem(self, "TinderSim", "Tester Login:", userList, 0, False)
        #QtGui.QInputDialog.getItem(self, "TinderSim", "Tester Login:", userList, 0, False)

        if ok and userName:
            return userName
###############################################

#############################
##   Show Image Window
#############################

class showImage(Qt.QWidget):                                                    #QtGui.QWidget
    #keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self):
        super(showImage, self).__init__()
        self.counter = 0
        self.dialog = Qt.QDialog()
        #QtGui.QDialog()
        self.initUI()

    def initUI(self):
        global currentUser, candidateUserID, candidateName, candidateImagePath, selectionValue

        #QtCore.QObject.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), self.dialog),
        #                       QtCore.SIGNAL('activated()'), self.fooLeft)
        #QtCore.QObject.connect(QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), self.dialog),
        #                       QtCore.SIGNAL('activated()'), self.fooRight)
        self.dialog.resize(800,600)
        image = Qt.QLabel(self.dialog)
        #QtGui.QLabel(self.dialog)
        image.setAlignment(QtCore.Qt.AlignCenter)
        hotButton = Qt.QPushButton("Hot", self.dialog)
        #QtGui.QPushButton("Hot", self.dialog)
        notButton = Qt.QPushButton("Not", self.dialog)
        #QtGui.QPushButton("Not", self.dialog)
        hotButton.clicked.connect(self.hotAdd)
        notButton.clicked.connect(self.notAdd)
        grid = Qt.QGridLayout(self.dialog)
        #QtGui.QGridLayout(self.dialog)
        grid.setSpacing(5)

        hbox = Qt.QHBoxLayout()
        #QtGui.QHBoxLayout()
        hbox.addWidget(image)

        grid.addLayout(hbox,0,0,12,12)
        grid.addWidget(notButton,14,4,1,2)
        grid.addWidget(hotButton,14,6,1,2)
        self.dialog.setLayout(grid)

        pixmap = Qt.QPixmap(candidateImagePath)
        #QtGui.QPixmap(candidateImagePath)
        scaledPixmap = pixmap.scaled(600,400, QtCore.Qt.KeepAspectRatio)
        image.setPixmap(scaledPixmap)
        self.dialog.setWindowTitle(candidateName)
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dialog.exec_()

    def center(self):
        qr = self.frameGeometry()
        cp = Qt.QDesktopWidget().availableGeometry().center()
        #QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def hotAdd(self):
        global selectionValue
        selectionValue = 1
        self.dialog.close()

    def notAdd(self):
        global selectionValue
        selectionValue = 0
        self.dialog.close()

    def fooLeft(self):
        global selectionValue
        selectionValue = 0
        self.dialog.close()

    def fooRight(self):
        global selectionValue
        selectionValue = 1
        self.dialog.close()
###############################################

def main():
    app = Qt.QApplication(sys.argv)                                             #QtGui.QApplication(sys.argv)
    a = progStart()
    a.show()
    sys.exit(app.exec_())

main()
