# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import dataclasses
import functools
import statistics

import configos
import germania
import konradus
import texmex
import utilo

SENTENCE_LENGTH_MIN = configos.HV_INT_PLUS(default=20)


@dataclasses.dataclass
class TextOnPage:
    words_: list[str] = dataclasses.field(default_factory=list)
    sentences_: list[str] = dataclasses.field(default_factory=list)
    paragraphs_: int = None
    headlines_: int = None
    # signs included in sentences
    signs_: konradus.Marks = dataclasses.field(default_factory=list)
    # ordinary dots ... which are used in table of content etc.
    dots_: konradus.Marks = dataclasses.field(default_factory=list)

    def append_sentence(self, item: str):
        self.sentences_.append(item)  # pylint:disable=E1101

    def append_sign(self, item: str):
        self.signs_.append(item)  # pylint:disable=E1101

    def append_word(self, item: str):
        self.words_.append(item)  # pylint:disable=E1101

    def append_dot(self, item: str):
        self.dots_.append(item)  # pylint:disable=E1101

    @property
    def words(self):
        return list(self.words_)  # pylint:disable=E1133

    @property
    def sentences(self):
        return list(self.sentences_)  # pylint:disable=E1133

    @property
    def signs(self):
        return list(item for item in self.signs_)  # pylint:disable=E1133

    @property
    def dots(self):
        return len(self.dots_)

    def __getattr__(self, key: str) -> float:
        variable, action = key.split('_', maxsplit=1)
        try:
            data = self.__dict__[f'{variable}_']
        except KeyError as error:
            raise AttributeError(f'could not access `{key}``') from error
        if not data:
            return None
        length = (len(item) for item in data)

        operation = {
            'max': max,
            'min': min,
            'mean': statistics.mean,
            'median': statistics.median,
            'mode': functools.partial(utilo.mode, maximize=True),
            'stdev': statistics.stdev,
            'variance': statistics.variance,
        }
        with contextlib.suppress(KeyError):
            result = operation[action](length)
            return utilo.roundme(result)
        raise ValueError(f'unsupported operation {action} {variable}')


def textonpage(page: texmex.PTN) -> TextOnPage:
    result = TextOnPage()
    for chunk in page:
        text = chunk.text.strip()
        sentences = germania.sentence_tokenize(text)
        for item in sentences:
            if not germania.is_sentence(item, length_min=SENTENCE_LENGTH_MIN):
                continue
            result.append_sentence(item)
        splitted = germania.words_fromstr(text)
        for item in splitted:
            if isinstance(item, str):
                if len(item) <= 2:
                    # skip parsing errors
                    continue
                result.append_word(item)
                continue
            if item == konradus.Mark.FULLSTOP:
                result.append_dot(item)
                continue
            if isinstance(item, konradus.Mark):
                result.append_sign(item)
                continue
            assert 0, f'unsupported item {item}'
    return result
