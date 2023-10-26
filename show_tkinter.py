import tkinter as tk
from Calc_f2 import calc
import tkinter.messagebox as msgbox
import math

# Определение размеров окна и других констант
WIN_H = 900
WIN_W = 1200
PANEL_H = WIN_H  # Высота панели
PANEL_W = 200  # Ширина панели
CANVAS_H = WIN_H  # Высота холста для рисования графика
CANVAS_W = WIN_W  # Ширина холста для рисования графика

win = tk.Tk()  # Создание основного окна приложения
win.title('График')  # Установка заголовка окна
win.config(width=WIN_W, height=WIN_H)  # Установка размеров окна
win.resizable(False, False)  # Запрет изменения размеров окна

panel = tk.Frame(win, bd=4, relief=tk.GROOVE)  # Создание панели элементов управления
panel.place(x=-2, y=0, width=CANVAS_W + 10, height=100)  # Установка позиции и размеров панели

canvas = tk.Canvas(win, width=CANVAS_W, height=CANVAS_H, bg='#012')  # Создание холста для рисования графика
canvas.place(x=-5, y=100, width=CANVAS_W + 10, height=CANVAS_W)  # Установка позиции и размеров холста

x_left, x_right = -10, 10  # Установка начальных значений для пределов по x
y_bottom, y_top = -10, 10  # Установка начальных значений для пределов по y

ol = False


def draw_axis(x_left, x_right, y_bottom, y_top):
    # Цена одного пиксела экрана
    dx = CANVAS_W / (x_right - x_left)
    dy = CANVAS_H / (y_top - y_bottom)
    # Центр координат
    cx = -x_left / (x_right - x_left) * CANVAS_W
    cy = y_top / (y_top - y_bottom) * CANVAS_H
    # Линии осей координат на нулях
    canvas.create_line(0, cy, CANVAS_W, cy, fill='white', width=2)
    canvas.create_line(cx, 0, cx, CANVAS_H, fill='white', width=2)
    # Простроение отрезков на осях координат, которые обозначают ед. отрезки
    x_step = (x_right - x_left) / 20
    x = x_left + x_step
    while x < x_right:
        if x != 0:
            x_canvas = (x - x_left) * dx
            if x_canvas != 0:
                canvas.create_line(x_canvas, 0, x_canvas, CANVAS_H, fill='#444',
                                   dash=(1, 2))  # Используем dash для пунктирной линии
            canvas.create_line(x_canvas, cy - 3, x_canvas, cy + 3, fill='white')
            canvas.create_text(x_canvas, cy + 15, text=str(round(x, 1)), font='Verdana 9', fill='white')
        x += x_step
    y_step = (y_top - y_bottom) / 20
    y = y_top
    while y >= y_bottom:
        y_canvas = (y - y_top) * dy
        if y != 0:
            if y_canvas != 0:
                canvas.create_line(0, -y_canvas, CANVAS_W, -y_canvas, fill='#444',
                                   dash=(1, 2))  # Используем dash для пунктирной линии
            canvas.create_line(cx - 3, -y_canvas, cx + 3, -y_canvas, fill='white')
            canvas.create_text(cx + 25, -y_canvas - 10, text=str(round(y, 1)), font='Verdana 9', fill='white')
        else:
            canvas.create_line(0, -y_canvas, CANVAS_W, -y_canvas, fill='#444',
                               dash=(1, 2))  # Используем dash для пунктирной линии
            canvas.create_line(cx - 3, -y_canvas, cx + 3, -y_canvas, fill='white')
            canvas.create_text(cx + 25, -y_canvas - 10, text=str(round(y, 1)), font='Verdana 9', fill='white')
        y -= y_step

    return dx, dy


def frange(begin, end, step):  # Создание списка точек на оси x
    x = begin
    t = []
    while x <= end:
        if not any(char.isalpha() for char in str(x)):  # Проверяет есть ли буквы в точках
            t.append(x)
        x += step
    return t


def points_generator(x_temp, expression):  # Просчитывает точки на y
    y_tmp = []
    for x in x_temp:
        y = calc(expression.replace('x', str(x)))
        # print(x,y)
        y_tmp.append(y)
    return y_tmp


