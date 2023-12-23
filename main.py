import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGridLayout, \
    QStackedWidget, QSizePolicy, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# В классе CalculatorBackend содержатся функции вычисления и изменения выражения
class CalculatorBackend:
    def __init__(self):
        self.expression = ""

    def set_expression(self, expression):
        self.expression = expression

    def calculate(self):
        try:
            result = eval(self.expression)
            return result
        except Exception as e:
            return str(e)

    def clear_all(self):
        self.expression = ""

    def clear_last(self):
        self.expression = self.expression[:-1]

    def add_to_expression(self, value):
        self.expression += value

    def square(self):
        self.expression += "**2"

    def cube(self):
        self.expression += "**3"

    def power(self):
        self.expression += "**"


# GUI класс калькулятора с использованием библиотеки Qt, обеспечивает визуализацию и взаимодействие с пользователем.
class CalculatorPage(QWidget):
    def __init__(self, backend, switch_function):
        super().__init__()
        self.backend = backend
        self.switch_function = switch_function
        self.init_ui()

    def init_ui(self):
        self.result_display = QLineEdit(self)
        self.result_display.setFixedHeight(50)
        self.result_display.setAlignment(Qt.AlignRight)
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont('Arial', 16))

        self.history_label = QLabel(self)
        self.history_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.history_label.setAlignment(Qt.AlignRight)
        self.history_label.setFont(QFont('Arial', 12))

        self.buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'Del', '(', ')',
            'x^2', 'x^3', 'x^n'
        ]

        self.grid_layout = QGridLayout()
        self.create_buttons()

        switch_button = QPushButton("Переключится на конвертер единиц", self)
        switch_button.clicked.connect(self.switch_to_converter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.history_label)
        main_layout.addWidget(self.result_display)
        main_layout.addLayout(self.grid_layout)
        main_layout.addWidget(switch_button)

        self.setLayout(main_layout)

    def create_buttons(self):
        row, col = 0, 0

        for button_text in self.buttons:
            button = QPushButton(button_text, self)
            button.setFixedSize(60, 60)
            button.clicked.connect(lambda _, text=button_text: self.on_button_click(text))
            button.setFont(QFont('Arial', 14))
            self.grid_layout.addWidget(button, row, col)

            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_button_click(self, button_text):
        if button_text == '=':
            self.backend.set_expression(self.result_display.text())
            result = self.backend.calculate()
            self.history_label.setText(f'{self.result_display.text()} = {result}')
            self.result_display.setText(str(result))
        elif button_text == 'C':
            self.backend.clear_all()
            self.result_display.clear()
            self.history_label.clear()
        elif button_text == 'Del':
            self.backend.clear_last()
            self.result_display.backspace()
        elif button_text == 'x^2':
            self.backend.square()
            self.result_display.setText(self.result_display.text() + "**2")
        elif button_text == 'x^3':
            self.backend.cube()
            self.result_display.setText(self.result_display.text() + "**3")
        elif button_text == 'x^n':
            self.backend.power()
            self.result_display.setText(self.result_display.text() + "**")
        else:
            current_text = self.result_display.text()
            new_text = current_text + button_text
            self.result_display.setText(new_text)
            self.backend.add_to_expression(button_text)

    def switch_to_converter(self):
        self.switch_function(1)  # Switch to the Unit Converter page


