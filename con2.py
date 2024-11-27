# food_order.py
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QRadioButton, QButtonGroup, QTabWidget,
                             QGroupBox, QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

style_sheet = """
QWidget {
    background-color: #C92108;
}
QWidget#Tabs {
    background-color: #FCEBCD;
    border-radius: 4px;
}
QWidget#ImageBorder {
    background-color: #FCF9F3;
    border: 2px solid #FABB4C;
    border-radius: 4px;
}
QWidget#Side {
    background-color: #EFD096;
    border-radius: 4px;
}
QLabel {
    background-color: #EFD096;
    border: 2px solid #EFD096;
    border-radius: 4px;
}
QLabel#Header {
    background-color: #EFD096;
    border: 2px solid #EFD096;
    border-radius: 4px;
    padding-left: 10px;
    color: #961A07;
}
QLabel#ImageInfo {
    background-color: #FCF9F3;
    border-radius: 4px;
}
QGroupBox {
    background-color: #FCEBCD;
    color: #961A07;
}
QRadioButton {
    background-color: #FCF9F3;
}
QPushButton {
    background-color: #C92108;
    border-radius: 4px;
    padding: 6px;
    color: #FFFFFF;
}
QPushButton:pressed {
    background-color: #C86354;
    color: #DFD8D7;
}
"""


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Настройте графический интерфейс приложения."""
        self.setMinimumSize(700, 700)
        self.setWindowTitle("6.1 - GUI заказа еды")
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Создайте и расположите виджеты в главном окне."""
        self.tab_bar = QTabWidget()
        self.pizza_tab = self.createPizzaTab()
        self.wings_tab = self.createWingsTab()

        self.tab_bar.addTab(self.pizza_tab, "Пицца")
        self.tab_bar.addTab(self.wings_tab, "Крылышки")

        self.side_widget = self.createSideWidget()
        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.tab_bar, 1)
        main_h_box.addWidget(self.side_widget)

        self.setLayout(main_h_box)

    def createSideWidget(self):
        """Создает боковое виджет для отображения заказа."""
        side_widget = QWidget()
        side_widget.setObjectName("Side")
        order_label = QLabel("ВАШ ЗАКАЗ", self)
        order_label.setObjectName("Header")

        self.display_pizza_label = QLabel("")
        self.display_toppings_label = QLabel("")
        self.display_wings_label = QLabel("")

        items_grid = QGridLayout()
        items_grid.addWidget(QLabel("Тип пиццы:"), 0, 0, Qt.AlignmentFlag.AlignRight)
        items_grid.addWidget(self.display_pizza_label, 0, 1)
        items_grid.addWidget(QLabel("Начинки:"), 1, 0, Qt.AlignmentFlag.AlignRight)
        items_grid.addWidget(self.display_toppings_label, 1, 1)
        items_grid.addWidget(QLabel("Дополнительно:"), 2, 0, Qt.AlignmentFlag.AlignRight)
        items_grid.addWidget(self.display_wings_label, 2, 1)

        side_layout = QVBoxLayout()
        side_layout.addWidget(order_label)
        side_layout.addLayout(items_grid)
        side_layout.addStretch()
        side_widget.setLayout(side_layout)

        return side_widget

    def createPizzaTab(self):
        """Создает вкладку пиццы с радиокнопками для выбора начинки и коржа."""
        pizza_tab = QWidget()
        tab_label = QLabel("СОЗДАЙТЕ СВОЮ СОБСТВЕННУЮ ПИЦЦУ", self)
        tab_label.setObjectName("Header")

        description_box = self.createImageDescriptionBox("images/pizza.png",
                                                         """<p>Создаем для вас пиццу на заказ. Начните с
                                                         вашего любимого коржа и добавьте любые начинки, а также
                                                         идеальное количество сыра и соуса.</p>""")

        crust_group = self.createRadioButtonGroup("ВЫБОР ВАШЕГО КОРЖА",
                                                  ["Ручной", "Плоский", "Фаршированный"])
        toppings_group = self.createRadioButtonGroup("ВЫБЕРИТЕ НАЧИНКУ",
                                                     ["Пепперони", "Колбаса", "Бекон", "Канадский бекон",
                                                      "Говядина", "Ананас", "Оливки", "Томат",
                                                      "Зеленый перец", "Грибы", "Лук", "Шпинат", "Сыр"])

        add_to_order_button = QPushButton("Добавить к заказу")
        add_to_order_button.clicked.connect(self.displayPizzaInOrder)

        pizza_layout = QVBoxLayout()
        pizza_layout.addWidget(tab_label)
        pizza_layout.addWidget(description_box)
        pizza_layout.addWidget(crust_group)
        pizza_layout.addWidget(toppings_group)
        pizza_layout.addStretch(1)
        pizza_layout.addWidget(add_to_order_button, alignment=Qt.AlignmentFlag.AlignRight)

        pizza_tab.setLayout(pizza_layout)
        return pizza_tab

    def createWingsTab(self):
        """Создает вкладку с крылышками и радиокнопками для выбора вкуса."""
        wings_tab = QWidget()
        tab_label = QLabel("ПРОБУЙТЕ НАШИ УДИВИТЕЛЬНЫЕ КРЫЛЫШКИ", self)
        tab_label.setObjectName("Header")

        description_box = self.createImageDescriptionBox("images/wings.png",
                                                         """<p>6 кусочков белого мяса с насыщенным вкусом
                                                         курицы, которые заставят вас вернуться за добавкой.</p>""")

        wings_group = self.createRadioButtonGroup("ВЫБЕРИТЕ СВОЙ ВКУС",
                                                  ["Баффало", "Кисло-сладкий", "Терияки", "Барбекю"])

        add_to_order_button = QPushButton("Добавить к заказу")
        add_to_order_button.clicked.connect(self.displayWingsInOrder)

        wings_layout = QVBoxLayout()
        wings_layout.addWidget(tab_label)
        wings_layout.addWidget(description_box)
        wings_layout.addWidget(wings_group)
        wings_layout.addWidget(add_to_order_button, alignment=Qt.AlignmentFlag.AlignRight)
        wings_layout.addStretch(1)

        wings_tab.setLayout(wings_layout)
        return wings_tab

    def createImageDescriptionBox(self, image_path, description_text):
        """Создает виджет с изображением и описанием."""
        description_box = QWidget()
        description_box.setObjectName("ImageBorder")

        pizza_image = self.loadImage(image_path)
        description_label = QLabel(description_text)
        description_label.setObjectName("ImageInfo")
        description_label.setWordWrap(True)
        description_label.setContentsMargins(10, 10, 10, 10)

        layout = QHBoxLayout()
        layout.addWidget(pizza_image)
        layout.addWidget(description_label, 1)

        description_box.setLayout(layout)
        return description_box

    def createRadioButtonGroup(self, title, options):
        """Создает групповой бокс с радиокнопками."""
        group_box = QGroupBox(title)
        button_group = QButtonGroup()
        layout = QVBoxLayout()

        for option in options:
            radio_button = QRadioButton(option)
            layout.addWidget(radio_button)
            button_group.addButton(radio_button)

        group_box.setLayout(layout)
        return group_box

    def displayPizzaInOrder(self):
        """Собирает информацию о выбранной пицце и обновляет боковой виджет."""
        if crust_button := self.crust_group.checkedButton():
            crust_text = crust_button.text()
            self.display_pizza_label.setText(crust_text)

            toppings = self.collectCheckedToppings()
            self.display_toppings_label.setText('\n'.join(toppings))
            self.update()

    def displayWingsInOrder(self):
        """Собирает информацию о выбранных крылышках и обновляет боковой виджет."""
        if wings_button := self.wings_group.checkedButton():
            wings_text = f"{wings_button.text()} Крылышки"
            self.display_wings_label.setText(wings_text)
            self.update()

    def collectCheckedToppings(self):
        """Создает список всех отмеченных радиокнопок для начинок."""
        return [button.text() for button in self.toppings_group.buttons() if button.isChecked()]

    def loadImage(self, img_path):
        """Загружает и масштабирует изображение."""
        try:
            pixmap = QPixmap(img_path)
            image_label = QLabel(self)
            image_label.setObjectName("ImageInfo")
            image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation))
            return image_label
        except FileNotFoundError as error:
            print(f"Изображение не найдено. Ошибка: {error}")
            return QLabel()  # Возврат пустого QLabel в случае ошибки


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = MainWindow()
    sys.exit(app.exec())
