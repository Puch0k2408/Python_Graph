from math import sin, cos, tan, acos, asin, atan, log, pi, fabs

''' Калькулирование '''


# todo: Данный код определяет функцию formatExpression, которая принимает на вход строку expression
#  и возвращает список, содержащий элементы этой строки.
def formatExpression(expression):
    tmp = ''
    a = []
    for x in expression:
        if x in '()+-*/^|,':
            if len(tmp) != 0:
                a.append(tmp)
                tmp = ''
            a.append(x)
        elif x == ' ':
            continue
        elif x == 'P':
            a.append(str(round(pi, 5)))
        else:
            tmp += x
    if len(tmp) != 0:
        a.append(tmp)
    return a


y_f = []
base = 0
currentNode = []
arr = []


# todo: Используется для получения каждого операнда в выражении для последующих вычислений
def getNode():
    if currentNode:
        return currentNode.pop(0)

    if not arr:
        return None

    x = arr.pop(0)
    if x in '^':
        x = calcdegree()
        getNode()
        return x
    elif x in '+':
        y = getNode()
        return y
    elif x in '-':
        y = getNode()
        return -y
    elif x == 'sin':
        y = getNode()
        return sin(y)
    elif x == 'cos':
        y = getNode()
        return cos(y)
    elif x == 'tan':
        y = getNode()
        return tan(y)
    elif x == 'ctan':
        y = getNode()
        return 1 / tan(y)
    elif x == 'acos':
        y = getNode()
        return acos(y)
    elif x == 'asin':
        y = getNode()
        return asin(y)
    elif x == 'atan':
        y = getNode()
        return atan(y)
    elif x == 'sqrt':
        x = getNode()
        number = getNode()
        return calculate_root(x, number)
    elif x == 'log':
        base = getNode()
        return logarithm(base)
    elif x == '|':
        x = calcPlusMinus()
        getNode()
        return fabs(x)
    elif x in '(':
        x = calcPlusMinus()
        getNode()
        return x
    else:
        if 'e' in x:
            x += '-1'
        return float(x)


# Считает корень
def calculate_root(x, number):
    if number % 2 == 0 and x < 0:
        return None
    else:
        if x >= 0:
            return x ** (1 / number)
        elif number & 1:
            return -(-x) ** (1 / number)
        elif x == 1:
            return x
        else:
            return None


# Считает логарифм
def logarithm(base):
    x = getNode()
    return log(x, base)


# Выполняет сложение, вычитание и возведение в степень в выражении
def calcPlusMinus():
    left = calcDivMult()

    if left is None:
        return 0

    operation = getOperation()
    while True:
        if operation == '^':
            right = calcdegree()
            if left >= 0:
                left = left ** right
            if left < 0:
                if left == (-1) and right % 2 == 0:
                    left = left * (-1)
                elif left == (-1) and right % 2 != 0:
                    left = left
                elif right % 2 == 0:
                    left = ((-left) ** right)
                elif right % 2 != 0:
                    left = -((-left) ** right)
                else:
                    return None

        if operation == '-':
            right = calcDivMult()
            left -= right
        elif operation == '+':
            right = calcDivMult()
            left += right
        else:
            setNode(operation)
            return left
        operation = getOperation()


# Выполнение выполняет умножение и деление в выражении
def calcDivMult():
    left = getNode()
    if not left:
        return 0

    operation = getOperation()
    while True:
        if operation == '*':
            right = getNode()
            left *= right
        elif operation == '/':
            right = getNode()
            left /= right
        else:
            setNode(operation)
            return left

        operation = getOperation()


# Вычисление степени в выражении
def calcdegree():
    left = getNode()
    if not left:
        return 0

    operation = getOperation()
    while True:
        if operation == '^':
            right = getNode()
            left = left ** right
        else:
            setNode(operation)
            return left

        operation = getOperation()


# todo: Используется для сохранения операции, которая была получена из функции getNode(), чтобы она могла быть
#  использована позже в вычислениях
def setNode(node):
    currentNode.append(node)


# todo: Получает следующую операцию в выражении
def getOperation():
    if currentNode:
        return currentNode.pop(0)
    else:
        if arr:
            return arr.pop(0)
        else:
            return None


# todo: Функция принимает выражение в качестве параметра expression, форматирует выражение с помощью функции,
#  formatExpression() и затем возвращает результат вычисления, вызывая функцию calcPlusMinus()*
def calc(expression):
    global arr
    global currentNode
    currentNode.clear()
    arr = formatExpression(expression)
    return calcPlusMinus()
