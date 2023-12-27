from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QLineEdit, QGridLayout, QPushButton, QCheckBox, QComboBox, QTableWidget, QMainWindow, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3
 

def connect_to_database(database_filename="./database.db"):
    connection = sqlite3.connect(database_filename)
    return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student managment system")
        grid = QGridLayout()

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add subitems to menus
        # *Add student on file menu item
        add_student_action = QAction(QIcon("./icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # *Add about on help menu item
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # *Add search on edit menu item
        search_action = QAction(QIcon("./icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        search_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)


        # Creating table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        self.resize(500, self.height())

        # *Creating toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # *Creating status bar and status bar elements
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)



        # *Detect a cell clik
        self.table.cellClicked.connect(self.cell_clicked)
 


    def cell_clicked(self):
        show_normal_window_button = QPushButton("Refresh table")
        show_normal_window_button.clicked.connect(self.load_data)
        edit_button = QPushButton("Edit record")
        edit_button.clicked.connect(self.edit)
        delete_button = QPushButton("Delete record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusBar.removeWidget(child)

        self.statusBar.addWidget(edit_button)
        self.statusBar.addWidget(delete_button)
        self.statusBar.addWidget(show_normal_window_button)



    def load_data(self):
        connection = connect_to_database()
        result = connection.execute("SELECt * FROM students")
        enumerated_result = enumerate(result)
        self.table.setRowCount(0)

        for row_number, row_data in enumerated_result:
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.table.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.table.setItem(row_number, 2, QTableWidgetItem(str(row_data[2])))
            self.table.setItem(row_number, 3, QTableWidgetItem(str(row_data[3])))

        connection.close()
    
    
    def load_specific_student(self, results):
        enumerated_result = enumerate(results)
        self.table.setRowCount(0)

        for row_number, row_data in enumerated_result:
            self.table.insertRow(row_number)
            self.table.setItem(row_number, 0, QTableWidgetItem(str(row_data[0])))
            self.table.setItem(row_number, 1, QTableWidgetItem(str(row_data[1])))
            self.table.setItem(row_number, 2, QTableWidgetItem(str(row_data[2])))
            self.table.setItem(row_number, 3, QTableWidgetItem(str(row_data[3])))

    
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


    def search(self):
        dialog = SearchDialog()
        dialog.exec()
    

    def edit(self):
        dialog = EditDialog()
        dialog.exec()
    

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    
    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student Information
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student's name")
        layout.addWidget(self.student_name)
        
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Student's mobile number")
        layout.addWidget(self.mobile)


        # Add submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)


    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Student's Name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student's name")
        layout.addWidget(self.student_name)
        
        # Add search button
        search_button = QPushButton("Search")   
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)


    def search_student(self):
        connection = connect_to_database()
        cursor = connection.cursor()
        name = self.student_name.text()
        cursor.execute("SELECT * FROM students WHERE name =?", (name,))
        results = cursor.fetchall()

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_specific_student(results)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout() # *QvBoxLayout used when we have a vertical layout, we know it won't change

        # Getting the selected student information from table

        index = main_window.table.currentRow()
        self.table_student_id = main_window.table.item(index, 0).text()   
        self.table_student_name = main_window.table.item(index, 1).text()
        table_course = main_window.table.item(index, 2).text()
        table_mobile = main_window.table.item(index, 3).text()
        # print(f"student: {table_student_name} course: {table_course}")

        # Student Information
        self.new_student_name = QLineEdit(self.table_student_name)
        self.new_student_name.setPlaceholderText("Student's name")
        layout.addWidget(self.new_student_name)

        self.new_course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.new_course_name.addItems(courses)

        # Set the default checked option
        for i in range(0,len(courses)):
            if courses[i] == table_course:
                self.new_course_name.setCurrentIndex(i)
                break
        
        layout.addWidget(self.new_course_name)

        # Add mobile widget
        self.new_mobile = QLineEdit(table_mobile)
        self.new_mobile.setPlaceholderText("Student's mobile number")
        layout.addWidget(self.new_mobile)


        # Add submit button
        update_button = QPushButton("Update Student")
        update_button.clicked.connect(self.update_student)
        layout.addWidget(update_button)

        self.setLayout(layout)
    

    def update_student(self):
        current_student_id = self.table_student_id
        new_name = self.new_student_name.text()
        new_course = self.new_course_name.itemText(self.new_course_name.currentIndex())
        new_mobile = self.new_mobile.text()

        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE students
            SET name =?,
                course =?,
                mobile =?
            WHERE id =?
        """, (new_name, new_course, new_mobile, current_student_id))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student")
        self.setFixedWidth(310)
        self.setFixedHeight(200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Label 
        label = QLabel("Are you sure you want to delete this student?")
        layout.addWidget(label)

        # Add submit button
        delete_button = QPushButton("Yes")
        delete_button.clicked.connect(self.delete_student)
        layout.addWidget(delete_button)

        cancel_button = QPushButton("No")
        cancel_button.clicked.connect(self.exit_dialog)
        layout.addWidget(cancel_button)

    
    def delete_student(self):
        connection = connect_to_database()
        cursor = connection.cursor()

        index = main_window.table.currentRow()
        self.table_student_id = main_window.table.item(index, 0).text()

        # Deleting the student record
        cursor.execute("DELETE FROM students WHERE id =?", (self.table_student_id,))

        # Refreshing main window and closing connections
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("Student deleted successfully!")
        confirmation_widget.exec()


    def exit_dialog(self):
        self.close()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        about_content = """
        This app was created during my python course. 
        Feel free to modify and reuse this app.
        Thanks for using it! 🫶🏻
        """
        self.setText(about_content)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.load_data()
main_window.show()
sys.exit(app.exec())
