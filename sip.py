import route
import json

class SIPAllocTree(route.AllocTree):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def locate(self, route: int, sif, verbose=True):
        stop = super().locate(route, verbose)
        return stop


if __name__ == '__main__':
    SIPAllocTree.SIZE = 1000
    root = SIPAllocTree([1, 2, 0])

    #          To                  From                    Token            OP  FLAG 1     FLAG 2      TAG 1
    packet = b'\x00\x00\x00\x00\x01\x02\x00\x00\x00\x00\x02\x00\x00\x00\x00\x03\x00\x00\x02\x00\x00\xf3\x00\x04\xe5\xaa\xaa\xaa\xaa'