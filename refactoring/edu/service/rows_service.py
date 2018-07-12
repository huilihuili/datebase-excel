import refactoring.edu.domain.qa as qa


def table_of_dimen_sum(item, table, exam_where, varied_where, ids, subject_ids=None):
    if subject_ids is None:
        cell = qa.Cell(item, table, [varied_where, exam_where])
    else:
        cell = qa.CellWithOrders(item, table, [varied_where, exam_where], "subjectId", subject_ids)
    if cell is None:
        return []
    else:
        return qa.ColSeriesCell(cell, ids).get_values()
