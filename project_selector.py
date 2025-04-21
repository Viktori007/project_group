from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QComboBox, QPushButton, QTableWidgetItem, QTableWidget

from db import Database
from contructor import ConstructorUi


class ProjectSelector(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QMainWindow):
        super(ProjectSelector, self).__init__()
        self.parent_window = parent

        self.comboBox_project: QComboBox = None
        self.auth_btn: QPushButton = None
        self.back_button: QPushButton = None

        uic.loadUi('UI/selection_project.ui', self)

        self.pr_list = []
        self.label_icon.setPixmap(QtGui.QPixmap("ui/images/logo-02.jpg"))
        self.label_icon.setScaledContents(True)
        self.setWindowIcon(QIcon("ui/images/logo-02.jpg"))

        self.tableWidget_project.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_project.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.tableWidget_project.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.load_orders()
        self.comboBox_project.currentIndexChanged.connect(self.load_projects)

        self.auth_btn.clicked.connect(self.go_to_constructor)
        self.back_button.clicked.connect(self.go_back)
        self.comboBox_project.currentIndexChanged.connect(self.load_projects)
        self.new_pr_btn.clicked.connect(self.create_new_pr)

        self.load_projects()

    def go_back(self):
        self.parent_window.show()
        self.close()

    def load_orders(self):
        """Загружает заказы в QComboBox."""
        self.comboBox_project.clear()
        self.comboBox_project.addItem("Все")

        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Id, ClientId, Date FROM Orders")
        orders = cursor.fetchall()

        for order in orders:
            order_id, client_id, date = order
            self.comboBox_project.addItem(f"Заказ {order_id} (Клиент {client_id}, {date})", order_id)

        conn.close()

    def load_projects(self):
        """Загружает проекты в QTableWidget в зависимости от выбранного заказа."""
        selected_order = self.comboBox_project.currentData()
        self.tableWidget_project.setRowCount(0)

        conn = Database.connect()
        cursor = conn.cursor()

        if selected_order is None:
            cursor.execute("""
                SELECT p.Id, p.Name, o.Id AS OrderId, p.Grid
                FROM Products p
                LEFT JOIN OrderItems oi ON p.Id = oi.ProductId
                LEFT JOIN Orders o ON oi.OrderId = o.Id
            """)
        else:
            cursor.execute("""
                SELECT p.Id, p.Name, o.Id AS OrderId, p.Grid
                FROM Products p
                JOIN OrderItems oi ON p.Id = oi.ProductId
                JOIN Orders o ON oi.OrderId = o.Id
                WHERE o.Id = %s
            """, (selected_order,))

        projects = cursor.fetchall()

        for row, project in enumerate(projects):
            project_id, project_name, order_id, grid = project
            self.tableWidget_project.insertRow(row)

            item_order = QTableWidgetItem(str(order_id or "Нет заказа"))
            item_order.setData(QtCore.Qt.ItemDataRole.UserRole, project_id)
            self.tableWidget_project.setItem(row, 0, item_order)

            self.tableWidget_project.setItem(row, 1, QTableWidgetItem(project_name))

            is_ready = "Нет" if grid is None else "Да"
            self.tableWidget_project.setItem(row, 2, QTableWidgetItem(is_ready))

            for col in range(self.tableWidget_project.columnCount()):
                item = self.tableWidget_project.item(row, col)
                if item is not None:
                    if row % 2 == 0:
                        item.setBackground(QColor(173, 216, 230))
                    else:
                        item.setBackground(QColor(255, 255, 224))

        conn.close()

    def go_to_constructor(self):
        selected_row = self.tableWidget_project.currentRow()
        if selected_row >= 0:
            project_id = self.tableWidget_project.item(selected_row, 0).data(QtCore.Qt.ItemDataRole.UserRole)
            if project_id:
                from contructor import ConstructorUi
                self.constructor_window = ConstructorUi(self, int(project_id))
                self.constructor_window.show()
                self.hide()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось получить ID проекта.")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите проект из таблицы.")

    def create_new_pr(self):
        from contructor import ConstructorUi
        self.constructor_window = ConstructorUi(self)
        self.constructor_window.show()
        self.hide()

    def show(self):
        self.load_projects()
        super().show()
