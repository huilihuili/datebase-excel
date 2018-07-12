from itertools import chain


def append_value(lista, value):
    if isinstance(value, list) or isinstance(value, tuple):
        lista.extend(value)
    else:
        lista.append(value)


def to_a_list(arg):
    result = []
    for a in arg:
        append_value(result, a)
    return result


def combine_values_by_col(*rows):
    result = []
    for xindex in range(len(rows[0])):
        row = []
        for yindex in range(len(rows)):
            append_value(row, rows[yindex][xindex])
        result.append(row)
    return result


def combine_values_by_row(*rows):
    result = []
    for row in rows:
        if isinstance(row[0], list):
            result.extend(row)
        else:
            result.append(row)
    return result


def add_something_to_list(something, lista):
    result = []
    for t in lista:
        t += str(something)
        result.append(t)
    return result


def cross_one_row(lista, listb):
    return list(chain(*zip(lista, listb)))


def cross_several_row(lista, listb):
    result = []
    for index in range(len(lista)):
        result.append(cross_one_row(lista[index], listb[index]))
    return result


if __name__ == '__main__':
    types = ["1", "32", "4"]
    types = add_something_to_list("tem", types)
    print(types)

    a = [0, 1, 2, 3, 4]
    b = [0, 1, 2, 3, 4]
    c = [''] * 5
    print(cross_one_row(a, b))
    print(cross_one_row(a, c))

    a = [[1, 2, 3], [4, 5, 6]]
    b = [[1, 2, 3], [4, 5, 6]]
    c = [[''] * 3] * 2
    print(cross_several_row(a, b))
    print(cross_several_row(a, c))

    a = [0, 1, 2, 3, 4]
    b = [0, 1, 2, 3, 4]
    print(combine_values_by_col(a, b))
    print(to_a_list([a, b]))