#region imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext
#------
from solver_ui import Ui_MainWindow
from solver import solve, to_readable, action
#endregion imports

class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """The main window. Instantiated once."""

    def __init__(self):
        """Initialize window; includes connecting signals/slots."""
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Counting is hard")

        self.solution = []

        self.solution_table.setColumnWidth(2, 200)
        self.solution_table.insertRow(0)
        self.solution_table.setItem(0, 2, QtWidgets.QTableWidgetItem("Fill container 1 from 2."))

        self.container_2_bar.setFixedHeight(150) #make a ratio calculation thing somewhere, where "all the way up" is 25 capacity

        self.solve_button.clicked.connect(self.get_solution)
        self.step_back_button.clicked.connect(lambda: self.change_step_from_buttons("back"))
        self.step_forward_button.clicked.connect(lambda: self.change_step_from_buttons("forward"))

    def get_solution(self):
        size_1 = self.capacity_1_spinbox.value()
        initial_1 = self.starting_1_spinbox.value()
        size_2 = self.capacity_2_spinbox.value()
        initial_2 = self.starting_2_spinbox.value()
        target = self.target_spinbox.value()
        solution = solve(size_1, size_2, target, initial_1, initial_2)
        if solution == 0:
            QtWidgets.QMessageBox.critical(self, "Invalid parameters",
                                           "<p>Please check that none of the following are true:</p>"
                                           "<p><ul><li>Your target is greater than the capacity "
                                           "of both containers.</li><li>The starting volume"
                                           "of one container is greater than its capacity.</li></ul>",
                                           QtWidgets.QMessageBox.Ok)
        elif solution == 1:
            QtWidgets.QMessageBox.critical(self, "Could not find solution",
                                           "<p>A solution could not be found.</p>"
                                           "<p>This means that the program has hit the max "
                                           "recursion depth - typically, this means that no "
                                           "solutions were found after 1,000 steps.</p>",
                                           QtWidgets.QMessageBox.Ok)
        else:
            self.solution = solution
            self.update_solution_text(to_readable(size_1, size_2, solution, initial_1, initial_2))
            self.update_solution_table()
            
            self.initialize_solution_area()
    def update_solution_table(self):
        self.solution_table.setRowCount(0)
        for step in self.solution:
            #action, current 1, current 2, index
            self.solution_table.insertRow(step[3])
            self.solution_table.setItem(step[3], 0, QtWidgets.QTableWidgetItem(str(step[1])))
            self.solution_table.setItem(step[3], 1, QtWidgets.QTableWidgetItem(str(step[2])))
            self.solution_table.setItem(step[3], 2, QtWidgets.QTableWidgetItem(action(step[0])))
    def update_solution_text(self, text):
        self.solution_text.setPlainText(text)
    def change_bar_height(self, bar):
        pass
    def initialize_solution_area(self):
        self.solution_area.setEnabled(True)
        self.max_steps_label.setText(f"of {len(self.solution)}")
        self.step_spinbox.setMinimum(1)
        self.step_spinbox.setMaximum(len(self.solution))
        #resize the bars
        #set highlighted table row
        self.update_solution_area(0)
    def change_step_from_buttons(self, direction):
        if direction == "back":
            current_index = self.step_spinbox.value()-1
            new_index = current_index-1
        elif direction == "forward":
            current_index = self.step_spinbox.value()-1
            new_index = current_index+1
        self.update_solution_area(new_index)
    def update_solution_area(self, index):
        self.step_spinbox.setValue(index+1)
    def play_through_solution(self):
        pass

 
class AppContext(ApplicationContext):
    """fbs requires that one instance of ApplicationContext be instantiated.

    This represents the app window.
    """

    def run(self):
        """Instantiate and show the window."""
        application_window = ApplicationWindow()
        application_window.show()
        return self.app.exec_()

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
