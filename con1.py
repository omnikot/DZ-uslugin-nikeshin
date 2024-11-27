import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QCheckBox, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.login_is_successful = False
        self.initializeUI()

    def initializeUI(self):
        """Настройте графический интерфейс приложения."""
        self.setFixedSize(360, 220)
        self.setWindowTitle("3.1 – Login GUI")
        self.setUpWindow()
        self.show()

    def setUpWindow(self):
        """Создайте и расположите виджеты в главном окне."""
        self.createLabels()
        self.createInputFields()
        self.createButtons()

    def createLabels(self):
        """Создает и размещает метки в окне."""
        login_label = QLabel("Login", self)
        login_label.setFont(QFont("Arial", 20))
        login_label.move(160, 10)

        username_label = QLabel("Имя пользователя:", self)
        username_label.move(20, 54)

        password_label = QLabel("Пароль:", self)
        password_label.move(20, 86)

        not_member_label = QLabel("Не являетесь членом?", self)
        not_member_label.move(20, 186)

    def createInputFields(self):
        """Создает и помещает поля ввода для имени пользователя и пароля."""
        self.username_edit = QLineEdit(self)
        self.username_edit.resize(250, 24)
        self.username_edit.move(90, 50)

        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.resize(250, 24)
        self.password_edit.move(90, 82)

        # Создаем QCheckBox для отображения пароля
        self.show_password_cb = QCheckBox("Показать пароль", self)
        self.show_password_cb.move(90, 110)
        self.show_password_cb.toggled.connect(self.displayPasswordIfChecked)

    def createButtons(self):
        """Создает и размещает кнопки в окне."""
        login_button = QPushButton("Login", self)
        login_button.resize(320, 34)
        login_button.move(20, 140)
        login_button.clicked.connect(self.clickLoginButton)

        sign_up_button = QPushButton("Зарегистрироваться", self)
        sign_up_button.move(120, 180)
        sign_up_button.clicked.connect(self.createNewUser)

    def clickLoginButton(self):
        """Проверяет, совпадают ли имя пользователя и пароль с существующими записями."""
        users = self.loadUsers()
        username = self.username_edit.text()
        password = self.password_edit.text()

        if (username in users) and (users[username] == password):
            QMessageBox.information(self, "Login Successful!", "Login Successful!", QMessageBox.StandardButton.Ok)
            self.login_is_successful = True
            self.close()
            self.openApplicationWindow()
        else:
            QMessageBox.warning(self, "Сообщение об ошибке", "Имя пользователя или пароль неверны.",
                                QMessageBox.StandardButton.Close)

    def loadUsers(self):
        """Загружает пользователей из файла."""
        users = {}
        file = "files/users.txt"

        try:
            with open(file, "r") as f:
                for line in f:
                    username_info, password_info = line.split()
                    users[username_info] = password_info.strip("\n")
        except FileNotFoundError as error:
            QMessageBox.warning(self, "Ошибка", f"Файл не найден.\nОшибка: {error}", QMessageBox.StandardButton.Ok)
            open(file, "w").close()  # Создаем файл, если он не существует

        return users

    def displayPasswordIfChecked(self, checked):
        """Отображает или маскирует пароль в зависимости от состояния QCheckBox."""
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)

    def createNewUser(self):
        """Открывает диалог для создания новой учетной записи."""
        # Assuming NewUserDialog is defined elsewhere
        from registration import NewUserDialog  # Импортируем только при необходимости
        self.create_new_user_window = NewUserDialog()
        self.create_new_user_window.show()

    def openApplicationWindow(self):
        """Открывает главное окно после входа в систему."""
        self.main_window = MainWindow()
        self.main_window.show()

    def closeEvent(self, event):
        """Обрабатывает событие закрытия окна."""
        if self.login_is_successful:
            event.accept()
        else:
            answer = QMessageBox.question(self, "Выйти из приложения?", "Вы уверены, что хотите выйти?",
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                          QMessageBox.StandardButton.Yes)
            event.accept() if answer == QMessageBox.StandardButton.Yes else event.ignore()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Настройте графический интерфейс главного окна."""
        self.setMinimumSize(640, 426)
        self.setWindowTitle('3.1 - Главное окно')
        self.setUpMainWindow()

    def setUpMainWindow(self):
        """Создайте и расположите виджеты в главном окне."""
        self.loadBackgroundImage()

    def loadBackgroundImage(self):
        """Загружает фоновое изображение."""
        image = "images/background_kingfisher.jpg"
        try:
            pixmap = QPixmap(image)
            main_label = QLabel(self)
            main_label.setPixmap(pixmap)
            main_label.move(0, 0)
        except FileNotFoundError as error:
            print(f"Изображение не найдено.\nError: {error}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec())
