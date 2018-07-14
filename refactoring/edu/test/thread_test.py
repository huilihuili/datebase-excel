import threading
import time


def action(arg):
    print('the arg is:%s\r' % arg)


for i in range(4):
    t = threading.Thread(target=action, args=(i,))
    t.start()
