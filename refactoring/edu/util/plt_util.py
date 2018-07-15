import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import threading

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

scatter_height = 9
scatter_width = 16

box_height = 9
box_width = 16


def setTitles(titles):
    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel(titles[2])


def pltShowAndSave(fig, isShow, path):
    if isShow:
        fig.show()
    if path != "":
        fig.savefig(path, bbox_inches='tight')


def pltLines(lines):
    if len(lines) != 0:
        for line in lines:
            type, value = line
            if type == "vline":
                plt.axvline(value, ls='--', color="r")
            elif type == "hline":
                plt.axhline(value, ls='--', color="r")


def pltText(xRows, yRows, xDif, yDif, texts, textSize):
    if len(texts) != 0:
        for i, x in enumerate(xRows):
            if textSize != 0:
                plt.text(x + xDif, yRows[i] + yDif, texts[i], ha='center', va='bottom', fontsize=textSize)
            else:
                plt.text(x + xDif, yRows[i] + yDif, texts[i], ha='center', va='bottom')


def pltAfter(fig, titles, isShow, isRotate, path, ax, lables):
    setTitles(titles)
    if lables is not None:
        if isRotate:
            ax.set_xticklabels(lables, rotation=90)
        else:
            ax.set_xticklabels(lables)
    pltShowAndSave(fig, isShow, path)
    plt.close()


def scatter(titles, xRows, yRows, path="", lines=[], points=[], isShow=False, isRotate=True, texts=[], xDif=-1,
            yDif=-1, textSize=0):
    print('画一张散点图--->%s' % path)
    fig = plt.figure()
    fig.set_size_inches(scatter_width, scatter_height)
    ax = fig.add_subplot(111)
    if len(points) != 0:
        ax.scatter(xRows, yRows, s=points)
    else:
        ax.scatter(xRows, yRows)
    pltLines(lines)
    pltText(xRows, yRows, xDif, yDif, texts, textSize)

    xmajorFormatter = FormatStrFormatter('%.2f')
    ax.xaxis.set_major_formatter(xmajorFormatter)
    pltAfter(fig, titles, isShow, isRotate, path, ax, None)


def boxplot(titles, rows, lables=None, isShow=False, isRotate=True, path=""):
    print('画一张箱形图--->%s' % path)
    fig = plt.figure()
    fig.set_size_inches(box_width, box_height)
    ax = fig.add_subplot(111)
    ax.boxplot(rows)
    pltAfter(fig, titles, isShow, isRotate, path, ax, lables)


if __name__ == '__main__':
    titles = ['测试', 'x轴', 'y轴']
    xRows = [1, 2, 3, 4, 5]
    yRows = [9, 8, 4, 10, 7]
    path = 'test.png'
    scatter(titles, xRows, yRows, path=path)

    titles = ['测试', 'x轴', 'y轴']
    rows = [[1, 2, 8], [2, 4, 4, 5], [3, 8, 5, 3]]
    lables = ['x1', 'x2', 'x3']
    path = 'test.png'
    boxplot(titles, rows, lables=lables, isRotate=False, path=path)
