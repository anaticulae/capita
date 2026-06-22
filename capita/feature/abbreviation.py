# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Likelihood Detection
=================================

We search for selective headline "Abkuerzungsverzeichnis, ...".

NOTE: This approach is only for demo time.
"""

import contextlib
import statistics

import configos
import elementae.headline.lookup
import geostrat
import serializeraw
import utilo

import capita.feature
import capita.strategy
import capita.utils.headline

BACKUP_PAGE = (1, 0.5)

ABBREVIATION_TRUST_MIN = configos.HV_PERCENT_PLUS(default=65)


def work(oneline_text: str, oneline_textpositions: str, pages=None) -> str:
    navigators = serializeraw.ptn_fromfile(
        oneline_text,
        oneline_textpositions,
        pages=pages,
    )
    result = capita.feature.pagebypage(
        navigators,
        analyse_page,
        name='abbreviation_table',
    )
    # TODO: A LITTLE HACKY BUT WORKS
    result = capita.strategy.merge_second(
        result,
        result,
        merge_min=0.49,
        replace=0.75,
        title='abbreviation',
    )
    for item in result:
        if item.content.value >= ABBREVIATION_TRUST_MIN:
            continue
        # remove too low confidence items. Skip to much double column pages
        item.content.value = 0.0

    dumped = serializeraw.dump_likelihood(result)
    return dumped


# TODO: ADD CONTENT ANALYZER TO DISTINGUISH BETWEEN SYMBOLTABLE


def analyse_page(content):
    if detected := byheadline(content):
        return detected
    # Use backup strategy to collect double column page which can follow
    # headlined page
    parsed = geostrat.parse(content, column_count=2)
    if not parsed:
        # no double column layouta detected
        return capita.feature.NO_PAGE
    if not invalid_column(parsed[0], parsed[1]):
        return BACKUP_PAGE
    return capita.feature.NO_PAGE


def byheadline(content):
    headlines = capita.utils.headline.headlines(content)
    if not headlines:
        return None
    if utilo.similar(
            expected=NOABBR,
            current=headlines,
            maxdiff=0.95,
    ):
        # SKIP ABBR HEADLINE INSIDE TABLE OF CONTENT
        return capita.feature.NO_PAGE
    if utilo.similar(
            expected=elementae.headline.lookup.ABBREVIATION,
            current=headlines,
            maxdiff=0.95,
    ):
        return capita.feature.PERFECT
    return None


NOABBR = elementae.headline.lookup.TOC


def invalid_column(left, right) -> bool:  # pylint:disable=R0911
    """\
    unbalanced columns, equal factor is not matching
    >>> invalid_column(*(['sos'], ['This is just data']*10))
    True
    """
    # remove very small data or -/lists
    left = [text(item).strip('-– ') for item in left]
    right = [text(item).strip('-– ') for item in right]
    left = [item for item in left if len(item) >= 2]
    if not left or not right:
        # both columns must have data
        return True
    if numbered_column(right):
        return True
    if not short_column(left):
        return True
    equal_factor = len(left) / len(right)
    if equal_factor < 0.3:
        # CHECK THAT LEFT AND RIGHT COLUMN ARE NEARLY EQUAL
        # assumption: the second column has max. 3 times more lines then
        # the left side.
        return True
    if whitespaced(right):
        return True
    return False


def numbered_column(column) -> bool:
    # item in right column in a row contain any number and may other stuff
    right_numbers = [
        item for item in column if item and utilo.parse_ints(text(item))
    ]
    if len(column) < 6:
        return False
    if not right_numbers:
        return False
    rate = len(right_numbers) / len(column)
    if rate <= 0.3:
        return False
    # right number column, maybe a table of content page
    return True


SHORT_COLUMN_MEAN_MAX = configos.HV_FLOAT_PLUS(default=10.0)


def short_column(left) -> bool:
    if not left:
        return False
    mean = statistics.mean([len(item) for item in left])
    if mean > SHORT_COLUMN_MEAN_MAX:
        return False
    return True


WHITESPACED_VALID_MAX = configos.HV_PERCENT_PLUS(default=30.0)

WHITESPACED_INVALID_RATE_MIN = configos.HV_PERCENT_PLUS(default=20.0)


def whitespaced(right) -> bool:
    valid, invalid = utilo.partition(
        key=lambda x: whitespace_rate(x) < WHITESPACED_VALID_MAX,
        items=right,
    )
    if not invalid:
        return False
    invalid_rate = len(invalid) / (len(invalid) + len(valid))
    if invalid_rate > WHITESPACED_INVALID_RATE_MIN:
        return True
    return False


def text(item):
    """Support simple str items."""
    with contextlib.suppress(AttributeError):
        return item.text
    return item


def whitespace_rate(item) -> float:
    """\
    >>> whitespace_rate('A B')
    0.33
    """
    # TODO: MOVE TO UTILA
    if not item:
        return 0
    rate = item.count(' ') / len(item)
    rate: float = utilo.roundme(rate)
    return rate
