from openpyxl.chart import (
    LineChart,
    Reference,
    RadarChart,
    BarChart,
)
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, Font
from openpyxl.chart.label import DataLabelList

import refactoring.edu.util.excel_util as excel_util

cpLegend = CharacterProperties(sz=500, b=False)
cpAxisTitle = CharacterProperties(sz=600, b=True)
cpAxisText = CharacterProperties(sz=500, b=False)
cpTitle = CharacterProperties(sz=1000, b=True)
cpDataLabel = CharacterProperties(sz=500, b=True)

lineWidth = 12658 * 1.5
chartHeight = 7.14
chartWidth = 10.64


# 给折线图加上三角形 和 控制线的粗细
def lineChartStyle(chart, isMark, isLineWidth):
    if isMark:
        for series in chart.series:
            series.marker.symbol = "triangle"
            if isLineWidth:
                series.graphicalProperties.line.width = lineWidth
                series.marker.size = 3


# 不让雷达图的线从最低开始
def radarLineLocation(chart, rows, min_row, min_col):
    if len(rows) != 0:
        min = 50
        max = -1
        # print(rows)
        for row in rows[min_row:]:
            for col in row[min_col:]:
                if col is None:
                    continue
                if col > max:
                    max = col
                if col < min:
                    min = col

        min -= 1
        max += 1
        # print(min, max)

        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = False


# 设置图标上各种字体的大小
def setChartFontSize(chart, isDataLabel):
    chart.title.tx.rich.p[0].r.rPr = cpTitle
    chart.x_axis.title.tx.rich.p[0].r.rPr = cpAxisTitle
    chart.y_axis.title.tx.rich.p[0].r.rPr = cpAxisTitle
    chart.x_axis.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cpAxisText), endParaRPr=cpAxisText)])
    chart.y_axis.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cpAxisText), endParaRPr=cpAxisText)])
    chart.legend.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cpLegend), endParaRPr=cpLegend)])

    if isDataLabel:
        chart.dataLabels = DataLabelList()
        chart.dataLabels.txPr = RichText(
            p=[Paragraph(pPr=ParagraphProperties(defRPr=cpDataLabel), endParaRPr=cpDataLabel)])
        chart.dataLabels.showVal = True


# 设置图表上各种标题 titles=[title, xAxisTitle, yAxisTitle]
def setChartTitleAndSize(chart, titles):
    chart.title = titles[0]
    chart.x_axis.title = titles[1]
    chart.y_axis.title = titles[2]
    chart.height = chartHeight
    chart.width = chartWidth


# 图表显示的顺序是倒叙
def setChartDesc(chart):
    chart.y_axis.scaling.orientation = "maxMin"
    chart.x_axis.crosses = "max"


# 图表 设置各种东西 是否倒叙、是否加点线、线是否细一点
def setChartByParameter(chart, isDesc, isMark, isLineWidth, isDataLable):
    if isinstance(chart, LineChart) or isinstance(chart, RadarChart):
        lineChartStyle(chart, isMark, isLineWidth)

    if isDesc:
        setChartDesc(chart)

    setChartFontSize(chart, isDataLable)
    return chart


# 根据字符串创建对应的图表
def createChartByType(type):
    if type == "bar":
        chart = BarChart()
    elif type == "line":
        chart = LineChart()
    elif type == "radar":
        chart = RadarChart()
    return chart


# 以行添加数据还是以列添加数据
def addChartDataBtType(ws, type, chart, max_row, max_col, min_row, min_col):
    if type == "row":
        labels = Reference(ws, min_row=min_row, min_col=min_col + 1, max_col=max_col)
        data = Reference(ws, min_row=min_row + 1, max_row=max_row, min_col=min_col, max_col=max_col)
        from_rows = True

    elif type == "col":
        labels = Reference(ws, min_col=min_col, min_row=min_row + 1, max_row=max_row)
        data = Reference(ws, min_col=min_col + 1, max_col=max_col, min_row=min_row, max_row=max_row)
        from_rows = False

    chart.add_data(data, titles_from_data=True, from_rows=from_rows)
    chart.set_categories(labels)


