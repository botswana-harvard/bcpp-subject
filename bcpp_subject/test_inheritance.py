class A:
    def __init__(self, a, b=None):
        self.a =a 
        self.b = b

    def get_b(self):
        return self.b


class B(A):
    def __init__(self, a, b=None, c=None):
        super().__init__(a, b)

if __name__ == '__main__':
    b = B(1, b=2)
    print(b.get_b())