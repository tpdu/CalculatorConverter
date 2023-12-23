Примечание: для скачивания презентации нажмите на файл презентации в GitHub и нажмите ViewRaw. Загрузка должна начаться автоматически.

Проект представляет собой калькулятор и конвертер единиц измерения

На странице калькулятора есть окно ввода, кнопки цифр и действий (включая возведение в квадрат, куб, другие степени, скобки), а также 2 кнопки: сброса и удаления одного символа
После ввода выражения и нажатия на "=" в верхней части окна отображается выражение, а в поле ввода - ответ.

На странице калькулятора можно переключится на страницу конвертера единиц.

Конвертер единиц позволяет конвертировать единицы измерения длины, скорости, температуры, площади, объёма.

В проекте используется PyQT 5

PyQT widgets: _QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QGridLayout, \
    QStackedWidget, QSizePolicy, QComboBox, QHBoxLayout

PyQT Core

PyQT GUI: _QFont_

Список поддерживаемых единиц измерения:
--------------------------------------
Длина:
* Километры
* Метры
* Сантиметры
* Миллиметры
* Мили
* Ярды
--------------------------------------
Скорость:
* Метр/секунда
* Километр/час
* Миля/час
* Фут/секунда
* Узлы
--------------------------------------
Температура:
* Цельсий
* Фаренгейт
* Кельвин
--------------------------------------
Объём:
* Литр
* Миллилитр
* Кубический метр
* Кубический Сантиметр
* Галлон
* Кварта
--------------------------------------
Площадь:
* Квадратный метр
* Квадратный Километр
* Квадратный миля
* Квадратный ярд
* Квадратный фут
* Квадратный дюйм
