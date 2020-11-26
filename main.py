import sys
import os
from random import randint

from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QSystemTrayIcon, QMenu
from plyer import notification
from ui_function import *


class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = uic.loadUi('ui_main.ui', self)
        #self.setWindowIcon(QtGui.QIcon('eye_icon.png'))
        # ~~~~~~~~~~~ SET UI DEFINITIONS ~~~~~~~~~~ #
        UIFunctions.uiDefinitions(self)
        self.setupIcon()

        # ~~~ GET ATTRIBUTES FROM SYSTEM SETTING ~~ #

        self.settings = QtCore.QSettings('CareurEyes', 'Settings')
        self.messages = self.settings.value('message_reminder')

        self.getUserName()
        self.getTime()
        self.getOption()
        self.setMessageList()
        self.getMessageList()

        self.timer = QtCore.QTimer()
        self.isRunning = False
        # ======================================================== #
        # ==================== LEFT SIDE MENU ==================== #
        # ======================================================== #

        # TOGGLE BUTTON 
        self.ui.btnToggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 100, True))

        # ======================================================== #
        # ========================= PAGES ======================== #
        # ======================================================== #
        
        # SET DEFAULT TO SETTING PAGE
        self.ui.stackedWidgetContainer.setCurrentWidget(self.ui.pageSetting)

        # PAGE 1
        self.ui.btnPageSetting.clicked.connect(
            lambda: self.ui.stackedWidgetContainer.setCurrentWidget(self.ui.pageSetting))

        # PAGE 2
        self.ui.btnPageReminder.clicked.connect(
            lambda: self.ui.stackedWidgetContainer.setCurrentWidget(self.ui.pageReminder))

        # PAGE 3
        self.ui.btnPageTips.clicked.connect(
            lambda: self.ui.stackedWidgetContainer.setCurrentWidget(self.ui.pageTips))
        # ======================================================== #
        # ======================= END PAGES ====================== #
        # ======================================================== #

        # ~~~~~~~~~~~ SETTING ON EDITING ~~~~~~~~~~ #
        self.ui.lineEditUserName.editingFinished.connect(self.setUserName)
        self.ui.spinBoxTime.valueChanged.connect(self.setTime)
        self.ui.radioButtonType_Toast.toggled.connect(self.setMessageOption)
        # self.ui.textEditReminder.textChanged.connect(self.setMessageList)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # ~~~~~~~~~~~ RUN/STOP REMINDER ~~~~~~~~~~~ # 
        self.ui.btnStart.clicked.connect(self.run)
        self.ui.btnStop.clicked.connect(self.stopReminder)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # ~~~~~~~~~~~~~~ MOVE WINDOW ~~~~~~~~~~~~~~ #
        def moveWindow(event):
            # RESTORE BEFORE MOVE
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximize_restore(self)

            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        # ~~~~~~~~~~~~~ SET TITLE BAR ~~~~~~~~~~~~~ #
        self.ui.frameTitleBar.mouseMoveEvent = moveWindow
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        self.getAnimalIcons()

    # ~~~~~~~~ SETUP ICONS FOR BUTTONS ~~~~~~~~ #
    def setupIcon(self):
        self.ui.btnClose.setIcon(QtGui.QIcon("icons/icon_close.png"))
        self.ui.btnMaximize.setIcon(QtGui.QIcon("icons/icon_resize.png"))
        self.ui.btnToggle.setIcon(QtGui.QIcon("icons/hamburger.png"))
        self.ui.btnPageSetting.setIcon(QtGui.QIcon("icons/icon_setting.png"))
        self.ui.btnPageReminder.setIcon(QtGui.QIcon("icons/icon_message.png"))
        self.ui.btnPageTips.setIcon(QtGui.QIcon("icons/icon_file_text.png"))
        self.ui.btnPageHelp.setIcon(QtGui.QIcon("icons/icon_help.png"))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # ~~~~~~~~~~~~~~~ APP EVENTS ~~~~~~~~~~~~~~ #
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # ======================================================== #
    # ======================== METHODS ======================= #
    # ======================================================== #
    def getMessageList(self):
        if not self.messages:
            mes_list = []
            listWidgetReminders = self.ui.listWidgetReminders
            if listWidgetReminders.count() > 0:
                for i in range(0, listWidgetReminders.count()):
                    mes_list.append(listWidgetReminders.item(i).text())
            return mes_list
        else:
            return self.messages

    def setMessageList(self):
        mes_list = []
        listWidgetReminders = self.ui.listWidgetReminders
        #print("count: ", listWidgetReminders.count())
        if listWidgetReminders.count() > 0:
            for i in range(0, listWidgetReminders.count()):
                mes_list.append(listWidgetReminders.item(i).text())
            self.settings.setValue('message_reminder', mes_list)

    def getRandomMessage(self):
        index = randint(0, len(self.getMessageList())-1)
        # print('len of list: ', len(self.getMessageList()))
        # print(self.getMessageList())
        # print('index: ', index)
        # print("mes from getRandom: ",self.getMessageList()[index] )
        return self.getMessageList()[index]

    def getUserName(self):
        st_user_name = self.settings.value('user_name')
        if not st_user_name:
            return self.ui.lineEditUserName.text()
        else:
            self.ui.lineEditUserName.setText(st_user_name)
            return st_user_name

    def getTime(self):
        st_time = self.settings.value('time')
        if not st_time:
            return self.ui.spinBoxTime.value()
        else:
            self.ui.spinBoxTime.setValue(st_time)
            return st_time

    def getOption(self):
        option = self.settings.value('message_option')
        if not option:
            if self.ui.radioButtonType_Toast.isChecked():
                option = 'toast'
            elif self.ui.radioButtonType_Popup.isChecked():
                option = 'popup'
        else:
            if option == 'toast':
                self.ui.radioButtonType_Toast.setChecked(True)
            elif option == 'popup':
                self.ui.radioButtonType_Popup.setChecked(True)
        return option

    def getAnimalIcons(self):
        path = os.path.dirname(__file__) + '/icons/cute_animals'
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if '.ico' in file:
                    files.append(os.path.join(r, file))
        return files

    def getRandomAnimal(self):
        index = randint(0, len(self.getAnimalIcons()) - 1)
        return self.getAnimalIcons()[index]

    def setUserName(self):
        self.settings.setValue('user_name', self.ui.lineEditUserName.text())

    def setTime(self):
        self.settings.setValue('time', self.ui.spinBoxTime.value())

    def setMessageOption(self):
        option = ''
        if self.ui.radioButtonType_Toast.isChecked():
            option = 'toast'
        elif self.ui.radioButtonType_Popup.isChecked():
            option = 'popup'
        self.settings.setValue('message_option', option)

    def toastNotification(self):
        userName = self.getUserName()
        title = '{} ơi'.format(userName if userName else "Bạn")
        message = self.getRandomMessage()
        return notification.notify(title,
                                   message,
                                   app_name='Care your Eyes',
                                   app_icon=self.getRandomAnimal(),
                                   timeout=10,
                                   ticker='Care your Eyes',
                                   toast=True)

    def popupReminder(self):
        popup_reminder = RemindDialog()
        popup_reminder.ui.labelUserName.setText('{} ơi !'.format(self.getUserName() if self.getUserName() else "Bạn"))
        popup_reminder.ui.labelReminderText.setText(self.getRandomMessage())
        QtCore.QTimer.singleShot(15000, popup_reminder.accept)

        app.setQuitLockEnabled(False)

    def run(self):
        if self.isRunning:
            self.stopReminder()
        if self.getOption() == 'toast':
            self.timer.timeout.connect(self.toastNotification)
        elif self.getOption() == 'popup':
            self.timer.timeout.connect(self.popupReminder)

        self.timer.setInterval(self.getTime() * 60000)
        self.timer.start()
        self.isRunning = True
        print('Running')
        # RUN APP IN SYSTEMTRAYICON
        self.trayIcon = QSystemTrayIcon(QtGui.QIcon('eye_icon-removebg.png'), parent=app)
        self.trayIcon.setToolTip("Care Your Eyes")
        self.trayIcon.activated.connect(self.showWindow)
        contextMenu = QMenu()
        openAction = contextMenu.addAction("Mở")
        openAction.triggered.connect(self.showWindow)
        exitAction = contextMenu.addAction('Thoát')
        exitAction.triggered.connect(app.quit)
        self.trayIcon.setContextMenu(contextMenu)
        self.trayIcon.show()

        # HIDE APP
        self.hide()

    def stopReminder(self):
        print('Stopped')
        if self.isRunning:
            self.timer.disconnect()
            self.timer.stop()
            self.isRunning = False

    def showWindow(self):
        self.show()
        app.setQuitLockEnabled(True)
    # ======================================================== #
    # ====================== END METHODS ===================== #
    # ======================================================== #
class RemindDialog(QDialog):
    def __init__(self):
        super(RemindDialog, self).__init__()
        self.ui = uic.loadUi('ui_remind_dialog.ui', self)
        self.setWindowIcon(QtGui.QIcon('eye_icon.png'))
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setQuitOnLastWindowClosed(False)
    window = AppWindow()
    # IF THE APP RUN IN THE FIRST TIME
    if not window.settings.value('user_name'):
        # SHOW WINDOW
        window.showWindow()
    else:
        # AUTO RUN APP IN SYS TRAYICON
        window.run()
        window.trayIcon.showMessage("Care your Eyes is running", "Click to open",
                                    QtGui.QIcon('icons/logoCareYourEyes_circle.ico'))
        window.trayIcon.messageClicked.connect(window.showWindow)
    # EXIT APP
    sys.exit(app.exec_())
