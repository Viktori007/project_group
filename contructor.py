import os

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor, QImage, QIcon
from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QTableWidgetItem, QTableWidget, QMessageBox, QVBoxLayout, \
    QGroupBox, QRadioButton, QFileDialog

from ObservableList import ObservableList
from db import Database
from schema import SquareCanvas, DraggableSquare


class ConstructorUi(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QMainWindow, project_id=None):
        super(ConstructorUi, self).__init__()

        self.product = (None, "", "")
        self.project_id = project_id
        self.comboBox_furniture = None
        self.furniture_add_pushButton = None

        self.curr_square: QtWidgets.QWidget = None
        self.widget_4 = None
        self.furnitura_tableWidget: QTableWidget = None

        self.widget_constructor: QtWidgets.QWidget = None
        self.border_comboBox: QtWidgets.QComboBox = None
        self.cloth_comboBox: QtWidgets.QComboBox = None
        self.parent_window = parent

        self.furniture_edit_pushButton: QPushButton = None
        self.widget_product: QWidget = None
        self.height_lineEdit: QLineEdit = None
        self.width_lineEdit: QLineEdit = None
        self.name_edit: QLineEdit = None

        uic.loadUi('UI/constructor.ui', self)

        self.widget: QWidget = uic.loadUi('UI/dialog_furniture.ui')

        self.widget_create: QWidget = uic.loadUi('UI/dialog_furniture_create.ui')
        self.label_icon.setPixmap(QtGui.QPixmap("ui/images/logo-02.jpg"))
        self.label_icon.setScaledContents(True)
        self.setWindowIcon(QIcon("ui/images/logo-02.jpg"))
        self.fill_data()
        self.furnitures = ObservableList()

        self.furnitura_tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(350, 40, 10, 40)
        layout.addWidget(self.widget_constructor)
        self.constructor_width = 880
        self.constructor_height = 640

        self.setLayout(layout)

        self.furnitures.item_added.connect(self.update_furniture_table)
        self.furnitures.item_removed.connect(self.update_furniture_table)
        self.furnitures.item_updated.connect(self.update_furniture_table)

        self.widget_create.pushButton_add_new_furniture.clicked.connect(
            lambda: self.add_new_object(material_type="фурнитура"))
        self.furniture_add_pushButton.clicked.connect(self.create_furniture)
        self.save_constructor_pushButton.clicked.connect(self.save_to_db)
        self.cloth_add_pushButton.clicked.connect(lambda: self.add_new_object(material_type="ткань"))
        self.widget_create.pushButton_select_furniture.clicked.connect(self.create_child_square_with_image)
        self.widget_create.pushButton_cancel.clicked.connect(lambda: self.widget_create.close())
        self.pushButton_rotate_left.setIcon(QIcon("UI/images/left.png"))
        self.pushButton_rotate_right.setIcon(QIcon("UI/images/right.png"))

        self.save_action.triggered.connect(self.save_to_db)

        self.pushButton_rotate_left.clicked.connect(self.rotate_left)
        self.pushButton_rotate_right.clicked.connect(self.rotate_right)

        self.canvas = SquareCanvas(width=self.constructor_width, height=self.constructor_height, padding=10,
                                   double_click=self.update_widget_product_size,
                                   constructor_ui=self)
        self.widget_constructor.close()
        self.canvas.setParent(self)
        self.canvas.setGeometry(350, 60, self.constructor_width, self.constructor_height)

        self.update_furniture_table()

        if self.project_id is not None:
            self.load_from_db(self.project_id)

        self.back_pushButton.clicked.connect(self.go_back)

    def go_back(self):
        """Возвращает пользователя на окно выбора проекта."""
        self.parent_window.show()
        self.close()

    def fill_data(self):
        self.cloth_comboBox.clear()
        self.widget_create.comboBox_furniture.clear()
        conn = Database.connect()
        cursor = conn.cursor()
        if self.project_id is not None:
            cursor.execute(f"""
            select * from Materials
            join MaterialTypes on Materials.MaterialTypeId = MaterialTypes.Id
            WHERE Materials.Id IN (SELECT mp.MaterialsId FROM MaterialProduct mp WHERE mp.ProductId = {self.project_id})
            """)
        else:
            cursor.execute("""
            select * from Materials 
            join MaterialTypes on Materials.MaterialTypeId = MaterialTypes.Id
            """)
        d = cursor.fetchall()
        self.cloth_comboBox.addItem(" ")
        self.widget_create.comboBox_furniture.addItem(" ")
        for i in d:
            if i[-1] != "фурнитура":
                self.cloth_comboBox.addItem(f"{i[1]}", i[0])

            if i[-1] == "фурнитура":
                self.widget_create.comboBox_furniture.addItem(f"{i[1]}")

        self.cloth_comboBox.currentIndexChanged.connect(self.update_main_product_image)

        conn.close()

    def rotate_left(self):
        """Поворачивает текущий квадрат на 90 градусов влево."""
        if self.curr_square:
            self.curr_square.rotate_image(-90)

    def rotate_right(self):
        """Поворачивает текущий квадрат на 90 градусов вправо."""
        if self.curr_square:
            self.curr_square.rotate_image(90)

    def update_widget_product_size(self, square: QWidget):
        try:
            if self.curr_square is not square:
                self.curr_square = square
                self.width_lineEdit.textChanged.connect(self.update_width_size)
                self.height_lineEdit.textChanged.connect(self.update_height_size)
                square.resize_delegate.add(lambda: self.width_lineEdit.setText(str(square.width())))
                square.resize_delegate.add(lambda: self.height_lineEdit.setText(str(square.height())))

            width = str(int(square.width()))
            height = str(int(square.height()))

            self.width_lineEdit.setText(width)
            self.height_lineEdit.setText(height)
            self.curr_square = square

        except ValueError:
            pass

    def update_main_product_image(self):
        selected_material_id = self.cloth_comboBox.currentData()

        if not selected_material_id:
            return

        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ImageId FROM Materials WHERE Id = %s", (selected_material_id,))
        result = cursor.fetchone()

        if not result:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти изображение для выбранной ткани!")
            return

        image_id = result[0]

        cursor.execute("SELECT Data FROM Images WHERE Id = %s", (image_id,))
        data = cursor.fetchone()
        if data is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти изображение для выбранной ткани!")
            return

        image = QImage()
        image.loadFromData(data[0])

        if self.canvas.main_square:
            self.canvas.main_square.set_image(image)

        conn.close()

    def create_furniture(self):
        self.widget_create.show()

        try:
            self.widget_create.pushButton_select_furniture.clicked.disconnect()
        except TypeError:
            pass

        self.widget_create.pushButton_select_furniture.clicked.connect(self.create_child_square_with_image)

    def create_child_square_with_image(self):
        selected_furniture = self.widget_create.comboBox_furniture.currentText()

        if not selected_furniture:
            self.widget.close()
            QMessageBox.warning(self, "Ошибка", "Фурнитура не выбрана!")
            return

        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ImageId, ROUND(Width,0), ROUND(Height,0) FROM Materials WHERE Name = %s LIMIT 1", (selected_furniture,))
        result = cursor.fetchone()
        width = int(result[1]) *10
        height = int(result[2]) *10

        if not result:
            self.widget.close()
            QMessageBox.warning(self, "Ошибка", "Не удалось найти изображение для выбранной фурнитуры!")
            return

        image_id = result[2]
        cursor.execute("SELECT Data FROM Images WHERE Id = %s", (image_id,))
        data = cursor.fetchone()
        if data is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти изображение для выбранной ткани!")
            return


        conn.close()
        image = QImage()
        image.loadFromData(data[0])

        if self.canvas.main_square:
            padding = 10
            square_size = width*height
            new_x, new_y = padding, padding

            while True:
                new_rect = QRect(new_x, new_y, width, height)
                collision = any(new_rect.intersects(sq.geometry()) for sq in self.canvas.main_square.squares)

                if not collision:
                    break

                new_x += square_size + padding
                if new_x + square_size > self.canvas.main_square.width():
                    new_x = padding
                    new_y += square_size + padding
                    if new_y + square_size > self.canvas.main_square.height():
                        QMessageBox.warning(self, "Ошибка", "Недостаточно места для нового квадрата!")
                        return

            new_square = DraggableSquare(
                parent=self.canvas.main_square,
                x=new_x, y=new_y,
                width=width, height=height,
                min_width=width, min_height=height,
                double_click=self.canvas.double_click,
                constructor_ui=self,
                image_path=image,
                name=selected_furniture
            )

            new_square.setStyleSheet("background-color: transparent;")

            self.canvas.main_square.squares.append(new_square)
            new_square.show()

            self.widget_create.close()

        else:
            QMessageBox.warning(self, "Ошибка", "Основной квадрат не найден!")
        self.widget_create.close()

    def add_image_to_square(self):
        selected_furniture = self.widget_create.comboBox_furniture.currentText()

        if not selected_furniture:
            QMessageBox.warning(self, "Ошибка", "Фурнитура не выбрана!")
            return

        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ImageId FROM Materials WHERE Name = %s", (selected_furniture,))
        result = cursor.fetchone()

        if not result:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти изображение для выбранной фурнитуры!")
            self.widget_create.close()
            return

        image_id = result[0]

        cursor.execute("SELECT Data FROM Images WHERE Id = %s", (image_id,))
        image_data = cursor.fetchone()[0]

        image = QImage()
        image.loadFromData(image_data)

        if self.curr_square:
            self.curr_square.set_image(image)
            QMessageBox.information(self, "Успех", "Изображение успешно добавлено на поле!")
        else:
            QMessageBox.warning(self, "Ошибка", "Не выбран квадрат для добавления изображения!")
        conn.close()

    def update_width_size(self):
        if self.curr_square is None:
            self.width_lineEdit.textChanged -= self.update_width_size()
        try:
            self.curr_square.try_resize(int(self.width_lineEdit.text()), int(self.height_lineEdit.text()))
        except Exception as e:
            pass

    def update_height_size(self):
        if self.curr_square is None:
            self.height_lineEdit.textChanged -= self.update_height_size()
        try:
            self.curr_square.try_resize(int(self.width_lineEdit.text()), int(self.height_lineEdit.text()))
        except Exception as e:
            pass

    def update_furniture_table(self):
        """Обновляет таблицу furnitura_tableWidget на основе дочерних квадратиков main_square."""
        if self.canvas.main_square is None:
            self.furnitura_tableWidget.setRowCount(0)
            return

        children = self.canvas.main_square.squares

        self.furnitura_tableWidget.setRowCount(len(children))
        self.furnitura_tableWidget.setColumnCount(3)
        self.furnitura_tableWidget.setHorizontalHeaderLabels(["Название", "Ширина", "Высота", "Цвет"])

        for row, square in enumerate(children):
            self.furnitura_tableWidget.setItem(row, 0, QTableWidgetItem(square.name))
            self.furnitura_tableWidget.setItem(row, 1, QTableWidgetItem(str(square.width())))
            self.furnitura_tableWidget.setItem(row, 2, QTableWidgetItem(str(square.height())))

            for col in range(self.furnitura_tableWidget.columnCount()):
                item = self.furnitura_tableWidget.item(row, col)
                if item is not None:
                    if row % 2 == 0:
                        item.setBackground(QColor(173, 216, 230))
                    else:
                        item.setBackground(QColor(255, 255, 224))

        self.furnitura_tableWidget.resizeColumnsToContents()

    def save_to_db(self):
        try:
            if self.name_edit.text() == "":
                QMessageBox.warning(self, "Ошибка", "Ну назови хоть как то")
                return
            if self.name_edit.text() == "":
                QMessageBox.warning(self, "Ошибка", "Разметь хоть что-то")
                return
            json_data = self.canvas.serialize()

            width = self.canvas.main_square.width()
            height = self.canvas.main_square.height()

            res = Database.save_project((self.product[0], self.name_edit.text(), json_data, width, height))
            if res is None:
                QMessageBox.warning(self, "Ошибка", "Идите ***** со своим сохранением")
            else:
                product_id = res
                print(f"Созданный продукт ID: {product_id}")

                material_ids = self.get_used_material_ids()
                print(f"Использованные материалы: {material_ids}")

                if material_ids:
                    Database.save_material_product_links(product_id, material_ids)

                QMessageBox.information(self, "Найс", "Сохранено")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "Не хочу я сохранять твое ******")

    def get_used_material_ids(self):
        """Возвращает список ID материалов, используемых в продукте."""
        material_ids = []

        selected_material_id = self.cloth_comboBox.currentData()
        if selected_material_id:
            material_ids.append(selected_material_id)
            print(f"Добавлен материал (ткань) ID: {selected_material_id}")

        if self.canvas.main_square:
            for square in self.canvas.main_square.squares:
                if square.name:
                    conn = Database.connect()
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id FROM Materials WHERE Name = %s", (square.name,))
                    result = cursor.fetchone()
                    conn.close()
                    if result:
                        material_id = result[0]
                        material_ids.append(material_id)
                        print(f"Добавлен материал (фурнитура) ID: {material_id}")

        return material_ids

    def add_new_object(self, material_type="фурнитура"):
        """
        Добавляет новый материал (ткань или фурнитуру) в базу данных.

        :param material_type: Тип материала ("ткань" или "фурнитура")
        """
        file_path, _ = QFileDialog.getOpenFileName(self, f"Выберите изображение {material_type}", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp)")

        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    image_data = file.read()

                file_name = os.path.splitext(os.path.basename(file_path))[0]
                conn = Database.connect()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Images (Data) VALUES (%s)", (image_data,))
                conn.commit()
                image_id = cursor.lastrowid

                query = f"""SELECT Id FROM MaterialTypes WHERE Name = '{material_type}'"""
                cursor.execute(query)
                material_type_id = cursor.fetchone()
                if material_type_id is None:
                    query = f"""INSERT INTO MaterialTypes(Name) VALUES ('{material_type}')"""
                    cursor.execute(query)
                    conn.commit()
                    cursor.execute(f"""SELECT Id FROM MaterialTypes WHERE Name = '{material_type}'""")
                    material_type_id = cursor.fetchone()[0]
                else:
                    material_type_id = material_type_id[0]

                # if material_type == "ткань":
                #     material_type_id = 1
                # elif material_type == "фурнитура":
                #     material_type_id = 2
                # else:
                #     QMessageBox.warning(self, "Ошибка", "Неизвестный тип материала!")
                #     return
                query = f"""SELECT Id from CalculationUnits where Name='{"см"}'"""
                cursor.execute(query)
                unit_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO Materials (Name, UnitId, MaterialTypeId, ImageId, Width, Height, Color)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (file_name, unit_id, material_type_id, image_id, 100, 100, "#ffffff"))

                conn.commit()
                conn.close()

                if material_type == "ткань":
                    self.fill_data()
                elif material_type == "фурнитура":
                    self.update_furniture_table()

                if material_type == "ткань":
                    image = QImage()
                    image.loadFromData(image_data)

                    if self.canvas.main_square:
                        self.canvas.main_square.set_image(image)

                QMessageBox.information(self, "Успех", f"{material_type.capitalize()} успешно добавлена!")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось добавить {material_type}: {str(e)}")

    def load_from_db(self, pr_id):
        try:
            self.product = Database.open_project(pr_id)
            if self.product:
                if self.product[-1]:
                    if self.canvas.deserialize(self.product[-1]) != False:
                        self.name_edit.setText(self.product[1])
                else:
                    self.canvas.main_square = None
                    self.canvas.squares = []
                    self.name_edit.setText(self.product[1])
            else:
                QMessageBox.warning(self, "Ошибка", "Проект не найден.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке проекта: {e}")
