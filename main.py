import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog
from PyQt6.QtCore import QTimer
from scorekeeper_ui import Ui_MainWindow
from options_ui import Ui_Dialog

class MainWindow:
    def __init__(self):

        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.signals()

    def show(self):
        self.main_win.show()

    def update_timer(self):
        time = self.ui.lcd_timer_minutes.value() * 60 + self.ui.lcd_timer_seconds.value()
        if time > 0:
            time -= 1
            self.ui.lcd_timer_minutes.display(time // 60)
            self.ui.lcd_timer_seconds.display(time % 60)
        else:
            self.timer.stop()
            self.ui.button_startstop.setText("Start")
            self.ui.lcd_timer_minutes.display(self.dialog.ui.spin_minutes.value())
            self.ui.lcd_timer_seconds.display(self.dialog.ui.spin_seconds.value())

    def signals(self):
        """
        Connects the UI buttons to the corresponding functions (see slots)
        """
        self.ui.action_configure.triggered.connect(self.options)
        self.ui.action_quit.triggered.connect(self.main_win.close)

        self.ui.action_reset.triggered.connect(lambda: self.ui.label_left_score.setText(str(0)))
        self.ui.action_reset.triggered.connect(lambda: self.ui.label_right_score.setText(str(0)))
        self.ui.action_reset.triggered.connect(lambda: self.ui.lcd_timer_minutes.display(self.dialog.ui.spin_minutes.value()))
        self.ui.action_reset.triggered.connect(lambda: self.ui.lcd_timer_seconds.display(self.dialog.ui.spin_seconds.value()))

        self.ui.action_export.triggered.connect(self.export_conf)
        self.ui.action_import.triggered.connect(self.import_conf)

        self.ui.button_startstop.clicked.connect(self.timer)
        
        self.ui.button_left_score_top.clicked.connect(lambda: self.ui.label_left_score.setText(str(int(self.ui.label_left_score.text()) + int(self.ui.button_left_score_top.text()))))
        self.ui.button_left_score_middle.clicked.connect(lambda: self.ui.label_left_score.setText(str(int(self.ui.label_left_score.text()) + int(self.ui.button_left_score_middle.text()))))
        self.ui.button_left_score_bottom.clicked.connect(lambda: self.ui.label_left_score.setText(str(int(self.ui.label_left_score.text()) + int(self.ui.button_left_score_bottom.text()))))

        self.ui.button_right_score_top.clicked.connect(lambda: self.ui.label_right_score.setText(str(int(self.ui.label_right_score.text()) + int(self.ui.button_right_score_top.text()))))
        self.ui.button_right_score_middle.clicked.connect(lambda: self.ui.label_right_score.setText(str(int(self.ui.label_right_score.text()) + int(self.ui.button_right_score_middle.text()))))
        self.ui.button_right_score_bottom.clicked.connect(lambda: self.ui.label_right_score.setText(str(int(self.ui.label_right_score.text()) + int(self.ui.button_right_score_bottom.text()))))

    # ----- slots ----- #

    def timer(self):
        if self.ui.button_startstop.text() == "Start":
            self.ui.button_startstop.setText("Stop")
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_timer)
            self.timer.start(1000)
        else:
            self.ui.button_startstop.setText("Start")
            self.timer.stop()

    def options(self):
        self.dialog = Options(self.main_win)

        self.dialog.ui.button_apply.clicked.connect(self.apply)
        self.dialog.ui.button_cancel.clicked.connect(self.dialog.close)

        self.dialog.ui.edit_left_name.setText(self.ui.label_left_name.text())
        self.dialog.ui.edit_right_name.setText(self.ui.label_right_name.text())

        self.dialog.ui.spin_button_top.setValue(int(self.ui.button_left_score_top.text()))
        self.dialog.ui.spin_button_middle.setValue(int(self.ui.button_left_score_middle.text()))
        self.dialog.ui.spin_button_bottom.setValue(int(self.ui.button_left_score_bottom.text()))

        self.dialog.ui.spin_minutes.setValue(int(self.ui.lcd_timer_minutes.value()))
        self.dialog.ui.spin_seconds.setValue(int(self.ui.lcd_timer_seconds.value()))

        self.dialog.exec()

    def apply(self):

        self.ui.label_left_name.setText(self.dialog.ui.edit_left_name.text())
        self.ui.label_right_name.setText(self.dialog.ui.edit_right_name.text())

        self.ui.button_left_score_top.setText(str(self.dialog.ui.spin_button_top.value()))
        self.ui.button_left_score_middle.setText(str(self.dialog.ui.spin_button_middle.value()))
        self.ui.button_left_score_bottom.setText(str(self.dialog.ui.spin_button_bottom.value()))

        self.ui.button_right_score_top.setText(str(self.dialog.ui.spin_button_top.value()))
        self.ui.button_right_score_middle.setText(str(self.dialog.ui.spin_button_middle.value()))
        self.ui.button_right_score_bottom.setText(str(self.dialog.ui.spin_button_bottom.value()))

        self.ui.lcd_timer_minutes.display(self.dialog.ui.spin_minutes.value())
        self.ui.lcd_timer_seconds.display(self.dialog.ui.spin_seconds.value())

        self.dialog.close()

    def export_conf(self):

        settings = {
            "left_name": self.ui.label_left_name.text(),
            "right_name": self.ui.label_right_name.text(),
            "button_top": self.ui.button_left_score_top.text(),
            "button_middle": self.ui.button_left_score_middle.text(),
            "button_bottom": self.ui.button_left_score_bottom.text(),
            "timer_minutes": int(self.ui.lcd_timer_minutes.value()),
            "timer_seconds": int(self.ui.lcd_timer_seconds.value())
        }

        file = QFileDialog.getSaveFileName(self.main_win, "Save file", f"configs/{self.ui.label_left_name.text()} v {self.ui.label_right_name.text()} ({int(self.ui.lcd_timer_minutes.value())}:{int(self.ui.lcd_timer_seconds.value()).format()}, {self.ui.button_left_score_top.text()}, {self.ui.button_left_score_middle.text()}, {self.ui.button_left_score_bottom.text()}).json", "JSON (*.json)")

        if file[0] != "":
            with open(file[0], "w") as export:
                json.dump(settings, export, indent=4)

    def import_conf(self):  # sourcery skip: extract-method

        file = QFileDialog.getOpenFileName(self.main_win, "Open file", "configs/", "JSON (*.json)")
        
        if file[0] != "":
            with open(file[0], "r") as import_:
                settings = json.load(import_)

            self.ui.label_left_name.setText(settings["left_name"])
            self.ui.label_right_name.setText(settings["right_name"])

            self.ui.button_left_score_top.setText(settings["button_top"])
            self.ui.button_left_score_middle.setText(settings["button_middle"])
            self.ui.button_left_score_bottom.setText(settings["button_bottom"])

            self.ui.button_right_score_top.setText(settings["button_top"])
            self.ui.button_right_score_middle.setText(settings["button_middle"])
            self.ui.button_right_score_bottom.setText(settings["button_bottom"])

            self.ui.lcd_timer_minutes.display(settings["timer_minutes"])
            self.ui.lcd_timer_seconds.display(settings["timer_seconds"])

class Options(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.signals()

    def signals(self):
        """
        Connects the UI buttons to the corresponding functions (see slots)
        """
        pass

    # ----- slots ----- #

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()

    sys.exit(app.exec())