def graph_dot(x_tmp, y_tmp, color, line_width=2.5):  # Рисование графика
    dot_list = []  # это список, в который будут добавляться элементы (точки и линии) графика.
    prev_x, prev_y = None, None  # переменные, которые используются для хранения предыдущих координат точек на графике.

    for x, y in zip(x_tmp,
                    y_tmp):  # Этот цикл выполняется для каждой пары координат x и y из списков x_tmp и y_tmp. Он перебирает точки графика.
        if x is None or y is None or any(c.isalpha() for c in str(y)):
            # Пропустить точку, если x, y или y содержат буквы
            prev_x, prev_y = None, None
            continue

        # Проверяем, содержит ли выражение танге

        y_rounded = round(y, 10)  # Ограничить число до 15 знаков после запятой
        y_str = "{:.15f}".format(y_rounded)  # Конвертировать в строку с ограничением в 15 символов
        y_str = y_str.rstrip('0').rstrip('.')  # Убрать нули и точку в конце

        x_canvas = (x - x_tmp[0]) * dx  # x_canvas и y_canvas - это координаты текущей точки на холсте (canvas).
        y_canvas = (y_rounded - y_top) * dy

        if prev_x is not None and prev_y is not None:
            if ol == True:
                if abs(y) - prev_y < 10:
                    prev_x, prev_y = x_canvas, y_canvas
                    continue
            # if abs(y) - prev_y < 20 :
            #     prev_x, prev_y = x_canvas, y_canvas
            #     continue

            line = canvas.create_line(prev_x, -prev_y, x_canvas, -y_canvas, fill=color,
                                      width=line_width)  # создается линия между предыдущей и текущей точкой на холсте.
            dot_list.append(
                line)  # Созданная линия добавляется в список dot_list, чтобы ее можно было в последствии удалить или обновить.

        dot = canvas.create_oval(x_canvas - 1, -(y_canvas - 1), x_canvas + 1, -(y_canvas + 1), fill=color,
                                 outline=color)  # Если нет предыдущей точки (то есть, это первая точка), то создается круглая точка (овал) на холсте в текущих координатах
        dot_list.append(dot)

        prev_x, prev_y = x_canvas, y_canvas  # Обновление предыдущих точек

    return dot_list


def initialize_graph():
    global graph, graph2, graph3, graph4, dx, dy, x_list, y_list, y_list2, y_list3, y_list4
    dx, dy = draw_axis(x_left, x_right, y_bottom, y_top)
    x_list = frange(x_left, x_right, 0.05)
    y_list = points_generator(x_list, '-1000')  # -100 для первого графика
    y_list2 = points_generator(x_list, '-1000')  # -100 для второго графика
    y_list3 = points_generator(x_list, '-1000')  # -100 для третьего графика
    y_list4 = points_generator(x_list, '-1000')  # -100 для четвертого графика
    graph = graph_dot(x_list, y_list, 'green', line_width=2)
    graph2 = graph_dot(x_list, y_list2, 'blue')  # Измените цвет или стиль линии по вашему желанию для второго графика
    graph3 = graph_dot(x_list, y_list3, 'red')  # Измените цвет или стиль линии по вашему желанию для третьего графика
    graph4 = graph_dot(x_list, y_list4,
                       'purple')  # Измените цвет или стиль линии по вашему желанию для четвертого графика


initialize_graph()  # Отображение всего при запуске программы


