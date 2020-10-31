# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import geostrat
import texmex

import sections.biblio.utils
import sections.utils.spa

MIN_LIKELIHOOD = 0.5

MIN_MARKER_COUNT = 50


def extract(data: sections.utils.spa.Data) -> list:
    config = sections.utils.spa.Config(
        likelihood_name='bibliography_table',
        page_analysis=analyse_page,
    )

    extracted = sections.utils.spa.work(data=data, config=config)

    # ignore to low valued bib pages
    valid = [item for item in extracted if item.content.value > MIN_LIKELIHOOD]

    hugest = sections.biblio.utils.cluster_bibpages(valid)
    return hugest


def analyse_page(navigator: texmex.PageTextNavigator
                ) -> sections.feature.StatisticalResultItem:
    parsed = geostrat.parse(navigator, column_count=2)
    if not parsed:
        return len(navigator), 0

    marker = 0

    left, right = parsed
    for item in left + right:
        marker += len(prenom(item.text))

    if marker <= MIN_MARKER_COUNT:
        return len(navigator), 0

    return len(navigator), marker


def prenom(raw: str) -> list:
    """\
    >>> prenom('Becker J. & Franz S.')
    ['J.', 'S.']
    """
    result = [
        item[0] + '.' for item in re.findall(r'\w+\s(?P<prenom>\w\.)', raw)
    ]
    return result