# GUI класс конвертера единиц с использованием библиотеки Qt. Позволяет выбирать категорию и производить конвертацию
# между единицами измерения
class UnitConverterPage(QWidget):
    def __init__(self, switch_function):
        super().__init__()
        self.switch_function = switch_function
        self.init_ui()

    def init_ui(self):
        self.categories_label = QLabel("Выберите категорию:")
        self.categories_combobox = QComboBox(self)
        self.categories_combobox.addItems(["Длина", "Скорость", "Температура", "Объём", "Площадь"])
        self.categories_combobox.currentIndexChanged.connect(self.update_units)

        self.from_unit_label = QLabel("Выберите изначальную единицу измерения:")
        self.to_unit_label = QLabel("Выберите конечную единицу измерения:")
        self.from_unit_combobox = QComboBox(self)
        self.to_unit_combobox = QComboBox(self)

        self.swap_button = QPushButton("Swap", self)
        self.swap_button.clicked.connect(self.swap_units)

        self.input_label = QLabel("Ввод:")
        self.output_label = QLabel("Вывод:")
        self.input_field = QLineEdit(self)
        self.output_field = QLineEdit(self)
        self.output_field.setReadOnly(True)

        conversion_button = QPushButton("Конвертировать", self)
        conversion_button.clicked.connect(self.convert_units)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.categories_label, 0, 0)
        grid_layout.addWidget(self.categories_combobox, 0, 1, 1, 2)
        grid_layout.addWidget(self.from_unit_label, 1, 0)
        grid_layout.addWidget(self.to_unit_label, 2, 0)
        grid_layout.addWidget(self.from_unit_combobox, 1, 1)
        grid_layout.addWidget(self.to_unit_combobox, 2, 1)
        grid_layout.addWidget(self.swap_button, 1, 2, 2, 1)
        grid_layout.addWidget(self.input_label, 3, 0)
        grid_layout.addWidget(self.output_label, 4, 0)
        grid_layout.addWidget(self.input_field, 3, 1)
        grid_layout.addWidget(self.output_field, 4, 1)
        grid_layout.addWidget(conversion_button, 3, 2, 2, 1)

        switch_button = QPushButton("Переключиться на калькулятор", self)
        switch_button.clicked.connect(self.switch_to_calculator)

        button_layout = QHBoxLayout()
        button_layout.addWidget(switch_button)
        button_layout.addStretch()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(grid_layout)
        main_layout.addLayout(button_layout)

        self.update_units()

    def update_units(self):
        selected_category = self.categories_combobox.currentText()
        units = self.get_units_for_category(selected_category)

        self.from_unit_combobox.clear()
        self.to_unit_combobox.clear()

        self.from_unit_combobox.addItems(units)
        self.to_unit_combobox.addItems(units)

    def swap_units(self):
        from_unit_index = self.from_unit_combobox.currentIndex()
        to_unit_index = self.to_unit_combobox.currentIndex()
        self.from_unit_combobox.setCurrentIndex(to_unit_index)
        self.to_unit_combobox.setCurrentIndex(from_unit_index)

    def convert_units(self):
        try:
            value_input = (self.input_field.text())
            if "," in value_input:
                self.output_field.setText("Используйте '.' вместо ','")
            else:
                input_value = float(self.input_field.text())
                from_unit = self.from_unit_combobox.currentText()
                to_unit = self.to_unit_combobox.currentText()

                result = self.perform_conversion(input_value, from_unit, to_unit)

                self.output_field.setText(str(result))

        except ValueError:
            self.output_field.setText("Invalid Input")

    def perform_conversion(self, value, from_unit, to_unit):
        conversion_factors = {
            # Length
            ("метр", "Километр"): 0.001,
            ("Километр", "метр"): 1000,
            ("метр", "Сантиметр"): 100,
            ("Сантиметр", "метр"): 0.01,
            ("метр", "миллиметр"): 1000,
            ("миллиметр", "метр"): 0.001,
            ("миля", "Километр"): 1.60934,
            ("Километр", "миля"): 0.621371,
            ("миля", "метр"): 1609.34,
            ("метр", "миля"): 0.000621371,
            ("ярд", "метр"): 0.9144,
            ("метр", "ярд"): 1.09361,

            # Speed
            ("метр/секунда", "Километр/час"): 3.6,
            ("Километр/час", "метр/секунда"): 0.277778,
            ("метр/секунда", "миля/час"): 2.23694,
            ("миля/час", "метр/секунда"): 0.44704,
            ("метр/секунда", "фут/секунда"): 3.28084,
            ("фут/секунда", "метр/секунда"): 0.3048,
            ("метр/секунда", "Узлы"): 1.94384,
            ("Узлы", "метр/секунда"): 0.514444,

            # Temperature
            ("Цельсий", "Фаренгейт"): lambda x: x * 9 / 5 + 32,
            ("Фаренгейт", "Цельсий"): lambda x: (x - 32) * 5 / 9,
            ("Цельсий", "Кельвин"): lambda x: x + 273.15,
            ("Кельвин", "Цельсий"): lambda x: x - 273.15,
            ("Фаренгейт", "Кельвин"): lambda x: (x - 32) * 5 / 9 + 273.15,
            ("Кельвин", "Фаренгейт"): lambda x: x * 9 / 5 - 459.67,

            # Volume
            ("Литр", "Миллилитр"): 1000,
            ("Миллилитр", "Литр"): 0.001,
            ("Литр", "Кубический метр"): 0.001,
            ("Кубический метр", "Литр"): 1000,
            ("Литр", "Кубический Сантиметр"): 1000,
            ("Кубический Сантиметр", "Литр"): 0.001,
            ("Галлон", "Литр"): 3.78541,
            ("Литр", "Галлон"): 0.264172,
            ("Галлон", "Миллилитр"): 3785.41,
            ("Миллилитр", "Галлон"): 0.000264172,
            ("Кварта", "Литр"): 0.946353,
            ("Литр", "Кварта"): 1.05669,

            # Area
            ("Квадратный метр", "Квадратный Километр"): 1e-6,
            ("Квадратный Километр", "Квадратный метр"): 1e6,
            ("Квадратный метр", "Квадратный миля"): 3.861e-7,
            ("Квадратная миля", "Квадратный метр"): 2.59e6,
            ("Квадратный метр", "Квадратный ярд"): 1.19599,
            ("Квадратный ярд", "Квадратный метр"): 0.836127,
            ("Квадратный метр", "Квадратный фут"): 10.7639,
            ("Квадратный фут", "Квадратный метр"): 0.092903,
            ("Квадратный метр", "Квадратный дюйм"): 1550.0031,
            ("Квадратный дюйм", "Квадратный метр"): 0.00064516,
        }

        conversion_factor = conversion_factors.get((from_unit, to_unit))

        if callable(conversion_factor):
            result = conversion_factor(value)
        elif conversion_factor is not None:
            result = value * conversion_factor
        else:
            result = None

        return result

    def switch_to_calculator(self):
        self.switch_function(0)  # Switch to the Calculator page

    def get_units_for_category(self, category):
        units_dict = {
            "Длина": ["метр", "Километр", "Сантиметр", "миллиметр", "миля", "ярд"],
            "Скорость": ["метр/секунда", "Километр/час", "миля/час", "фут/секунда", "Узлы"],
            "Температура": ["Цельсий", "Фаренгейт", "Кельвин"],
            "Объём": ["Литр", "Миллилитр", "Кубический метр", "Кубический Сантиметр", "Галлон", "Кварта"],
            "Площадь": ["Квадратный метр", "Квадратный Километр", "Квадратный миля", "Квадратный ярд", "Квадратный фут",
                        "Квадратный дюйм"],
        }

        return units_dict.get(category, [])


# GUI класс главной страницы с использованием библиотеки Qt. Обеспечивает переключение между страницами калькулятора
# и конвертера единиц.
class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator_backend = CalculatorBackend()
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget()

        calculator_page = CalculatorPage(self.calculator_backend, self.switch_page)
        unit_converter_page = UnitConverterPage(self.switch_page)

        self.stacked_widget.addWidget(calculator_page)
        self.stacked_widget.addWidget(unit_converter_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_page = MainPage()
    main_page.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_page = MainPage()
    main_page.show()
    sys.exit(app.exec_())