def graph_redraw():
    global ol
    global graph
    try:
        for item in graph:  # Проходит по точкам в графике
            canvas.delete(item)

        expression = ent.get()
        if expression == '':  # Для того, если пустое поле, то графика не будет видно
            expression = '-1000'

        if 'tan' in expression:
            for item in graph:  # Проходит по точкам в графике
                canvas.delete(item)
            ol = True
        else:
            ol = False
        if '<=' in expression or '>=' in expression or '<' in expression or '>' in expression:  # Проверка на неравенства
            inequalities = expression.split('\n')  # Разбитие
            graph = []

            for inequality in inequalities:  # Проверка на неравенство и следующий подсчет этого
                try:
                    if '<=' in inequality:
                        left, right = inequality.split('<=')
                        op = '<='
                    elif '>=' in inequality:
                        left, right = inequality.split('>=')
                        op = '>='
                    elif '<' in inequality:
                        left, right = inequality.split('<')
                        op = '<'
                    elif '>' in inequality:
                        left, right = inequality.split('>')
                        op = '>'
                    else:
                        continue  # Неизвестный оператор, пропускаем

                    if len(right) == 0:
                        right = '0'

                    y_list = []

                    for x in x_list:
                        try:
                            # Заменяем 'x' на значение x в выражении и вычисляем значения левой и правой части неравенства
                            left_val = calc(left.replace('x', str(x)))
                            right_val = calc(right.replace('x', str(x)))

                            # Проверяем, удовлетворяет ли значение левой части неравенства условию
                            if (op == '<=' and left_val <= right_val) or \
                                    (op == '>=' and left_val >= right_val) or \
                                    (op == '<' and left_val < right_val) or \
                                    (op == '>' and left_val > right_val):
                                y_list.append(left_val)
                            else:
                                y_list.append(None)
                        except:
                            y_list.append(None)

                    graph += graph_dot(x_list, y_list, 'green')
                except:
                    pass  # Пропускаем некорректные неравенства
        else:
            # Обработка уравнений
            y_list = points_generator(x_list, expression)
            graph = graph_dot(x_list, y_list, 'green')
    except Exception as e:
        msgbox.showerror("Ошибка", f"Неверное выражение!")


second_graph_value = -1000


def graph_redraw2():
    global graph2, second_graph_value
    try:
        for item in graph2:  # Проходит по точкам в графике
            canvas.delete(item)
        selected_value = selected_option.get()  # Используется для отображения графика с помощью кнопок
        if selected_value == "1":
            second_graph_value = -1000
        else:
            expression2 = ent2.get()
        expression2 = ent2.get()
        if expression2 == '':  # Для того, если пустое поле, то графика не будет видно
            expression2 = '-1000'

        if 'tan' in expression2:
            for item in graph:  # Проходит по точкам в графике
                canvas.delete(item)
            ol = True
        else:
            ol = False
        if '<=' in expression2 or '>=' in expression2 or '<' in expression2 or '>' in expression2:  # Проверка на неравенства
            inequalities2 = expression2.split('\n')
            graph2 = []

            for inequality in inequalities2:  # Проверка на неравенство и следующий подсчет этого
                try:
                    if '<=' in inequality:
                        left, right = inequality.split('<=')
                        op = '<='
                    elif '>=' in inequality:
                        left, right = inequality.split('>=')
                        op = '>='
                    elif '<' in inequality:
                        left, right = inequality.split('<')
                        op = '<'
                    elif '>' in inequality:
                        left, right = inequality.split('>')
                        op = '>'
                    else:
                        continue  # Неизвестный оператор, пропускаем

                    if len(right) == 0:
                        right = '0'

                    y_list = []

                    for x in x_list:
                        try:
                            # Заменяем 'x' на значение x в выражении и вычисляем значения левой и правой части неравенства
                            left_val = calc(left.replace('x', str(x)))
                            right_val = calc(right.replace('x', str(x)))

                            # Проверяем, удовлетворяет ли значение левой части неравенства условию
                            if (op == '<=' and left_val <= right_val) or \
                                    (op == '>=' and left_val >= right_val) or \
                                    (op == '<' and left_val < right_val) or \
                                    (op == '>' and left_val > right_val):
                                y_list.append(left_val)
                            else:
                                y_list.append(None)
                        except:
                            y_list.append(None)

                    graph2 += graph_dot(x_list, y_list, 'blue')
                except:
                    pass  # Пропускаем некорректные неравенства
        else:
            # Обработка уравнений для второго графика
            y_list2 = points_generator(x_list, expression2)
            graph2 = graph_dot(x_list, y_list2,
                               'blue')  # Измените цвет или стиль линии по вашему желанию для второго графика
    except Exception as e:
        msgbox.showerror("Ошибка", f"Неверное выражение!")


third_graph_value = -1000


