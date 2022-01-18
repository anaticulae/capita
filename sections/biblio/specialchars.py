# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Special Chars
=============

Determine potential bib pages dues analysing the structure of used
characters on a page. Bib pages contain a lot of brackets, dots,
semicolons. etc.

A document contains only one bib page(s) block. Therefore we look for
the highest rated valued block of bib pages and return only this single
one. Without selecting the biggest cluster, more than one bib can be
detected.
"""

import re
import statistics

import configo
import elements.headline.lookup
import german
import texmex
import utila

import sections.biblio
import sections.biblio.utils
import sections.utils.headline
import sections.utils.spa

LIKELIHOOD_MIN = configo.HV_PERCENT_PLUS(default=30.0)


def extract(data: sections.utils.spa.Data) -> list:
    config = sections.utils.spa.Config(
        likelihood_name='bibliography_table',
        page_analysis=analyse_page,
    )
    extracted = sections.utils.spa.work(data=data, config=config)
    # ignore to low valued bib pages
    valid = [item for item in extracted if item.content.value > LIKELIHOOD_MIN]
    hugest = sections.biblio.utils.cluster_bibpages(valid)
    return hugest


SPECIAL_CHAR_BONUS = configo.HV_PERCENT_PLUS(default=30)


def analyse_page(
    navigator: texmex.PageTextNavigator
) -> sections.feature.StatisticalResultItem:
    if bib_headline(navigator):
        # Bibliography headline on page
        return len(navigator), len(navigator)
    raw = navigator.debug
    marker = special_pattern(raw, page=navigator.page)
    if special_chars(raw):
        # thirty percent bonus
        marker *= (1 + SPECIAL_CHAR_BONUS)
    if content_page(raw):
        marker = 0
    likelihood = 0.0
    if marker and len(navigator) >= 1:
        likelihood = marker / len(navigator)
    if likelihood < LIKELIHOOD_MIN:
        # TODO: CHECK THIS
        # this can not be a bib table
        marker = 0
    return len(navigator), marker


def bib_headline(ptn: texmex.PageTextNavigator) -> bool:
    """Determine if a BIB-HEADLINE is on current navigator."""
    headlines = sections.utils.headline.headlines(ptn)
    if not headlines:
        return False
    smilar = utila.similar(
        expected=elements.headline.lookup.BIBLIOGRAPHY,
        current=headlines,
        maxdiff=0.95,
    )
    if not smilar:
        return False
    return True


VOLUME = utila.compiles(r"""
(
    (AUFLAGE|VOL\.)
    [ ]{0,2}
    (\d{1,2})
    |
    (\d)\.
    [ ]{0,2}
    (AUFLAGE)
)
""")


def volume(text, verbose: bool = True):
    """\
    >>> volume('(The Formation of the Classical Islamic World). Vol. 36, S. 225-234.')
    [(36, 'Vol. 36')]
    >>> volume('Schriftsprache der Gegenwart. 5. Auflage.')
    [(5, '5. Auflage')]
    """
    # TODO: MOVE TO GERMAN
    result = []
    for item in re.finditer(VOLUME, text):
        group = item.groups()
        value = group[3] if group[3] and group[3].isnumeric() else group[2]
        if verbose:
            result.append((int(value), item[0]))
        else:
            result.append(int(value))
    return result


PATTERN = (
    german.dates,
    german.years,
    german.pagenumbers,
    german.authors,
    german.hyperlink,
    volume,
)


def special_pattern(raw: str, page: int) -> int:
    """Search for bib page typical pattern like: authors, dates, years...

    If too few pages occurs, disable pattern approach, because its may
    not a bib may a toc or table table.
    """
    collected = collect_and_replace(raw, PATTERN)
    # this patterns typically occurs mostly once's.
    allmarker = len(collected)
    collected: set = set(collected)
    marker = len(collected)
    marker_min = MARKER_COUNT_MIN(len(raw.splitlines()))
    if marker < marker_min:
        utila.debug(f'too few marker {page}: {marker}/{marker_min}')
        return 0
    pages = collect_and_replace(raw, (german.pagenumbers,))
    pagerate = len(pages) / allmarker
    if pagerate > 0.8:
        msg = f'too many pages {page}: {pagerate} {len(pages)} {allmarker}'
        utila.debug(msg)
        return 0
    return allmarker


MARKER_COUNT_MIN = configo.HolyTable(items=(
    (0, 5),
    (5, 5),
    (10, 10),
    (15, 15),
))


def collect_and_replace(raw: str, pattern: list) -> list:
    """Collect due list of pattern and avoids parsing items twice."""
    collected = []
    for method in pattern:
        parsed = method(raw, verbose=True)
        for item, itemraw in parsed:
            # do not parse pattern twice
            raw = raw.replace(itemraw, ' **************** ')
            collected.append(item)
    return collected


SPECIAL_CHARS = ";,/:[]()&"

SPECIAL_CHARS_CLASSIFIER_MIN = configo.HV_PERCENT_PLUS(default=30.0)

SPECIAL_CHARS_WORDCOUNT_MIN = configo.HV_INT_PLUS(default=40)


def special_chars(raw: str) -> bool:
    # TODO: A LOT OF MISMATCHES AS A RESULT OF PROGRAM CODE IN DOCUMENT
    result = []
    for line in raw.splitlines():
        parsed = german.word_tokenize(line, validate_sentences=False)
        result.extend(parsed)
    word_count = len(result)
    if word_count < SPECIAL_CHARS_WORDCOUNT_MIN:
        return False
    counted = sum([raw.count(char) for char in SPECIAL_CHARS])
    classifier = counted / word_count if word_count else 0
    if classifier < SPECIAL_CHARS_CLASSIFIER_MIN:
        return False
    return True


SENTENCE_MEAN_TRUST_MIN = configo.HV_INT_PLUS(default=100)


def content_page(raw: str) -> bool:
    """Verify that page contains a `normal` number of sentences."""
    sentences = german.sentence_tokenize(raw, normalize_spaces=True)
    if not sentences:
        return False
    # german does not split sentences at `:` but bib tables uses : often
    # for separating parts. If we do not split by double collon we archive
    # a lot of false postive results.
    sentences = utila.flatten([split_doublecolon(item) for item in sentences])
    length_mean = statistics.mean([len(sentence) for sentence in sentences])
    if length_mean > SENTENCE_MEAN_TRUST_MIN:
        return True
    return False


DOUBLE_COLON = utila.compiles(r"""
    (?!https?)
    \:
    (?!//)
""")


def split_doublecolon(text: str) -> list:
    """\
    >>> split_doublecolon('Ich glaube:"Heute is ein guter Tag"')
    ['Ich glaube', '"Heute is ein guter Tag"']
    >>> split_doublecolon('http://donotsplit.com https://donotsplit.com')
    ['http://donotsplit.com https://donotsplit.com']
    """
    return re.split(DOUBLE_COLON, text)
