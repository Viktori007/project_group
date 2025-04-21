import base64
import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QMenu, QLabel
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QMouseEvent, QAction, QPixmap, QImage, QTransform
from PyQt6.uic.properties import QtGui
from PyQt6.uic.uiparser import QtCore
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice


class DraggableSquare(QWidget):
    def __init__(self, parent=None, x=50, y=50, width=100, height=100,
                 min_width=50, min_height=50, double_click=None, constructor_ui=None, image_path=None, name=None):
        super().__init__(parent)
        self.constructor_ui = constructor_ui
        self.setGeometry(x, y, width, height)
        self.min_width = min_width
        self.min_height = min_height
        self.setMinimumSize(self.min_width, self.min_height)
        self.dragging = False
        self.offset = None
        self.resize_handle_size = 10
        self.resize_mode = False
        self.double_click = double_click
        self.squares = []
        self.image_path = image_path
        self.name = name

        self.original_width = width
        self.original_height = height
        self.setStyleSheet("background-color: transparent;")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rotation_angle = 0
        self.original_pixmap = None
        self.set_image(image_path)

        self.layout.addWidget(self.image_label)

        self.size_label = QLabel(self)
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.size_label.setText(f"{self.width()}x{self.height()}")
        self.size_label.setStyleSheet("background: transparent; color: black;")
        self.size_label.setFixedHeight(20)
        self.layout.addWidget(self.size_label)

        self.setLayout(self.layout)

        self.resizeEvent = self.on_resize
        self.resize_delegate = {
            lambda: self.size_label.setText(f"{self.width()}x{self.height()}")
        }

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        if double_click is not None:
            self.mouseDoubleClickEvent = lambda x: double_click(self)

    def set_image(self, image_path):
        """Устанавливает изображение в QLabel или placeholder, если изображение отсутствует."""
        if image_path:
            if isinstance(image_path, QImage):
                self.original_pixmap = QPixmap.fromImage(image_path)
            else:
                self.original_pixmap = QPixmap(image_path)

            if not self.original_pixmap.isNull():
                self.apply_rotation()
                self.image_label.setScaledContents(True)
                self.image_label.show()
            else:
                self.image_label.hide()
                self.show_placeholder()
        else:
            self.image_label.hide()
            self.show_placeholder()

    def apply_rotation(self):
        """Применяет текущий угол поворота к изображению."""
        if self.original_pixmap:
            transform = QTransform()
            transform.rotate(self.rotation_angle)
            rotated_pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(rotated_pixmap)

    def rotate_image(self, angle):
        """Поворачивает изображение на заданный угол и обновляет размеры виджета."""
        self.rotation_angle += angle
        self.rotation_angle %= 360
        self.apply_rotation()
        self.rotate_widget()

    def rotate_widget(self):
        """Поворачивает виджет на 90 градусов, меняя ширину и высоту местами."""
        if self.rotation_angle % 180 == 90:
            new_width = self.height()
            new_height = self.width()

            self.setGeometry(self.x(), self.y(), new_width, new_height)
            self.setGeometry(self.x(), self.y(), new_width, new_height)

            self.size_label.setText(f"{self.width()}x{self.height()}")

    def show_placeholder(self):
        """Отображает placeholder, если изображение отсутствует."""
        placeholder_text = "Нет изображения"
        self.image_label.setText(placeholder_text)
        self.image_label.show()

    def on_resize(self, event):
        for f in self.resize_delegate:
            f()
        if self.constructor_ui:
            self.constructor_ui.update_furniture_table()
        if self.image_path:
            self.set_image(self.image_path)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.apply_rotation()
        self.rotate_widget()
        if self.constructor_ui:
            self.constructor_ui.update_furniture_table()

    def paintEvent(self, event):
        """Отрисовывает окантовку вокруг изображения."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        border_width = 1
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.rect().adjusted(border_width, border_width, -border_width, -border_width))

        painter.setBrush(QColor(255, 0, 0))
        painter.setPen(Qt.GlobalColor.black)
        handle_rect = QRect(
            self.width() - self.resize_handle_size,
            self.height() - self.resize_handle_size,
            self.resize_handle_size,
            self.resize_handle_size
        )
        painter.drawRect(handle_rect)

    def try_resize(self, width: int, height: int):
        self.resize(max(self.min_width, width), max(self.min_height, height))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_in_resize_handle(event.pos()):
                self.resize_mode = True
            else:
                self.dragging = True
                self.offset = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.parent().dragging = False
        self.parent().resize_mode = False

        if self.dragging:
            new_pos = self.mapToParent(event.pos() - self.offset)
            new_pos = self.constrain_position(new_pos)
            if not self.check_collision(new_pos):
                self.move(new_pos)
        elif self.resize_mode:
            new_width = max(self.min_width, event.pos().x())
            new_height = max(self.min_height, event.pos().y())
            new_width, new_height = self.constrain_size(new_width, new_height)
            if not self.check_collision(self.pos(), new_width, new_height):
                self.resize(new_width, new_height)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.resize_mode = False
        super().mouseReleaseEvent(event)

    def is_in_resize_handle(self, pos):
        return (self.width() - self.resize_handle_size <= pos.x() <= self.width() and
                self.height() - self.resize_handle_size <= pos.y() <= self.height())

    def check_collision(self, new_pos, new_width=None, new_height=None):
        if new_width is None:
            new_width = self.width()
        if new_height is None:
            new_height = self.height()

        new_rect = QRect(new_pos.x(), new_pos.y(), new_width, new_height)
        parent = self.parent()
        if hasattr(parent, 'squares'):
            for square in parent.squares:
                if square != self and new_rect.intersects(square.geometry()):
                    return True
        return False

    def constrain_position(self, pos):
        parent_rect = self.parent().rect() if self.parent() else QRect()
        x = max(parent_rect.left(), min(pos.x(), parent_rect.right() - self.width()))
        y = max(parent_rect.top(), min(pos.y(), parent_rect.bottom() - self.height()))
        return QPoint(x, y)

    def constrain_size(self, width, height):
        parent = self.parent()
        if parent:
            max_width = parent.width() - self.x()
            max_height = parent.height() - self.y()
            return min(width, max_width), min(height, max_height)
        return width, height

    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.delete_square)
        context_menu.addAction(delete_action)

        context_menu.exec(self.mapToGlobal(pos))

    def delete_square(self):
        for child in self.squares:
            child.delete_square()

        if self.parent() and hasattr(self.parent(), 'main_square'):
            self.parent().main_square = None

        if self.parent() and hasattr(self.parent(), 'squares'):
            self.parent().squares.remove(self)

        if self.constructor_ui:
            self.constructor_ui.update_furniture_table()

        self.hide()
        self.deleteLater()

    def to_dict(self):
        """Сериализует квадратик и его дочерние элементы в словарь."""
        data = {
            "x": self.x(),
            "y": self.y(),
            "width": self.width(),
            "height": self.height(),
            "min_width": self.min_width,
            "min_height": self.min_height,
            "rotation_angle": self.rotation_angle,
            "image": image_to_base64(self.original_pixmap.toImage()) if self.original_pixmap else None,
            "name": self.name,
            "children": [child.to_dict() for child in self.squares]
        }
        return data

    @classmethod
    def from_dict(cls, data, parent, constructor_ui=None):
        """Десериализует квадратик и его дочерние элементы из словаря."""
        square = cls(
            parent=parent,
            x=data["x"],
            y=data["y"],
            width=data["width"],
            height=data["height"],
            min_width=data.get("min_width", 50),
            min_height=data.get("min_height", 50),
            double_click=parent.double_click if hasattr(parent, 'double_click') else None,
            constructor_ui=constructor_ui,
            name=data.get("name")
        )

        if data.get("image"):
            image = base64_to_image(data["image"])
            square.set_image(image)

        square.rotation_angle = data.get("rotation_angle", 0)
        square.apply_rotation()

        for child_data in data.get("children", []):
            child = cls.from_dict(child_data, parent=square, constructor_ui=constructor_ui)
            square.squares.append(child)
            child.show()

        return square


def image_to_base64(image: QImage) -> str:
    """Преобразует QImage в base64-строку."""
    if image.isNull():
        return None

    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    return base64.b64encode(byte_array.data()).decode('utf-8')


def base64_to_image(base64_str: str) -> QImage:
    """Преобразует base64-строку в QImage."""
    byte_array = QByteArray(base64.b64decode(base64_str))
    image = QImage()
    image.loadFromData(byte_array)
    return image


class SquareCanvas(QWidget):

    def __init__(self, width=500, height=500, padding=10, square_width=100, square_height=100, square_min_width=50,
                 square_min_height=50, double_click=None, constructor_ui=None):
        super().__init__()
        self.constructor_ui = constructor_ui
        self.double_click = double_click
        self.setGeometry(20, 90, width, height)
        self.setMinimumSize(width, height)
        self.padding = padding
        self.main_square = None
        self.square_min_width = square_min_width
        self.square_min_height = square_min_height
        self.square_width = square_width
        self.square_height = square_height

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def add_square(self):
        square = DraggableSquare(self, self.padding, self.padding, self.square_width, self.square_height,
                                 self.square_min_width, self.square_min_height, self.double_click,
                                 constructor_ui=self.constructor_ui)
        self.main_square = square
        square.show()

    def show_context_menu(self, pos):
        if self.main_square is None:
            context_menu = QMenu(self)
            add_action = QAction("Добавить квадрат", self)
            add_action.triggered.connect(self.add_square)
            context_menu.addAction(add_action)
            context_menu.exec(self.mapToGlobal(pos))

    def serialize(self):
        """Сериализует main_square и его дочерние элементы в JSON."""
        if self.main_square is None:
            return json.dumps([])

        data = {
            "main_square": self.main_square.to_dict(),
            "width": self.width(),
            "height": self.height()
        }
        return json.dumps(data)

    def deserialize(self, json_str):
        """Десериализует main_square и его дочерние элементы из JSON."""
        try:
            data = json.loads(json_str)
            if not data:
                return False

            if self.main_square:
                self.main_square.deleteLater()
                self.main_square = None

            self.main_square = DraggableSquare.from_dict(
                data["main_square"], parent=self, constructor_ui=self.constructor_ui
            )
            self.main_square.show()

            self.resize(data.get("width", self.width()), data.get("height", self.height()))

            if self.constructor_ui:
                self.constructor_ui.update_furniture_table()

        except json.JSONDecodeError:
            QMessageBox.warning(self, "Ошибка", "Некорректный JSON-формат данных.")
            return False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)
