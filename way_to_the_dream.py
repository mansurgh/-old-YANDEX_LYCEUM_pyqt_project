import re
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from design_project import Ui_MainWindow

# глобальные переменные:

# самый большой возраст человека в мире
OLDEST_HUMAN = 112

# минимальный возраст
MIN_AGE_FOR_CALC = 7

# самый большой вес человека в мире
GREATEST_WEIGHT = 635

# минимальный вес
MIN_WEIGHT_FOR_CALC = 20

# самый большой рост в мире
HIGHEST_GROWTH = 272

# самый маленький рост в мире
LOWEST_GROWTH = 55

# максимальный возможный суточный расход калорий
MAX_EXP = 14241

# минимальный возможный суточный расход калорий
MIN_EXP = 417

# css для светлой темы
LIGHT_LINE_COMBO_STYLE = "color: black; background-color: #FFFFFF;"
LIGHT_BTN_STYLE = "color: black; background-color: #EDEDED;"

# css для тёмной темы
DARK_LINE_COMBO_STYLE = "color: white; background-color: #27292D;"
DARK_BTN_STYLE = "color: white; background-color: #2D2F34;"


class WayToTheDream(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # настройки окна
        self.setWindowTitle('Way To The Dream!')
        self.setFixedSize(1010, 763)
        # условия для запуска  | калькулятор
        self.text_for_calc()
        self.LineVivodCalc.setDisabled(True)
        self.PolMuzh.stateChanged.connect(self.calculating_if_polmuzh)
        self.PolZhen.stateChanged.connect(self.calculating_if_polzhen)
        # лимит на количество символов в лайнэдитах + возможность вводить только цифры
        self.LineRost.setValidator(QtGui.QIntValidator(1, 999))
        self.LineVes.setValidator(QtGui.QIntValidator(1, 999))
        self.LineVozrast.setValidator(QtGui.QIntValidator(1, 999))
        self.lineEdit.setValidator(QtGui.QIntValidator(1, 99999))
        # условия для запуска  | блюда
        self.text_for_dishes_lib()
        self.NazvanieBluda.setGeometry(QtCore.QRect(280, 350, 180, 21))
        self.ComboViborBluda.activated.connect(self.dish_lib)
        self.ComboViborBluda.activated.connect(self.set_image)
        # при выборе блюда из комбобокса, текст лэйбла меняется на название блюда
        self.ComboViborBluda.textActivated.connect(self.NazvanieBluda.setText)
        # смена темы приложения
        self.light_theme()
        self.BtnThemeLight.clicked.connect(self.light_theme)
        self.BtnThemeDark.clicked.connect(self.dark_theme)
        # текст и условия запуска  | советы
        self.label_4.setText('-------------------------------------->')
        self.label_5.setText('')
        self.label.setText('Введите сут. расход ккал (округлите)')
        self.comboBox.addItem('Ничего не хочу')
        self.comboBox.addItem('Хочу похудеть')
        self.comboBox.addItem('Хочу улучшить фигуру')
        self.comboBox.addItem('Хочу набрать мыш. массу')
        self.comboBox.activated.connect(self.expenditure_advice)

    # информация о калькуляторе расхода калорий
    def text_for_calc(self):
        self.TextCalc.setText("<html><head/><body><p>||-----------------------------------------------><br>||<br"
                              ">||Калькулятор расхода "
                              "калорий.<br>||<br> ||Вы можете посчитать свой суточный<br> ||расход калорий!</p></body>"
                              "</html>")
        self.UkazatVozrast.setText("Возраст (лет)")
        self.UkazatVes.setText("Вес (кг)")
        self.UkazatRost.setText("Рост (см)")

    # информация о библиотеке блюд
    def text_for_dishes_lib(self):
        self.TextBluda.setText("<html><head/><body><p>||Библиотека блюд.<br>||<br> ||Вы можете выбрать<br> ||блюдо из "
                               "выпадающего<br> ||списка и увидеть его<br> ||описание и "
                               "картинку!<br>\/</p></body></html>")

    # настройка светлой темы
    def light_theme(self):
        self.setStyleSheet("background-color: #F0F0F0;")
        self.LineVozrast.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.LineVes.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.LineRost.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.LineVivodCalc.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.lineEdit.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.ComboFizAkt.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.ComboTrenirovki.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.ComboViborBluda.setStyleSheet(LIGHT_LINE_COMBO_STYLE)
        self.comboBox.setStyleSheet(LIGHT_LINE_COMBO_STYLE)

        self.BtnThemeLight.setStyleSheet(LIGHT_BTN_STYLE)
        self.BtnThemeDark.setStyleSheet(LIGHT_BTN_STYLE)

    # настройка тёмной темы
    def dark_theme(self):
        self.setStyleSheet("background-color: #1F2023;")
        self.LineVozrast.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.LineVes.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.LineRost.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.LineVivodCalc.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.lineEdit.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.ComboFizAkt.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.ComboTrenirovki.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.ComboViborBluda.setStyleSheet(DARK_LINE_COMBO_STYLE)
        self.comboBox.setStyleSheet(DARK_LINE_COMBO_STYLE)

        self.BtnThemeLight.setStyleSheet(DARK_BTN_STYLE)
        self.BtnThemeDark.setStyleSheet(DARK_BTN_STYLE)

    # проверка на соблюдение условий В КАЛЬКУЛЯТОРЕ СУТОЧНОГО РАСХОДА КАЛОРИЙ если пользователь выбрал МУЖСКОЙ ПОЛ
    def checking_for_a_condition_polmuzh(self):
        string_vozrast1 = int("0" + "".join(list(map(str, re.findall(r'\d+', self.LineVozrast.text())))))
        if MIN_AGE_FOR_CALC <= string_vozrast1 <= OLDEST_HUMAN:
            string_ves1 = int("0" + "".join(list(map(str, re.findall(r'\d+', self.LineVes.text())))))
            if GREATEST_WEIGHT >= string_ves1 >= MIN_WEIGHT_FOR_CALC:
                string_rost1 = int("0" + "".join(list(map(str, re.findall(r'\d+', self.LineRost.text())))))
                if HIGHEST_GROWTH >= string_rost1 >= LOWEST_GROWTH:
                    return 5 + (10 * string_ves1) + (6.25 * string_rost1) - (
                            5 * string_vozrast1)

    # проверка на соблюдение условий В КАЛЬКУЛЯТОРЕ СУТОЧНОГО РАСХОДА КАЛОРИЙ если пользователь выбрал ЖЕНСКИЙ ПОЛ
    def checking_for_a_condition_polzhen(self):
        string_vozrast1 = int("0" + "".join(list(map(str, re.findall(r'\d+', self.LineVozrast.text())))))
        if MIN_AGE_FOR_CALC <= string_vozrast1 <= OLDEST_HUMAN:
            string_ves1 = int("0" + "".join(list(map(str, re.findall(r'\d+', self.LineVes.text())))))
            if GREATEST_WEIGHT >= string_ves1 >= MIN_WEIGHT_FOR_CALC:
                string_rost1 = int("0" + "".join(list(map(str, re.findall(r'\d+', self.LineRost.text())))))
                if HIGHEST_GROWTH >= string_rost1 >= LOWEST_GROWTH:
                    return (10 * string_ves1) + (6.25 * string_rost1) - (
                            5 * string_vozrast1) - 161

    # вывод суточного расхода калорий если пользователь выбрал МУЖСКОЙ ПОЛ
    def calculating_if_polmuzh(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.PolZhen.setEnabled(False)
            if self.checking_for_a_condition_polmuzh() is None:
                self.LineVivodCalc.clear()
            elif self.ComboFizAkt.currentText() == 'Сидячий':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polmuzh() * 1.2) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Слабый физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polmuzh() * 1.375) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Преобладает физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polmuzh() * 1.55) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Тяжёлый физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polmuzh() * 1.725) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Очень тяжёлый физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polmuzh() * 1.9) + ' ккал/сут.')
        else:
            self.PolZhen.setEnabled(True)
            self.LineVivodCalc.clear()

    # вывод суточного расхода калорий если пользователь выбрал ЖЕНСКИЙ ПОЛ
    def calculating_if_polzhen(self, toggle):
        if toggle == QtCore.Qt.Checked:
            self.PolMuzh.setEnabled(False)
            if self.checking_for_a_condition_polzhen() is None:
                self.LineVivodCalc.clear()
            elif self.ComboFizAkt.currentText() == 'Сидячий':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polzhen() * 1.2) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Слабый физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polzhen() * 1.375) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Преобладает физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polzhen() * 1.55) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Тяжёлый физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polzhen() * 1.725) + ' ккал/сут.')
            elif self.ComboFizAkt.currentText() == 'Очень тяжёлый физ. труд':
                self.LineVivodCalc.setText(str(self.checking_for_a_condition_polzhen() * 1.9) + ' ккал/сут.')
        else:
            self.PolMuzh.setEnabled(True)
            self.LineVivodCalc.clear()

    # шаблон html текста для вывода состава и КБЖУ блюда
    @staticmethod
    def generate_html_text(ing1, ing2, ing3, ing4, c, p, f, carb):
        return f'<html><head><body><p>Состав:<br>{ing1}<br>{ing2}<br>{ing3}<br>{ing4}<br><br>КБЖУ - {c}Ккал, {p}г, ' \
               f'{f}г, <br> {carb}г.</p></body></head></html>'

    # вывод состава и КБЖУ выбранного блюда
    def dish_lib(self):
        if self.ComboViborBluda.currentText() == 'Гамбургер':
            self.label_2.setText(self.generate_html_text('Булочка, Говяжья котлета,', 'Кетчуп, Горчица,',
                                                         'Лук, Огурцы маринованные,',
                                                         'Приправа для гриля', 257, 14, '8,6', 29))
        elif self.ComboViborBluda.currentText() == 'Пицца':
            self.label_2.setText(self.generate_html_text('Тесто, овощи,', 'Мясо, сыр,', 'Соусы', '', 340, 10, 14, 30))
        elif self.ComboViborBluda.currentText() == 'Салат "Цезарь"':
            self.label_2.setText(self.generate_html_text('Листовый салат, ', 'Сыр "Пармезан",', 'Сухарики пшеничные, ',
                                                         'Соус "Цезарь"', 375, '7,4', 9, 11))
        elif self.ComboViborBluda.currentText() == 'Салат "Греческий"':
            self.label_2.setText(self.generate_html_text('Помидоры, Перец болг.', 'Огурцы, Лук, Брынза,',
                                                         'Маслины, Соус', '', 877, 25, 64, 41))
        elif self.ComboViborBluda.currentText() == 'Картошка Фри':
            self.label_2.setText(self.generate_html_text('Картошка.', '', '', '', 274, '3,48', '35,66', '14,06'))
        elif self.ComboViborBluda.currentText() == 'Картошка по-деревенски (Айдахо)':
            self.label_2.setText(self.generate_html_text('Картошка.', '', '', '', 331, '4,6', 15, 42))
        elif self.ComboViborBluda.currentText() == 'Наггетсы':
            self.label_2.setText(self.generate_html_text('Котлеты куриные', '', '', '', 440, 25, 21, 28))
        elif self.ComboViborBluda.currentText() == 'Крылышки':
            self.label_2.setText(self.generate_html_text('Куриные крылья, Специи', '', '', '', 487, '28,4', '31,5',
                                                         '22,5'))
        else:
            self.label_2.clear()

    # вывод картинки выбранного блюда
    def set_image(self):
        burger = QPixmap("photos_for_project/burger.png")
        pizza = QPixmap("photos_for_project/pizza.png")
        cezar = QPixmap("photos_for_project/cezar.png")
        grec = QPixmap("photos_for_project/grec.png")
        free = QPixmap("photos_for_project/free.png")
        aydaho = QPixmap("photos_for_project/aydaho.png")
        naggetsy = QPixmap("photos_for_project/naggetsy.png")
        wings = QPixmap("photos_for_project/wings.png")
        if self.ComboViborBluda.currentText() == 'Гамбургер':
            self.photo.setPixmap(burger)
        elif self.ComboViborBluda.currentText() == 'Пицца':
            self.photo.setPixmap(pizza)
        elif self.ComboViborBluda.currentText() == 'Салат "Цезарь"':
            self.photo.setPixmap(cezar)
        elif self.ComboViborBluda.currentText() == 'Салат "Греческий"':
            self.photo.setPixmap(grec)
        elif self.ComboViborBluda.currentText() == 'Картошка Фри':
            self.photo.setPixmap(free)
        elif self.ComboViborBluda.currentText() == 'Картошка по-деревенски (Айдахо)':
            self.photo.setPixmap(aydaho)
        elif self.ComboViborBluda.currentText() == 'Наггетсы':
            self.photo.setPixmap(naggetsy)
        elif self.ComboViborBluda.currentText() == 'Крылышки':
            self.photo.setPixmap(wings)
        else:
            self.photo.clear()

    # проверка введённого пользователем суточного расхода калорий
    def checking_condition_exp(self):
        find_d = re.findall(r'\d+', self.lineEdit.text())
        if find_d:
            if MAX_EXP >= int(''.join(list(map(str, find_d)))) >= MIN_EXP:
                return int(''.join(list(map(str, find_d))))
        return False

    # вывод совета, в зависимости от выбора в комбобоксе
    def expenditure_advice(self):
        if self.comboBox.currentText() == 'Хочу похудеть':
            _condition_exp = self.checking_condition_exp()
            if _condition_exp:
                _condition_exp = _condition_exp - 500
                self.label_5.setText(
                    f'Чтобы похудеть нужно понизить свой суточный расход калорий до '
                    f'{_condition_exp} ккал.'
                )
                self.label_5.setWordWrap(True)
        elif self.comboBox.currentText() == 'Хочу улучшить фигуру':
            _condition_exp = self.checking_condition_exp()
            self.label_5.setText(
                f'Чтобы улучшить фигуру, нужно больше тренироваться при том же суточном'
                f' расходе калорий.'
            )
            self.label_5.setWordWrap(True)
        elif self.comboBox.currentText() == 'Хочу набрать мыш. массу':
            _condition_exp2 = self.checking_condition_exp()
            if _condition_exp2:
                _condition_exp2 = _condition_exp2 + 400
                self.label_5.setText(
                    f'Чтобы набрать мышечную массу нужно больше тренироваться и повысить суточный расход калорий до '
                    f'{_condition_exp2} ккал.'
                )
                self.label_5.setWordWrap(True)
        else:
            self.label_5.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WayToTheDream()
    ex.show()
    sys.exit(app.exec_())
