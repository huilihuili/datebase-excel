import refactoring.edu.dao.base_dao as base_dao
import refactoring.edu.util.str_util as str_util
import refactoring.edu.util.list_util as list_util


class Where(object):
    def __init__(self, name, value='', symbol="="):
        self.name = name
        self.value = value
        self.symbol = symbol

    def get_where_item(self):
        result = "%s %s " % (self.name, self.symbol)
        return result + ("'%s'" % self.value if isinstance(self.value, str) else str(self.value))

    def set_value(self, value):
        self.value = value

    def add(self, other):
        return str(self) + str(other)

    def __repr__(self):
        return self.get_where_item()

    def __str__(self):
        return self.get_where_item()

    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.add(other)


class Cell(object):
    def __init__(self, select_name, table_name, where_list):
        self.select_name = select_name
        self.table_name = table_name
        self.where_list = where_list

    def get_select_name(self):
        return str_util.list_to_str(self.select_name)

    def get_table_name(self):
        return str_util.list_to_str(self.table_name)

    def get_where_list(self):
        return str_util.list_to_str(list_util.to_a_list(self.where_list), symbol=" AND")

    @staticmethod
    def set_where_value_static(where, value):
        if isinstance(where, list):
            for i, w in enumerate(where):
                w.set_value(value[i])
        else:
            where.set_value(value)

    def set_where_value(self, index, value):
        Cell.set_where_value_static(self.where_list[index], value)

    def get_sql(self):
        sql = """
                 SELECT %s
                 FROM %s
                 WHERE %s
             """ % (self.get_select_name(), self.get_table_name(), self.get_where_list())
        return sql

    def get_row_values(self):
        return list_util.to_a_list(base_dao.select(self.get_sql()))

    def get_value(self):
        return base_dao.select_one_cell(self.get_sql())


class CellWithOrders(Cell):
    def __init__(self, select_name, table_name, where_list, field, orders):
        super(CellWithOrders, self).__init__(select_name, table_name, where_list)
        self.field = field
        self.orders = orders

    def get_sql(self):
        orders_str = str_util.list_to_str(self.orders, left_symbol="'", right_symbol="'")
        sql = "%s and %s in (%s) order by Field(%s, %s)" \
              % (super(CellWithOrders, self).get_sql(), self.field, orders_str, self.field, orders_str)
        return sql


class SeriesCell(object):
    def __init__(self, cell, ids, index):
        self.cell = cell
        self.xids = ids
        self.index = index

    def get_values(self):
        return []


# [[]]
class RowSeriesCell(SeriesCell):
    def __init__(self, cell, ids, index=0):
        super(RowSeriesCell, self).__init__(cell, ids, index)

    def get_values(self):
        result = []
        for xid in self.xids:
            self.cell.set_where_value(self.index, xid)
            result.extend(self.cell.get_row_values())
        return result


# [[], [], [], ...]
class ColSeriesCell(SeriesCell):
    def __init__(self, cell, ids):
        super(ColSeriesCell, self).__init__(cell, ids, 0)

    def get_values(self):
        result = []
        for xid in self.xids:
            self.cell.set_where_value(self.index, xid)
            result.append(self.cell.get_row_values())
        return result


# [[], [], [], ...]
class BlockSeriesCell(RowSeriesCell):
    def __init__(self, cell, xids, yids):
        super(BlockSeriesCell, self).__init__(cell, yids, index=1)
        self.yids = xids

    def get_values(self):
        result = []
        for yid in self.yids:
            self.cell.set_where_value(0, yid)
            result.append(super(BlockSeriesCell, self).get_values())
        return result


class DataRows(object):
    @staticmethod
    def rows_to_list(rows):
        result = []
        for row in rows:
            result.append(row.get_values())
        return result

    @staticmethod
    def combine_col_rows(*rows):
        return list_util.combine_values_by_col(*DataRows.rows_to_list(rows))

    @staticmethod
    def combine_row_rows(*rows):
        return list_util.combine_values_by_row(*DataRows.rows_to_list(rows))

    @staticmethod
    def get_values(*data_rows):
        result = []
        for rows in data_rows:
            if isinstance(rows, list):
                result.extend(DataRows.combine_col_rows(*rows))
            else:
                result.extend(rows.get_values())
        return result


class TableRows(object):
    def __init__(self, first_row, first_col, *data_rows):
        self.first_row = first_row
        self.first_col = first_col
        self.data_rows = data_rows

    def get_values(self):
        self.first_row = list_util.to_a_list(self.first_row)
        result = [self.first_row]
        if isinstance(self.first_col[0], list):
            result.extend(list_util.combine_values_by_col(self.first_col, DataRows.get_values(*self.data_rows)))
        else:
            for index, data_row in enumerate(DataRows.get_values(*self.data_rows)):
                data_row.insert(0, self.first_col[index])
                result.append(data_row)
        return result


if __name__ == '__main__':
    exam_where = Where('examId', '8c4646637f44489c9ba9333e580fe9d0')
    subject_where = Where('subjectId', 121)
    district_where = Where('districtId', '9')

    cellt = Cell(["avg", "num_nz"], "qa_district_dimen", [exam_where, subject_where, subject_where])
    print(cellt.get_value())
