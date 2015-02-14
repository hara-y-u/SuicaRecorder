import history


def sorted_by(collection, key, asc=True):
    ret = sorted(collection, key=lambda h: getattr(h, key))
    if not asc:
        ret.reverse()
    return ret


class HistoryCollection(list):
    def __init__(self, histories):
        super(HistoryCollection, self).__init__(histories)
        self._prepare_previous()
        self._brought_balance = None

    def sort_by(self, key, asc=True):
        self.sort(key=lambda h: getattr(h, key))
        if not asc:
            self.reverse()

    def _prepare_previous(self):
        hs = sorted_by(self, 'id', asc=False)
        for i, h in enumerate(hs):
            if 0 < i:
                hs[i-1].previous = h

    @property
    def brought_balance(self):
        return self._brought_balance

    @brought_balance.setter
    def brought_balance(self, balance):
        hs = sorted_by(self, 'id')
        hs[0].previous = history.History({'balance': balance})
        self._brought_balance = balance

    @classmethod
    def from_blocks(cls, blocks):
        return cls([history.from_block(b) for b in blocks])


def from_blocks(blocks):
    return HistoryCollection.from_blocks(blocks)
