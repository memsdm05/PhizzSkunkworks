import route

class SIPAllocTree(route.AllocTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def locate(self, route: int, sif, verbose=True):
        stop = super().locate(route, verbose)
        return stop


if __name__ == '__main__':
    SIPAllocTree.SIZE = 1000
    root = SIPAllocTree([1, 2, 0])