# 一个坐标轴（柱状图/折线图/雷达图）
def createChart(wb, chartType, readType, rows, titles,
                place="C10",
                max_row=-1, max_col=-1,
                min_row=1, min_col=1,
                isDesc=False, isMark=True, isLineWidth=True, isDataLable=True):
    ws = excel_util.creatSheet(wb, False, titles[0])
    excel_util.putRowsToSheet(rows, ws)

    chart = createChartByType(chartType)

    if max_row == -1:
        max_row = len(rows)

    if max_col == -1:
        max_col = len(rows[0])

    addChartDataBtType(ws, readType, chart, max_row, max_col, min_row, min_col)

    setChartTitleAndSize(chart, titles)

    setChartByParameter(chart, isDesc, isMark, isLineWidth, isDataLable)

    if isinstance(chart, RadarChart):
        radarLineLocation(chart, rows, min_row, min_col)
    ws.add_chart(chart, place)


# 两个坐标轴，左柱右折
# 左分数 右排名
# 排名降序
def createTwoAxisChart(wb, readType, rows, titles, lineNumber,
                       place="C10",
                       max_row=-1, max_col=-1,
                       min_row=1, min_col=1,
                       isDesc=True, isMark=True, isLineWidth=True, isDataLable=True):
    ws = excel_util.creatSheet(wb, False, titles[0])
    excel_util.putRowsToSheet(rows, ws)

    if max_row == -1:
        max_row = len(rows)

    if max_col == -1:
        max_col = len(rows[0])

    c1 = LineChart()
    c2 = BarChart()

    if readType == "row":
        addChartDataBtType(ws, readType, c2, max_row, max_col, lineNumber, min_col)
        addChartDataBtType(ws, readType, c1, lineNumber, max_col, min_row, min_col)
    elif readType == "col":
        addChartDataBtType(ws, readType, c2, max_row, max_col, min_row, lineNumber)
        addChartDataBtType(ws, readType, c1, max_row, lineNumber, min_row, min_col)

    c1.y_axis.axId = 200
    c1.y_axis.crosses = "max"
    c1 += c2

    c2.y_axis.title = titles[3]
    c2.y_axis.title.tx.rich.p[0].r.rPr = cpAxisTitle
    c2.y_axis.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cpAxisText), endParaRPr=cpAxisText)])
    c2.dataLabels = DataLabelList()
    c2.dataLabels.txPr = RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cpDataLabel), endParaRPr=cpDataLabel)])
    c2.dataLabels.showVal = True

    setChartTitleAndSize(c1, titles)
    setChartByParameter(c1, isDesc, isMark, isLineWidth, isDataLable)

    # 逆序
    if isDesc:
        c1.y_axis.scaling.orientation = "maxMin"
        c1.x_axis.crosses = "min"
    ws.add_chart(c1, place)


if __name__ == '__main__':
    # rows = [
    #     ['考试', '排名', '区平均分', '同类平均分'],
    #     ['初中预备', 32, 80.28, 80.28, ],
    #     ['初一期末', 32, 79.04, 79.04, ],
    #     ['初二期末', 32, 74.32, 79.04, ],
    #     ['初三期末', 32, 105.88, 79.04, ],
    # ]

    wb = excel_util.createExcel()
    readType = 'row'
    rows = [
        ['考试', '初中预备', '初一期末', '初二期末', '初三期末', ],
        ['排名', 32, 30, 30, 27, ],
        ['区平均分', 80.28, 79.04, 74.32, 105.88, ],
        ['同类平均分', 81.28, 72.04, 73.32, 104.88, ],
    ]
    titles = ['语文分数和排名', '学校', '排名', '分数']
    lineNumber = 2
    createTwoAxisChart(wb, readType, rows, titles, lineNumber)
    wb.save("test.xlsx")
