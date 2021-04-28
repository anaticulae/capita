# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Abbreviation Likelihood Detection
=================================

We search for selective headline "Abkuerzungsverzeichnis, ...".

NOTE: This approach is only for demo time.
"""

import statistics

import geostrat
import iamraw
import serializeraw
import utila

import sections.feature
import sections.table.strategy
import sections.utils.headline

NO_PAGE = (0, 0)
BACKUP_PAGE = (1, 0.5)

ABBREVIATION_TRUST_MIN = 0.65  # TODO: HOLY VALUE


def work(oneline_text: str, oneline_textpositions: str, pages=None) -> str:
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        oneline_text,
        oneline_textpositions,
        pages=pages,
    )

    result = {page.page: analyse_page(page) for page in navigators}

    uniformed = sections.feature.uniform_result(result)
    multiformed = sections.feature.multiform_result(result)
    if multiformed is not None:
        uniformed = multiformed
    assert len(uniformed) == len(navigators)

    result = [
        iamraw.PageContentLikelihood(
            page=page,
            content=iamraw.Likelihood(value, name='abbreviation_table'),
        ) for page, value in uniformed.items()
    ]
    result = sorted(result, key=lambda x: x.page)

    # TODO: A LITTLE HACKY BUT WORKS
    result = sections.table.strategy.merge_second(
        result,
        result,
        min_merge=0.49,
        replace=0.75,
    )
    for item in result:
        if item.content.value >= ABBREVIATION_TRUST_MIN:
            continue
        # remove too low confidence items. Skip to much double column pages
        item.content.value = 0.0

    dumped = serializeraw.dump_likelihood(result)
    return dumped


HEADLINES = [
    'Abbreviations',
    'Abbreviationtable',
    'Abkürzungen',
    'Abkürzungsverzeichnis',
]


def analyse_page(content):
    headlines = sections.utils.headline.headlines(content)
    if not headlines:
        # Use backup strategy to collect double column page which can
        # follow headlined page
        parsed = geostrat.parse(content, column_count=2)
        if not invalid_column(parsed):
            return BACKUP_PAGE
        return NO_PAGE
    if isinstance(headlines, str):
        headlines = [headlines]
    for item in HEADLINES:
        if item in headlines:
            return 1, 1
    return NO_PAGE


def invalid_column(data: list) -> bool:  # pylint:disable=R0911
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
    # TODO: CHECK THAT LEFT AND RIGHT COLUMN ARE NEARLY EQUAL
    return False


def numbered_column(data: list) -> bool:
    right = data[1]
    right_numbers = [
        item for item in right if item and utila.parse_numbers(item.text)
    ]
    if len(right) < 6:
        return False
    if not right_numbers:
        return False
    rate = len(right) / len(right_numbers)
    if rate <= 0.3:
        return False
    # right number column, maybe a table of content page
    return True


def short_column(left) -> bool:
    if not left:
        return False
    mean = statistics.mean([len(item.text) for item in left])
    if mean > 10.0:  # HOLY VALUE
        return False
    return True