def graph_redraw3():
    global graph3, third_graph_value
    try:
        for item in graph3:  # Проходит по точкам в графике
            canvas.delete(item)
        selected_value = selected_option.get()  # Используется для отображения графика с помощью кнопок
        if selected_value == '1' or selected_value == '2':
            third_graph_value = -1000
        else:
            expression3 = ent3.get()
        expression3 = ent3.get()
        if expression3 == '':  # Для того, если пустое поле, то графика не будет видно
            expression3 = '-1000'

        if 'tan' in expression3:
            for item in graph:  # Проходит по точкам в графике
                canvas.delete(item)
            ol = True
        else:
            ol = False
        if '<=' in expression3 or '>=' in expression3 or '<' in expression3 or '>' in expression3:  # Проверка на неравенства
            inequalities3 = expression3.split('\n')
            graph3 = []

            for inequality in inequalities3:  # Проверка на неравенство и следующий подсчет этого
                try:
                    if '<=' in inequality:
                        left, right = inequality.split('<=')
                        op = '<='
                    elif '>=' in inequality:
                        left, right = inequality.split('>=')
                        op = '>='
                    elif '<' in inequality:
                        left, right = inequality.split('<')
                        op = '<'
                    elif '>' in inequality:
                        left, right = inequality.split('>')
                        op = '>'
                    else:
                        continue  # Неизвестный оператор, пропускаем

                    if len(right) == 0:
                        right = '0'

                    y_list = []

                    for x in x_list:
                        try:
                            left_val = calc(left.replace('x', str(x)))
                            right_val = calc(right.replace('x', str(x)))

                            if (op == '<=' and left_val <= right_val) or \
                                    (op == '>=' and left_val >= right_val) or \
                                    (op == '<' and left_val < right_val) or \
                                    (op == '>' and left_val > right_val):
                                y_list.append(left_val)
                            else:
                                y_list.append(None)
                        except:
                            y_list.append(None)

                    graph3 += graph_dot(x_list, y_list, 'red')
                except:
                    pass  # Пропускаем некорректные неравенства
        else:
            y_list3 = points_generator(x_list, expression3)
            graph3 = graph_dot(x_list, y_list3, 'red')

    except Exception as e:
        msgbox.showerror("Ошибка", f"Неверное выражение!")


fourth_graph_value = -1000


def graph_redraw4():
    global graph4, fourth_graph_value
    try:
        for item in graph4:  # Проходит по точкам в графике
            canvas.delete(item)
        selected_value = selected_option.get()  # Используется для отображения графика с помощью кнопок
        if selected_value == '1' or selected_value == '2' or selected_value == '3':
            fourth_graph_value = -1000
        else:
            expression4 = ent4.get()
        expression4 = ent4.get()
        if expression4 == '':  # Для того, если пустое поле, то графика не будет видно
            expression4 = '-1000'

        if 'tan' in expression4:
            for item in graph:  # Проходит по точкам в графике
                canvas.delete(item)
            ol = True
        else:
            ol = False
        if '<=' in expression4 or '>=' in expression4 or '<' in expression4 or '>' in expression4:  # Проверка на неравенства
            inequalities4 = expression4.split('\n')
            graph4 = []

            for inequality in inequalities4:  # Проверка на неравенство и следующий подсчет этого
                try:
                    if '<=' in inequality:
                        left, right = inequality.split('<=')
                        op = '<='
                    elif '>=' in inequality:
                        left, right = inequality.split('>=')
                        op = '>='
                    elif '<' in inequality:
                        left, right = inequality.split('<')
                        op = '<'
                    elif '>' in inequality:
                        left, right = inequality.split('>')
                        op = '>'
                    else:
                        continue  # Неизвестный оператор, пропускаем

                    if len(right) == 0:
                        right = '0'

                    y_list = []

                    for x in x_list:
                        try:
                            left_val = calc(left.replace('x', str(x)))
                            right_val = calc(right.replace('x', str(x)))

                            if (op == '<=' and left_val <= right_val) or \
                                    (op == '>=' and left_val >= right_val) or \
                                    (op == '<' and left_val < right_val) or \
                                    (op == '>' and left_val > right_val):
                                y_list.append(left_val)
                            else:
                                y_list.append(None)
                        except:
                            y_list.append(None)

                    graph4 += graph_dot(x_list, y_list, 'purple')
                except:
                    pass  # Пропускаем некорректные неравенства
        else:
            y_list4 = points_generator(x_list, expression4)
            graph4 = graph_dot(x_list, y_list4, 'purple')

    except Exception as e:
        msgbox.showerror("Ошибка", f"Неверное выражение!")


