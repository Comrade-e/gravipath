import random
import time
from math import gcd
import matplotlib.pyplot as plt
class Node(): # инициализация класса нод
    def __init__(self, depth):
        self.depth = depth
def adjacent(matrix, node): #возвращает словарь смежных с нодой в ключе нод
    return dict(zip([str(x) for x in range(len(matrix[int(node)])) if matrix[int(node)][x] != 0 and matrix[int(node)][x] != float('inf')], [el for el in matrix[int(node)] if el != 0 and el != float('inf')]))
def gravity(matrix, start): # нахожение кратчайшего пути физическим алгоритмом
    nodes = {}
    fixed = set()
    result = {}
    for key in range(len(matrix)): # генератор нод: изначально все ноды находятся на глубине 0
        nodes[str(key)] = Node(0)
    all_edges = []
    for x in nodes.keys():
        all_edges.extend(adjacent(matrix, x).values()) #вычисление всех рёбер для нахожения шага
    fixed.add(start) # начальная нода вносится в множество закреплённых нод
    while len(fixed) < len(nodes.keys()):
        for node in nodes.keys():
            if node not in fixed: # итерация каждой ноды в сгенерированном словаре
                nodes[node].depth += gcd(*all_edges) # каждая нода, не являющаяся закреплённой, перемещается в глубину со скоростью, равной наибольшему общему делителю всех рёбер
                if any([nodes[node].depth - nodes[key].depth == dist for key, dist in adjacent(matrix, node).items() if key in fixed]): # если хотя бы одна "нить натянута", т.е расстояние от рассматриваемого узла до каждого узла в графе равно соответствующему ребру
                    fixed.add(node) # точка фиксируется и больше не двигается
    for el in nodes.keys():
        result[el] = nodes[el].depth
    return result

def dijkstra(graph, start): #алгоритм Дейкстры
    # Инициализация расстояний до всех вершин как бесконечность
    distances = [float('inf')] * len(graph)
    # Расстояние до начальной вершины равно 0
    distances[start] = 0

    # Множество посещенных вершин
    visited = set()

    # Цикл по всем вершинам
    while len(visited) < len(graph):
        # Найти вершину с наименьшим расстоянием
        min_distance = float('inf')
        min_vertex = -1
        for v in range(len(graph)):
            if v not in visited and distances[v] < min_distance:
                min_distance = distances[v]
                min_vertex = v

        # Посетить найденную вершину
        visited.add(min_vertex)

        # Обновить расстояния до смежных вершин
        for v in range(len(graph)):
            if graph[min_vertex][v] != float('inf') and v not in visited:
                new_distance = distances[min_vertex] + graph[min_vertex][v]
                if new_distance < distances[v]:
                    distances[v] = new_distance

    return distances
def generate_random_graph(nodes, minedgeweight, maxedgeweight): #генератор случайных графов
    matrix = [[None for i in range(nodes)] for j in range(nodes)]
    for y in range(nodes):
        for x in range(nodes):
            if y < x:
                if any(map(lambda el: el != float('inf') and el != 0 and el != None, matrix[y])):
                    matrix[y][x] = random.randint(minedgeweight, maxedgeweight) if random.randint(0, 2) == 1 else float('inf')
                else:
                    matrix[y][x] = random.randint(minedgeweight, maxedgeweight)
            else:
                matrix[y][x] = 0
    for y in range(nodes):
        for x in range(nodes):
            matrix[x][y] = matrix[y][x]
    return matrix
def mul_all_edges(matrix): #умножить все веса рёбер в графе на 10
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] *= 10
    return matrix

c = int(input())
if c == 1: #эксперимент 1 (см.тезисы)
    graph_to_solve = generate_random_graph(10, 1, 10)
    target_node = random.randint(1, 10)
    dijkstra_solve = dijkstra(graph_to_solve, 0)[target_node]
    gravity_solve = gravity(graph_to_solve, '0')[str(target_node)]
    print(dijkstra_solve)
    print(gravity_solve)
    print(dijkstra_solve == gravity_solve) # True всегда
if c == 2: #эксперимент 2 (см. тезисы)
    timelist_gravity = {}
    timelist_dijkstra = {}
    for v in range(2, 200):
        gr = generate_random_graph(v, 5, 10)
        target = random.randint(0, v - 1)
        print(v)
        start_grav = time.time()
        print(gravity(gr, '0', str(target)))
        end_grav = time.time()
        timelist_gravity[v] = (end_grav - start_grav)
        start_dij = time.time()
        print(dijkstra(gr, 0)[target])
        end_dij = time.time()
        timelist_dijkstra[v] = (end_dij - start_dij)
    x = list(range(198))
    yg = timelist_gravity.values()
    yd = timelist_dijkstra.values()
    plt.plot(x, yd)
    plt.show()
    plt.plot(x, yg, '-', x, yd, '-.')
    plt.show()
elif c == 3: #эксперимент 3 (см.тезисы)
    timelist = {}
    mul_timelist = {}
    for v in range(2, 150):
        gr = generate_random_graph(v, 5, 10)
        target = random.randint(0, v - 1)
        print(v)
        start_time = time.time()
        print(gravity(gr, '0', str(target)))
        end_time = time.time()
        timelist[v] = (end_time - start_time)
        start_time_mul = time.time()
        print(gravity(mul_all_edges(gr), '0', str(target)))
        end_time_mul = time.time()
        mul_timelist[v] = (end_time_mul - start_time_mul)
    x = list(range(148))
    yn = timelist.values()
    ym = mul_timelist.values()
    plt.plot(x, yn, '-', x, ym, '-.')
    plt.show()


