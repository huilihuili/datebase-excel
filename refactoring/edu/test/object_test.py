class A(object):
    def __init__(self):
        self.a = 5

    def print_value(self):
        print(self.a)


class B(A):
    def __init__(self):
        super(B, self).__init__()
        self.a = 6

    def print_value(self):
        print(self.a)
        super(B, self).print_value()


if __name__ == '__main__':
    b = B()
    b.print_value()