# Функции для кнопочек перемещения
def zoom_out():  # Отдаление
    global x_left, x_right, y_bottom, y_top
    x_left -= 10
    x_right += 10
    y_bottom -= 10
    y_top += 10
    canvas.delete('all')
    initialize_graph()
    graph_redraw()
    graph_redraw2()
    graph_redraw3()
    graph_redraw4()


def zoom():  # Приближение
    global x_left, x_right, y_bottom, y_top
    if not math.fabs(x_left) + math.fabs(x_right) == 20:
        x_left += 10
        x_right -= 10
        y_bottom += 10
        y_top -= 10
        canvas.delete('all')
        initialize_graph()
        graph_redraw()
        graph_redraw2()
        graph_redraw3()
        graph_redraw4()


def move_right():  # Мувинг вправо
    global x_left, x_right
    x_left += 1
    x_right += 1
    canvas.delete('all')
    initialize_graph()
    graph_redraw()
    graph_redraw2()
    graph_redraw3()
    graph_redraw4()


def move_left():  # Мувинг влево
    global x_left, x_right
    x_left -= 1
    x_right -= 1
    canvas.delete('all')
    initialize_graph()
    graph_redraw()
    graph_redraw2()
    graph_redraw3()
    graph_redraw4()


def move_up():  # Мувинг вверх
    global y_bottom, y_top
    y_bottom += 1
    y_top += 1
    canvas.delete('all')
    initialize_graph()
    graph_redraw()
    graph_redraw2()
    graph_redraw3()
    graph_redraw4()


def move_down():  # Мувинг вниз
    global y_bottom, y_top
    y_bottom -= 1
    y_top -= 1
    canvas.delete('all')
    initialize_graph()
    graph_redraw()
    graph_redraw2()
    graph_redraw3()
    graph_redraw4()


def show_help():  # Помощь
    help_text = (
        "Добро пожаловать в программу для построения простейших графиков функций вида y=f(x)\n\n"
        "Для использования данной программы введите математическое выражение в поле ввода и нажмите 'Отобразить'.\n\n"
        "Выражение может содержать базовые операции (+, -, *, /), функции (sin, cos, tan, acos, asin, atan, sqrt, log),\n"
        "а также операцию возведения в степень (^).\n\n"
        "Примеры выражений: sin(x), x^2 + cos(x), sqrt(1 - x^2), log(10, x).\n\n"
        "В функции log(a, b) 'a' представляет собой основание логарифма, а 'b' - логарифмируемое выражение.\n\n"
        "Для приближения графика используйте кнопку '+', а для отдаления - '-'.\n\n"
        "Чтобы переместить график, используйте кнопки '←', '→', '↑' и '↓'.\n\n"
        "Приятного использования!"
    )
    msgbox.showinfo("Помощь", help_text)


lab = tk.Label(panel, text='Поле ввода:')  # Надпись
lab.place(x=-50, y=0, width=190)

ent = tk.Entry(panel, bd=2)  # Поле ввода 1
ent.place(x=100, y=0, width=145)

but1 = tk.Button(panel, text='Отобразить', command=graph_redraw)  # Кнопка Отобразить 1
but1.place(x=250, y=0, width=75, height=21)

ent2 = tk.Entry(panel, bd=2)  # Поле ввода 2
ent2.place(x=100, y=-100, width=145)

but2 = tk.Button(panel, text='Отобразить', command=graph_redraw2)  # Кнопка Отобразить 2
but2.place(x=250, y=-100, width=75, height=21)

ent3 = tk.Entry(panel, bd=2)  # Поле ввода 3
ent3.place(x=330, y=-100, width=145)

but3 = tk.Button(panel, text='Отобразить', command=graph_redraw3)  # Кнопка Отобразить 3
but3.place(x=480, y=-100, width=75, height=21)

ent4 = tk.Entry(panel, bd=2)  # Поле ввода 4
ent4.place(x=330, y=-100, width=145)

