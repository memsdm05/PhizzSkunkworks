'''
Rules of Routing
1. If routing number is out of your own allocation then send to parent.
2. If routing number is equal to your routing number stop and receive
3. If routing number is in your allocation find which child alloc its in and send to respective child

For this example:
Congruent
Modulo allocs are thrown away

'''

import random as r
class AllocTree:
    SIZE = 10_000

    def __init__(self, chain, start:int=None, end:int=None, parent:'AllocTree'=None, isLeaf:bool=False,):
        # Node attributes
        self.root = parent is None
        self.children = []
        self.parent = parent
        self.isLeaf = isLeaf

        # Range start and end (Inclusive, Inclusive)
        self.start = start
        self.end = end

        if self.root:
            self.start = 0
            self.end = self.SIZE
            sp = 1


        if len(chain) > 0:
            sp = chain[0]
        else:
            sp = -1

        self.id = self.start
        nstart = self.start + 1

        if not self.isLeaf:
            if sp > 0:
                div = round((self.end - nstart + 1) / sp)
                for n in range(sp):
                    s = nstart + n * div
                    e = s + div - 1
                    self.children.append(AllocTree(chain[1:], s, e, self))
            elif sp == 0:
                for n in range(self.start, self.end+1):
                    self.children.append(AllocTree([], n, n+1, self, True))
        else:
            self.id += 1

    def in_alloc(self, n:int):
        return self.start <= n <= self.end

    def locate(self, route:int):
        if route == self.id:
            print('~ S&R', self.isLeaf, self, self.start, self.end)
            return self
        elif not self.in_alloc(route):
            print('^ OUT OF RANGE', self.isLeaf, self, self.start, self.end)
            return self.parent.locate(route)
        else:
            print('v IN RANGE', self.isLeaf, self, self.start, self.end)
            for child in self.children:
                if child.in_alloc(route):
                    return child.locate(route)

    def __str__(self):
        return str(self.id)

    def __int__(self):
        return self.id


'''
def segment_test(start, end, d):
    div = round((end - start + 1) / d)
    for n in range(d):
        s = start + n * div
        e = s + div
        print(n, s, e)
    print('trash = ' + str(end + 1 - e))
    print('div   = ' + str(div))
'''


if __name__ == '__main__':
    AllocTree.SIZE = 10000
    root = AllocTree([4, 0])

    print(root.locate(5).locate(1233).locate(0))