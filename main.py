import ui


class Calculator(ui.Ui_MainWindow):

    def setupUi(self, MainWindow):
        super(Calculator, self).setupUi(MainWindow)
        self.btn_event_listener()

    def btn_event_listener(self):
        self.n0.clicked.connect(lambda: self.write_element(self.n0.text()))
        self.n1.clicked.connect(lambda: self.write_element(self.n1.text()))
        self.n2.clicked.connect(lambda: self.write_element(self.n2.text()))
        self.n3.clicked.connect(lambda: self.write_element(self.n3.text()))
        self.n4.clicked.connect(lambda: self.write_element(self.n4.text()))
        self.n5.clicked.connect(lambda: self.write_element(self.n5.text()))
        self.n6.clicked.connect(lambda: self.write_element(self.n6.text()))
        self.n7.clicked.connect(lambda: self.write_element(self.n7.text()))
        self.n8.clicked.connect(lambda: self.write_element(self.n8.text()))
        self.n9.clicked.connect(lambda: self.write_element(self.n9.text()))
        self.plus.clicked.connect(lambda: self.write_element(' ' + self.plus.text() + ' '))
        self.minus.clicked.connect(lambda: self.write_element(' ' + self.minus.text() + ' '))
        self.div_float.clicked.connect(lambda: self.write_element(' ' + self.div_float.text() + ' '))
        self.pow.clicked.connect(lambda: self.write_element(' ' + self.pow.text() + ' '))
        self.umnozh.clicked.connect(lambda: self.write_element(' ' + self.umnozh.text() + ' '))
        self.mod.clicked.connect(lambda: self.write_element(' ' + self.mod.text() + ' '))
        self.convert_to.clicked.connect(lambda: self.write_element(' ' + self.convert_to.text() + ' '))
        self.clear_all.clicked.connect(self.clear_text_area)
        self.clear.clicked.connect(lambda: self.clear_one_element(self.input_area))
        self.equal.clicked.connect(lambda: self.solve(self.input_area))
        self.float.clicked.connect(lambda: self.write_element('.'))
        self.sign.clicked.connect(lambda: self.change_sign(self.input_area))

    input_area = ''
    prev_letter = ''
    operators = [' + ', ' - ', ' / ', ' * ', ' -> ', ' ^ ', ' % ', '.']
    strip_operators = ['+', '-', '/', '*', '->', '^', '%', '.']

    def write_element(self, letter):
        """
        input_area - хранит лишь промежуточные значения, чтобы затем вывести в поле вывода
        prev_letter - хранит в себе значение предыдущего элемента
        Тут такая логика: чтобы избежать двойных операторов, мы проверяем входящий символ на принадлежность к операторам
        Если предыдущий символ тоже принадлежит к операторам(запятая туда тоже входит), то
        1) Если поле вывода пустое, ничего не делаем, иначе мы вообще потом ничего не сможем делать
        2) Если число уже имеет запятую, ничего не делаем
        3) Если предыдущий знак такой же как текущий - не приписываем ничего
        4) Если предыдущий не такой же как текущий - оставляем текущий, предудщий убираем
        Иначе просто приписываем символ, так как это по-любому число
        :param letter: символ поself.ступающий на отрисовку
        :return:
        """

        if letter in self.operators and self.output.text() == '':
            return 0

        if letter == '.':
            temp = self.input_area
            temp = temp.split()
            if (temp[-1] + letter).count('.') > 1:
                return 0

        if letter in self.operators:
            if letter == self.prev_letter:
                self.input_area += ''
            elif self.prev_letter in self.operators:
                self.input_area = self.input_area.replace(self.prev_letter, letter)
            else:
                self.input_area += letter
        else:
            self.input_area += letter
        self.prev_letter = letter
        self.output.setText(self.input_area)

    def change_sign(self, text_area):
        """
        Берём строку, делим с помощью метода split смотрим последний элемент и проверяем его знак
        1) Если это какой-то оператор, ничего не делаем
        2) Если же это число, то при необходимости заменяем минус пустотой или приписываем минус
        3) Обратно собираем строку и выводим её
        :param text_area: значение поля вывода
        :return:
        """

        text_area = text_area.split()

        if text_area[-1] in self.strip_operators:
            return 0
        if text_area[-1].startswith('-'):
            text_area[-1] = text_area[-1].replace('-', '')
        else:
            text_area[-1] = '-' + text_area[-1]

        a = ''
        for i in range(len(text_area)):
            if text_area[i] in self.strip_operators:
                a += ' ' + text_area[i] + ' '
            else:
                a += text_area[i]
        self.input_area = a
        self.output.setText(a)

    def solve(self, text_area):
        """
        Берём строку, делим и проверяем её операторы. Пробелы здесь очень много значат - благодаря ним можно грамотно
        поделить строку на нужные составляющие. Приоритет действий определяется тем, что сначала проверяются сильные
        операторы, затем только слабые. После проверки на сильные операторы остаются пустые строки - их удаляем.
        Для удобства всё отображается в типе float.
        1 + 3 * 6                  Исходная строка
        ['1', '+', '3', '*', '6']  Обрабатываемое значение
        ['1', '+', '', '', '18.0'] Проверили сильные операторы
        ['', '', '19.0']           Проверка слыбых операторов
        19.0                       Результат
        :param text_area: значение поля вывода
        :return:
        """
        text_area = text_area.split(' ')

        if text_area[-1] == '':
            return 0
        for i in range(len(text_area)):
            if text_area[i] == '*':
                text_area[i + 1] = str(float(text_area[i - 1]) * float(text_area[i + 1]))
                text_area[i - 1], text_area[i] = '', ''
            if text_area[i] == '/':
                try:
                    text_area[i + 1] = str(float(text_area[i - 1]) / float(text_area[i + 1]))
                except ZeroDivisionError:
                    text_area[i + 1] = 'На ноль делить нельзя'
                text_area[i - 1], text_area[i] = '', ''
            if text_area[i] == '^':
                text_area[i + 1] = str(float(text_area[i - 1]) ** float(text_area[i + 1]))
                text_area[i - 1], text_area[i] = '', ''
            if text_area[i] == '%':
                try:
                    text_area[i + 1] = str(float(text_area[i - 1]) % float(text_area[i + 1]))
                except ZeroDivisionError:
                    text_area[i + 1] = 'На ноль делить нельзя'
                text_area[i - 1], text_area[i] = '', ''

        while '' in text_area:
            text_area.remove('')

        for i in range(len(text_area)):
            if text_area[i] == '+':
                text_area[i + 1] = str(float(text_area[i - 1]) + float(text_area[i + 1]))
                text_area[i - 1], text_area[i] = '', ''
            if text_area[i] == '-':
                text_area[i + 1] = str(float(text_area[i - 1]) - float(text_area[i + 1]))
                text_area[i - 1], text_area[i] = '', ''
        for i in range(len(text_area)):
            if text_area[i] == '->':
                try:
                    text_area[i + 1] = str(self.convert(int(text_area[i - 1]), int(text_area[i + 1])))
                except Exception:
                    text_area[i + 1] = 'Только целые числа'
                text_area[i - 1], text_area[i] = '', ''

        for i in text_area:
            if i != '':
                self.output.setText(i)
                self.input_area = i

    def clear_text_area(self):
        """
        Просто удаляем всё поле вывода
        :return:
        """
        self.input_area = ''
        self.output.setText(self.input_area)

    def clear_one_element(self, text_area):
        """
        Удаление элементов посимвольно.
        Если встречается оператор, удаляется весь оператор вместе с пробелами, иначе удаляется один символ
        :param text_area: значение поля вывода
        :return:
        """
        if text_area == '':
            return 0
        temp = text_area.split()
        if temp[-1] in self.strip_operators or temp[-1].startswith('-'):
            text_area = " ".join(temp[:-1])  # таким макаром я удалял поэлементно
        else:
            text_area = ''.join(text_area[:-1])  # сейчас посимвольно
        self.input_area = text_area
        self.output.setText(self.input_area)

    def convert(self, number, gen):
        """
        Перевод числа a в N-ую СС, где N (- [2,16]. Если type(a) - float, то возникает ошибка.
        :param number: число a
        :param gen: N-ая СС
        :return: число в N-ой СС
        """

        if gen == 1:
            return 0

        alphabet = 'ABCDEF'
        temp = int(number)
        result = ''
        while temp > 0:
            if temp % int(gen) > 9:
                result += alphabet[(temp % int(gen)) - 10]
            else:
                result += str(temp % int(gen))
            temp //= int(gen)
        return result[::-1]


if __name__ == "__main__":
    import sys

    app = ui.QtWidgets.QApplication(sys.argv)
    MainWindow = ui.QtWidgets.QMainWindow()
    ui = Calculator()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
