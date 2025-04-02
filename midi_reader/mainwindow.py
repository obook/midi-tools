# This Python file uses the following encoding: utf-8
'''
Require : PySide6 mido python-rtmidi
'''
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QEvent
from midifile_reader import class_reader
from midi_numbers import number_to_note

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    ''' QT main window '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("MIDI Reader")

        self.ui.pushButton_Load.clicked.connect(self.load_file)
        self.ui.pushButton_Quit.clicked.connect(self.quit_application)
        self.setAcceptDrops(True)
        self.installEventFilter(self)  # drop files on readonly PlainTextEdit

    def load_file(self):
        ''' file dialog '''

        fname = QFileDialog.getOpenFileName(
                self,
                "Open Midi File",
                "",
                "MIDI Files (*.mid) ;; All Files (*)",
                )

        # pour tests
        # fname = ["/home/obooklage/Insync/obooklage@gmail.com/Google Drive/ownCloud.CAP/MUSIQUE/A-TRIER-2025/69131_Black-Ops-Zombie.mid"]

        if fname:
            file = fname[0]
            self.print_info(file)

    def print_info(self, file):
        ''' print informations in QPlainEditText '''
        name = os.path.basename(file)
        reader = class_reader(file)
        self.setWindowTitle(name)
        notes_msg = reader.get_notes()

        self.ui.plainTextEdit.clear()

        self.ui.plainTextEdit.appendPlainText("START")

        for msg in notes_msg:
            self.ui.plainTextEdit.appendPlainText(str(number_to_note(msg.note)))

        self.ui.plainTextEdit.appendPlainText("END")

    def eventFilter(self, o, e):
        ''' intercept files dropped '''
        '''
        Il faut que le QMainWindow soit droppable *MAIS PAS* QPlainTextEdit !
        '''
        if e.type() == QEvent.DragEnter:  # remember to accept the enter event
            e.acceptProposedAction()
            return True
        if e.type() == QEvent.Drop:
            data = e.mimeData()
            urls = data.urls()

            print("DROP !")

            if urls and urls[0].scheme() == "file":
                self.print_info(urls[0].toLocalFile())
            return True
        return False  # remember to return false for other event types

    def closeEvent(self, event):  # overwritten
        ''' Windows closed by desktop '''
        print("closeEvent")
        self.quit_application()

    def quit_application(self):
        ''' The end '''
        print("quit_application")
        # self.deleteLater()
        QApplication.quit()


if __name__ == "__main__":
    # BUG : fnot closed under Qt Python virtual env
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
