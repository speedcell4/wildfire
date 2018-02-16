import itertools
from collections import Counter, defaultdict
from typing import Union, List

__all__ = [
    'Vocab',
]


def _identify(x):
    return x


# TODO dump and load
# TODO most common n
class Vocab(object):
    def __init__(self, counter: Counter = None, specials: List[str] = None, tensor_factory=None):
        super(Vocab, self).__init__()
        if counter is None:
            counter = Counter()
        self.counter = counter

        if specials is None:
            specials = []
        self.specials = specials

        if tensor_factory is None:
            tensor_factory = _identify
        self.tensor_factory = tensor_factory

        self.token2ix = defaultdict(lambda: 0)
        self.ix2token = defaultdict(lambda: '<unk>')

        stream = itertools.chain(counter.values(), specials)
        for ix, token in enumerate(stream, start=self.__len__()):
            self._insert(ix, token)

    def __len__(self) -> int:
        return self.ix2token.__len__()

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.__len__()} tokens)'

    def __getitem__(self, item: Union[int, str]) -> Union[str, int]:
        if isinstance(item, int):
            return self.ix2token[item]
        return self.token2ix[item]

    def _insert(self, ix: int, token: str) -> None:
        self.token2ix[token] = ix
        self.ix2token[ix] = token

    def query(self, tokens: List[str]):
        return self.tensor_factory([self.token2ix[token] for token in tokens])

    def inverse(self, indexes: List[int]) -> List[str]:
        return [self.ix2token[index] for index in indexes]

    def update(self, tokens: List[str]) -> List[int]:
        for token in tokens:
            if token not in self.token2ix:
                self._insert(self.__len__(), token)

        self.counter.update(tokens)
        return self.query(tokens)

    @property
    def tokens(self):
        return self.counter.keys()

    def most_common(self, n: int = None):
        return Vocab(Counter(self.counter.most_common(n)), self.specials, self.tensor_factory)


if __name__ == '__main__':
    vocab = Vocab()
    print(vocab.update('this is a nice word'.split()))
    print(vocab.inverse([1, 2, 3, 4, 5, 10]))
    print(vocab.update('this is nice'.split()))

    print(vocab.most_common(2).tokens)
