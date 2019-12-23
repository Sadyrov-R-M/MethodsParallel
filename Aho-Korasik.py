# -*- coding: utf-8 -*-
# пример реализации (написан на Python 2.x) взят с https://clck.ru/LNrJ7

from threading import Thread

class AhoNode:
    # Вспомогательный класс для построения дерева
    def __init__(self):
        self.goto = {}
        self.out = []
        self.fail = None


def aho_create_forest(patterns):
    # Создать бор - дерево паттернов
    root = AhoNode()

    for path in patterns:
        node = root
        for symbol in path:
            node = node.goto.setdefault(symbol, AhoNode())
        node.out.append(path)
    return root


def aho_create_statemachine(patterns):
    # Создать автомат Ахо-Корасика.
    # Фактически создает бор и инициализирует fail-функции всех узлов, обходя дерево в ширину.
    
    # Создаем бор, инициализируем непосредственных потомков корневого узла

    global root
    
    root = aho_create_forest(patterns)
    queue = []
    for node in root.goto.values():
        queue.append(node)
        node.fail = root

    # Инициализируем остальные узлы:
    # 1. Берем очередной узел (важно, что проход в ширину)
    # 2. Находим самую длинную суффиксную ссылку для этой вершины - это и будет fail-функция
    # 3. Если таковой не нашлось - устанавливаем fail-функцию в корневой узел
    while len(queue) > 0:
        rnode = queue.pop(0)

        for key, unode in rnode.goto.items():
            queue.append(unode)
            fnode = rnode.fail
            while fnode is not None and key not in fnode.goto:
                fnode = fnode.fail
            unode.fail = fnode.goto[key] if fnode else root
            unode.out += unode.fail.out


def aho_find_all(s, root, callback):
    # Находит все возможные подстроки из набора паттернов в строке.
    node = root

    for i in range(len(s)):
        while node is not None and s[i] not in node.goto:
            node = node.fail
        if node is None:
            node = root
            continue
        node = node.goto[s[i]]
        for pattern in node.out:
            callback(i - len(pattern) + 1, pattern)


############################
# Демонстрация работы алгоритма
def on_occurence(pos, patterns):
    print("На позиции %s найдено слово: %s" % (pos, patterns))


patterns = (input("Введите искомые слова через пробел: ")).lower().split()

thread = Thread(target = aho_create_statemachine, args = [patterns])
thread.start()

s = (input("Введите текст: ")).lower()
thread.join()

aho_find_all(s, root, on_occurence)
