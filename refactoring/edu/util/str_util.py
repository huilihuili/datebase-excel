def underline_name(name):
    result = ""
    for s in name:
        if s.isupper():
            result += ("_" + s.lower())
        else:
            result += s
    return result


def change_fields(fields):
    for i in range(len(fields)):
        fields[i] = underline_name(fields[i])


def list_to_str(lista, symbol=",", left_symbol="", right_symbol=""):
    if not isinstance(lista, list):
        return lista

    if len(lista) < 1:
        return ""

    result = "%s%s%s" % (left_symbol, str(lista[0]), right_symbol)
    for item in lista[1:]:
        result += ("%s %s%s%s" % (symbol, left_symbol, str(item), right_symbol))
    return result
