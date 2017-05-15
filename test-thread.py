
class T:
    def __init__(self):
        self.l = [1, 2]

    def getList(self):
        return self.l

    def clearList(self):
        self.l.clear()


def test(l):
    print(len(l))

t = T()
l = t.getList().copy()
test(l)
t.clearList()
test(l)
