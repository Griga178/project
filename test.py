class MyClass():
    max = 0
    param = False

    def __new__(cls, param = False):
        if param > MyClass.max:
            example = super().__new__(cls)
            example.my_f()
            return example
        else:
            return None

    def __init__(self, param):

        self.param = param
        MyClass.max = param
    def my_f(self):
        print('ia', self)

    def __repr__(self):
        # return f'{self.param}'
        return str(self.param)

    def __str__(self):
        return f'{self.param}'


def print_l(self):
    print(self)

m_l = [1,2,3,2,4,5,4]
print(m_l)
new_l = []
for el in m_l:
    new_el = MyClass(el)
    if new_el:
        new_l.append(new_el)
    print(el, new_el)



print(new_l)
a = MyClass()
print(a)
