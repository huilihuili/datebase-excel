import mysql.connector

import refactoring.edu.util.str_util as str_util
import refactoring.edu.util.object_util as object_util

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_PORT = '3306'
MYSQL_DB = 'refactoring_edu'
CHATSET = 'utf8mb4'
COLLATION = 'utf8mb4_general_ci'
cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)


def update(sql):
    # print("update--->" + sql)
    cur.execute(sql)
    cnx.commit()


def select(sql):
    # print("select--->" + sql)
    cur.execute(sql)
    return cur.fetchall()


def select_one_cell(sql):
    return select(sql)[0][0]


def select_one_row(sql):
    return select(sql)[0]


def get_fields(sql):
    cur.execute(sql)
    fields = []
    for field_desc in cur.description:
        fields.append(field_desc[0])
    return fields


def select_with_object(sql, o):
    fields = get_fields(sql)
    str_util.change_fields(fields)
    values = select(sql)

    if not object_util.has_attr(o, fields):
        return []

    object_results = object_util.get_objects_with_fields_and_values(o, fields, values)
    return object_results if len(object_results) > 1 else object_results[0]


if __name__ == '__main__':
    print([4] * 2)
    a = 1
    b = 2
    h = ""
    h = a - b if a > b else a + b
    print(h)
