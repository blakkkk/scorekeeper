import sys
import json
import os
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
        time = (
            self.ui.lcd_timer_minutes.value() * 60 + self.ui.lcd_timer_seconds.value()
        )  # calculate time in seconds

        if time > 0:                                # when time is not over
            time -= 1                                   # decrease time by 1 second
            self.ui.lcd_timer_minutes.display(
                time // 60                              # floor division on seconds to display minutes
            ) 
            self.ui.lcd_timer_seconds.display(
                self.leading_zero(time % 60)            # modulo on seconds to display seconds
            )

            if self.ui.lcd_timer_seconds.value() % 2 == 0: # blink the colon every second
                self.ui.label_colon.setProperty(
                    "styleSheet",
                    "border-color: transparent; font: bold 50pt ""TT Supermolot""",
                )
            else:
                self.ui.label_colon.setProperty(
                    "styleSheet",
                    "border-color: transparent; font: bold 50pt ""TT Supermolot""; color: transparent",
                )

        else:                                       # when time is over
            self.timer.stop()                           # stop the timer
            self.ui.button_startstop.setText("Start")   # display start on the button
            self.ui.lcd_timer_minutes.display(
                timer_minutes                           # reset the minutes
            )
            self.ui.lcd_timer_seconds.display(
                timer_seconds                           # reset the seconds
            )

    def leading_zero(self, number):
        return f"{int(number):02d}"  # add a leading zero to the number if it is less than 10

    def signals(self):
        # actions menu

        self.ui.action_undo.triggered.connect(self.undo)

        self.ui.action_reset.triggered.connect(lambda: self.reset())

        self.ui.action_quit.triggered.connect(self.main_win.close)

        # configuration menu

        self.ui.action_configure.triggered.connect(self.options)

        self.ui.action_export.triggered.connect(self.export_conf)
        self.ui.action_import.triggered.connect(self.import_conf)

        # main window buttons

        self.ui.button_startstop.clicked.connect(self.timer)

        self.ui.button_left_score_top.clicked.connect(
            lambda: self.score("left", "top")
        )
        self.ui.button_left_score_middle.clicked.connect(
            lambda: self.score("left", "middle")
        )
        self.ui.button_left_score_bottom.clicked.connect(
            lambda: self.score("left", "bottom")
        )

        self.ui.button_right_score_top.clicked.connect(
            lambda: self.score("right", "top")
        )
        self.ui.button_right_score_middle.clicked.connect(
            lambda: self.score("right", "middle")
        )
        self.ui.button_right_score_bottom.clicked.connect(
            lambda: self.score("right", "bottom")
        )

    # ----- slots ----- #

    def timer(self):
        if (
            self.ui.button_startstop.text() == "Start"      # if the button displays start (i.e. the timer is not running)
        ):
            self.ui.button_startstop.setText("Stop")            # display stop on the button
            self.timer = QTimer()                               # create a timer
            self.timer.timeout.connect(self.update_timer)       # connect the timer to the update_timer function
            self.timer.start(1000)                              # start the timer with a 1 second interval
        else:                                               # if the button displays stop (i.e. the timer is running)
            self.ui.button_startstop.setText("Start")           # display start on the button
            self.timer.stop()                                   # stop the timer

    def score(self, side, position):
        # execute an f string the updates the score with the value and team of the button
        exec(
            f"self.ui.label_{side}_score.setText(str(int(self.ui.label_{side}_score.text()) + int(self.ui.button_{side}_score_{position}.text())))"
        )

        # appends the button pressed a list to allow undoing
        scoring.append((side, position))

    def undo(self):
        # if there is nothing to undo, return
        if len(scoring) <= 0:
            return

        # grab the last button pressed from the list
        last = scoring.pop()

        # execute and f string that subtract the value of the button pressed from the score of the team
        exec(
            f"self.ui.label_{last[0]}_score.setText(str(int(self.ui.label_{last[0]}_score.text()) - int(self.ui.button_{last[0]}_score_{last[1]}.text())))"
        )

    def reset(self):
        # reset the scores, timer and scoring list
        self.ui.label_left_score.setText(str(0))
        self.ui.label_right_score.setText(str(0))

        self.ui.lcd_timer_minutes.display(timer_minutes)
        self.ui.lcd_timer_seconds.display(timer_seconds)
        self.ui.button_startstop.setText("Start")
        self.timer.stop()

        scoring.clear()

    def options(self):
        # create a dialog window
        self.dialog = Options(self.main_win)

        # connect the buttons to their respective functions
        self.dialog.ui.button_apply.clicked.connect(self.apply)
        self.dialog.ui.button_cancel.clicked.connect(self.dialog.close)

        # set the values of the dialog window to the values of the main window in order to make editing easier
        self.dialog.ui.edit_left_name.setText(self.ui.label_left_name.text())
        self.dialog.ui.edit_right_name.setText(self.ui.label_right_name.text())
        self.dialog.ui.spin_button_top.setValue(
            int(self.ui.button_left_score_top.text())
        )
        self.dialog.ui.spin_button_middle.setValue(
            int(self.ui.button_left_score_middle.text())
        )
        self.dialog.ui.spin_button_bottom.setValue(
            int(self.ui.button_left_score_bottom.text())
        )
        self.dialog.ui.spin_minutes.setValue(int(self.ui.lcd_timer_minutes.value()))
        self.dialog.ui.spin_seconds.setValue(int(self.ui.lcd_timer_seconds.value()))

        # open the dialog window
        self.dialog.exec()

    def apply(self):
        # set the values of the main window to the values of the dialog window
        self.ui.label_left_name.setText(self.dialog.ui.edit_left_name.text())
        self.ui.label_right_name.setText(self.dialog.ui.edit_right_name.text())
        self.ui.button_left_score_top.setText(
            str(self.dialog.ui.spin_button_top.value())
        )
        self.ui.button_left_score_middle.setText(
            str(self.dialog.ui.spin_button_middle.value())
        )
        self.ui.button_left_score_bottom.setText(
            str(self.dialog.ui.spin_button_bottom.value())
        )
        self.ui.button_right_score_top.setText(
            str(self.dialog.ui.spin_button_top.value())
        )
        self.ui.button_right_score_middle.setText(
            str(self.dialog.ui.spin_button_middle.value())
        )
        self.ui.button_right_score_bottom.setText(
            str(self.dialog.ui.spin_button_bottom.value())
        )
        self.ui.lcd_timer_minutes.display(self.dialog.ui.spin_minutes.value())
        self.ui.lcd_timer_seconds.display(self.leading_zero(self.dialog.ui.spin_seconds.value()))

        global timer_seconds, timer_minutes
        timer_minutes = self.dialog.ui.spin_minutes.value()
        timer_seconds = self.dialog.ui.spin_seconds.value()

        # close the dialog window
        self.dialog.close()

    def export_conf(self):
        # create a dictionary of the settings
        settings = {
            "left_name": self.ui.label_left_name.text(),
            "right_name": self.ui.label_right_name.text(),
            "button_top": self.ui.button_left_score_top.text(),
            "button_middle": self.ui.button_left_score_middle.text(),
            "button_bottom": self.ui.button_left_score_bottom.text(),
            "timer_minutes": int(self.ui.lcd_timer_minutes.value()),
            "timer_seconds": int(self.ui.lcd_timer_seconds.value()),
        }

        # an f string the creates a name based on the configuration with the layout: left v right mm˸ss (top, middle, bottom).json
        name = (
            f"configs/{self.ui.label_left_name.text()} v {self.ui.label_right_name.text()}{int(self.ui.lcd_timer_minutes.value())}˸{int(self.ui.lcd_timer_seconds.value()):02d} ({self.ui.button_left_score_top.text()}, {self.ui.button_left_score_middle.text()}, {self.ui.button_left_score_bottom.text()}).json"
        )

        # create a configs folder if it doesnt exist
        if not os.path.exists("configs"):
            os.makedirs("configs")

        # if any of the required fields are empty, set the name to nothing
        if (
            self.ui.label_left_name.text() == ""
            or self.ui.label_right_name.text() == ""
            or self.ui.button_left_score_top.text() == ""
            or self.ui.button_left_score_middle.text() == ""
            or self.ui.button_left_score_bottom.text() == ""
            or int(self.ui.lcd_timer_minutes.value()) == 0 and int(self.ui.lcd_timer_seconds.value()) == 0
        ):
            name = "configs/"

        # open a save file dialog
        file = QFileDialog.getSaveFileName(
            self.main_win, "Save file", name, "JSON (*.json)"
        )

        if file[0] != "":  # if the file name is not empty
            with open(file[0], "w") as export:  # open the file for writing
                json.dump(settings, export, indent=4)  # write the settings to the file

    def import_conf(self):
        # open an open file dialoag
        file = QFileDialog.getOpenFileName(
            self.main_win, "Open file", "configs/", "JSON (*.json)"
        )

        if file[0] != "":                           # if the file name is not empty
            with open(file[0], "r") as import_:         # open the file for reading
                settings = json.load(import_)           # load the settings from the file

            # set the values of the main window to the values of the settings (can they have the config file open at the same time? i dunno. EDIT: no they can't)
            self.ui.label_left_name.setText(settings["left_name"])
            self.ui.label_right_name.setText(settings["right_name"])
            self.ui.button_left_score_top.setText(settings["button_top"])
            self.ui.button_left_score_middle.setText(settings["button_middle"])
            self.ui.button_left_score_bottom.setText(settings["button_bottom"])
            self.ui.button_right_score_top.setText(settings["button_top"])
            self.ui.button_right_score_middle.setText(settings["button_middle"])
            self.ui.button_right_score_bottom.setText(settings["button_bottom"])
            self.ui.lcd_timer_minutes.display(settings["timer_minutes"])
            self.ui.lcd_timer_seconds.display(self.leading_zero(settings["timer_seconds"]))

            global timer_seconds, timer_minutes
            timer_minutes = settings["timer_minutes"]
            timer_seconds = settings["timer_seconds"]

class Options(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.signals()

    def signals(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()

    # define the list of scoring actions
    scoring = []

    global timer_seconds, timer_minutes
    timer_seconds = 0
    timer_minutes = 0

    sys.exit(app.exec())
