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

    def __init__(self, chain, start: int = None, end: int = None, parent: 'AllocTree' = None):
        # Node attributes
        self.root = parent is None
        self.leaf = len(chain) == 0
        self.children = []
        self.parent = parent

        # Range start and end (Inclusive, Inclusive)
        self.start = start
        self.end = end

        if self.root:
            self.start = 0
            self.end = self.SIZE

        # Alloc engine
        self.id = self.start
        nstart = self.start + 1

        # If node is a regular node (dispatcher, link, supervisor, etc)
        if len(chain) > 1:
            op = chain[0]

            # Get segment size
            div = round((self.end - nstart + 1) / op)

            for n in range(op):
                s = nstart + n * div # start is a multiplication of div + the start
                e = s + div - 1      # end is just start + div - 1 (- 1 is because it's inclusive, inclusive)
                self.children.append(AllocTree(chain[1:], s, e, self))
        # If node is a leaf (bots, apps, healths, etc)
        elif self.leaf:
            op = chain[0]

            # If leaf no need to calculate segment size, just fill to the op
            # if op is 0 then fill entire segment with leaves
            self.children = [AllocTree([], n, n, self) for n in range(nstart, nstart+op if op>0 else self.end+1)]

    def _in_alloc(self, n: int):
        return self.start <= n <= self.end

    def locate(self, route: int, verbose = True):
        # If routing number is equal to your routing number stop and receive
        if route == self.id:
            if verbose: print('~ S&R', self.leaf, self, self.start, self.end)
            return self

        # If routing number is out of your own allocation then send to parent
        elif not self._in_alloc(route):
            if self.root:
                # Error, outside global segment
                if verbose: print('X AT ROOT NO AVAIL, RETURNING ROOT')
                return self

            if verbose: print('↑ OUT OF RANGE', self.leaf, self, self.start, self.end)
            return self.parent.locate(route, verbose)

        # If routing number is in your allocation find which child alloc its in and send to respective child
        else:
            if verbose: print('↓ IN RANGE', self.leaf, self, self.start, self.end)

            # TODO figure out all that __getitem__ indexing stuff for better than O(n) performance
            for child in self.children:
                if child._in_alloc(route):
                    return child.locate(route, verbose)

            # child not found error
            if verbose: print('X N/A, RETURNING', self)
            return self

    def separator(self):
        print('-----------------------------------')
        return self

    def address(self):
        print(self)
        return self

    def info(self):
        yn = lambda a: "Yes" if a else "No"
        print('Address:', self)
        print('Start:', self.start)
        print('End:', self.end)
        print('Parent:', self.parent)
        print('Children:', list(map(int, self.children)) if len(self.children) > 0 else 'N/A')
        print('Is Leaf:', yn(self.leaf))
        print('Is Root:', yn(self.root))
        return self

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
    AllocTree.SIZE = 100
    root = AllocTree([1, 2, 10])

    for i in range(100):
        print(i)
        root.address().locate(i).separator()
