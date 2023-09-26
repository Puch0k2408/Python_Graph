from math import sin, cos, tan, acos, asin, atan, log, pi, fabs

''' Калькулирование '''

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

def calculate_root(x, number):
    if x >= 0:
        return x ** (1 / number)
    elif number & 1:
        return -(-x) ** (1 / number)
    elif x == 1:
        return x
    else:
        return None

def logarithm(base):
    x = getNode()
    return log(x, base)


def setNode(node):
    currentNode.append(node)


def getOperation():
    if currentNode:
        return currentNode.pop(0)
    else:
        if arr:
            return arr.pop(0)
        else:
            return None


def calcPlusMinus():
    left = calcDivMult()

    if left is None:  # Изменено условие проверки
        return 0

    operation = getOperation()
    while True:
        if operation == '^':
            right = calcdegree()
            if left >= 0:
                left **= right
            elif left == -1 and right % 2 == 0:
                left = left * (-1)
            elif left < 0 and right % 2 == 0:
                left = left ** right
            elif (left < 0) and left != -1:
                left = -((-left) ** (right))
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

def calc(expression):
    global arr
    global currentNode
    currentNode.clear()
    arr = formatExpression(expression)
    return calcPlusMinus()

print(calc('(-3)^(3)'))

print(calc('sqrt(25, 2)'))