but4 = tk.Button(panel, text='Отобразить', command=graph_redraw4)  # Кнопка Отобразить 4
but4.place(x=480, y=-100, width=75, height=21)

zoom_button = tk.Button(panel, text='-', command=zoom_out, font=('Helvetica', 14))  # Кнопка уменьшения масштаба
zoom_button.place(x=1130, y=50, width=30, height=30)

zoom_out_button = tk.Button(panel, text='+', command=zoom, font=('Helvetica', 14))  # Кнопка увеличения масштаба
zoom_out_button.place(x=1130, y=20, width=30, height=30)

move_left_button = tk.Button(panel, text='←', command=move_left, font=('Helvetica', 14))  # Кнопка движения влево
move_left_button.place(x=1030, y=50, width=30, height=30)

move_right_button = tk.Button(panel, text='→', command=move_right, font=('Helvetica', 14))  # Кнопка движения вправо
move_right_button.place(x=1090, y=50, width=30, height=30)

move_up_button = tk.Button(panel, text='↑', command=move_up, font=('Helvetica', 14))  # Кнопка движения вверх
move_up_button.place(x=1060, y=20, width=30, height=30)

move_down_button = tk.Button(panel, text='↓', command=move_down, font=('Helvetica', 14))  # Кнопка движения вниз
move_down_button.place(x=1060, y=50, width=30, height=30)

help_button = tk.Button(panel, text='help', command=show_help)
help_button.place(x=0, y=70, width=35, height=20)

# Переменная для хранения выбора пользователя
selected_option = tk.StringVar()
selected_option.set("1")  # Устанавливаем первую кнопку по умолчанию


# Функция для отображения выбора пользователя
def on_option_select():
    selected_value = selected_option.get()
    if selected_value == "1":
        but2.place(x=250, y=-100, width=75, height=21)
        ent2.place(x=100, y=-100, width=145)
        but3.place(x=480, y=-100, width=75, height=21)
        ent3.place(x=330, y=-100, width=145)
        but4.place(x=480, y=-100, width=75, height=21)
        ent4.place(x=330, y=-100, width=145)
        canvas.delete('all')
        initialize_graph()
        graph_redraw()
    elif selected_value == "2":
        but2.place(x=250, y=30, width=75, height=21)
        ent2.place(x=100, y=30, width=145)
        but3.place(x=480, y=-100, width=75, height=21)
        ent3.place(x=330, y=-100, width=145)
        but4.place(x=480, y=-100, width=75, height=21)
        ent4.place(x=330, y=-100, width=145)
        canvas.delete('all')
        initialize_graph()
        graph_redraw()
        graph_redraw2()
    elif selected_value == "3":
        but2.place(x=250, y=30, width=75, height=21)
        ent2.place(x=100, y=30, width=145)
        but3.place(x=480, y=0, width=75, height=21)
        ent3.place(x=330, y=0, width=145)
        but4.place(x=480, y=-100, width=75, height=21)
        ent4.place(x=330, y=-100, width=145)
        canvas.delete('all')
        initialize_graph()
        graph_redraw()
        graph_redraw2()
        graph_redraw3()
    elif selected_value == "4":
        but2.place(x=250, y=30, width=75, height=21)
        ent2.place(x=100, y=30, width=145)
        but3.place(x=480, y=0, width=75, height=21)
        ent3.place(x=330, y=0, width=145)
        but4.place(x=480, y=30, width=75, height=21)
        ent4.place(x=330, y=30, width=145)
        canvas.delete('all')
        initialize_graph()
        graph_redraw()
        graph_redraw2()
        graph_redraw3()
        graph_redraw4()
    # Создаем "радио" кнопки


option1 = tk.Radiobutton(panel, text="1", variable=selected_option, value="1", command=on_option_select)
option1.place(x=10, y=20)
option2 = tk.Radiobutton(panel, text="2", variable=selected_option, value="2", command=on_option_select)
option2.place(x=50, y=20)
option3 = tk.Radiobutton(panel, text="3", variable=selected_option, value="3", command=on_option_select)
option3.place(x=10, y=40)
option4 = tk.Radiobutton(panel, text="4", variable=selected_option, value="4", command=on_option_select)
option4.place(x=50, y=40)

win.mainloop()
