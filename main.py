import sys
from time import sleep

from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QSystemTrayIcon, QMenu
from plyer import notification
import appresources
from ui_function import *


class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = uic.loadUi('ui_main.ui', self)
        self.setWindowIcon(QtGui.QIcon('eye_icon.png'))
        self.setupIcon()
        self.settings = QtCore.QSettings('CareurEyes', 'Settings')
        self.getUserName()
        self.getTime()
        self.getOption()
        self.ui.btnToggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 100, True))
        self.ui.btnStart.clicked.connect(self.run)
        self.ui.lineEditUserName.editingFinished.connect(self.setUserName)
        self.ui.spinBoxTime.valueChanged.connect(self.setTime)
        self.ui.radioButtonType_Toast.toggled.connect(self.setMessageOption)

        # MOVE WINDOW
        def moveWindow(event):
            # RESTORE BEFORE MOVE
            if UIFunctions.returnStatus() == 1:
                UIFunctions.maximize_restore(self)

            # IF LEFT CLICK MOVE WINDOW
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # SET TITLE BAR
        self.ui.frameTitleBar.mouseMoveEvent = moveWindow

        ## ==> SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)
        # self.show()

    ## SETUP
    def setupIcon(self):
        self.ui.btnClose.setIcon(QtGui.QIcon("icons/icon_close.png"))
        self.ui.btnMaximize.setIcon(QtGui.QIcon("icons/icon_resize.png"))
        self.ui.btnToggle.setIcon(QtGui.QIcon("icons/hamburger.png"))
        self.ui.btnPageSetting.setIcon(QtGui.QIcon("icons/icon_setting.png"))
        self.ui.btnPageReminder.setIcon(QtGui.QIcon("icons/icon_message.png"))
        self.ui.btnPageMessages.setIcon(QtGui.QIcon("icons/icon_file_text.png"))
        self.ui.btnPageHelp.setIcon(QtGui.QIcon("icons/icon_help.png"))

    ## APP EVENTS
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def getMessage(self):
        return '{0}\nĐã {1} phút rồi bạn chưa rời mắt khỏi màn hình đó :<'. \
            format(self.ui.textEditReminder.toPlainText(), str(self.getTime()))

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
        return notification.notify(title='{} ơi'.format(userName if userName else "Bạn"),
                                   message=self.getMessage(),
                                   app_name='Rest for Eyes', app_icon='eye_icon.ico',
                                   timeout=10,
                                   ticker='Rest for Eyes',
                                   toast=True)

    def popupReminder(self):
        popup_reminder = RemindDialog()
        popup_reminder.ui.labelUserName.setText('{} ơi !'.format(self.getUserName() if self.getUserName() else "Bạn"))
        popup_reminder.ui.labelReminderText.setText(self.getMessage())

    def run(self):
        timer = QtCore.QTimer()
        if self.getOption() == 'toast':
            timer.timeout.connect(self.toastNotification)
        elif self.getOption() == 'popup':
            timer.timeout.connect(self.popupReminder)

        timer.setInterval(1000)
        timer.start()


class RemindDialog(QDialog):
    def __init__(self):
        super(RemindDialog, self).__init__()
        self.ui = uic.loadUi('ui_remind_dialog.ui', self)
        self.setWindowIcon(QtGui.QIcon('eye_icon.png'))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    # IF THE APP RUN THE FIRST TIME
    print(not window.settings.value('user_name'))
    if not window.settings.value('user_name'):
        window.show()
    else:
        # RUN APP IN SYSTEMTRAYICON
        trayIcon = QSystemTrayIcon(QtGui.QIcon('eye_icon-removebg.png'), parent=app)
        trayIcon.setToolTip("Care Your Eyes")

        contextMenu = QMenu()
        openAction = contextMenu.addAction("Mở")
        openAction.triggered.connect(window.show)
        exitAction = contextMenu.addAction('Thoát')
        exitAction.triggered.connect(app.quit)

        trayIcon.setContextMenu(contextMenu)
        trayIcon.show()

    # EXIT APP
    sys.exit(app.exec_())
