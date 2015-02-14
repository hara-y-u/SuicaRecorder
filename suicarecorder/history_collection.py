import history


class HistoryCollection(list):
    def __init__(self, histories):
        super(HistoryCollection, self).__init__(histories)
        self.set_previous()

    def sort_by(self, key, asc=True):
        res = sorted(self, key=lambda h: getattr(h, key))
        if not asc:
            res.reverse()
        return res

    def set_previous(self):
        hs = self.sort_by('id', asc=False)
        for i, h in enumerate(hs):
            if 0 < i:
                hs[i-1].previous = h

    @classmethod
    def from_blocks(cls, blocks):
        return cls([history.from_block(b) for b in blocks])


def from_blocks(blocks):
    return HistoryCollection.from_blocks(blocks)
