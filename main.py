import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QSizeGrip
from PyQt5 import uic, QtCore, QtGui
from plyer import notification
from ui_function import *
class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = uic.loadUi('ui_main.ui', self)
        self.setWindowIcon(QtGui.QIcon('eye_icon.png'))
        self.ui.btnToggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))
        self.ui.btnStart.clicked.connect(self.run)

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
        self.show()

    ## APP EVENTS
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def getMessage(self):
        return '{0}\nĐã {1} phút rồi bạn chưa rời mắt khỏi màn hình đó :<'. \
            format(self.ui.textEditReminder.toPlainText(), str(self.getTime()))

    def getUserName(self):
        return self.ui.lineEditUserName.text()

    def getTime(self):
        return self.ui.spinBoxTime.value()

    def getOption(self):
        option = ''
        if self.ui.radioButtonType_Toast.isChecked():
            option = 'toast'
        elif self.ui.radioButtonType_Popup.isChecked():
            option = 'popup'
        return option

    def toastNotification(self):
        userName = self.getUserName()
        toaster = notification.notify(title='{} ơi'.format(userName if userName else "Bạn"),
                                      message=self.getMessage(),
                                      app_name='Rest for Eyes', app_icon='eye_icon.ico',
                                      timeout=30,
                                      ticker='Rest for Eyes',
                                      toast=True)

    def popupReminder(self):
        popup_reminder = RemindDialog()
        popup_reminder.ui.labelUserName.setText('{} ơi !'.format(self.getUserName() if self.getUserName() else "Bạn"))
        popup_reminder.ui.labelReminderText.setText(self.getMessage())

    def run(self):
        if self.getOption() == 'toast':
            self.toastNotification()
        elif self.getOption() == 'popup':
            self.popupReminder()


class RemindDialog(QDialog):
    def __init__(self):
        super(RemindDialog, self).__init__()
        self.ui = uic.loadUi('ui_remind_dialog.ui', self)
        self.setWindowIcon(QtGui.QIcon('eye_icon.png'))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    sys.exit(app.exec_())
