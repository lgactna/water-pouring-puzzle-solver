#region imports
import sys
from PyQt5 import QtCore, QtWidgets
from fbs_runtime.application_context.PyQt5 import ApplicationContext
#------
from solver_ui import Ui_MainWindow
from solver import solve, to_readable, action_str
#endregion imports

def calculate_container_sizes(size_1, size_2, max_height):
    """Determine how tall each container (progress bar) should be.
    
    This is done by first allocating 25 px per capacity unit for each container.
    If either container exceeds the maximum allowed height dictated by its layout,
    then the largest container is set to the height of the layout. The smaller container
    is then sized proportionally to the larger container.
    Returns a list of [`height_1`, `height_2`].
    """
    #We reduce the inherent max height by 25, the height of the label and then some
    #Since the layout includes this label, it we need to account for it
    #Otherwise the layout will resize itself to be larger, thus uncapping the max height
    max_height -= 25
    if size_1*25 > max_height or size_2*25 > max_height:
        if size_1 > size_2:
            height_1 = max_height
            height_2 = (size_2*max_height)/size_1
        else:
            height_2 = max_height
            height_1 = (size_1*max_height)/size_2
    else:
        height_1 = size_1*25
        height_2 = size_2*25
    #print(height_1, height_2, max_height)
    return [height_1, height_2]


class ApplicationWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """The main window. Instantiated once."""

    def __init__(self):
        """Initialize window; includes connecting signals/slots."""
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Counting is hard")

        self.solution = []
        self.problem_parameters = []

        #here we'll define how the playback_timer should work
        #if a user is stepping through at intervals
        self.playback_timer = QtCore.QTimer()
        #this should always result in incrementing the index
        self.playback_timer.timeout.connect(lambda: self.update_solution_area(self.step_spinbox.value()))

        #make the last column bigger
        self.solution_table.setColumnWidth(2, 200)

        self.container_2_bar.setFixedHeight(150) #just for initialization/demonstration

        self.solve_button.clicked.connect(self.get_solution)
        self.step_back_button.clicked.connect(lambda: self.change_step_from_buttons("back"))
        self.step_forward_button.clicked.connect(lambda: self.change_step_from_buttons("forward"))
        self.play_solution_button.clicked.connect(self.toggle_solution_playback)
        self.step_spinbox.valueChanged.connect(self.change_step_from_spinbox)
        self.solution_table.currentItemChanged.connect(self.change_step_from_table)
        self.set_depth_button.clicked.connect(self.set_depth)
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
                                           "solutions were found after ~1,000 steps. (The max "
                                           "recursion depth is currently %s.)</p>"
                                           "<p>This does not mean that no solution exists - "
                                           "rather, that it could not be found in a reasonable "
                                           "number of steps.</p>"%sys.getrecursionlimit(),
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
    def initialize_solution_area(self):
        """Initialize the solution area."""
        self.solution_area.setEnabled(True)
        self.max_steps_label.setText(f"of {len(self.solution)}")
        self.step_spinbox.setMinimum(1)
        self.step_spinbox.setMaximum(len(self.solution))
        self.container_1_bar.setMaximum(self.problem_parameters[0])
        self.container_2_bar.setMaximum(self.problem_parameters[1])
        #resize the progress bars/"containers"
        self.resize_bars()
        #set current step to step 1
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
        """Handle step updates from spinbox changes."""
        self.update_solution_area(step-1, False)
    def change_step_from_table(self, table_item):
        """Handle step updates from table clicks."""
        if table_item:
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
        #if we've hit the end, then stop playback and change button text
        if self.playback_timer.isActive() and index+1 == len(self.solution):
            self.toggle_solution_playback()
    def toggle_solution_playback(self):
        """Toggle a QTimer that will automatically step through the solution at regular intervals.
        
        Also change the button text to reflect what will happen.
        """
        if self.playback_timer.isActive():
            self.playback_timer.stop()
            self.play_solution_button.setText("Play through solution")
            self.steprate_spinbox.setEnabled(True)
        else:
            #go to beginning if currently at end
            if self.step_spinbox.value() == len(self.solution):
                self.update_solution_area(0)
            interval = self.steprate_spinbox.value()
            self.playback_timer.start(interval)
            self.play_solution_button.setText("Stop playback")
            #disable the spinbox to prevent a user from thinking they can change it midway
            self.steprate_spinbox.setEnabled(False)
    def resize_bars(self):
        """Resize the progress bars/containers."""
        #here we determine the maximum height that a bar can be, which is the size
        #of this layout
        max_height = self.verticalLayout_3.geometry().height()
        #print(max_height)
        sizes = calculate_container_sizes(self.problem_parameters[0], self.problem_parameters[1], max_height)
        self.container_1_bar.setFixedHeight(sizes[0])
        self.container_2_bar.setFixedHeight(sizes[1])
    def set_depth(self):
        """Set a new recursion limit via user input."""
        new_depth, response = QtWidgets.QInputDialog.getInt(self, "Set max recursion depth",
                                                  "<p>You can set the maximum recursion depth "
                                                  "of the program here, default ~1000.</p>"
                                                  "<p>Large values will crash the program "
                                                  "if a solution is not found within that depth. "
                                                  "The max is platform-dependent.</p>",
                                                  sys.getrecursionlimit(), 0)
        if response:
            sys.setrecursionlimit(new_depth)


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
