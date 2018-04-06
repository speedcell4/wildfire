from pathlib import Path
from typing import NamedTuple

__all__ = [
    'CTB5_CHAR_FORMAT', 'CTB5_WORD_FORMAT',
    'CTB7_CHAR_FORMAT', 'CTB7_WORD_FORMAT',
    'Token', 'CoNLLReader',
]

CTB5_WORD_FORMAT = '{ix}\t{form}\t{form}\t{wpos}\t{wpos}_\t{head}\t{drel}'
CTB5_CHAR_FORMAT = '{ix}\t{form}\t{form}\t{wpos}\t{cpos}_\t{head}\t{drel}'

CTB7_WORD_FORMAT = '{ix}\t{form}\t{wpos}\t{head}\t{drel}'
CTB7_CHAR_FORMAT = '{ix}\t{form}\t{wpos}\t{cpos}\t{head}\t{drel}'


class Token(NamedTuple):
    form: str
    wpos: str
    head: int
    drel: str


class CoNLLReader(object):
    def __init__(self, path: Path, encoding: str = 'utf-8', separator: str = '\t',
                 form: int = 1, wpos: int = 3, head: int = 6, drel: int = 7) -> None:
        self.path = path
        self.encoding = encoding
        self.separator = separator

        self.form = form
        self.wpos = wpos
        self.head = head
        self.drel = drel

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}, {self.path}>'

    def __iter__(self):
        with self.path.open(mode='r', encoding=self.encoding) as fp:
            sentence = []
            for line in fp:
                line = line.strip()
                if line.__len__() > 0:
                    tokens = line.split(self.separator)
                    form = str(tokens[self.form])
                    wpos = str(tokens[self.wpos])
                    head = int(tokens[self.head])
                    drel = str(tokens[self.drel])
                    sentence.append(Token(form, wpos, head, drel))
                elif sentence.__len__() > 0:
                    yield sentence
                    sentence = []

    @staticmethod
    def dump_stream(stream, path: Path, format_string: str, encoding: str = 'utf-8') -> None:
        with path.open(mode='w', encoding=encoding) as fp:
            for sentence in stream:
                for ix, token in enumerate(sentence):
                    print(format_string.format(ix, **token._asdict()), file=fp)
                print('\n', file=fp)
