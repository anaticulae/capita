# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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

import configo
import elements.headline.lookup
import geostrat
import serializeraw
import utila

import sections.feature
import sections.table.strategy
import sections.utils.headline

BACKUP_PAGE = (1, 0.5)

ABBREVIATION_TRUST_MIN = configo.HV_PERCENT_PLUS(default=65)


def work(oneline_text: str, oneline_textpositions: str, pages=None) -> str:
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        oneline_text,
        oneline_textpositions,
        pages=pages,
    )
    result = sections.feature.pagebypage(
        navigators,
        analyse_page,
        name='abbreviation_table',
    )
    # TODO: A LITTLE HACKY BUT WORKS
    result = sections.table.strategy.merge_second(
        result,
        result,
        merge_min=0.49,
        replace=0.75,
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
    if not invalid_column(parsed):
        return BACKUP_PAGE
    return sections.feature.NO_PAGE


def byheadline(content):
    headlines = sections.utils.headline.headlines(content)
    if not headlines:
        return None
    if utila.similar(
            expected=NOABBR,
            current=headlines,
            maxdiff=0.95,
    ):
        # SKIP ABBR HEADLINE INSIDE TABLE OF CONTENT
        return sections.feature.NO_PAGE
    if utila.similar(
            expected=elements.headline.lookup.ABBREVIATION,
            current=headlines,
            maxdiff=0.95,
    ):
        return sections.feature.PERFECT
    return None


NOABBR = elements.headline.lookup.TOC


def invalid_column(data: list) -> bool:  # pylint:disable=R0911
    """\
    unbalanced columns, equal factor is not matching
    >>> invalid_column((['sos'], ['This is just data']*10))
    True
    """
    if not data:
        return True
    if not data[0]:
        return True
    if not data[1]:
        return True
    if len(data) != 2:
        return True
    if numbered_column(data):
        return True
    if not short_column(data[0]):
        return True
    equal_factor = len(data[0]) / len(data[1])
    if equal_factor < 0.3:
        # CHECK THAT LEFT AND RIGHT COLUMN ARE NEARLY EQUAL
        # assumption: the second column has max. 3 times more lines then
        # the left side.
        return True
    if whitespaced(data[1]):
        return True
    return False


def numbered_column(data: list) -> bool:
    right = data[1]
    # item in right column in a row contain any number and may other stuff
    right_numbers = [
        item for item in right if item and utila.parse_numbers(text(item))
    ]
    if len(right) < 6:
        return False
    if not right_numbers:
        return False
    rate = len(right_numbers) / len(right)
    if rate <= 0.3:
        return False
    # right number column, maybe a table of content page
    return True


SHORT_COLUMN_MEAN_MAX = configo.HV_FLOAT_PLUS(default=10.0)


def short_column(left) -> bool:
    if not left:
        return False
    mean = statistics.mean([len(text(item)) for item in left])
    if mean > SHORT_COLUMN_MEAN_MAX:
        return False
    return True


WHITESPACED_VALID_MAX = configo.HV_PERCENT_PLUS(default=30.0)

WHITESPACED_INVALID_RATE_MIN = configo.HV_PERCENT_PLUS(default=20.0)


def whitespaced(right) -> bool:
    valid, invalid = utila.partition(
        key=lambda x: whitespace_rate(x.text) < WHITESPACED_VALID_MAX,
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
    rate: float = utila.roundme(rate)
    return rate
