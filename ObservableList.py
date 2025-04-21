from PyQt6.QtCore import QObject, pyqtSignal


class ObservableList(QObject):
    item_added = pyqtSignal(object)
    item_removed = pyqtSignal(object)
    item_updated = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self._items = []

    def append(self, item):
        """Добавляет элемент и отправляет сигнал."""
        self._items.append(item)
        self.item_added.emit(item)

    def remove(self, item):
        """Удаляет элемент и отправляет сигнал."""
        self._items.remove(item)
        self.item_removed.emit(item)

    def __getitem__(self, index):
        """Возвращает элемент по индексу."""
        return self._items[index]

    def __len__(self):
        """Возвращает количество элементов."""
        return len(self._items)

    def __iter__(self):
        """Итератор по элементам."""
        return iter(self._items)

    def update_item(self, item):
        """Уведомляет об изменении элемента."""
        self.item_updated.emit(item)
