#region imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext
#------
from solver_ui import Ui_MainWindow
from solver import solve, to_readable, action_str
#endregion imports

class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """The main window. Instantiated once."""

    def __init__(self):
        """Initialize window; includes connecting signals/slots."""
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Counting is hard")

        self.solution = []
        self.problem_parameters = []

        self.solution_table.setColumnWidth(2, 200)

        self.container_2_bar.setFixedHeight(150) #make a ratio calculation thing somewhere, where "all the way up" is 25 capacity

        self.solve_button.clicked.connect(self.get_solution)
        self.step_back_button.clicked.connect(lambda: self.change_step_from_buttons("back"))
        self.step_forward_button.clicked.connect(lambda: self.change_step_from_buttons("forward"))
        self.step_spinbox.valueChanged.connect(self.change_step_from_spinbox)
        self.solution_table.currentItemChanged.connect(self.change_step_from_table)
    def get_solution(self):
        """Get solution to the entered puzzle and act accordingly.
        
        If the puzzle is determined to be inherently unsolvable, throw an "Invalid parameters"
        error box. If it could not be solved within 1,000 steps in all directions, throw a "No
        solution found" error. If solvable, get and set the solution to `self.solution` and
        make calls to update UI elements.
        """
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
            QtWidgets.QMessageBox.critical(self, "No solution found within max depth",
                                           "<p>A solution could not be found.</p>"
                                           "<p>This means that the program has hit the max "
                                           "recursion depth - typically, this means that no "
                                           "solutions were found after 1,000 steps.</p>"
                                           "</p>This does not mean that no solution exists - "
                                           "rather, that it could not be found in a reasonable "
                                           "number of steps.<p>",
                                           QtWidgets.QMessageBox.Ok)
        elif solution == 2:
            QtWidgets.QMessageBox.critical(self, "No solution found",
                                           "<p>A solution could not be found.</p>"
                                           "<p>This means that all action branches returned dead. "
                                           "No solution exists.</p>",
                                           QtWidgets.QMessageBox.Ok)
        else:
            self.solution = solution
            self.problem_parameters = [size_1, size_2, initial_1, initial_2, target]
            self.update_solution_text(to_readable(size_1, size_2, solution, initial_1, initial_2))
            self.update_solution_table()
            self.initialize_solution_area()
    def update_solution_table(self):
        """Completely rebuild the solution table with the current solution."""
        self.solution_table.setRowCount(0)
        for step in self.solution:
            #action, current 1, current 2, index
            self.solution_table.insertRow(step[3])
            self.solution_table.setItem(step[3], 0, QtWidgets.QTableWidgetItem(str(step[1])))
            self.solution_table.setItem(step[3], 1, QtWidgets.QTableWidgetItem(str(step[2])))
            self.solution_table.setItem(step[3], 2, QtWidgets.QTableWidgetItem(action_str(step[0])))
    def update_solution_text(self, text):
        """Update the solution text area with `text`, a `str`."""
        self.solution_text.setPlainText(text)
    def change_bar_height(self, container, height):
        """Update `container` (`int`) to be `height` px high."""
        pass
    def initialize_solution_area(self):
        """Initialize the solution area."""
        self.solution_area.setEnabled(True)
        self.max_steps_label.setText(f"of {len(self.solution)}")
        self.step_spinbox.setMinimum(1)
        self.step_spinbox.setMaximum(len(self.solution))
        self.container_1_bar.setMaximum(self.problem_parameters[0])
        self.container_2_bar.setMaximum(self.problem_parameters[1])
        #resize the bars
        #set highlighted table row
        self.update_solution_area(0)
    def change_step_from_buttons(self, direction):
        """Increment or decrement what step is currently displayed in the solution area.

        This is intended for use with the "back"/"forward" step buttons.
        """
        current_index = self.step_spinbox.value()-1
        if direction == "back":
            new_index = current_index-1
        elif direction == "forward":
            new_index = current_index+1
        self.update_solution_area(new_index)
    def change_step_from_spinbox(self, step):
        """Handles step updates from spinbox changes."""
        self.update_solution_area(step-1, False)
    def change_step_from_table(self, table_item):
        """Handles step updates from table clicks."""
        self.update_solution_area(table_item.row(), highlight_table=False)
    def update_solution_area(self, index, change_spinbox=True, highlight_table=True):
        """Update the solution area with the values for step `index` (zero-indexed).

        Note that `index` is implicitly validated via the spinbox, which will have a
        minimum value of 1 and a maximum value of the number of steps involved in the
        solution. QSpinBox ignores value setting beyond these parameters.
        If `change_spinbox` is True, then update `step_spinbox` to reflect the new index.
        Else, leave it alone. Similarly, if `highlight_table` is True, select the row
        associated with this index.
        """
        #prevent these from calling twice
        if change_spinbox:
            self.step_spinbox.valueChanged.disconnect(self.change_step_from_spinbox)
            self.step_spinbox.setValue(index+1)
            self.step_spinbox.valueChanged.connect(self.change_step_from_spinbox)
        if highlight_table:
            self.solution_table.currentItemChanged.disconnect(self.change_step_from_table)
            self.solution_table.selectRow(index)
            self.solution_table.currentItemChanged.connect(self.change_step_from_table)
        index = self.step_spinbox.value()-1
        current_step = self.solution[index]
        self.container_1_bar.setValue(current_step[1])
        self.container_2_bar.setValue(current_step[2])
        self.container_1_label.setText(f"{current_step[1]}/{self.problem_parameters[0]}")
        self.container_2_label.setText(f"{current_step[2]}/{self.problem_parameters[1]}")
        self.step_description_label.setText(action_str(current_step[0]))
    def play_through_solution(self):
        """Start a QTimer that will automatically step through the solution at regular intervals."""
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
